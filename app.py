import json
from pathlib import Path
from urllib.parse import quote

import dash_bootstrap_components as dbc
import dash_molstar
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from chemFilters.img_render import MolPlotter
from dash import Dash, Input, Output, State, callback_context, dcc, html, no_update
from dash.exceptions import PreventUpdate
from dash_molstar.utils import molstar_helper
from loguru import logger
from QligFEP.pdb_utils import read_pdb_to_dataframe, rm_HOH_clash_NN
from WeightedCCC import GraphClosure

from assets.graph_handler import (
    add_legend_trace_to_graph_figure,
    extract_graph_coordinates,
    generate_graph,
    get_most_connected_cpd,
    set_nx_graph_coordinates,
)
from assets.molecule_handler import add_images_to_df, lomap_json_to_dataframe

# local imports
from assets.pdb_handler import create_pdb_ligand_files, merge_protein_lig
from assets.stats_make import cinnabar_stats

# initialize some data that can be later updated based on the dropdown menu...
method_name = "Gbar"
results_root = Path("results")
CACHE_DIR = Path("cache")
molplotter = MolPlotter(from_smi=True, size=(-1, -1))
stats_dict = None
crashed_edges = []
perturbation_root = None  # Will be set in initialize_data
ddG_df = pd.DataFrame()  # Initialize empty DataFrame
perturbations = []  # Initialize empty list
G = None
node_labels, node_x, node_y, edge_x, edge_y = [], [], [], [], []
most_connected_name = ""


color_dict = {
    # pallette from https://colorhunt.co/palette/f9f7f7dbe2ef3f72af112d4e
    "most_connected": "#DBE2EF",
    "from": "#3F72AF",
    "to": "#112D4E",
    "no_highlight": "#F9F7F7",
}

available_targets = sorted([p.name for p in Path("perturbations/").glob("*") if p.is_dir()])


# write the pdb files for the ligands
def initialize_data(target_name):
    try:
        global perturbation_root, mapping, ddG_df, G, node_labels, node_x, node_y, edge_x, edge_y, most_connected_name, perturbations, crashed_edges, stats_dict
        perturbation_root = Path(f"perturbations/{target_name}")
        if not perturbation_root.exists():
            raise FileNotFoundError(f"Target directory {perturbation_root} not found")

        # Ensure cache directory exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{target_name}_ddG_df.pkl"
        loaded_from_cache = False

        if cache_file.is_file():
            try:
                logger.info(f"Loading cached ddG data from {cache_file}")
                ddG_df = pd.read_pickle(cache_file)
                # Basic check to ensure essential columns are present
                if (
                    "from" in ddG_df.columns
                    and "to" in ddG_df.columns
                    and "Q_ddG_avg" in ddG_df.columns
                    and "from_svg" in ddG_df.columns
                ):
                    loaded_from_cache = True
                else:
                    logger.warning("Cached file seems incomplete. Recalculating.")
            except Exception as e:
                logger.warning(f"Failed to load cached file {cache_file}: {e}. Recalculating.")

        if not loaded_from_cache:
            logger.info(f"Calculating ddG data for {target_name}")
            create_pdb_ligand_files(
                root_path=perturbation_root, overwrite=False
            )  # Keep this here? Maybe not needed if PDBs are cached later? For now, keep.
            mapping_file = results_root / f"{target_name}/mapping_ddG.json"
            if not mapping_file.exists():
                raise FileNotFoundError(f"Mapping file not found: {mapping_file}")
            mapping = json.loads(mapping_file.read_text())
            ddG_df = lomap_json_to_dataframe(mapping)
            # Add images only if not loaded from cache or if missing
            if not np.isin(["from_svg", "to_svg"], ddG_df.columns).all():
                ddG_df = add_images_to_df(ddG_df, molplotter)
            # Save to cache after calculation
            try:
                ddG_df.to_pickle(cache_file)
                logger.info(f"Saved calculated ddG data to {cache_file}")
            except Exception as e:
                logger.error(f"Failed to save data to cache file {cache_file}: {e}")

        # Generate graph and extract coordinates regardless of cache status
        G = generate_graph(ddG_df)
        G = set_nx_graph_coordinates(G)
        node_labels, node_x, node_y, edge_x, edge_y = extract_graph_coordinates(G)
        most_connected_name, most_connected_smiles = get_most_connected_cpd(G, ddG_df)

        nan_edges = ddG_df.query("Q_ddG_avg.isnull()")
        crashed_edges = nan_edges.apply(lambda x: f"FEP_{x['from']}_{x['to']}", axis=1).tolist()
        ddG_df = ddG_df.dropna(subset=["Q_ddG_avg"]).reset_index(drop=True)  # Drop NaN and reset index

        perturbations = list(zip(ddG_df["from"], ddG_df["to"]))
        ccc = GraphClosure(from_lig=ddG_df["from"], to_lig=ddG_df["to"], b_ddG=ddG_df["Q_ddG_avg"])
        ccc.getAllCyles()
        if len(ccc.cycles) == 0:
            logger.warning("No cycle found!")
            # Handle case with no cycles gracefully, maybe skip CCC part
            ddG_df = ddG_df.assign(
                ccc_ddG=np.nan, ccc_error=np.nan, residual=lambda x: x["Q_ddG_avg"] - x["ddg_value"]
            )
        else:
            ccc.iterateCycleClosure(minimum_cycles=2)
            ccc_results_df = (
                ccc.getEnergyPairsDataFrame(verbose=False)
                .rename(columns={"ddG_wcc0": "ccc_ddG", "pair_error": "ccc_error"})
                .drop(columns=["Pair"])
                .assign(
                    ccc_ddG=lambda x: x["ccc_ddG"].astype(float),
                    ccc_error=lambda x: x["ccc_error"].astype(float),
                )
            )
            # Ensure index alignment before concatenation
            ddG_df = ddG_df.reset_index(drop=True)
            ccc_results_df = ccc_results_df.reset_index(drop=True)
            ddG_df = pd.concat([ddG_df, ccc_results_df], axis=1).assign(
                residual=lambda x: x["Q_ddG_avg"] - x["ddg_value"]
            )

        # Calculate statistics once and store them
        stats_dict = cinnabar_stats(ddG_df["Q_ddG_avg"], ddG_df["ddg_value"])

    except Exception as e:
        print(f"Error initializing data for target {target_name}: {e}")
        raise


# Initialize with the first target
initialize_data(available_targets[0])
# Set the CSS for the app & layout
FLATLY_CSS = "https://bootswatch.com/4/flatly/bootstrap.min.css"
app = Dash(
    __name__, external_stylesheets=[FLATLY_CSS], suppress_callback_exceptions=True
)  # Suppress for dynamic layout if needed

app.layout = html.Div(
    style={
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "center",  # Center children vertically in the column
        "align-items": "center",  # Center children horizontally
        "height": "100vh",  # Use full height of the viewport
        "padding": "20px",  # Add some padding around the outer div
    },
    children=[
        # Dropdown for selecting target_name
        html.Div(
            style={
                "width": "100%",
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "20px",
                "zIndex": "1000",  # Ensure dropdown is above other elements
            },
            children=[
                html.Label(
                    "Select Target: ",
                    style={"marginRight": "10px", "fontSize": "16px", "alignSelf": "center"},
                ),
                dcc.Dropdown(
                    id="target-dropdown",
                    options=[{"label": target, "value": target} for target in available_targets],
                    value=available_targets[0],
                    clearable=False,
                    style={
                        "width": "200px",
                        "fontSize": "14px",
                        "backgroundColor": "white",
                    },
                ),
            ],
        ),
        # Top row
        html.Div(
            style={
                "display": "flex",
                "justify-content": "center",  # Center children horizontally
                "align-items": "center",  # Center children vertically
                "width": "100%",  # Take full width to properly space out children
                "margin-bottom": "20px",  # Space between top and bottom rows
            },
            children=[
                dcc.Graph(id="ddg-plot", style={"width": "28%", "height": "100%"}),  # Reduced width
                html.Div(
                    [
                        # Text above the images
                        html.A(
                            id="chem_name",
                            style={
                                "fontSize": "22px",
                                "marginBottom": "20px",
                                "width": "100%",  # Ensure the text spans the full width of the container
                                "textAlign": "center",  # Center the text horizontally
                            },
                        ),
                        # Container for images and arrow
                        html.Div(
                            [
                                html.Img(
                                    id="lig1_img",
                                    style={
                                        "maxWidth": "35%",
                                        "marginRight": "1%",
                                        "height": "300px"
                                    }
                                ),
                                # Arrow in between images
                                html.Div(
                                    "→",
                                    style={
                                        "fontSize": "22px",  # Match the arrow size with the text size
                                        "display": "flex",
                                        "alignItems": "center",  # Vertically center the arrow
                                        "justifyContent": "center",  # Horizontally center the arrow
                                        "width": "5%",  # Allocate width for the arrow, adjust as needed
                                    },
                                ),
                                html.Img(
                                    id="lig2_img", style={"maxWidth": "35%", "height": "300px"}
                                ),
                            ],
                            style={
                                "width": "100%",  # Container takes the full width of its parent
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                        ),
                        # Optional: Description text (uncomment if needed)
                        # html.P(id='chem_desc', style={"textAlign": "center"}),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",  # Stack elements vertically
                        "alignItems": "center",  # Center elements horizontally
                        "justifyContent": "space-around",  # Evenly space out the elements
                        "height": "450px",  # Increased height for the container
                        "width": "48%",  # Increased width for the container
                    },
                ),
            ],
        ),
        # Bottom row
        html.Div(
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "width": "100%",
            },
            children=[
                dcc.Graph(
                    id="perturbation-graph", style={"width": "28%", "height": "400px"}
                ),  # Reduced width
                dash_molstar.MolstarViewer(
                    id="viewer", style={"width": "800px", "height": "600px", "marginLeft": "5%"}
                ),  # Increased size
                # Hidden divs for storing "from" and "to" node identifiers
                html.Div(id="from-node-storage", style={"display": "none"}),
                html.Div(id="to-node-storage", style={"display": "none"}),
                html.Div(id="both-nodes-storage", style={"display": "none"}),
                # Buttons for loading "from" and "to" nodes
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            'Load "From" Ligand', id="load_from_lig", color="primary", className="mb-2"
                        ),
                        dbc.Button('Load "To" Ligand', id="load_to_lig", color="info", className="mb-2"),
                        dbc.Button(
                            "Load Both Ligands", id="load_both_ligs", color="secondary", className="mb-2"
                        ),
                    ],
                    vertical=True,
                ),
            ],
        ),
        dcc.Store(id="clicked-ddg-index-store", storage_type="memory"),
        dcc.Store(id="perturbation-graph-click-store", storage_type="memory", data={"nodes": []}),
    ],
)


def construct_network_graph(highlighted_nodes: list = None):
    if highlighted_nodes is None:
        highlighted_nodes = ["", ""]
    elif len(highlighted_nodes) != 2:
        highlighted_nodes = ["", ""]
    # Assuming edge_x, edge_y, node_x, node_y are available globally or passed to this function
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
        showlegend=False,
    )

    _from, _to = highlighted_nodes

    color_mapping = {
        _from: color_dict["from"],
        _to: color_dict["to"],
    }
    # Use global most_connected_name
    if most_connected_name not in highlighted_nodes:
        color_mapping.update({most_connected_name: color_dict["most_connected"]})
    highlighted = np.unique(highlighted_nodes + [most_connected_name])
    rest = np.setdiff1d(node_labels, highlighted)
    color_mapping.update({node: color_dict["no_highlight"] for node in rest})

    node_colors = [
        color_mapping.get(node, color_dict["no_highlight"]) for node in node_labels
    ]  # Use .get for safety
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_labels,  # Now includes names for hover
        showlegend=False,
        marker=dict(
            color=node_colors,  # Dynamically set from previous logic
            size=15,  # Increased node size
            line=dict(width=1, color="black"),  # Reduced border thickness and set to black
            showscale=False,  # Assuming no scale is needed due to custom coloring
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Perturbation mapping",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text=f"Most connected compound: {most_connected_name}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            clickmode="event+select",
        ),
    )
    add_legend_trace_to_graph_figure(fig, color_dict)
    fig.update_layout(
        plot_bgcolor="white",  # Set background to white
        paper_bgcolor="white",  # Set background to white
        # set title a bit more up
        title_y=0.9,
        showlegend=True,
    )
    return fig


@app.callback(
    [
        Output("ddg-plot", "figure"),
        Output("perturbation-graph", "figure"),
        Output("chem_name", "children"),
        Output("lig1_img", "src"),
        Output("lig2_img", "src"),
        Output("from-node-storage", "children"),
        Output("to-node-storage", "children"),
        # Keep this output, but its value might be overwritten by the other callback
        Output("clicked-ddg-index-store", "data", allow_duplicate=True),
    ],
    [
        Input("ddg-plot", "clickData"),
        Input("target-dropdown", "value"),
        Input("clicked-ddg-index-store", "data"),  # Add input from the store
    ],
    prevent_initial_call=True,  # Prevent initial call confusion
)
def update_all_components(ddg_clickData, selected_target, highlight_index_from_store):
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    triggered_value = ctx.triggered[0]["value"]

    # Default values for outputs to allow partial updates
    ddg_fig = no_update
    pert_graph_fig = no_update
    chem_name = no_update
    lig1_img = no_update
    lig2_img = no_update
    from_node = no_update
    to_node = no_update
    clicked_ddg_idx_output = no_update  # Avoid loops

    if triggered_id == "target-dropdown":
        logger.info(f"Target dropdown changed to: {selected_target}")
        initialize_data(selected_target)
        ddg_fig = create_ddg_plot(ddG_df, perturbations)
        pert_graph_fig = construct_network_graph()
        chem_name = ""
        lig1_img = ""
        lig2_img = ""
        from_node = ""
        to_node = ""
        clicked_ddg_idx_output = None  # Reset highlight
        return (
            ddg_fig,
            pert_graph_fig,
            chem_name,
            lig1_img,
            lig2_img,
            from_node,
            to_node,
            clicked_ddg_idx_output,
        )

    # Handle ddg-plot click OR highlight update triggered by perturbation graph click
    elif triggered_id == "ddg-plot" or triggered_id == "clicked-ddg-index-store":
        clicked_ddg_index = None
        if triggered_id == "ddg-plot":
            if ddg_clickData is None:
                # Reset highlight if click is cleared
                logger.info("ddg-plot click cleared.")
                ddg_fig = create_ddg_plot(ddG_df, perturbations, highlight_index=None)
                clicked_ddg_idx_output = None
                # Reset other elements as well
                pert_graph_fig = construct_network_graph()  # Reset graph highlight
                chem_name = ""
                lig1_img = ""
                lig2_img = ""
                from_node = ""
                to_node = ""
                return (
                    ddg_fig,
                    pert_graph_fig,
                    chem_name,
                    lig1_img,
                    lig2_img,
                    from_node,
                    to_node,
                    clicked_ddg_idx_output,
                )
            else:
                try:
                    clicked_ddg_index = ddg_clickData["points"][0]["customdata"]
                    logger.info(f"ddg-plot clicked. Index: {clicked_ddg_index}")
                except (KeyError, IndexError):
                    logger.warning("Could not extract index from ddg-plot clickData.")
                    raise PreventUpdate
        elif triggered_id == "clicked-ddg-index-store":
            clicked_ddg_index = highlight_index_from_store
            logger.info(f"Highlight index received from store: {clicked_ddg_index}")
            if clicked_ddg_index is None:
                logger.info("Received None index from store, preventing update.")
                raise PreventUpdate  # Don't update if the store sends None

        # If we have a valid index from either trigger, perform full update
        if clicked_ddg_index is not None:
            try:
                index = clicked_ddg_index
                if index not in ddG_df.index:
                    logger.warning(f"Index {index} not found in current ddG_df. Preventing update.")
                    raise PreventUpdate

                data = ddG_df.loc[index]
                lig1, lig2 = data["from"], data["to"]

                ddg_fig = create_ddg_plot(ddG_df, perturbations, highlight_index=clicked_ddg_index)
                pert_graph_fig = construct_network_graph([lig1, lig2])
                chem_name = [
                    "ΔΔG - calc(ΔΔG):",
                    html.Br(),
                    f"{data['residual']:.2f} ± {data['Q_ddG_sem']:.2f} (SEM) kcal/mol",
                ]
                lig1_img = f"data:image/svg+xml;utf8,{quote(data['from_svg'])}"
                lig2_img = f"data:image/svg+xml;utf8,{quote(data['to_svg'])}"
                from_node = lig1
                to_node = lig2
                clicked_ddg_idx_output = clicked_ddg_index  # Store/confirm the index

            except Exception as e:
                logger.error(f"Error processing index {clicked_ddg_index}: {e}")
                # Fallback to a non-highlighted state in case of error
                ddg_fig = create_ddg_plot(ddG_df, perturbations)
                pert_graph_fig = construct_network_graph()
                chem_name = "Error processing selection"
                lig1_img = ""
                lig2_img = ""
                from_node = ""
                to_node = ""
                clicked_ddg_idx_output = None
        else:
            # This case should ideally not be reached if logic above is correct
            logger.warning("Update triggered but no valid index found.")
            raise PreventUpdate

    else:
        logger.warning(f"Unhandled trigger in update_all_components: {triggered_id}")
        raise PreventUpdate

    return ddg_fig, pert_graph_fig, chem_name, lig1_img, lig2_img, from_node, to_node, clicked_ddg_idx_output


def create_ddg_plot(ddG_df, perturbations=None, highlight_index=None):
    # Ensure perturbations match the current ddG_df state if not provided
    if perturbations is None:
        if not ddG_df.empty:
            perturbations = list(zip(ddG_df["from"], ddG_df["to"]))
        else:
            perturbations = []

    # logger.info(f"Crashed perturbations: {crashed_edges}") # Can be noisy
    n_crashes = len(crashed_edges)
    # Ensure ddG_df is not empty before proceeding
    if ddG_df.empty:
        logger.warning("ddG_df is empty in create_ddg_plot. Returning empty figure.")
        return go.Figure()
    plot_df = ddG_df  # Use the passed df directly
    if plot_df.empty:
        logger.warning("ddG_df is empty after potential dropna in create_ddg_plot. Returning empty figure.")
        return go.Figure()

    # Use pre-calculated statistics instead of recalculating
    all_values = np.concatenate((plot_df["Q_ddG_avg"], plot_df["ddg_value"]))
    margin = 1.0
    min_val, max_val = all_values.min() - margin, all_values.max() + margin

    # Define marker colors: red for highlighted, default otherwise
    marker_colors = ["#1f77b4"] * len(plot_df)  # Default plotly blue
    marker_sizes = [8] * len(plot_df)  # Default size
    if highlight_index is not None and highlight_index in plot_df.index:
        try:
            # Get the integer position of the highlight_index in the potentially filtered plot_df
            loc = plot_df.index.get_loc(highlight_index)
            marker_colors[loc] = "red"
            marker_sizes[loc] = 10  # Make highlighted point larger
        except KeyError:
            logger.warning(
                f"highlight_index {highlight_index} not found in plot_df index. Skipping highlight."
            )
        except TypeError as e:
            logger.error(f"TypeError getting location for highlight_index {highlight_index}: {e}")

    fig = go.Figure()
    # Add scatter plot with error bars
    fig.add_trace(
        go.Scattergl(
            x=plot_df["ddg_value"],
            y=plot_df["Q_ddG_avg"],
            mode="markers",
            error_y=dict(
                type="data", array=plot_df["Q_ddG_sem"], visible=True, thickness=0.75, color="Black"
            ),
            marker=dict(
                size=marker_sizes,  # Use dynamic sizes
                color=marker_colors,  # Use the dynamic color list
                opacity=0.8,
                line=dict(width=0.5, color="Black"),
            ),
            name="Perturbation",
            customdata=plot_df.index,  # Ensure index is passed as customdata
            text=[f"{m[0]} to {m[1]}" for m in perturbations],  # Ensure perturbations match plot_df
            hoverinfo="text+name",
        )
    )

    # Shaded error areas as traces for legend
    # ±1 kcal/mol area
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val, max_val, min_val],
            y=[min_val - 1, max_val - 1, max_val + 1, min_val + 1],
            fill="toself",
            fillcolor="darkgray",
            line=dict(width=0),
            name="± 1 kcal/mol",
            opacity=0.5,
            hoverinfo="skip",
            mode="lines",
        )
    )

    # ±2 kcal/mol area
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val, max_val, min_val],
            y=[min_val - 2, max_val - 2, max_val + 2, min_val + 2],
            fill="toself",
            fillcolor="lightgray",
            line=dict(width=0),
            name="± 2 kcal/mol",
            opacity=0.5,
            hoverinfo="skip",
            mode="lines",
        )
    )
    # Identity line
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name="Identity line",
            line=dict(color="black"),
        )
    )

    # Statistical information
    ktau = f"{stats_dict['KTAU']}"
    rmse = f"{stats_dict['RMSE']}"
    mae = f"{stats_dict['MUE']}"
    text = f"N = {plot_df.shape[0]} | crashes = {n_crashes} | τ = {ktau} | RMSE = {rmse} kcal/mol | MAE = {mae} kcal/mol"
    annotations = [
        {
            "x": 0.5,
            "y": 1.15,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "text": text,
            "font": {"size": 12},
            "xanchor": "center",
            "yanchor": "auto",
        }
    ]
    # Update layout for white background and add annotations
    fig.update_layout(
        plot_bgcolor="white",  # Set background to white
        paper_bgcolor="white",  # Also set paper background
        annotations=annotations,
        xaxis_title="ΔΔG<sub>exp</sub> [kcal/mol]",
        yaxis_title="ΔΔG<sub>pred</sub> [kcal/mol]",
        xaxis=dict(
            range=[min_val, max_val], gridcolor="lightgrey", constrain="domain"
        ),  # Add light grid, constrain domain
        yaxis=dict(
            range=[min_val, max_val], gridcolor="lightgrey", scaleanchor="x", scaleratio=1, constrain="domain"
        ),  # same as x-axis, scale to 1
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),  # Position legend at bottom right
        clickmode="event+select",  # Ensure click events are captured
    )
    return fig


@app.callback(
    [
        Output("perturbation-graph-click-store", "data"),
        Output("clicked-ddg-index-store", "data", allow_duplicate=True),
    ],  # Allow duplicate output
    [Input("perturbation-graph", "clickData")],
    [State("perturbation-graph-click-store", "data")],
    prevent_initial_call=True,  # Prevent initial call
)
def update_highlight_from_graph_click(clickData, current_click_store):
    logger.info(f"Perturbation graph clicked. Data: {clickData}")
    if clickData is None:
        raise PreventUpdate

    try:
        # Ensure the click is on a marker point which has 'text'
        if "points" not in clickData or not clickData["points"] or "text" not in clickData["points"][0]:
            logger.warning("Click on perturbation graph did not contain node text.")
            raise PreventUpdate
        clicked_node = clickData["points"][0]["text"]
        logger.info(f"Clicked node: {clicked_node}")
    except (KeyError, IndexError):
        logger.warning("Could not extract node name from perturbation graph clickData")
        raise PreventUpdate

    selected_nodes = current_click_store.get("nodes", [])
    highlight_index = None  # Default: no highlight update
    new_store_state = current_click_store  # Default to no change in node selection state

    if len(selected_nodes) == 0:  # First node selected
        new_store_state = {"nodes": [clicked_node]}
        logger.info(f"First node selected: {clicked_node}. Store: {new_store_state}")
        # No highlight index to output yet
        return new_store_state, no_update

    elif len(selected_nodes) == 1:  # Second node selected
        node1 = selected_nodes[0]
        node2 = clicked_node
        if node1 == node2:  # Clicked the same node twice
            new_store_state = {"nodes": []}  # Reset selection
            logger.info(f"Same node clicked twice. Resetting selection. Store: {new_store_state}")
            # No highlight index to output
            return new_store_state, no_update
        else:
            try:
                edge_forward = ddG_df[(ddG_df["from"] == node1) & (ddG_df["to"] == node2)]
                edge_backward = ddG_df[(ddG_df["from"] == node2) & (ddG_df["to"] == node1)]

                if not edge_forward.empty:
                    highlight_index = edge_forward.index[0]
                    new_store_state = {"nodes": []}  # Reset store after finding pair
                    logger.info(
                        f"Second node selected: {node2}. Found edge {node1}->{node2}. Highlight index: {highlight_index}. Resetting store."
                    )
                elif not edge_backward.empty:
                    highlight_index = edge_backward.index[0]
                    new_store_state = {"nodes": []}  # Reset store after finding pair
                    logger.info(
                        f"Second node selected: {node2}. Found edge {node2}->{node1}. Highlight index: {highlight_index}. Resetting store."
                    )
                else:
                    logger.warning(
                        f"No edge found between {node1} and {node2}. Resetting selection to {node2}."
                    )
                    new_store_state = {"nodes": [clicked_node]}  # Start new selection with current node
                    return new_store_state, no_update

            except NameError:
                logger.error(
                    "ddG_df not accessible in update_highlight_from_graph_click. Was initialize_data run?"
                )
                new_store_state = {"nodes": [clicked_node]}  # Reset safely
                return new_store_state, no_update
            except Exception as e:
                logger.error(f"Error finding edge between {node1} and {node2}: {e}")
                new_store_state = {"nodes": [clicked_node]}  # Reset safely
                return new_store_state, no_update

            # If highlight_index was found, return it along with the reset store state
            return new_store_state, highlight_index

    else:  # len(selected_nodes) >= 2 (Should ideally be exactly 2 before reset)
        # This case handles clicks after a pair was already selected (store should be empty now)
        # or if somehow the store ended up with >2 nodes. Treat as first click.
        new_store_state = {"nodes": [clicked_node]}
        logger.info(
            f"Store had {len(selected_nodes)} nodes. Resetting to first click: {clicked_node}. Store: {new_store_state}"
        )
        return new_store_state, no_update


@app.callback(
    Output("viewer", "data"),
    [
        Input("load_from_lig", "n_clicks"),
        Input("load_to_lig", "n_clicks"),
        Input("load_both_ligs", "n_clicks"),
    ],
    [
        State("from-node-storage", "children"),
        State("to-node-storage", "children"),
        State("target-dropdown", "value"),
    ],
)
def update_viewer(from_clicks, to_clicks, both_clicks, from_node, to_node, selected_target):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    try:
        prot_path = perturbation_root / "protein.pdb"
        water_path = perturbation_root / "water.pdb"
        if not prot_path.exists():
            logger.error(f"Protein PDB not found: {prot_path}")
            raise PreventUpdate
        elif not water_path.exists():
            logger.error(f"Water PDB not found: {water_path}")
            raise PreventUpdate
    except NameError:
        logger.error("perturbation_root not defined globally. Was initialize_data run?")
        raise PreventUpdate

    pdb_path = None
    if button_id == "load_from_lig" and from_node:
        pdb_path = CACHE_DIR / f"{perturbation_root.name}/protlig_{from_node}.pdb"
    elif button_id == "load_to_lig" and to_node:
        pdb_path = CACHE_DIR / f"{perturbation_root.name}/protlig_{to_node}.pdb"
    elif button_id == "load_both_ligs" and from_node and to_node:
        pdb_path = CACHE_DIR / f"{perturbation_root.name}/protlig_{from_node}_{to_node}.pdb"

    if not pdb_path.parent.exists():
        pdb_path.parent.mkdir(parents=True, exist_ok=True)

    if not pdb_path.exists():
        if button_id == "load_from_lig" and from_node:
            lig1_path = perturbation_root / f"{from_node}.pdb"
            logger.info(f"Loading ligand from {lig1_path}")
            pdb_df = merge_protein_lig(prot_path, lig1_path, pdb_path, new_ligname="LIG")
            water_cloud, _ = rm_HOH_clash_NN(
                pdb_df_query=read_pdb_to_dataframe(water_path),
                pdb_df_target=pdb_df,
                th=1.4,  # TODO: improve this to parse from the command tha created the FEP's
            )
            pdb_df = merge_protein_lig(
                protein_pdb=pdb_df, lig_pdb=water_cloud, save_pdb=pdb_path, new_ligname="HOH"
            )

        elif button_id == "load_to_lig" and to_node:
            lig1_path = perturbation_root / f"{to_node}.pdb"
            logger.info(f"Loading ligand from {lig1_path}")
            pdb_df = merge_protein_lig(prot_path, lig1_path, pdb_path, new_ligname="LIG")
            water_cloud, _ = rm_HOH_clash_NN(
                pdb_df_query=read_pdb_to_dataframe(water_path),
                pdb_df_target=pdb_df,
                th=1.4,
            )
            pdb_df = merge_protein_lig(
                protein_pdb=pdb_df, lig_pdb=water_cloud, save_pdb=pdb_path, new_ligname="HOH"
            )

        elif button_id == "load_both_ligs" and from_node and to_node:
            lig1_path = perturbation_root / f"{from_node}.pdb"
            lig2_path = perturbation_root / f"{to_node}.pdb"
            logger.info(f"Loading ligand from {lig1_path}")
            logger.info(f"Loading ligand from {lig2_path}")
            if lig1_path.exists() and lig2_path.exists():
                pdb_df = merge_protein_lig(prot_path, lig1_path, pdb_path, new_ligname="LIG")
                pdb_df = merge_protein_lig(pdb_path, lig2_path, pdb_path, new_ligname="LID")
                water_cloud, _ = rm_HOH_clash_NN(
                    pdb_df_query=read_pdb_to_dataframe(water_path),
                    pdb_df_target=pdb_df,
                    th=1.4,
                )
                pdb_df = merge_protein_lig(
                    protein_pdb=pdb_df, lig_pdb=water_cloud, save_pdb=pdb_path, new_ligname="HOH"
                )
            else:
                logger.error(
                    f"One or both ligand PDBs not found for 'load_both_ligs': {lig1_path}, {lig2_path}"
                )
                raise PreventUpdate
    else:
        pdb_df = read_pdb_to_dataframe(pdb_path)

    # Generate payload if PDB content was created
    if pdb_df is not None:
        if not pdb_path.exists():
            logger.error(f"PDB file not found after merge: {pdb_path}")
            raise PreventUpdate
        else:
            return molstar_helper.parse_molecule(pdb_path)
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run(debug=True)
