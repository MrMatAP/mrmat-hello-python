#!/usr/bin/env python

"""
py-io.py - Python basic I/O
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

try:
    LOG.info('IO from stdin')
    s = input('Enter a line of text: ')
    print('We got the following input {}'.format(s))

    #
    # Basic File IO

    LOG.info("Writing that line to a simple text file")
    f = open('py-io-output.txt', 'w')
    f.write(s)
    f.close()
    LOG.info('Reading that file again')
    g = open('py-io-output.txt', 'r')
    t = g.readline()
    g.close()
    if s != t:
        LOG.error('The input string {} does not match the string read from the file {}'.format(s, t))
    else:
        LOG.info('The input string {} matches the string read from the file {}'.format(s, t))



except EOFError:
    LOG.warn('Got an EOFError because you pressed Ctrl-D')
except Exception as ex:
    LOG.fatal('{} - {}'.format(type(ex), ex))
else:
    LOG.debug('No exception occurred within the code block')
finally:
    LOG.debug('The finally block is always executed')
