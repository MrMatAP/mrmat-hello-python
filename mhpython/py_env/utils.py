"""
Utilities for py-env.py

Note how single-quotes still perform expansion on \\n
"""

import sys


def print_arguments() -> str:
    """
    Print the arguments of the invoking script
    :return: A simple string
    """
    print('Arguments:')
    for i, arg in enumerate(sys.argv):
        print("\t{} {}".format(i, arg))
    print('\n')


def print_search_path() -> str:
    """
    Print the current module search path. When looking for a module, Python first checks whether it's
    an internal module. Then it goes and looks iteratively for them in the sys.path.

    It is possible to modify sys.path using sys.path.append
    :return:
    """
    print('Search Path')
    for i, path in enumerate(sys.path):
        print("\t{} {}".format(i, path))
    print('\n')


if __name__ == '__main__':
    """
    If this module is executed directly then print the same thing the calling script would
    """
    print_arguments()
