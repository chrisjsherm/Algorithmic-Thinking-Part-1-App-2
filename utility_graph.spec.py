"""
Test suite for graph utility module for Week 2 of Algorithmic Thinking.
"""
import unittest
import utility_graph


class TestUtilityGraph(unittest.TestCase):
    """
    Unit tests for graph utility.
    """

    def setUp(self):
        """
        Run before each test.
        Each test method must begin with "test_"
        """
        pass

    def test_make_complete_graph(self):
        """
        Test make_complete_graph(num_nodes).
        """
        self.assertEqual(utility_graph.make_complete_graph(-1), {})
        self.assertEqual(utility_graph.make_complete_graph(1), {0: set([])})
        self.assertEqual(utility_graph.make_complete_graph(2),
                         {0: set([1]), 1: set([0])})
        self.assertEqual(utility_graph.make_complete_graph(4),
                         {0: set([1, 2, 3]), 1: set([0, 2, 3]),
                          2: set([0, 1, 3]), 3: set([0, 1, 2])})

    def test_compute_in_degrees(self):
        """
        Test compute_in_degrees(digraph).
        """
        self.assertEqual(utility_graph.compute_in_degrees({0: [1], 1: []}),
                         {0: 0, 1: 1})
        self.assertEqual(utility_graph.compute_in_degrees(
            {0: [1, 3], 1: [2], 2: [0], 3: []}),
            {0: 1, 1: 1, 2: 1, 3: 1})
        self.assertEqual(utility_graph.compute_in_degrees(
            {0: set([]), 1: set([0]), 2: set([0]), 3: set([0]), 4: set([0])}),
            {0: 4, 1: 0, 2: 0, 3: 0, 4: 0})

    def test_count_edges(self):
        """
        Test count_edges.
        """
        my_graph = {}
        my_graph[0] = set([1])
        my_graph[1] = set([0, 2])
        my_graph[2] = set([1])
        my_graph[3] = set([4])
        my_graph[4] = set([3])
        my_graph[5] = set([0, 1, 3, 4])
        self.assertEqual(utility_graph.count_edges(my_graph), 10)
        self.assertEqual(utility_graph.count_edges(my_graph, False), 7)

    def test_in_degree_distribution(self):
        """
        Test in_degree_distribution(digraph).
        """
        self.assertEqual(utility_graph.in_degree_distribution({0: [1], 1: []}),
                         {0: 1, 1: 1})
        self.assertEqual(utility_graph.in_degree_distribution(
            {0: [1, 3], 1: [2], 2: [0], 3: []}),
            {1: 4})
        self.assertEqual(utility_graph.in_degree_distribution(
            {0: set([]), 1: set([0]), 2: set([0]), 3: set([0]), 4: set([0])}),
            {0: 4, 4: 1})

    def test_out_degree_distribution(self):
        """
        Test out_degree_distribution(digraph).
        """
        self.assertEqual(utility_graph.out_degree_distribution({0: [1], 1: []}),
                         {0: 1, 1: 1})
        self.assertEqual(utility_graph.out_degree_distribution(
            {0: [1, 3], 1: [2], 2: [0], 3: []}),
            {0: 1, 1: 2, 2: 1})
        self.assertEqual(utility_graph.out_degree_distribution(
            {0: set([]), 1: set([0]), 2: set([0]), 3: set([0]), 4: set([0])}),
            {0: 1, 1: 4})

    def test_average_out_degree(self):
        """
        Test average_out_degree(digraph).
        """
        self.assertEqual(utility_graph.average_out_degree({0: [1], 1: []}),
                         0.5)

        self.assertEqual(utility_graph.average_out_degree({0: [1, 3], 1: [2], 2: [0], 3: []}),
                         1.0)

    def test_normalize_distribution(self):
        """
        Test normalize_distribution(distribution_dict).
        """
        self.assertEqual(utility_graph.normalize_distribution(
            {0: 4, 4: 1}),
            {0: 0.8, 4: 0.2}
        )

    def test_random_order(self):
        my_graph = {}
        my_graph[0] = set([1])
        my_graph[1] = set([0, 2])
        my_graph[2] = set([1])
        my_graph[3] = set([4])
        my_graph[4] = set([3])

        self.assertItemsEqual(utility_graph.random_order(my_graph),
                              [0, 1, 2, 3, 4])
        self.assertEqual(my_graph, my_graph) # Make sure graph is still intact.

        self.assertItemsEqual(utility_graph.random_order({}), [])


suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilityGraph)
unittest.TextTestRunner(verbosity=2).run(suite)
# Run in terminal with: python ./utility_graph.spec.py
