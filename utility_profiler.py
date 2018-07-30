"""
Utility functions for performance profiling.
"""

import pstats
import distutils.dir_util
import utility_algorithm
import utility_graph
import provided_targeted_order
import time
from functools import wraps

PROF_DATA = {}

def collect_stats(stats_dir_name, iter_range, profile_expression, params_dict):
    """
    Helper function to collect profile statistics on an expression and print
    the cumulative statistics.

    :param stats_dir_name: String name of the directory to put the stats files.
    :param iter_range: Iterable defining the number of times to loop through
        the expression we're profiling.
    :param profile_expression: String expression to call in the profiler.
    :params_dict: Dictionary of parameters to pass to the expression.

    :returns: pstats.Stats instance.
    """
    # Remove files from previous run.
    try:
        distutils.dir_util.remove_tree(stats_dir_name)
    except OSError as err:
        print("OS error: {0}".format(err) + '. ' + \
              'Nothing deleted. Directory will be created.')

    # Create directory if it doesn't exist.
    distutils.dir_util.mkpath(stats_dir_name)

    # Initialize the filename string formatter.
    filename_format_str = '{0}/profile_stats_{1}.stats'

    # Run the profiler to generate stats files.
    for i in iter_range:
        filename = filename_format_str.format(stats_dir_name, i)
        profile.runctx(profile_expression.format(i),
                       globals(),
                       params_dict,
                       filename)

    # Read all stats files into a single object
    first_file_name = filename_format_str.format(stats_dir_name, iter_range[0])
    stats = pstats.Stats(first_file_name)
    for i in iter_range:
        stats.add(filename_format_str.format(stats_dir_name, i))

    # Clean up filenames for the report
    stats.strip_dirs()

    # Sort the statistics by the cumulative time spent
    # in the function
    stats.sort_stats('cumulative')

    return stats

def profile_func(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        if fn.__name__ not in PROF_DATA:
            PROF_DATA[fn.__name__] = [0, []]
        PROF_DATA[fn.__name__][0] += 1
        PROF_DATA[fn.__name__][1].append(elapsed_time)

        return ret

    return with_profiling

def print_prof_data():
    for fname, data in PROF_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        print "Function %s called %d times. " % (fname, data[0]),
        print 'Execution time max: %.3f, average: %.3f' % (max_time, avg_time)
    return PROF_DATA

def clear_prof_data():
    global PROF_DATA
    PROF_DATA = {}
