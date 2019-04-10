#!/usr/bin/env python3
#
# This program makes a directory <depth> deep with ten random files in each
# subdirectory. The final subdirectories are left empty. 
#
# Author: Justin Cook <jhcook@secnix.com>

import sys
import os
import random

rand = random.seed(os.urandom(256))
with open("/usr/share/dict/words", 'r') as wordFile:
    words = [word.strip().capitalize() for word in wordFile.readlines() 
             if len(word) > 4]
wordCount = len(words)

def createNestedDirFiles(path:str, depth:int):
    """Create a directory with files and nested subdirectories of depth with
    files.
    """
    depth -= 1
    try:
        for f in range(10):
            open(os.path.join(path, "%s%s" % (words[random.randint(0, 
                                                    wordCount-1)], 
                                              words[random.randint(0, 
                                                    wordCount-1)])), 
                 "a")
            os.mkdir(os.path.join(path, "dir_%s" % str(f)))
            if depth > 0:
                 createNestedDirFiles(os.path.join(path, 
                                                   "dir_%s" % str(f)), depth)
    except (IOError, PermissionError) as err:
        print(err)

if __name__ == "__main__":
    try:
        pathname = sys.argv[1]
    except IndexError:
        pathname = os.getcwd()
    try:
        depth = int(sys.argv[2])
    except IndexError:
        depth = 1
    try:
        createNestedDirFiles(os.path.join(pathname), depth)
    except KeyboardInterrupt:
        pass

