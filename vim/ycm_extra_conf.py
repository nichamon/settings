import os
import re
import json
import socket
import subprocess as sp

RE_SEARCH_START = re.compile(r'#include .* search starts here:')

def gcc_include_search_paths():
    search_start = 0
    paths = []
    out = sp.check_output("gcc -E -v - < /dev/null",
                          shell=True, stderr=sp.STDOUT)
    for line in out.splitlines():
        if RE_SEARCH_START.match(line):
            search_start = 1
            continue
        if search_start and line.startswith(' /'):
            paths.append(line.strip())
            continue
        search_start = 0
    return paths

def c_handle(filename):
    h = socket.gethostname()
    b = '/build-' + h
    d = '/home/narate/projects/OVIS'
    flags = [ '-Wall', '-x', 'c', '-DDEBUG' ]
    flags += [ '-I' + p for p in gcc_include_search_paths() ]
    return {'flags': flags, 'do_cache': True}

type_handle = {
        '.c': c_handle,
        '.h': c_handle,
        }

def FlagsForFile(filename, **kwargs):
    try:
        t = os.path.splitext(filename)
        return type_handle[t](filename)
    except Exception, e:
        return c_handle(filename)

if __name__ == '__main__':
    # testing
    obj = FlagsForFile("/a/b/c.h")
    print json.dumps(obj, indent=2)
