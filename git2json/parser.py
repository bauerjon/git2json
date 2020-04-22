#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse git logs.

These parsing functions expect output of the following command:

    git log --pretty=raw --numstat

"""

import re

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.1'

PAT_COMMIT = r'''
(
commit\ (?P<commit>[a-f0-9]+)\n
tree\ (?P<tree>[a-f0-9]+)\n
(?P<parents>(parent\ [a-f0-9]+\n)*)
(?P<author>author \s+(.+)\s+<(.*)>\s+(\d+)\s+([+\-]\d\d\d\d)\n)
(?P<committer>committer \s+(.+)\s+<(.*)>\s+(\d+)\s+([+\-]\d\d\d\d)\n)\n
(?P<message>
(\ \ \ \ [^\n]*\n)*
)
\n
(?P<numstats>
(^(\d+|-)\s+(\d+|-)\s+(.*)$\n)*
)
)
'''
RE_COMMIT = re.compile(PAT_COMMIT, re.MULTILINE | re.VERBOSE)

# https://regex101.com/r/g41DnR/1
PAT_COMMIT_WITH_SIG = (r"(commit\ (?P<commit>[a-f0-9]+)\ntree\ (?P<tree>[a-f0-9]+)\n(?P<parents>(parent\ ([a-f0-9]|\n)+)*)(?P<author>author .*)\n(?P<committer>committer .*)\n(?P<gpgsig>gpgsig -----BEGIN PGP SIGNATURE-----(.|\n|\r)+?-----END PGP SIGNATURE-----\n\n)?\n(?P<message>((\ \ \ \ [^\n]*\n)|\n)+)?(\n)?(?P<numstats>(^(\d+|-).*(\n)?)+)?)")

RE_COMMIT_WITH_PGP_SIGNATURE = re.compile(PAT_COMMIT_WITH_SIG, re.MULTILINE | re.VERBOSE)

# -------------------------------------------------------------------
# Main parsing functions


def parse_commits(data):
    print '123'
    print data
    '''Accept a string and parse it into many commits.
    Parse and yield each commit-dictionary.
    This function is a generator.
    '''
    raw_commits = RE_COMMIT.finditer(data)
    for rc in raw_commits:
        print rc
        full_commit = rc.groups()[0]
        parts = RE_COMMIT.match(full_commit).groupdict()
        parsed_commit = parse_commit(parts)
        yield parsed_commit

    regex = r"(commit\ (?P<commit>[a-f0-9]+)\ntree\ (?P<tree>[a-f0-9]+)\n(?P<parents>(parent\ ([a-f0-9]|\n)+)*)(?P<author>author .*)\n(?P<committer>committer .*)\n(?P<gpgsig>gpgsig -----BEGIN PGP SIGNATURE-----(.|\n|\r)+?-----END PGP SIGNATURE-----\n\n)?\n(?P<message>((\ \ \ \ [^\n]*\n)|\n)+)?(\n)?(?P<numstats>(^(\d+|-).*(\n)?)+)?)"

    test_str = ("commit 4991324767f3fc14042c58894262e3a07900c0f2\n"
      "tree e9d75a0541f8c8046c8769e909a9e3f6c4fbc995\n"
      "parent bc977d7acfd293babdfecc0dbb00f6ee8dc22ca4\n"
      "parent 0e609a6087468d8189baa0e280742de7a8a4970f\n"
      "author Jon Bauer <bauerjon@hotmail.com> 1578499975 -0600\n"
      "committer GitHub <noreply@github.com> 1578499975 -0600\n"
      "gpgsig -----BEGIN PGP SIGNATURE-----\n\n"
      " wsBcBAABCAAQBQJeFf+HCRBK7hj4Ov3rIwAAdHIIAF5qXLG633IAl7jNDp7KYW3H\n"
      " 057d8y16GulwTVdb+pmQKkDkj8krWkw91Ht4/qxFi7qL9hJIjwzdhnJMvZYS0xLi\n"
      " DXcxYw0vljFqtQKHzFxw2VAe/8H+NLUNn1kq0XConamckUNmb8QbiRtiTcCZ6Xzk\n"
      " jcGLuUkb8cP7SXR/go/7qtuCvfQ6Jisufcm8py1KRqsrSNKZ9fij5yJpk08t806D\n"
      " m0SGBPTCdZ+5sZXESJ9GdOGEq0HM8efWpuNfa12oA5sip7bUhnh42ZbpqcKYnc/N\n"
      " /z/FuQBpG9oFpkVSRSONT9V5hah/i1Q4+lvLLpWln/+cWmK/V7q6yG7owJl/63Q=\n"
      " =JJ2J\n"
      " -----END PGP SIGNATURE-----\n\n\n"
      "    Merge pull request #34 from PopularPays/jb-update-creator-earnings-script\n\n"
      "    Update creator_earnings.rb\n\n"
      "commit 0e609a6087468d8189baa0e280742de7a8a4970f\n"
      "tree e9d75a0541f8c8046c8769e909a9e3f6c4fbc995\n"
      "parent bc977d7acfd293babdfecc0dbb00f6ee8dc22ca4\n"
      "author Jon Bauer <bauerjon@hotmail.com> 1578499591 -0600\n"
      "committer GitHub <noreply@github.com> 1578499591 -0600\n"
      "gpgsig -----BEGIN PGP SIGNATURE-----\n\n"
      " wsBcBAABCAAQBQJeFf4HCRBK7hj4Ov3rIwAAdHIIAHf27mDGguuYshYZZU5OWYK1\n"
      " IQI9/0RdwEmfxWip3KDt7Fqo6eaNApKUvBSEhRpUvzAr/aIR0RC49BjtIQGaxaCh\n"
      " I+T3onfCw16AsjG+wcXZFi+S591v3H/ONHBslzranHvRgUI7s9gy5lp8ZSdocjp9\n"
      " Wv7uh7SwlhpLWN8E7xyN1SIIdLf2zBcpR9xhkqqnHHuYdxqPn8fVX7OanEulklvb\n"
      " 7ZVbpo2Xvo3BYrQ4pG0yhm8QX4irJOd2J1FA64vYFWAgNAcQcto8+BqpkxfIET2l\n"
      " 3sDH837iXWdxSjSNpEziW6rjC8G7wJGN6LccHBdwT42O3ZczUJOxtMhBIP+UbtE=\n"
      " =cSNG\n"
      " -----END PGP SIGNATURE-----\n\n\n"
      "    Update creator_earnings.rb\n\n"
      "6  6 support/useful-scripts/creator_earnings.rb\n")

    matches = re.finditer(regex, test_str, re.MULTILINE)

    for rc in matches:
        print 'hey'
        full_commit = rc.groups()[0]
        print full_commit

def parse_commit(parts):
    '''Accept a parsed single commit. Some of the named groups
    require further processing, so parse those groups.
    Return a dictionary representing the completely parsed
    commit.
    '''
    commit = {}
    commit['commit'] = parts['commit']
    commit['tree'] = parts['tree']
    parent_block = parts['parents']
    commit['parents'] = [
        parse_parent_line(parentline)
        for parentline in
        parent_block.splitlines()
    ]
    commit['author'] = parse_author_line(parts['author'])
    commit['committer'] = parse_committer_line(parts['committer'])
    message_lines = [
        parse_message_line(msgline)
        for msgline in
        parts['message'].split("\n")
    ]
    commit['message'] = "\n".join(
        msgline
        for msgline in
        message_lines
        if msgline is not None
    )
    commit['changes'] = [
        parse_numstat_line(numstat)
        for numstat in
        parts['numstats'].splitlines()
    ]
    return commit


# -------------------------------------------------------------------
# Parsing helper functions


def parse_hash_line(line, name):
    RE_HASH_LINE = name + r' ([abcdef0-9]+)'
    result = re.match(RE_HASH_LINE, line)
    if result is None:
        return result
    else:
        return result.groups()[0]


def parse_commit_line(line):
    return parse_hash_line(line, 'commit')


def parse_parent_line(line):
    return parse_hash_line(line, 'parent')


def parse_tree_line(line):
    return parse_hash_line(line, 'tree')


def parse_person_line(line, name):
    RE_PERSON = name + r' (.+) <(.*)> (\d+) ([+\-]\d\d\d\d)'
    result = re.match(RE_PERSON, line)
    if result is None:
        return result
    else:
        groups = result.groups()
        name = groups[0]
        email = groups[1]
        timestamp = int(groups[2])
        timezone = groups[3]
        d_result = {
            'name': name,
            'email': email,
            'date': timestamp,
            'timezone': timezone,
        }
        return d_result


def parse_committer_line(line):
    return parse_person_line(line, 'committer')


def parse_author_line(line):
    return parse_person_line(line, 'author')


def parse_message_line(line):
    RE_MESSAGE = r'    (.*)'
    result = re.match(RE_MESSAGE, line)
    if result is None:
        return result
    else:
        return result.groups()[0]


def parse_numstat_line(line):
    RE_NUMSTAT = r'(\d+|-)\s+(\d+|-)\s+(.*)'
    result = re.match(RE_NUMSTAT, line)
    if result is None:
        return result
    else:
        (sadd, sdel, fname) = result.groups()
        try:
            return (int(sadd), int(sdel), fname)
        except ValueError:
            return (sadd, sdel, fname)
