"""
Graph utility module for Week 2 of Algorithmic Thinking.
"""

import matplotlib.pyplot as plt
import numpy
import random

EX_GRAPH0 = {
    0: set([1, 2]),
    1: set([]),
    2: set([])
}

EX_GRAPH1 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3]),
    3: set([0]),
    4: set([1]),
    5: set([2]),
    6: set([])
}

EX_GRAPH2 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3, 7]),
    3: set([7]),
    4: set([1]),
    5: set([2]),
    6: set([]),
    7: set([3]),
    8: set([1, 2]),
    9: set([0, 3, 4, 5, 6, 7])
}


def make_complete_graph(num_nodes):
    """
    Returns a dictionary corresponding to a complete directed graph with the
    specified number of nodes.
    A "complete graph" contains all possible edges subject to the restriction that
    self-loops are not allowed.
    The nodes of the graph should be numbered 0 to num_nodes - 1 when num_nodes
    is positive.
    Otherwise, returns a dictionary corresponding to the empty graph.
    """
    if num_nodes <= 0:
        return {}

    if num_nodes == 1:
        return {0: set([])}

    graph = {}
    elements = [idx for idx in xrange(num_nodes)]
    for node_i in xrange(num_nodes):
        graph[node_i] = set(elements[0:node_i] + elements[node_i + 1:])

    return graph


def compute_out_degrees(digraph):
    """
    Takes a directed graph (represented as a dictionary) and computes the
    out-degrees for the nodes in the graph.
    Returns a dictionary with the same keys as the graph parameter whose
    corresponding values are the number of edges whose tail matches a
    particular node.
    """
    out_degrees_by_node = {}
    for node in digraph:
        out_degrees_by_node[node] = len(digraph[node])
    return out_degrees_by_node


def compute_in_degrees(digraph):
    """
    Takes a directed graph (represented as a dictionary) and computes the
    in-degrees for the nodes in the graph.
    Returns a dictionary with the same keys as the graph parameter whose
    corresponding values are the number of edges whose head matches a
    particular node.
    """
    in_degrees_by_node = {}

    for node in digraph:
        if not node in in_degrees_by_node:
            in_degrees_by_node[node] = 0
        for head in digraph[node]:
            in_degrees_by_node[head] = in_degrees_by_node.get(head, 0) + 1
    return in_degrees_by_node

def count_edges(graph, is_directed=True):
    """
    Takes a graph and whether it is directed and returns the number of edges
    that exist in the graph.

    :param graph: Graph represented as a dictionary with nodes as the keys and
        adjacency sets as the values.
    :param is_directed: Boolean determining whether the graph is directed or not.
    :returns: Integer representing the number of edges in the graph.
    """
    edges = set()
    if is_directed:
        for node in graph:
            for edge in graph[node]:
                edges.add(tuple((node, edge)))
        return len(edges)

    for node in graph:
        for edge in graph[node]:
            if is_directed:
                # Tuples maintain order, which is good for directed edges.
                edges.add(tuple((node, edge)))
            else:
                # Sets do not consider order, which is good for undirected edges.
                # We need to use a frozenset to indicate it is immutable and can
                # be hashed by the outer set we're adding it to.
                edges.add(frozenset((node, edge)))
    return len(edges)

def in_degree_distribution(digraph):
    """
    Takes a directed graph (represented as a dictionary) and computes the 
    unnormalized distribution of the in-degrees of the graph.
    Returns a dictionary whose keys correspond to in-degrees of nodes in the
    graph. The value associated with each key is the number of nodes with that
    in-degree.
    In-degrees with no corresponding nodes in the graph are not included in
    the dictionary.
    """
    distribution_dict = dict()
    in_degrees_dict = compute_in_degrees(digraph)
    for key in in_degrees_dict:
        distribution_dict[in_degrees_dict[key]] = distribution_dict.get(
            in_degrees_dict[key], 0) + 1

    return distribution_dict


def out_degree_distribution(digraph):
    """
    Takes a directed graph (represented as a dictionary) and computes the 
    unnormalized distribution of the out-degrees of the graph.
    Returns a dictionary whose keys correspond to out-degrees of nodes in the
    graph. The value associated with each key is the number of nodes with that
    out-degree.
    Out-degrees with no corresponding nodes in the graph are not included in
    the dictionary.
    """
    distribution_dict = dict()
    out_degrees_dict = compute_out_degrees(digraph)
    for key in out_degrees_dict:
        distribution_dict[out_degrees_dict[key]] = distribution_dict.get(
            out_degrees_dict[key], 0) + 1

    return distribution_dict


def average_out_degree(digraph):
    """
    Takes a directed graph (respresented as a dictionary) and computes the
    average out degree of nodes in the graph.
    """
    sum_out_degrees = 0.0

    if len(digraph) == 0:
        return sum_out_degrees

    for key, value in digraph.items():
        sum_out_degrees += len(value)

    return sum_out_degrees / len(digraph)


def normalize_distribution(distribution_dict):
    """
    Takes a distribution of in degrees (represented as a dictionary) and
    computes the normalized distribution (make the values in the dictionary
    sum to one).
    """
    normalized_distribution_dict = {}
    denominator = 0.0
    for key in distribution_dict:
        denominator += distribution_dict[key]
        normalized_distribution_dict[key] = \
            lambda x=distribution_dict[key]: x / denominator

    return {edge_count: normalized_distribution_dict[edge_count]()
            for edge_count in normalized_distribution_dict}


def plot_log_log_scatter(normalized_dist_dict, title, x_axis_label, y_axis_label):
    """
    Use matplotlib to create a log/log scatter plot.
    """
    plt.scatter(numpy.log10(normalized_dist_dict.keys()),
                numpy.log10(normalized_dist_dict.values()))
    plt.title(title)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)

    plt.show()

def random_order(a_graph):
    """
    Takes a graph and returns a list of nodes in the graph in random order.

    :param a_graph: Dictionary representation of a graph.
    :returns: List of nodes in the graph in random order.
    """
    node_list = []

    # Copy dictionary to avoid removing elements from input parameter.
    graph_copy = dict((a_key, a_value) for a_key, a_value in a_graph.items())

    while len(graph_copy) != 0:
        node = random.choice(graph_copy.keys())
        node_list.append(node)
        graph_copy.pop(node, -1)

    return node_list