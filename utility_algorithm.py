"""
Algorithms from Application #1.
"""
import utility_graph
import random

def er_algorithm(node_count, p, is_directed_graph=True):
    """
    Compute a graph given the number of nodes in the graph and the probability
    each pair of nodes is connected.

    :param node_count: Number of nodes in the graph.
    :param p: Probability that two nodes are connected.
    :param is_directed_graph: Indicates whether the resulting graph should have
        directed or undirected edges.
    :returns: Dictionary representation of the graph, with each key an integer
        representing the node and each value a set respresenting the in node
        edges.
    """
    node_list = [node for node in xrange(node_count)]
    graph_dict = {}
    for node in node_list:
        # Protect against the node already existing in the dictionary when
        # the graph is undirected.
        if node not in graph_dict:
            graph_dict[node] = set()
        if is_directed_graph:
            potential_edges = node_list[0:node] + node_list[node + 1:]
        else:
            # Undirected graphs consider each connection between nodes once.
            potential_edges = node_list[node + 1:]
        for edge in potential_edges:
            a = random.uniform(0, 1)
            if a < p:
                graph_dict[node].add(edge)

                # If the graph is not directed, we need the edge's adjacency
                # set to have a matching entry for node.
                if not is_directed_graph:
                    if edge not in graph_dict:
                        # Edge is not yet in the dictionary. Add it.
                        graph_dict[edge] = set()
                    # Add the matching edge in the undirected graph.
                    graph_dict[edge].add(node)

    return graph_dict


def dpa_algorithm(node_count, m, is_directed_graph=True):
    """
    Create a directed graph of n nodes iteratively, where in each iteration a
    new node is created, added to the graph, and connected to a subset of
    existing nodes.
    Grow the graph by adding n - m nodes, where each new node is connected to
    m nodes randomply chosen from the set of existing nodes. An existing node
    may be chosen more than once in an iteration, but duplicates are eliminated.

    :param node_count: Final number of nodes in the graph.
    :param m: Number of existing nodes to which a new node is connected.
    :param is_directed_graph: Optionally specify the graph is undirected.
    :returns: Dictionary representation of the graph with each key an integer
        representing the node and each value a set representing the in-node edges.
    """
    dpa_graph = utility_graph.make_complete_graph(m)

    # Add each node to the list "in-degree count + 1" times.
    # In-degree count for each node is (m - 1).
    nodes_prob_by_in_degree = [node for node in xrange(m)
                               for dummy_idx in range((m - 1) + 1)]

    for idx in xrange(m, node_count):
        # The ID of the new node is the length of the graph keys.
        node_id = len(dpa_graph)
        new_node_edges = set()

        # Add "m" edges.
        for edge_idx in xrange(0, m):
            new_node_edges.add(random.choice(nodes_prob_by_in_degree))

        # Add the new node to the graph.
        dpa_graph[node_id] = new_node_edges

        # Add the new edges to the probability list to keep the probability of
        # randomly choosing a node equal to it's in-degree + 1.
        nodes_prob_by_in_degree.extend(new_node_edges)

        # If the graph is undirected, add the new node as an edge to each node
        # it is has edge with.
        if not is_directed_graph:
            for edge in new_node_edges:
                dpa_graph[edge].add(node_id)

            # Add the new node to the probability graph proportional to its
            # number of edges.
            nodes_prob_by_in_degree.extend(list(node_id for dummy_x in xrange(
                0, len(new_node_edges))))

        # Add the new node to the probability graph since the probability of
        # randomly choosing a node is equal to it's in-degree (which is
        # currently zero) + 1.
        nodes_prob_by_in_degree.append(node_id)

    return dpa_graph


def fast_targeted_order(ugraph):
    """
    Takes an undirected graph, ugraph, and creates a list, degree_sets, whose
    kth element is the set of nodes with degree k. Then, iterate through the 
    list, degree_sets, in order of decreasing degree.

    When encountering a non-empty set, the nodes in this set must be of
    maximum degree. Repeatedly choose a node from this set, delete the node from
    the graph, and update degree_sets accordingly.

    :param ugraph: Dictionary representing an undirected graph, with the keys
        equivalent to the nodes and the values a set equivalent to the edges.
    :return: Ordered list of the nodes in the graph in decreasing order of
        their degrees.
    """
    degree_sets = dict()
    for idx in xrange(len(ugraph)):
        degree_sets[idx] = set()

    for node, edges in ugraph.iteritems():
        node_degree = len(edges)
        degree_sets[node_degree].add(node)

    list_decreasing_degrees = []

    for k in xrange(len(ugraph) - 1, 0, -1):
        while len(degree_sets[k]) != 0:
            print('k equals ', str(k))
            node = degree_sets[k].pop()
            node_neighbors = ugraph[node]
            for neighbor in node_neighbors:
                neighbor_degree = len(ugraph[neighbor])
                degree_sets[neighbor_degree].remove(neighbor)
                degree_sets[neighbor_degree - 1].add(neighbor)
            
            list_decreasing_degrees.append(node)
            ugraph.pop(node)

    return list_decreasing_degrees

