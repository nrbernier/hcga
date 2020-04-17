"""make test datasets"""
import networkx as nx
import numpy as np

from hcga.io import save_dataset


def _add_graph_desc(g, desc):
    """Add descrition desc to graph g as a graph attribute"""
    g.graph["description"] = desc
    return g


def add_dummy_node_features(graph):
    """add random node features"""
    for u in graph.nodes():
        graph.nodes[u]["feat"] = np.random.rand(10)
    return graph


def make_test_dataset(folder="./datasets", add_features=False, write_to_file=True, n_graphs=5):
    """ Makes pickle with graphs that test robustness of hcga """

    graphs = []

    # one, two and three node graphs
    for i in range(n_graphs):
        graphs.append(_add_graph_desc(nx.grid_graph([1]), "one-node graph"))
        graphs.append(_add_graph_desc(nx.grid_graph([2]), "two-node graph"))
        graphs.append(_add_graph_desc(nx.grid_graph([3]), "three-node graph"))

    # no edges
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1, weight=2)
    G.add_node(2, weight=3)
    for i in range(n_graphs):
        graphs.append(_add_graph_desc(G, "graph without edges"))

    # directed graph no weights
    G = nx.DiGraph()
    G.add_nodes_from(range(100, 110))
    for i in range(n_graphs):
        graphs.append(_add_graph_desc(G, "directed graph with no weights"))

    # directed graph weighted
    G = nx.DiGraph()
    H = nx.path_graph(10)
    G.add_nodes_from(H)
    G.add_edges_from(H.edges)
    for i in range(n_graphs):
        graphs.append(_add_graph_desc(G, "directed graph weighted"))

    # adding features to all
    if add_features:
        graphs = [add_dummy_node_features(graph) for graph in graphs]

    labels = np.random.randint(0, 2, len(graphs))

    if write_to_file:
        save_dataset(graphs, labels, "TESTDATA", folder=folder)

    for i, graph in enumerate(graphs):
        graph.graph['id'] = 1

    return graphs, labels
