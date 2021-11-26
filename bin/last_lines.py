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
from sys import argv, exit
from os import SEEK_END, SEEK_SET
from re import finditer

# The amount of data to read in one go, i.e., each chunk
block = 256

def last_n_lines(file_name: str, num_lines: int=10):
    ''' Return num_lines lines from file_name

        Author: Justin Cook <jhcook@secnix.com>
    '''
    num_found = 0
    lines = ''
    offset = block
    try:
        with open(file_name, 'r') as f:    
            while num_found < num_lines:
                try:
                    f.seek(0, SEEK_END)
                    f.seek(f.tell() - offset, SEEK_SET) 
                except ValueError:
                    offset = offset / 2
                    continue
                lines = f.read(block) + lines
                num_found = len([s.start() for s in finditer('\n', lines)])
                offset += block
    except IOError as err:
        raise err
    return lines.split('\n')[-num_lines:]
        
if __name__ == "__main__":
    file_name = argv[0].rpartition('/')[2]
    number_lines = 10
    try:
        opts, args = getopt(argv[1:], "hn:")
    except GetoptError:
        print("{} -n <number_of_lines> <file_name>".format(file_name))
        exit (2)
    for opt, arg in opts:
        if opt == '-h':
            print("{} -n <number_of_lines> <file_name>".format(file_name))
            exit(0)
        elif opt == '-n':
            number_lines = int(arg)
    try:
        for line in last_n_lines(args[0], number_lines):
            print(line)
    except NameError as err:
        print(err)
        print("last_lines.py <file_name>")
    except FileNotFoundError as err:
        print(err)