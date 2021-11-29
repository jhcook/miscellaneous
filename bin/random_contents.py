#!/usr/bin/env python3

from sys import exit, argv, stdout
from getopt import GetoptError, getopt
from random import choice, randrange
from string import ascii_letters, digits
import contextlib

class RandomStuff():
    """A class that generates meaningless random garbage for cases content
    does not matter.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RandomStuff, cls).__new__(cls)
        return cls._instance

    def __init__(self, wfile="/usr/share/dict/words"):
        with open(wfile, 'r') as f:
            self.__words = [w.strip() for w in f.readlines()]
    
    @property
    def word(self):
        """Return a random word from the dictionary."""
        return choice(self.__words)

    @property
    def string(self):
        """Return a random string of ASCII letters and digits."""
        allowed_chars = ascii_letters + digits
        return ''.join((choice(allowed_chars) for x in 
                        range(randrange(0,100))))
    
    def get_sentence(self, gen="word"):
        """Return a random line of words from the internal dictionary.
        
        For more information on why this is not decorated @property please see
        https://newbedev.com/python-how-to-pass-more-than-one-argument-to-the-property-getter
        """
        line = ' '.join([getattr(self, gen)
                        for _ in range(1, randrange(0, 100))])
        if gen != "word":
            return line 
        sentence = line.capitalize()
        return sentence + '.\n' if sentence != '' else ''
    sentence = property(get_sentence)

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = stdout
    try:
        yield fh
    finally:
        if fh is not stdout:
            fh.close()

if __name__ == "__main__":
    usage = "{} <file_name>".format(argv[0].rpartition('/')[2])
    ofile = None
    try:
        opts, args = getopt(argv[1:], "h")
        ofile = args[0]
    except GetoptError:
        print(usage)
        exit (-1)
    except IndexError:
        ofile = '-'
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            exit(0)
    
    blah = RandomStuff()

    # Write a random range from 1 to 1000 sentences of random words from
    # RandomStuff's dictionary to file.
    try:
        with smart_open(ofile) as f:
            for _ in range(1, 1000):
                f.write(blah.sentence)
    except IOError as err:
        print(err)
        exit(2)
    except IndexError:
        print(usage)
        exit(1)
