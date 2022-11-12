"""
localized.py - A localized Python boilerplate

A description of this localized boilerplate.
"""

import argparse
import logging
import gettext

from mhpython.locale import localedir

# Establish the fallback in English
en = gettext.translation('messages',
                         localedir=localedir,
                         languages=['en'])
# Localize text, fallback to English if we don't have a localization
t = gettext.translation('messages',
                        localedir=localedir,
                        codeset='UTF-8',
                        fallback=en)
_ = t.gettext


def run():

    #
    # Establish logging

    logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
    log = logging.getLogger(__name__)

    #
    # Parse arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help=_('Be verbose'), action='store_true')
    parser.add_argument('--debug', help=_('Be very verbose'), action='store_true')
    options = parser.parse_args()
    if options.verbose:
        log.setLevel(logging.INFO)
    if options.debug:
        log.setLevel(logging.DEBUG)

    try:
        log.debug(_('This is a DEBUG message'))
        log.info(_('This is a INFO message'))
        log.warning(_('This is a WARN message'))
        log.error(_('This is an ERROR message'))
        log.fatal(_('This is a FATAL message'))

    except Exception as ex:
        log.fatal('{} - {}'.format(type(ex), ex))
    else:
        log.debug(_('No exception occurred within the code block'))
    finally:
        log.debug(_('The finally block is always executed'))


if __name__ == '__main__':
    run()
