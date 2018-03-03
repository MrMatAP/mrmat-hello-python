
"""
py-env.py - Introspection of the Python execution environment

Introspection of the Python execution environment
"""

import argparse
import logging

from mhpython.py_env.utils import print_arguments, print_search_path

#
# Establish logging

logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
LOG = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Be chatty', action='store_true')
    parser.add_argument('--debug', help='Be very chatty', action='store_true')
    options = parser.parse_args()
    if options.verbose:
        LOG.setLevel(logging.INFO)
    if options.debug:
        LOG.setLevel(logging.DEBUG)

    print_arguments()
    print_search_path()


if __name__ == '__main__':
    run()
