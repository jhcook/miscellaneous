#!/usr/bin/env python3
#
#
# Author:Justin Cook

import sys
import json
from random import choice as randomchoice

try:
    import requests
except ImportError as err:
    print("Error importing: {0}".format(err), file=sys.stderr)

class OxfordDictionary:
    """This class provides verbs to fetch dictionary items from Oxford
    Dictionary. 
    """
    def __init__(self):
        self.app_id = '<my app_id>'
        self.app_key = '<my app_key>'
        self.language = 'en'
        self.word_id = 'Ace'

class Hangman:
    """This class represents a game of Hangman."""
    pass

class Words:
    """Produce a word and definition."""
    def __init__(self, words:str = "/usr/share/dict/words"):
        with open(words) as wordfile:
            self.__words = wordfile.readlines()
    
    @property
    def word(self):
        self.__word = randomchoice(self.__words)
        return self.__word.strip()


if __name__ == "__main__":
    # Create an instance of OxfordDictionary
    od = OxfordDictionary()

    # Create an instance of Hangman
    hm = Hangman()

    # Create an instance of Word
    words = Words()
    for i in range(0, 10):
        print(words.word)