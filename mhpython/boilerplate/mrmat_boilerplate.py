"""
py-boilerplate.py - A Python boilerplate

A description of this boilerplate.
"""

import argparse
import logging


def run():

    #
    # Establish logging

    logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
    log = logging.getLogger(__name__)

    #
    # Parse arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Be verbose', action='store_true')
    parser.add_argument('--debug', help='Be very verbose', action='store_true')
    options = parser.parse_args()
    if options.verbose:
        log.setLevel(logging.INFO)
    if options.debug:
        log.setLevel(logging.DEBUG)

    try:
        log.debug("This is a DEBUG message")
        log.info("This is a INFO message")
        log.warning("This is a WARN message")
        log.error("This is an ERROR message")
        log.fatal("This is a FATAL message")

    except Exception as ex:
        log.fatal('{} - {}'.format(type(ex), ex))
    else:
        log.debug('No exception occurred within the code block')
    finally:
        log.debug('The finally block is always executed')


if __name__ == '__main__':
    run()
