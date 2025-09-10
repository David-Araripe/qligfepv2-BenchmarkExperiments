import networkx as nx
import numpy as np
from typing import List, Tuple
import plotly.graph_objects as go


def generate_graph(df) -> nx.Graph:
    """create a networkx graph from a dataframe

    Args:
        df: dataframe with the edges of the graph

    Returns:
        networkx graph
    """    
    all_nodes = np.unique(df["from"].tolist() + df["to"].tolist())
    G = nx.Graph()
    for node in all_nodes:
        G.add_node(node, label=node)
    for idx, row in df.iterrows():
        G.add_edge(row["from"], row["to"])
    for idx, row in df.iterrows():
        G[row["from"]][row["to"]]["similarity"] = row["similarity"]
    return G


def get_most_connected_cpd(G, df) -> Tuple[str, str]:
    most_connected = max(G.degree, key=lambda x: x[1])[0]
    from_structs = df[df["from"] == most_connected]
    to_structs = df[df["to"] == most_connected]
    if not from_structs.empty:
        most_connected_smiles = from_structs["from_smiles"].values[0]
        most_connected_name = from_structs["from"].values[0]
    else:
        most_connected_smiles = to_structs["to_smiles"].values[0]
        most_connected_name = to_structs["to"].values[0]
    return most_connected_name, most_connected_smiles


def set_nx_graph_coordinates(G, k=0.7, iterations=50, seed=50, weight="weight", threshold=0.005):
    pos = nx.spring_layout(G, k=k, iterations=iterations, seed=seed, weight=weight, threshold=threshold)
    nx.set_node_attributes(G, pos, "pos")
    return G


def extract_graph_coordinates(G) -> Tuple[List, List, List, List, List]:
    """extracts the x and y coordinates of the nodes and edges of a networkx graph so
    that it can be plotted using plotly

    Args:
        G: networkx graph

    Returns:
        Tuple of node_x, node_y, edge_x, edge_y
    """
    node_x = []
    node_y = []
    node_labels = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(node)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    return node_labels, node_x, node_y, edge_x, edge_y


def extract_graph_coordinates_with_crashed_edges(G, crashed_edge_pairs) -> Tuple[List, List, List, List, List, List]:
    """extracts the x and y coordinates of the nodes and edges of a networkx graph,
    separating crashed edges from normal edges

    Args:
        G: networkx graph
        crashed_edge_pairs: set of (from, to) tuples representing crashed edges

    Returns:
        Tuple of node_labels, node_x, node_y, edge_x, edge_y, crashed_edge_coords
    """
    node_x = []
    node_y = []
    node_labels = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(node)

    # Separate normal edges and crashed edges
    normal_edge_x = []
    normal_edge_y = []
    crashed_edge_x = []
    crashed_edge_y = []
    
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        
        # Check if this edge is a crashed edge (check both directions)
        if (edge[0], edge[1]) in crashed_edge_pairs or (edge[1], edge[0]) in crashed_edge_pairs:
            # Add to crashed edges
            crashed_edge_x.extend([x0, x1, None])
            crashed_edge_y.extend([y0, y1, None])
        else:
            # Add to normal edges
            normal_edge_x.extend([x0, x1, None])
            normal_edge_y.extend([y0, y1, None])

    # Return normal edge coordinates and crashed edge coordinates separately
    crashed_edge_coords = [crashed_edge_x, crashed_edge_y]
    return node_labels, node_x, node_y, normal_edge_x, normal_edge_y, crashed_edge_coords


def add_legend_trace_to_graph_figure(fig, color_dict):
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],  # No actual data points
            mode="markers",
            marker=dict(size=10, color=color_dict["from"]),
            legendgroup="from",  # Same legend group for "from" items
            showlegend=True,
            name="From",
        )
    )
    # Add a trace for "to" legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],  # No actual data points
            mode="markers",
            marker=dict(size=10, color=color_dict["to"]),
            legendgroup="to",  # Same legend group for "to" items
            showlegend=True,
            name="To",
        )
    )
    # Add a trace for "most connected" legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],  # No actual data points
            mode="markers",
            marker=dict(size=10, color=color_dict["most_connected"]),
            legendgroup="most_connected",  # Same legend group for "most connected" items
            showlegend=True,
            name="Most Connected",
        )
    )
    # Add a trace for "no_highlight" legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],  # No actual data points
            mode="markers",
            marker=dict(size=10, color=color_dict["no_highlight"]),
            legendgroup="no_highlight",  # Same legend group for "no_highlight" items
            showlegend=True,
            name="No Highlight",
        )
    )
    # Add a trace for crashed edges legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],  # No actual data points
            mode="lines",
            line=dict(width=3, color="red", dash="dash"),
            showlegend=True,
            name="Crashed Edges",
        )
    )
