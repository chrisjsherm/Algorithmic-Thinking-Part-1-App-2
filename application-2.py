"""
Answer the questions for Application 2 of Algorithmic Thinking Part 1.
"""
import load_graph_data
import utility_algorithm
import utility_graph
import random
import bfs
import matplotlib.pyplot as plt
import distutils.dir_util
import utility_profiler
import provided_targeted_order
import os
import utility_profiler


class X_Axis_Value:
    Nodes_Removed = 1,
    Nodes_Remaining = 2


def question_1(x_axis_value, is_attack_targeted = False):
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

    if (is_attack_targeted):
        network_attack_order = utility_algorithm.fast_targeted_order(
            utility_graph.copy_graph(network_graph))
        er_attack_order = utility_algorithm.fast_targeted_order(
            utility_graph.copy_graph(er_graph))
        upa_attack_order = utility_algorithm.fast_targeted_order(
            utility_graph.copy_graph(upa_graph))
    else:
        network_attack_order = utility_graph.random_order(network_graph)
        er_attack_order = utility_graph.random_order(er_graph)
        upa_attack_order = utility_graph.random_order(upa_graph)

    network_resilience = bfs.compute_resilience(network_graph, network_attack_order)
    er_resilience = bfs.compute_resilience(er_graph, er_attack_order)
    upa_resilience = bfs.compute_resilience(upa_graph, upa_attack_order)

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


def question_3():
    """
    Run the provided targeted_order and your implementation of 
    fast_targeted_order on a sequence of UPA graphs with n in 
    (10, 1000, 10) and m=5. Use the time module (or your favorite 
    Python timing utility) to compute the running times of these 
    functions. 

    Then, plot these running times (vertical axis) as 
    a function of the number of nodes nn (horizontal axis) using 
    a standard plot. Your plot should consist of two curves showing 
    the results of your timings. Remember to format your plot 
    appropriately and include a legend. The title of your plot 
    should indicate the implementation of Python (desktop Python 
    vs. CodeSkulptor) used to generate the timing results.
    """
    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])

    n_values = xrange(10, 1000, 10)
    m_value = 5

    provided_target_dirname = 'stats_provided_target'
    provided_target_expression = 'provided_targeted_order' + \
        '.targeted_order(utility_algorithm.dpa_algorithm({0}, m_value, False))'
    provided_target_stats = utility_profiler.collect_stats(provided_target_dirname,
                                                           n_values,
                                                           provided_target_expression,
                                                           {'m_value': m_value})
    provided_target_stats.print_stats()

    fast_target_dirname = 'stats_fast_target'
    fast_target_expression = 'utility_algorithm' + \
        '.fast_targeted_order(utility_algorithm.dpa_algorithm({0}, m_value, False))'
    fast_target_stats = utility_profiler.collect_stats(fast_target_dirname,
                                                       n_values,
                                                       fast_target_expression,
                                                       {'m_value': m_value})
    fast_target_stats.print_stats()
    for filename in os.listdir(fast_target_dirname):
        print(filename)


@utility_profiler.profile_func
def call_provided_targeted_order(ugraph):
    """
    Call the provided targeted order function with the supplied ugraph and
    profile the running time.

    @param ugraph: Dictionary representation of an undirected graph.
    """
    provided_targeted_order.targeted_order(ugraph)


@utility_profiler.profile_func
def call_fast_targeted_order(ugraph):
    """
    Call the provided targeted order function with the supplied ugraph and
    profile the running time.

    @param ugraph: Dictionary representation of an undirected graph.
    """
    utility_algorithm.fast_targeted_order(ugraph)


def question_3_profile():
    """
    Run the provided targeted_order and your implementation of 
    fast_targeted_order on a sequence of UPA graphs with n in 
    (10, 1000, 10) and m=5. Use the time module (or your favorite 
    Python timing utility) to compute the running times of these 
    functions. 

    Then, plot these running times (vertical axis) as 
    a function of the number of nodes nn (horizontal axis) using 
    a standard plot. Your plot should consist of two curves showing 
    the results of your timings. Remember to format your plot 
    appropriately and include a legend. The title of your plot 
    should indicate the implementation of Python (desktop Python 
    vs. CodeSkulptor) used to generate the timing results.
    """
    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])

    n_values = xrange(10, 1000, 10)
    m_value = 5

    for n in n_values:
        ugraph = utility_algorithm.dpa_algorithm(
            n, m_value, False
        )
        call_provided_targeted_order(ugraph)
        call_fast_targeted_order(ugraph)

    profile_data = utility_profiler.print_prof_data()

    plt.title('Targeted Order Running Time (Desktop Python)')
    plt.ylabel('Running Time (seconds)')
    plt.xlabel('Node Count')
    plt.plot(n_values, profile_data['call_provided_targeted_order'][1], '-r', label='Provided Targeted Order')
    plt.plot(n_values, profile_data['call_fast_targeted_order'][1], '-b', label='Fast Targeted Order')
    plt.legend(loc='upper right')
    plt.show()

# Question 1:
# question_1(X_Axis_Value.Nodes_Removed)

# Question 2:
# The ER and UPA graphs are resilient under random attacks as the first
# 20% of nodes are removed. Each has a largest connected component roughly
# equal to the number of nodes remaining while the first 20% of nodes are
# removed. The Network graph's largest connected component drops down to about
# 75% of the number of nodes remaining once about 12-15% of its nodes are
# removed. 
# question_1(X_Axis_Value.Nodes_Remaining)


# Question 3:
# targeted_order => O(n) = n^2
# fast_targeted_order => O(n) = n
# question_3_profile()

# Question 4:
# question_1(X_Axis_Value.Nodes_Remaining, True)

# Question 5:
# The ER graph is resilient under targeted attacks as the first 20% of its
# nodes are removed. Neither the UPA graph nor the Network graph are 
# resilient as the first 20% of nodes are removed.

# Question 6:
# While using the randomized graph from the ER algorithm gives us a graph
# resilient to targeted attacks, we cannot reccommend network designers 
# always use this random model. Networks have other considerations, such
# as latency, to consider when designing networks.