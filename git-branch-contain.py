#!/usr/bin/python3
import os
import re
import sys
import subprocess as sp
import argparse as ap

if __name__ != "__main__":
    raise RuntimeError("This is not a module")

EXAMPLES = """
Examples:
    # Check all LOCAL branches if they are contained in github/OVIS-4
    $ ./git-branch-contain.py -b github/OVIS-4 '*'

    # Check all LOCAL branches matching 'v4-*' wildcard pattern whether or not
    # they are contained in github/OVIS-4
    $ ./git-branch-contain.py -b github/OVIS-4 -d 'v4-*'

    # Check specific list of LOCAL branches if they are contained in
    # github/OVIS-4.
    $ ./git-branch-contain.py -b github/OVIS-4 v4-red v4-blue

    # Check REMOTE branches (on all remotes) if they are contained in
    # github/OVIS-4 (github/OVIS-4 will be skipped though).
    $ ./git-branch-contain.py -b github/OVIS-4 -r '*'

    # Check all LOCAL and REMOTE branches (on all remotes) if they are
    # contained in github/OVIS-4 (github/OVIS-4 will be skipped though).
    $ ./git-branch-contain.py -b github/OVIS-4 -a '*'

    # Check all branches in 'bob' remote repository if they are contained in
    # github/OVIS-4
    $ ./git-branch-contain.py -b github/OVIS-4 -r 'bob/*'

    # In all above examples, add `-d` to DELETE the matching branches that are
    # also contained in the base branch (github/OVIS-4).
"""

p = ap.ArgumentParser(description = "Check if branches is contained in "
                      "another branch by commit messages.")
p.add_argument("--base", "-b", metavar="BASE", default="",
               help="The base branch.")
p.add_argument("--delete", "-d", action="store_true",
               help="Delete the matching branches contained by the BASE. "
               "By default, the script does NOT delete the branches.")
p.add_argument("--remote", "-r", action="store_true",
               help="Matching remote branches only. By default, the script "
               "matches only local branches.")
p.add_argument("--all", "-a", action="store_true",
               help="Matching all branches (local and remote). By default, "
               "the script matches only local branches.")
p.add_argument("--examples", "-E", action="store_true",
               help="Show examples and exit.")
p.add_argument("branch", metavar="BRANCH", nargs='*',
               help="The branches to check. This can be a pattern, e.g. "
               "'bob/*' or 'v4-*'")
args = p.parse_args()

if args.examples:
    print(EXAMPLES)
    sys.exit(0)

MATCH_LOCAL = args.all or not args.remote
MATCH_REMOTE = args.all or args.remote

RE = re.compile(r'^([0-9a-fA-F]+) (.*)$')

def base_commits(base):
    cmd = "git log --oneline --no-decorate {}".format(base)
    lines = sp.check_output(cmd, shell=True).splitlines()
    return set( RE.match(l.decode()).group(2) for l in lines )

def branch_commits(base, branch):
    cmd = "git log --oneline --no-decorate {}..{}".format(base, branch)
    lines = sp.check_output(cmd, shell=True).splitlines()
    return set( RE.match(l.decode()).group(2) for l in lines )

def branches(_b):
    q = [ "'{}'".format(x) for x in _b ]
    cmd = "git branch --list -a " + (" ".join(q))
    lines = sp.check_output(cmd, shell=True).splitlines()
    return [ l[2:].decode() for l in lines ]

BRANCH_RE = re.compile("""
    # remote branch
    remotes/(?P<remote>[^/]+)/(?P<remote_branch>\S+) |

    # local branch
    (?P<local_branch>(?!remotes/)\S+)
""", re.VERBOSE)
_br = branches(args.branch)
ecode = 0
ba_c = base_commits(args.base)
for b in _br:
    m = BRANCH_RE.match(b)
    if not m:
        raise ValueError("Bad branch name: {}".format(b))
    gd = m.groupdict()
    br = m.group(0)
    rb = None if not gd['remote'] else '{remote}/{remote_branch}'.format(**gd)
    if args.base in [ br, rb, gd['local_branch']]:
        continue # skip self
    if not MATCH_LOCAL and gd['local_branch']: # skip local
        continue
    if not MATCH_REMOTE and gd['remote']: # skip remote
        continue
    br_c = branch_commits(args.base, br)
    f = br_c < ba_c
    print(br, f)
    if not f:
        ecode = -1
    elif args.delete:
        if gd['remote']: # remote branch
            cmd = "git push {remote} :{remote_branch}".format(**gd)
        else: # local branch
            cmd = "git branch -D {local_branch}".format(**gd)
        print(" ", cmd)
        rc, out = sp.getstatusoutput(cmd)
sys.exit(ecode)
