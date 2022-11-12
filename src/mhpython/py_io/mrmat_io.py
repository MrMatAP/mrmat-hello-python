

"""
py-io.py - Python basic I/O
"""

import argparse
import logging

#
# Establish logging

logging.basicConfig(level=logging.WARN, format='%(levelname)s - %(message)s')
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

    try:
        LOG.info('IO from stdin')
        s = input('Enter a line of text: ')
        print(f'We got the following input {s}')

        #
        # Basic File IO

        LOG.info('Writing that line to a simple text file')
        with open('py-io-output.txt', 'w', encoding='UTF-8') as f:
            f.write(s)
        LOG.info('Reading that file again')
        with open('py-io-output.txt', 'r', encoding='UTF-8') as g:
            t = g.readline()
        if s != t:
            LOG.error('The input string %s does not match the string read from the file %s', s, t)
        else:
            LOG.info('The input string %s matches the string read from the file %s', s, t)

    except EOFError:
        LOG.warning('Got an EOFError because you pressed Ctrl-D')
    except Exception as ex:                     # pylint: disable=W0703
        LOG.fatal('%s - %s', type(ex), ex)
    else:
        LOG.debug('No exception occurred within the code block')
    finally:
        LOG.debug('The finally block is always executed')


if __name__ == '__main__':
    run()
