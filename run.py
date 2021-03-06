#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a json log of a git repository.
"""

from __future__ import print_function
import json
import sys
from git2json.parser import parse_commits

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.3'

# -------------------------------------------------------------------
# Main


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--git-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    parser.add_argument(
        '--since',
        default=None,
        help=('Show commits more recent than a specific date. If present, '
              'this argument is passed through to "git log" unchecked. ')
    )
    parser.add_argument(
        '--until',
        default=None,
        help=('Show commits before a specific date. If present, '
              'this argument is passed through to "git log" unchecked. ')
    )
    parser.add_argument(
        '--commit_shas_string',
        default=None,
        help=('Show commits given a list of commit shas. If present, '
              'this argument is passed through to "git log" unchecked. ')
    )
    args = parser.parse_args()
    if sys.version_info < (3, 0):
        print(git2json(run_git_log(args.git_dir, args.since, args.until, args.commit_shas_string)))
    else:
        print(git2jsons(run_git_log(args.git_dir, args.since, args.until, args.commit_shas_string)))

# -------------------------------------------------------------------
# Main API functions

def git2jsons(s):
    return json.dumps(list(parse_commits(s)), ensure_ascii=False)


def git2json(fil):
    return json.dumps(list(parse_commits(fil.read())), ensure_ascii=False)


# -------------------------------------------------------------------
# Functions for interfacing with git


def run_git_log(git_dir=None, git_since=None, git_until=None, git_commit_shas_string=None):
    '''run_git_log([git_dir]) -> File

    Run `git log --numstat --pretty=raw --remotes on the specified
    git repository and return its stdout as a pseudo-File.'''
    import subprocess
    if git_dir:
        command = [
            'git',
            '--git-dir=' + git_dir,
            'log',
            '--numstat',
            '--pretty=raw',
            '--date=local'
        ]
    else:
        command = ['git', 'log', '--numstat', '--pretty=raw']
    if git_since is not None:
        command.append('--remotes --since=' + git_since)
    if git_until is not None:
        command.append('--remotes --until=' + git_until)
    if git_commit_shas_string is not None:
        command.append('--no-walk')
        all_commit_shas = git_commit_shas_string.split(' ')
        command.extend(all_commit_shas)
    raw_git_log = subprocess.Popen(
        command,
        stdout=subprocess.PIPE
    )
    if sys.version_info < (3, 0):
        return raw_git_log.stdout
    else:
        return raw_git_log.stdout.read().decode('utf-8', 'ignore')


if __name__ == "__main__":
   main()
