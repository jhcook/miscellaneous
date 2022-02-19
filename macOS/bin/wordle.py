#!/usr/bin/env python3
#
# An implementation of Wordle.
# Inspired by: https://www.mongodb.com/developer/how-to/wordle-bash-data-api/
#
# Tested on macOS Monterey
#
# Author: Justin Cook

from sys import exit
from argparse import ArgumentParser
from re import (compile, search)
from collections import Counter
from random import choice

word_length = 5

class Wordle():
    guess_lst = ['1st', '2nd', '3rd', '4th', '5th', '6th']
    dictionary = wordle = game_word = srch_str = user_word = None
    potential_words = blacked_out = unknown_chars = assistance = None

    def __init__(self, words=None, assistance=False):
        # Get a word six characters in length
        self.dictionary = words if words else "/usr/share/dict/words"
        try:
            with open(self.dictionary, 'r') as d:
                searcher = compile(f"[a-z]{{{word_length}}}")
                self.the_words = [line.strip() for line in d.readlines() 
                                if len(line) == word_length+1]
                self.game_word = choice(list(filter(searcher.match,
                                                    self.the_words)))
        except (FileNotFoundError, PermissionError, OSError) as err:
            self.game_word = err
        self.srch_str = ["[a-z]"] * word_length
        self.potential_words = []
        self.wordle = [None] * word_length
        self.num_guess = 0
        self.blacked_out = set()
        self.unknown_chars = {i: set() for i in range(word_length)}
        self.assistance = assistance

    def __user_guess(self):
        """Prompt the user for input and increment num_guess"""
        while True:
            self.user_word = input("Enter {} word: ".format(self.guess_lst[self.num_guess]))
            if len(self.user_word) != word_length:
                print("Word must be {} characters.".format(word_length))
                continue
            elif self.user_word not in self.the_words:
                print("That's not a word!")
                continue
            self.num_guess += 1
            break
    
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
                    commit = True
                    the_word = word.group()
                    for res in [c in the_word for c in required_letters]:
                        if not res: 
                            commit = False
                            break
                    if commit:
                        self.potential_words.append(the_word)

    def __letter_frequency(self): 
        potential_words = {w: Counter(list(w)) for w in self.potential_words}
        potential_words = {k: v for k, v in sorted(potential_words.items(), 
                           key=lambda c: [c[1][v] for v in 'chare'],
                           reverse=True)}
        self.potential_words = [k for k in potential_words]

    def __check_guess(self):
        if self.user_word == self.game_word.lower():
            print("Good job!")
            return True
        self.__gen_wordle()
        self.__gen_search()
        self.__search_dictionary()
    
    def __gen_wordle(self):
        """Enumerate through `self.user_word` anc compare each character with
        `self.game_word`. Update self.wordle with the appropriate character and
        recreate the search string based on the results."""
        for i, v in enumerate(self.user_word):
            if self.game_word[i].lower() == v:
                self.wordle[i] = "🟩"
                self.srch_str[i] = v
            elif search(rf"{v}", self.game_word):
                self.wordle[i] = "🟨"
                self.unknown_chars[i].add(v)
            else:
                self.wordle[i] = "⬛️"
                self.blacked_out.add(v)
        
    def __gen_search(self):
        for i, v in enumerate(self.srch_str):
            if not self.unknown_chars[i] and not self.blacked_out: continue
            if len(v) > 1:
                self.srch_str[i] = "(?:(?![{}])[a-z]){{1}}".format(''.join(
                        set.union(self.unknown_chars[i], self.blacked_out)))

    def play(self):
        while self.num_guess < len(self.guess_lst):
            # Prompt for user try
            self.__user_guess()
            # Check user's input
            if self.__check_guess():
                return
            # Print Wordle
            print("".join(self.wordle))
            # Print suggested words
            self.__letter_frequency()
            if self.assistance:
               print("Suggestions: {}".format(", ".join(self.potential_words)))
        else:
            print("Sorry, the answer is: {}".format(self.game_word))

if __name__ == "__main__":
    # Get command-line arguments
    parser = ArgumentParser(prog='wordle.py', usage='%(prog)s [options]',
                            description="The game of Wordle.",
                            epilog="...is a lot of fun!")
    parser.add_argument('-a', '--assistance', action='store_true',
                        help='give word hints')
    parser.add_argument('-w', '--words', type=str,
                        help='path to dictionary')
    args = parser.parse_args()

    # Create game
    wordle = Wordle(**vars(args))
    if issubclass(type(wordle.game_word), BaseException):
        print(wordle.game_word)
        exit(2)

    # Play game
    try:
        wordle.play()
    except KeyboardInterrupt:
        print()
