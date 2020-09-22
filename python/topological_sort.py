#!/usr/bin/env python3
#
# A utility to install set of packages complete with dependency resolution.
#
# Usage: `basename $0 <command> <package>...<package>
#
# Author: Justin Cook <jhcook@secnix.com>
#
# https://en.wikipedia.org/wiki/Topological_sorting

from sys import argv
from collections import deque

class Package():

    def __init__(self, pkgs):
        self._depends = deque()
        self.pkgs = pkgs

    @property
    def depends(self):
        return self._depends

    def parse_pkg(self, first=True, pkgs=None):
        """A recursive implementation of Kahn's algorithm that traverses
        dependencies and updates a queue. If the dependency is already in the
        set then it is circular and ignored.
        """
        if first:
            pkgs = self.pkgs
            first = False
        for pkg in pkgs:
            with open("{}.pkg".format(pkg)) as f:
                deps = None
                while True:
                    header, value = f.readline().split(':')
                    if header == "Requires":
                        deps = value.split()
                        break
                if deps is not None:
                    self.parse_pkg(first, [dep.strip() for dep in deps])
            if pkg not in self._depends:
                self._depends.append(pkg)

if __name__ == "__main__":
    # List dependencies of requested packages
    to_install = Package(argv[2:])
    to_install.parse_pkg()
    for pkg in to_install.depends:
        print("installing: {}".format(pkg))
