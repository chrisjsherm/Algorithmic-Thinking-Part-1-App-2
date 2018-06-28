"""
Test suite for bfs utility for Week 4 of Algorithmic Thinking.
"""
import unittest
import bfs

class TestBFS(unittest.TestCase):
  """
  Unit tests for bfs utility.
  """
  def setUp(self):
    """
    Run before each test.
    Each test method must begin with "test_".
    """
    pass

  def test_bfs_visited(self):
    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])

    self.assertEqual(bfs.bfs_visited(my_graph, 0), set([0, 1, 2]))
    self.assertEqual(bfs.bfs_visited(my_graph, 3), set([3, 4]))
    self.assertEqual(bfs.bfs_visited(my_graph, 4), set([3, 4]))

  def test_cc_visited(self):
    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])

    self.assertEqual(bfs.cc_visited(my_graph), [set([0, 1, 2]), set([3, 4])])

  def test_largest_cc_size(self):
    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])
    my_graph[5] = set([0, 1, 3, 4])

    self.assertEqual(bfs.largest_cc_size(my_graph), 6)

  def test_compute_resilience(self):
    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])

    self.assertEqual(bfs.compute_resilience(my_graph, [2]), [3, 2])

    my_graph = {}
    my_graph[0] = set([1])
    my_graph[1] = set([0, 2])
    my_graph[2] = set([1])
    my_graph[3] = set([4])
    my_graph[4] = set([3])
    my_graph[5] = set([0, 1, 3, 4])

    self.assertEqual(bfs.compute_resilience(my_graph, [5, 2]), [6, 3, 2])

suite = unittest.TestLoader().loadTestsFromTestCase(TestBFS)
unittest.TextTestRunner(verbosity=2).run(suite)
# Run in terminal with python ./bfs.spec.py