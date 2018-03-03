#!/usr/bin/env python

import argparse
import sys
import time
import itertools
import threading


def spinner():
    spin = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    while True:
        sys.stdout.write(next(spin) + " - Creating host")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\r')


def lengthy_task():
    time.sleep(5)
    print("\nDONE")


def run():
    parser = argparse.ArgumentParser(description='Argument Parsing')
    parser.add_argument('verbose', action='store_true', help='Be verbose')
    subparsers = parser.add_subparsers(help='sub-command help')

    # Create the parser for the create_alias command
    parser_create_alias = subparsers.add_parser('create-alias', help='Create an alias')
    parser_create_alias.add_argument('--fqdn', required=True, help='The FQDN to add the alias to')
    parser_create_alias.add_argument('--alias', required=True, help='The alias to create')

    # Create the parsers for the create_host command
    parser_create_host = subparsers.add_parser('create-host', help='Create a host')
    parser_create_host.add_argument('--fqdn', required=True, help='FQDN to create')
    parser_create_host.add_argument('--ip', required=True, help='IP to create')

    args = parser.parse_args()

    t = threading.Thread(target=spinner, name="spinner")
    t.setDaemon(True)
    t.start()
    lengthy_task()


if __name__ == '__main__':
    run()
