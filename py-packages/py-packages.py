#!/usr/bin/env python

"""
py-packages.py - Exploring Python Packages
"""

import argparse
import logging
from pkg import me
from pkg.subpkg import subme

#
# Establish logging

logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
LOG = logging.getLogger(__name__)

#
# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Be chatty', action='store_true')
parser.add_argument('--debug', help='Be very chatty', action='store_true')
options = parser.parse_args()
if options.verbose:
    LOG.setLevel(logging.INFO)
if options.debug:
    LOG.setLevel(logging.DEBUG)

me.test()
subme.test()

