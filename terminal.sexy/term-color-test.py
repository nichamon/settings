#!/usr/bin/python3

FG_LIST = range(30,38)
BG_LIST = range(40,48)

for bld in ["", 1]:
    for fg in FG_LIST:
        for bg in BG_LIST:
            print(" \033[{bld};{fg};{bg}mWord\033[0m".format(**locals()), end="")
        print("")
