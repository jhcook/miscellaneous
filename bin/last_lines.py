#!/usr/bin/env python3
#
# This function uses Python3 to begin reading at the end of file in discrete
# blocks and carry on reading backwards incrementing until the specific number
# of lines are found.
#
# Notes: 
# - https://stackoverflow.com/questions/21533391/seeking-from-end-of-file-throwing-unsupported-exception
# - https://www.tutorialspoint.com/python3/python_command_line_arguments.htm
#
# Author: Justin Cook <jhcook@secnix.com>

from getopt import GetoptError, getopt
from sys import stdin, argv, exit
from os import SEEK_END, SEEK_SET
from re import finditer
from io import StringIO
import contextlib

# The amount of data to read in one go, i.e., each chunk
block = 256

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'r')
    else:
        fh = StringIO(''.join(stdin.readlines()))
    try:
        yield fh
    finally:
        if fh is not stdin:
            fh.close()

def last_n_lines(file_name: str, num_lines: int=10):
    ''' Return num_lines lines from file_name

        Author: Justin Cook <jhcook@secnix.com>
    '''
    num_found = 0
    lines = ''
    offset = block
    try:
        with smart_open(file_name) as f:    
            while num_found < num_lines:
                try:
                    f.seek(0, SEEK_END)
                    f.seek(f.tell() - offset, SEEK_SET) 
                except ValueError:
                    f.seek(0, 0)
                    num_lines = 0
                lines = f.read(block) + lines
                num_found = len([s.start() for s in finditer('\n', lines)])
                offset += block
    except IOError as err:
        raise err
    return lines.split('\n')[-num_lines:]
        
if __name__ == "__main__":
    usage = "{} -n <number_of_lines> <file_name>".format(argv[0].rpartition('/')[2])
    number_lines = 10
    ifile = None
    try:
        opts, args = getopt(argv[1:], "hn:")
        ifile = args[0]
    except GetoptError:
        print(usage)
        exit (2)
    except IndexError:
        ifile = '-'
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            exit(0)
        elif opt == '-n':
            try:
                number_lines = int(arg)
            except ValueError as err:
                print(err)
                exit(4)
    try:
        for line in last_n_lines(ifile, number_lines):
            print(line)
    except FileNotFoundError as err:
        print(err)