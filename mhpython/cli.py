"""
CLI class that will be turned into a script/executable as the package is installed.
"""

import logging
import argparse
import sys

logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def cmd_fix(repo):
    """
    Fix one or all repositories
    :param repo: If set, the repository to fix
    :return:
    """
    print("cmd_fix")
    return 0


def cmd_show():
    """
    Show the current webhooks for all repositories
    :return:
    """
    print("cmd_show")
    return 0


def gh_webhook_manager():  # pragma: no cover
    """
    Main entry point the gh-webhook-manager script
    :return: 0 exit code for success
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Be chatty', action='store_true')
    parser.add_argument('--debug', help='Be very chatty', action='store_true')

    parser.add_argument('--token', required=True, help='The personal access token to use')
    subparsers = parser.add_subparsers(dest='cmd')

    subparsers.add_parser('show', help='Show the current webhooks for all repositories')

    fix_parser = subparsers.add_parser('fix', help='Fix webhooks')
    fix_parser.add_argument('-r', '--repo', help='The repository to fix')

    args = parser.parse_args()

    #
    # Establish Logging

    if args.verbose:
        log.setLevel(logging.INFO)
    if args.debug:
        log.setLevel(logging.DEBUG)

    ret = None
    if args.cmd == 'show':
        ret = cmd_show()
    elif args.cmd == 'fix':
        ret = cmd_fix(args.repo)
    else:
        parser.print_help()

    sys.exit(ret)



