"""
CLI class containing github commands that will be turned into a script/executable as the package is installed.
"""

import logging
import argparse
import sys
import requests
import requests.auth

logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
log = logging.getLogger(__name__)
session = None
args = None


def cmd_fix():
    """
    Fix all repositories
    :return:
    """

    repos = _get_gh_repos()
    for repo in repos:
        for hook in repo['hooks']:
            if '.bobeli.org:10443/' not in hook['url'] or hook['ssl'] == 0:
                old = hook['url']
                new = hook['url'].replace('.bobeli.org/', '.bobeli.org:10443/')
                oldssl = hook['ssl']
                newssl = 1
                print('{:25} Old: {:10} {:70} {:1}'.format(repo['name'], hook['id'], old, oldssl))
                print('{:25} New: {:10} {:70} {:1}'.format('', hook['id'], new, newssl))
                print()

                payload = {'config': dict(url=new, insecure_ssl=newssl)}
                r = session.patch(
                    'https://api.github.com/repos/MrMatAP/{}/hooks/{}'.format(repo['name'], hook['id']),
                    json=payload
                )
                print(r.status_code)

    return 0


def cmd_remove():
    """
    Remove webhooks
    :return:
    """

    repos = _get_gh_repos()
    for repo in repos:
        for hook in repo['hooks']:
            if args.jira and 'jira.bobeli.org' in hook['url']:
                r = session.delete('https://api.github.com/repos/MrMatAP/{}/hooks/{}'.format(repo['name'], hook['id']))
                print(r.status_code)

    return 0


def cmd_show():
    """
    Show the current webhooks for all repositories
    :return: 0 when successful
    """

    repos = _get_gh_repos()
    for repo in repos:
        first_hook = dict(url='', ssl='')
        if len(repo['hooks']) != 0:
            first_hook = repo['hooks'].pop()
        print('{:25} {:10} {:70} {:1}'.format(repo['name'], repo['language'], first_hook['url'], first_hook['ssl']))
        for hook in repo['hooks']:
            print('{:25} {:10} {:70} {:1}'.format('', '', hook['url'], hook['ssl']))
        print()

    return 0


def _get_gh_repos():
    """
    Return information about the repositories in GitHub
    :return: An array of dicts containing repository information
    """

    r = session.get('https://api.github.com/user/repos')
    repos = []
    for repo in r.json():
        language = 'Unknown'
        if repo['language'] is not None:
            language = repo['language']

        h = session.get('https://api.github.com/repos/MrMatAP/{}/hooks'.format(repo['name']))
        hooks = []
        for hook in h.json():
            hooks.append(dict(id=hook['id'], url=hook['config']['url'], ssl=hook['config']['insecure_ssl']))

        repos.append(dict(
            id=repo['id'],
            name=repo['name'],
            language=language,
            hooks=hooks
        ))

    return repos


def run():  # pragma: no cover
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
    subparsers.add_parser('fix', help='Fix webhooks')
    remove_parser = subparsers.add_parser('remove', help='Remove webhooks')
    remove_parser.add_argument('--jira', action='store_true', help='Remove JIRA webhooks')
    remove_parser.add_argument('--jenkins', action='store_true', help='Remove Jenkins webhooks')

    global args
    args = parser.parse_args()

    #
    # Establish Logging

    if args.verbose:
        log.setLevel(logging.INFO)
    if args.debug:
        log.setLevel(logging.DEBUG)

    #
    # Establish a session

    global session
    session = requests.Session()
    session.headers.update({
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': "token " + args.token
    })

    #
    # Parse the command

    ret = None
    if args.cmd == 'show':
        ret = cmd_show()
    elif args.cmd == 'fix':
        ret = cmd_fix()
    elif args.cmd == 'remove':
        ret = cmd_remove()
    else:
        parser.print_help()

    sys.exit(ret)


if __name__ == '__main__':
    run()


