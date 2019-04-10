#!/usr/bin/env python3
#
# Use Python3 to recursively delete a directory's content. 
#
# Author: Justin Cook <jhcook@secnix.com>

import os, sys
from stat import *

def traverse_directory(callback, path:str=None):
    """Traverse a directory recursing into subdirectories and calling callback
    on files that are not a directory. Each directory is removed on exit.
    """
    files, sdirs = [], []
    top = path if path else os.getcwd()
    try:
        for fobj in os.scandir(top):
            if fobj.is_dir(): sdirs.append(fobj.path)
            else: files.append(fobj.path)
        for d in sdirs: traverse_directory(callback, d)
        for f in files: callback(f)
        callback(top)
    except (IOError, PermissionError) as err:
        print("{}: {}".format(sys._getframe().f_code.co_name, err))

def delete_file(fil:str):
    """Delete a file that is passed as a string and remove empty directories
    if stat is not a regular file.
    """
    try: 
        stat = os.lstat(fil).st_mode
        if S_ISREG(stat) or S_ISLNK(stat):
            os.unlink(fil) 
            print("unlinked: {}".format(fil))
        elif S_ISDIR(stat):
            os.rmdir(fil)
            print("rmdir: {}".format(fil))
        else:
            os.unlink(fil)
            print("smashed: {}".format(fil))
    except (IOError, PermissionError, OSError) as err:
        print("{} {}: {}".format(sys._getframe().f_code.co_name, fil, err))

def main():
    try:
        pathname = sys.argv[1]
    except IndexError:
        try:
            pathname = os.getcwd()
        except FileNotFoundError as err:
            print(err)
            sys.exit(1)
    try:
        traverse_directory(delete_file, os.path.join(pathname))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
