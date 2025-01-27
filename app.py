import json
from loguru import logger
from urllib.parse import quote
from pathlib import Path
from dash import Dash, dcc, html, Input, Output, callback_context, State
import plotly.graph_objs as go
import numpy as np
from dash.exceptions import PreventUpdate
from chemFilters.img_render import MolPlotter
from WeightedCCC import GraphClosure
from dash_molstar.utils import molstar_helper
import dash_molstar
import pandas as pd

# local imports
from assets.pdb_handler import merge_protein_lig, create_pdb_ligand_files
from assets.molecule_handler import lomap_json_to_dataframe, add_images_to_df
from assets.graph_handler import (
    extract_graph_coordinates,
    generate_graph,
    get_most_connected_cpd,
    set_nx_graph_coordinates,
    add_legend_trace_to_graph_figure,
)
from assets.stats_make import cinnabar_stats

# initialize some data that can be later updated based on the dropdown menu...
target_name = "tyk2"
method_name = "Gbar"
results_root = Path("results")
molplotter = MolPlotter(from_smi=True, size=(-1, -1))
crashed_edges = []

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
        global perturbation_root, mapping, ddG_df, G, node_labels, node_x, node_y, edge_x, edge_y, most_connected_name, perturbations, crashed_edges
        perturbation_root = Path(f"perturbations/{target_name}")
        if not perturbation_root.exists():
            raise FileNotFoundError(f"Target directory {perturbation_root} not found")

        create_pdb_ligand_files(root_path=perturbation_root, overwrite=False)
        mapping = json.loads((results_root / f"{target_name}/mapping_ddG.json").read_text())
        ddG_df = lomap_json_to_dataframe(mapping, molplotter)
        G = generate_graph(ddG_df)
        G = set_nx_graph_coordinates(G)
        node_labels, node_x, node_y, edge_x, edge_y = extract_graph_coordinates(G)
        most_connected_name, most_connected_smiles = get_most_connected_cpd(G, ddG_df)
        if not np.isin(["from_svg", "to_svg"], ddG_df.columns).all():
            ddG_df = add_images_to_df(ddG_df, molplotter)

        nan_edges = ddG_df.query("Q_ddG_avg.isnull()")
        crashed_edges = nan_edges.apply(lambda x: f"FEP_{x['from']}_{x['to']}", axis=1).tolist()
        ddG_df = ddG_df.dropna(subset=["Q_ddG_avg"]).reset_index(drop=True)

        perturbations = list(zip(ddG_df["from"], ddG_df["to"]))
        ccc = GraphClosure(from_lig=ddG_df["from"], to_lig=ddG_df["to"], b_ddG=ddG_df["Q_ddG_avg"])
        ccc.getAllCyles()
        if len(ccc.cycles) == 0:
            raise Exception("No cycle found!")
        ccc.iterateCycleClosure(minimum_cycles=2)
        ccc_results_df = (
            ccc.getEnergyPairsDataFrame(verbose=False)
            .rename(columns={"ddG_wcc0": "ccc_ddG", "pair_error": "ccc_error"})
            .drop(columns=["Pair"])
            .assign(
                ccc_ddG=lambda x: x["ccc_ddG"].astype(float), ccc_error=lambda x: x["ccc_error"].astype(float)
            )
        )
        ddG_df = pd.concat([ddG_df, ccc_results_df], axis=1).assign(
            residual=lambda x: x["Q_ddG_avg"] - x["ddg_value"]
        )
    except Exception as e:
        print(f"Error initializing data for target {target_name}: {e}")
        raise


# Initialize with the first target
initialize_data(available_targets[0])
# Set the CSS for the app & layout
FLATLY_CSS = "https://bootswatch.com/4/flatly/bootstrap.min.css"
app = Dash(__name__, external_stylesheets=[FLATLY_CSS])
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
                dcc.Graph(id="ddg-plot", style={"width": "38%", "height": "100%"}),
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
                                    style={"maxWidth": "35%", "marginRight": "5%", "height": "250px"},
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
                                html.Img(id="lig2_img", style={"maxWidth": "35%", "height": "250px"}),
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
                        "height": "400px",  # Fixed height for the container
                        "width": "38%",  # Fixed width for the container
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
                # TODO: change here to display the network graph
                # TODO: add the network graph to the layout,
                dcc.Graph(id="perturbation-graph", style={"width": "38%", "height": "400px"}),
                # html.Img(src="my-graph-structure-here", style={"height": "400px", "width": "48%", "marginRight": "2%"}),
                # html.Img(src="your-second-image-url-here", style={"width": "38%", "height": "50%"}),
                dash_molstar.MolstarViewer(id="viewer", style={"width": "700px", "height": "500px"}),
                # Hidden divs for storing "from" and "to" node identifiers
                html.Div(id="from-node-storage", style={"display": "none"}),
                html.Div(id="to-node-storage", style={"display": "none"}),
                html.Div(id="both-nodes-storage", style={"display": "none"}),
                # Buttons for loading "from" and "to" nodes
                html.Div(
                    [
                        html.Button(
                            'Load "From" Ligand', id="load_from_lig", style={"margin-bottom": "10px"}
                        ),
                        html.Button('Load "To" Ligand', id="load_to_lig", style={"margin-bottom": "10px"}),
                        html.Button(
                            "Load Both Ligands", id="load_both_ligs", style={"margin-bottom": "10px"}
                        ),
                    ],
                    style={"display": "flex", "flex-direction": "column", "align-items": "center"},
                ),
            ],
        ),
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
    most_connected_name

    color_mapping = {
        _from: color_dict["from"],
        _to: color_dict["to"],
    }
    if most_connected_name not in highlighted_nodes:
        color_mapping.update({most_connected_name: color_dict["most_connected"]})
    highlighted = np.unique(highlighted_nodes + [most_connected_name])
    rest = np.setdiff1d(node_labels, highlighted)
    color_mapping.update({node: color_dict["no_highlight"] for node in rest})

    node_colors = [color_mapping[node] for node in node_labels]
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
    ],
    [Input("ddg-plot", "clickData"), Input("target-dropdown", "value")],
)
def update_all_components(clickData, selected_target):
    ctx = callback_context
    if not ctx.triggered:
        # Initialize with default view
        initialize_data(selected_target)
        return create_ddg_plot(ddG_df, perturbations), construct_network_graph(), "", "", "", "", ""

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Handle target selection
    if trigger_id == "target-dropdown":
        initialize_data(selected_target)
        return create_ddg_plot(ddG_df, perturbations), construct_network_graph(), "", "", "", "", ""

    # Handle plot click
    elif trigger_id == "ddg-plot":
        if clickData is None:
            raise PreventUpdate

        try:
            index = clickData["points"][0]["customdata"]
            data = ddG_df.loc[index]
            lig1, lig2 = data["from"], data["to"]

            molecule_name = f"Perturbation error = {data['residual']:.2f}"
            lig1_img = f"data:image/svg+xml;utf8,{quote(data['from_svg'])}"
            lig2_img = f"data:image/svg+xml;utf8,{quote(data['to_svg'])}"

            return (
                create_ddg_plot(ddG_df, perturbations),
                construct_network_graph([lig1, lig2]),
                molecule_name,
                lig1_img,
                lig2_img,
                lig1,
                lig2,
            )
        except Exception as e:
            print(f"Error in update_all_components: {e}")
            raise PreventUpdate


def create_ddg_plot(ddG_df, perturbations=None):
    if perturbations is None:
        perturbations = list(zip(ddG_df["from"], ddG_df["to"]))
    # Move the plot creation code here from the old update_ddg_plot function
    logger.info(f"Crashed perturbations: {crashed_edges}")
    n_crashes = len(crashed_edges)
    ddG_df = ddG_df.dropna(subset=["Q_ddG_avg"])
    stats_dict = cinnabar_stats(ddG_df["Q_ddG_avg"], ddG_df["ddg_value"])
    all_values = np.concatenate((ddG_df["Q_ddG_avg"], ddG_df["ddg_value"]))
    margin = 1.0
    min_val, max_val = all_values.min() - margin, all_values.max() + margin

    # Create figure
    fig = go.Figure()
    # Add scatter plot with error bars
    fig.add_trace(
        go.Scattergl(
            x=ddG_df["ddg_value"],
            y=ddG_df["Q_ddG_avg"],
            mode="markers",
            error_y=dict(type="data", array=ddG_df["Q_ddG_sem"], visible=True, thickness=0.75, color="Black"),
            marker=dict(size=6, opacity=0.8, line=dict(width=0.5, color="Black")),
            name="Perturbation",
            customdata=ddG_df.index,
            text=[f"{m[0]} to {m[1]}" for m in perturbations],
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
    text = f"N = {ddG_df.shape[0]} | crashes = {n_crashes} | τ = {ktau} | RMSE = {rmse} kcal/mol | MAE = {mae} kcal/mol"
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
        annotations=annotations,
        xaxis_title="ΔΔG<sub>exp</sub> [kcal/mol]",
        yaxis_title="ΔΔG<sub>pred</sub> [kcal/mol]",
        xaxis=dict(range=[min_val, max_val]),
        yaxis=dict(range=[min_val, max_val]),
        legend=dict(yanchor="middle", y=0.5, xanchor="left", x=1.1),
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


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
    prevent_initial_call=True,
)
def update_viewer(from_clicks, to_clicks, both_clicks, from_node, to_node, selected_target):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    perturbation_root = Path(f"perturbations/{selected_target}")

    try:
        if button_id == "load_from_lig" and from_node:
            prot_path = perturbation_root / "protein.pdb"
            lig_path = perturbation_root / f"{from_node}.pdb"
            merge_protein_lig(prot_path, lig_path, perturbation_root / "protlig.pdb", new_ligname="LIG")
        elif button_id == "load_to_lig" and to_node:
            prot_path = perturbation_root / "protein.pdb"
            lig_path = perturbation_root / f"{to_node}.pdb"
            merge_protein_lig(prot_path, lig_path, perturbation_root / "protlig.pdb", new_ligname="LIG")
        elif button_id == "load_both_ligs" and from_node and to_node:
            prot_path = perturbation_root / "protein.pdb"
            lig1_path = perturbation_root / f"{from_node}.pdb"
            lig2_path = perturbation_root / f"{to_node}.pdb"
            merge_protein_lig(prot_path, lig1_path, perturbation_root / "protlig.pdb", new_ligname="LIG")
            merge_protein_lig(
                perturbation_root / "protlig.pdb",
                lig2_path,
                perturbation_root / "protlig.pdb",
                new_ligname="LID",
            )
        else:
            raise PreventUpdate

        outname = str(perturbation_root / "protlig.pdb")
        return molstar_helper.parse_molecule(outname)
    except Exception as e:
        print(f"Error in update_viewer: {e}")
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
