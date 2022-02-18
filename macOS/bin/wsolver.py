#!/usr/bin/env python3
#
# A solver tool for Wordle.
# Inspired by: https://www.mongodb.com/developer/how-to/wordle-bash-data-api/
# Example dictionary: https://raw.githubusercontent.com/dwyl/english-words/master/words.txt
#
# Tested on macOS Monterey
#
# Example:
# ./wsolver.py
# 1st known letter: !l
# 2nd known letter: !uc
# 3rd known letter: u
# 4th known letter: l
# 5th known letter:
# Known duds: nhoi
# Suggestions: cauld, caulk, cauls, crull
#
# Author: Justin Cook

from sys import argv
from argparse import ArgumentParser
from re import compile
from collections import Counter

word_length = 5

class WordleSolver():
    
    dictionary = "wwords"
    letters = ['first', 'second', 'third', 'fourth', 'fifth']
    srch_str = potential_words = blacked_out = unknown_chars = None

    def __init__(self):
        self.potential_words = []
        self.blacked_out = set()
        self.unknown_chars = {i: set() for i in range(word_length)}
        self.srch_str = ['[a-z]{1}'] * word_length

    def __user_prompt(self, args):
        for i, l in enumerate(self.letters):
            if not args:
                known = input(f"{l} known letter: ")
            else:
                known = eval(f"args.{l}")
            if known.startswith('!'):
                [self.unknown_chars[i].add(c) for c in known[1:]]
            elif known:
                self.srch_str[i] = known
        if not args:
            [self.blacked_out.add(c) for c in input("Known duds: ")]
        else:
            [self.blacked_out.add(c) for c in args.dud]
    
    def __letter_frequency(self): 
        potential_words = {w: Counter(list(w)) for w in self.potential_words}
        potential_words = {k: v for k, v in sorted(potential_words.items(), 
                           key=lambda c: [c[1][v] for v in 'chare'],
                           reverse=True)}
        self.potential_words = [k for k in potential_words]

    def __gen_search(self):
        for i, v in enumerate(self.srch_str):
            if not self.unknown_chars[i] or not self.blacked_out: continue
            self.srch_str[i] = "(?:(?![{}])[a-z]){{1}}".format(''.join(
                        set.union(self.unknown_chars[i], self.blacked_out)))

    def __search_dictionary(self):
        """Consult known matched characters `self.srch_str` to narrow down
        word candidates.
        """
        self.potential_words = []
        temp_str = ''.join(self.srch_str)
        regex = compile(rf"^{temp_str}$")
        with open(self.dictionary, 'r') as d:
            tl = self.unknown_chars.values() 
            required_letters = [item for tl in tl for item in tl]
            for line in d.readlines():
                word = regex.search(line)
                if word:
                    the_word = word.group()
                    commit = True
                    if required_letters: # This should be replaced with lookaheads
                        for res in [c in the_word for c in required_letters]:
                            if not res: 
                                commit = False
                                break
                    if self.blacked_out: # This should be replaced with lookaheads
                        for bo in [c in the_word for c in self.blacked_out]:
                            if bo:
                                commit = False
                                break
                    if commit:
                        self.potential_words.append(the_word)

    def play(self, args=None):
        self.__user_prompt(args)
        self.__gen_search()
        self.__search_dictionary()
        self.__letter_frequency()

if __name__ == "__main__":
    if len(argv) > 1:
        # Get command-line arguments
        parser = ArgumentParser(prog='wsolver.py', usage='%(prog)s [options]',
                                description="A tool to help solve Wordle.",
                                epilog="...just like that!")
        parser.add_argument('-a', '--first', type=str, default='',
                            help='1st character hint')
        parser.add_argument('-b', '--second', type=str, default='',
                            help='2nd character hint')
        parser.add_argument('-c', '--third', type=str, default='',
                            help='3rd character hint')
        parser.add_argument('-d', '--fourth', type=str, default='',
                            help='4th character hint')
        parser.add_argument('-e', '--fifth', type=str, default='',
                            help='5th character hint')
        parser.add_argument('-z', '--dud', type=str, default='',
                            help='characters not in word')
        args = parser.parse_args()
    else:
        args = None

    # Create solver
    wordle = WordleSolver()
    # Generate words
    try:
        wordle.play(args)
        print("Suggestions: {}".format(', '.join(wordle.potential_words)))
    except KeyboardInterrupt:
        pass
