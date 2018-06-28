"""
Answer the questions for Application 2 of Algorithmic Thinking Part 1.
"""
import load_graph_data
import utility_algorithm
import utility_graph
import random
import bfs
import matplotlib.pyplot as plt


class X_Axis_Value:
    Nodes_Removed = 1,
    Nodes_Remaining = 2


def question_1(x_axis_value):
    """
    Determine the probability "p" such that the ER graph computed using this
    probability has approximately the same number of edges as the computer
    network ("p" should be consistent with considering each edge in the
    undirected graph exactly once, not twice).

    Likewise, compute an integer "m" such that the number of edges
    in the UPA graph is close to the number of edges in the computer network.

    For each graph, compute a random attack order and use this attack order
    to compute the resilience of the graph. Plot the results  as three curves
    in a single standard plot. Use a line plot for each curve. The x-axis
    is the number of nodes removed while the y-axis is the size of the largest
    connected component.
    """
    network_graph = load_graph_data.load_graph(load_graph_data.NETWORK_URL)
    node_count = len(network_graph)
    edge_count = utility_graph.count_edges(network_graph, False)
    print('The network graph has ' + str(node_count) + ' nodes and ' +
          str(edge_count) + ' edges.')

    probability_connected = 0.004
    er_graph = utility_algorithm.er_algorithm(
        node_count, probability_connected, False)
    er_edge_count = utility_graph.count_edges(er_graph, False)
    print('With the probability two nodes are connected equal to ' +
          str(probability_connected) +
          ', this run of the ER graph algorithm resulted in ' +
          str(len(er_graph)) + ' nodes and ' +
          str(er_edge_count) + ' edges.')

    # Divide average_out_degree by two since this is an undirected graph.
    avg_out_degree = int(
        round(utility_graph.average_out_degree(network_graph) / 2))
    print('Number of existing nodes to which a new node in the UPA graph ' +
          'will be connected is ' + str(avg_out_degree) + '.')

    upa_graph = utility_algorithm.dpa_algorithm(
        node_count, avg_out_degree, False)
    print('This run of the UPA algorithm resulted in a graph with ' +
          str(len(upa_graph)) + ' nodes and ' +
          str(utility_graph.count_edges(upa_graph, False)) + ' edges.')

    attack_order = utility_graph.random_order(network_graph)
    network_resilience = bfs.compute_resilience(network_graph, attack_order)

    attack_order = utility_graph.random_order(er_graph)
    er_resilience = bfs.compute_resilience(er_graph, attack_order)

    attack_order = utility_graph.random_order(upa_graph)
    upa_resilience = bfs.compute_resilience(upa_graph, attack_order)

    if x_axis_value == X_Axis_Value.Nodes_Removed:
        plt.xlabel('Nodes Removed')
        x_axis_values = [idx for idx in xrange(node_count + 1)]
    elif x_axis_value == X_Axis_Value.Nodes_Remaining:
        plt.xlabel('Nodes Remaining')

        # Invert x-axis so it counts down as nodes are removed.
        plt.gca().invert_xaxis()

        x_axis_values = [idx for idx in xrange(node_count + 1, 0, -1)]
    else:
        raise ValueError('X-axis value ', str(x_axis_value),
                         ' does not exist.')

    plt.title('Attack Resiliency')
    plt.ylabel('Largest Connected Component')
    plt.plot(x_axis_values, network_resilience, '-b', label='Network')
    plt.plot(x_axis_values, er_resilience, '-r', label='ER')
    plt.plot(x_axis_values, upa_resilience, '-g', label='UPA')
    plt.legend(loc='upper right')
    plt.show()

#question_1(X_Axis_Value.Nodes_Removed)

# Question 2.
question_1(X_Axis_Value.Nodes_Remaining)


