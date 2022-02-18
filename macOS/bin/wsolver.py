#!/usr/bin/env python3
#
# A solver tool for Wordle.
# Inspired by: https://www.mongodb.com/developer/how-to/wordle-bash-data-api/
# Example dictionary: https://raw.githubusercontent.com/dwyl/english-words/master/words.txt
#
# Tested on macOS Monterey
#
# Example:
# $ ./wsolver.py -w words -a \!l -b \!uc -cu -dl -z nhoi
# Suggestions: cauld, caulk, cauls, crull
#
# Author: Justin Cook

from sys import argv
from argparse import ArgumentParser
from re import compile
from collections import Counter

word_length = 5

class WordleSolver():
    
    letters = ['first', 'second', 'third', 'fourth', 'fifth']
    dictionary = srch_str = potential_words = blacked_out = None
    unknown_chars = interactive = None

    def __init__(self, args):
        self.potential_words = []
        self.blacked_out = set()
        self.unknown_chars = {i: set() for i in range(word_length)}
        self.srch_str = ['[a-z]{1}'] * word_length
        self.dictionary = args.words if args.words else "/usr/share/dict/words"
        self.interactive = args.interactive

    def __user_prompt(self, args):
        for i, l in enumerate(self.letters):
            if self.interactive:
                known = input(f"{l} known letter: ")
            else:
                known = eval(f"args.{l}")
            if known.startswith('!'):
                [self.unknown_chars[i].add(c) for c in known[1:]]
            elif known:
                self.srch_str[i] = known
        if self.interactive:
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
            if not self.unknown_chars[i] and not self.blacked_out: continue
            if len(v) > 1:
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
                    for res in [c in the_word for c in required_letters]:
                        if not res: 
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
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='interactive session')
    parser.add_argument('-w', '--words', type=str, default='',
                        help='path to dictionary')
    parser.add_argument('-z', '--dud', type=str, default='',
                        help='characters not in word')
    args = parser.parse_args()

    # Create solver
    wordle = WordleSolver(args)
    # Generate words
    try:
        wordle.play(args)
        print("Suggestions: {}".format(', '.join(wordle.potential_words)))
    except KeyboardInterrupt:
        pass
