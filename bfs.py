"""
Implementation of algorithms related to breadth-first search.
"""
from collections import deque


def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph "ugraph" and the node "start_node" and returns
    the set of all nodes that are visited by a bread-first search that
    starts at "start_node".
    """
    my_queue = deque([])
    nodes_visited = {start_node}
    my_queue.append(start_node)

    while len(my_queue) != 0:
        source_node = my_queue.popleft()

        if source_node not in ugraph:
            print(str(source_node) + ' does not exist in the graph.')
            continue

        for neighbor_node in ugraph[source_node]:
            if not neighbor_node in nodes_visited:
                nodes_visited.add(neighbor_node)
                my_queue.append(neighbor_node)

    return nodes_visited


def cc_visited(ugraph):
    """
    Takes the undirected graph "ugraph" and returns a list of sets, where each
    set consists of all the nodes (and nothing else) in a connected component,
    and there is exactly one set in the list for each connected component
    in "ugraph".
    """
    remaining_nodes = set(ugraph.keys())
    connected_components = list()

    while len(remaining_nodes) != 0:
        source_node = remaining_nodes.pop()
        component = bfs_visited(ugraph, source_node)
        connected_components.append(component)
        remaining_nodes.difference_update(component)

    return connected_components


def largest_cc_size(ugraph):
    """
    Takes the undirected graph "ugraph" and returns the size (an integer) of the
    largest connected component in "ugraph".
    """
    largest_component = max(cc_visited(ugraph), key=len) if ugraph else []
    return len(largest_component)


def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph, "ugraph", a list of nodes, "attack_order", and
    iterates through the nodes in "attack_order". For each node in the list,
    the function removes the given node and its edges from the graph and then
    computes the size of the largest connected component for the resulting
    graph.
    The function should return a list whose k + 1 entry is the size of the
    largest connected component in the graph after the removal of k nodes in 
    "attack_order". the first entry (indexed by zero), is the size of the 
    largest connected component in the original graph.
    """
    k_largest_component = [largest_cc_size(ugraph)]
    for node in attack_order:
        try:
            node_neighbors = ugraph.pop(node)
        except KeyError:
            print('Node ' + str(node) + ' does not exist in the graph.')

        # Remove edges of the removed node.
        for neighbor in node_neighbors:
            edges = ugraph.get(neighbor)

            if node in edges:
                edges.remove(node)

        k_largest_component.append(largest_cc_size(ugraph))

    return k_largest_component
