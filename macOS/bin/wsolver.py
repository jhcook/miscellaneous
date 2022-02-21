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

from sys import exit
from argparse import ArgumentParser
from re import compile
from collections import Counter

word_length = 5

class WordleSolver():
    
    letters = ['first', 'second', 'third', 'fourth', 'fifth']
    dictionary = srch_str = potential_words = blacked_out = None
    unknown_chars = interactive = study = None

    def __init__(self, args):
        self.potential_words = []
        self.blacked_out = set()
        self.unknown_chars = {i: set() for i in range(word_length)}
        self.srch_str = ['[a-z]{1}'] * word_length
        self.study = args.study
        self.dictionary = args.words if args.words else "/usr/share/dict/words"
        try:
            with open(self.dictionary, 'r') as d:
                searcher = compile(f"^[a-z]{{{word_length}}}$")
                self.the_words = [line.strip() for line in d.readlines()
                                  if searcher.search(line)]
        except (FileNotFoundError, PermissionError, OSError) as err:
            self.dictionary = err
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
        potential_words = {w: Counter(w) for w in self.potential_words}
        potential_words = {k: v for k, v in sorted(potential_words.items(), 
                           key=self.frequency, reverse=True)}
        self.potential_words = [k for k in potential_words]

    def __gen_frequency(self):
        """Calculate letter frequency amost all five-letter words in the
        dictionary and create an algorithm weighing groups of letters and
        distribution.
        """
        if not self.study:
            self.frequency =lambda c: [len(set(c[1].keys()))*4] + \
                                      [c[1][l]*3 for l in 'sea'] + \
                                      [c[1][l]*2 for l in 'ori'] + \
                                      [c[1][l] for l in 'ltn']
            return

        # Count all letters across all words in the dictionary.
        letter_count = Counter()
        [letter_count.update(w) for w in self.the_words]

        # Group the letters by 10%. Counters are ordered by value.
        letter_groups = {}
        i, rank = (0, 0)
        for letter, count in letter_count.most_common():
            if rank == 0: rank = count
            letter_groups.setdefault(i, [])
            if count <= int(.9*rank):
                i += 1
                rank = count
                letter_groups.setdefault(i, [])
            letter_groups[i].extend(letter)

        self.frequency = lambda c: [len(set(c[1].keys()))*8] + \
                                   [c[1][l]*7 for l in letter_groups[0]] + \
                                   [c[1][l]*6 for l in letter_groups[1]] + \
                                   [c[1][l]*5 for l in letter_groups[2]] + \
                                   [c[1][l]*4 for l in letter_groups[3]] + \
                                   [c[1][l]*3 for l in letter_groups[4]] + \
                                   [c[1][l]*2 for l in letter_groups[5]] + \
                                   [c[1][l] for l in letter_groups[6]]

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
        tl = self.unknown_chars.values() 
        rl = set([item for tl in tl for item in tl])
        required_letters = ["(?=.*{})".format(c) for c in rl]
        ss = "(?:{})^{}$".format(''.join(required_letters), temp_str) if \
                          required_letters else rf"^{temp_str}$"
        regex = compile(ss)
        with open(self.dictionary, 'r') as d:
            for line in d.readlines():
                word = regex.search(line)
                if word:
                    self.potential_words.append(word.group())

    def play(self, args=None):
        self.__user_prompt(args)
        self.__gen_search()
        self.__search_dictionary()
        self.__gen_frequency()
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
    parser.add_argument('-s', '--study', action='store_true',
                        help='analyze the dictionary for letter frequency')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase verbosity')
    parser.add_argument('-w', '--words', type=str, default='',
                        help='path to dictionary')
    parser.add_argument('-z', '--dud', type=str, default='',
                        help='characters not in word')
    args = parser.parse_args()

    # Create solver
    wordle = WordleSolver(args)
    if issubclass(type(wordle.dictionary), BaseException):
        print(wordle.dictionary)
        exit(2)

    # Generate and display words
    wordle.play(args)
    if not args.verbose:
        print("Suggestions: {}".format(", ".join([w for i, w in
                                enumerate(wordle.potential_words) if i < 5])))
    else:
        print("Suggestions: {}".format(", ".join([w for w in 
                                                  wordle.potential_words])))
