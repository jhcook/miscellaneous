#!/usr/bin/env python3
#
# This function uses Python3 to begin reading at the end of file in discrete
# blocks and carry on reading backwards incrementing until the specific number
# of lines are found.
#
# Notes: 
# - https://stackoverflow.com/questions/21533391/seeking-from-end-of-file-throwing-unsupported-exception
#
# Author: Justin Cook <jhcook@secnix.com>

from os import SEEK_END, SEEK_SET
from re import finditer
from posixpath import expanduser

# The amount of data to read in one go, i.e., each chunk
block = 256

def last_n_lines(file_name, num_lines=10):
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
    return lines.split('\n')[-10:]
        
if __name__ == "__main__":
    lines = last_n_lines(expanduser('~/stuff.txt'))
    print("{}: {}".format(len(lines), lines))