"""
Test suite for algorithm utilty module for Week 4 of Algorithmic Thinking Part 1.
"""
import unittest
import utility_algorithm


class TestUtilityAlgorithm(unittest.TestCase):
    """
    Unit tests for algorithm utility.
    """

    def setup(self):
        """
        Run before each test.
        Each test method must begin with "test_".
        """
        pass

    # TODO: Figure out why all elements are not added to list.
    def test_fast_targeted_order(self):
        my_graph = {}
        my_graph[0] = set([1])
        my_graph[1] = set([0, 2])
        my_graph[2] = set([1])
        my_graph[3] = set([4])
        my_graph[4] = set([3])
        self.assertEqual(utility_algorithm.fast_targeted_order(my_graph),
            [1, 0, 2, 3, 4])

suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilityAlgorithm)
unittest.TextTestRunner(verbosity=2).run(suite)
# Run in terminal with: python ./utility_graph.spec.py
