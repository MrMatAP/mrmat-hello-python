#!/usr/bin/env python

"""
py-boilerplate.py - A Python boilerplate

A description of this boilerplate.
"""

import argparse
import logging

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

LOG.debug("This is a DEBUG message")
LOG.info("This is a INFO message")
LOG.warn("This is a WARN message")
LOG.error("This is an ERROR message")
LOG.fatal("This is a FATAL message")

