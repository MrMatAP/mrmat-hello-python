#!/usr/bin/env python

import argparse
import sys
import time
import itertools
import threading
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


def spinner():
    spin = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    while True:
        sys.stdout.write(next(spin) + ' - {}'.format(_("Creating host")))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\r')


def lengthy_task():
    time.sleep(5)
    print("\n{}".format(_('Done')))


def run():
    parser = argparse.ArgumentParser(description=_('Argument Parser'))
    parser.add_argument('verbose', action='store_true', help=_('Be verbose'))
    subparsers = parser.add_subparsers(help=_('sub-command help'))

    # Create the parser for the create_alias command
    parser_create_alias = subparsers.add_parser('create-alias', help=_('Create an alias'))
    parser_create_alias.add_argument('--fqdn', required=True, help=_('The FQDN to add the alias to'))
    parser_create_alias.add_argument('--alias', required=True, help=_('The alias to create'))

    # Create the parsers for the create_host command
    parser_create_host = subparsers.add_parser('create-host', help=_('Create a host'))
    parser_create_host.add_argument('--fqdn', required=True, help=_('FQDN to create'))
    parser_create_host.add_argument('--ip', required=True, help=_('IP to create'))

    args = parser.parse_args()

    t = threading.Thread(target=spinner, name="spinner")
    t.setDaemon(True)
    t.start()

    lengthy_task()


if __name__ == '__main__':
    run()
