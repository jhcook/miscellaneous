#!/usr/bin/env python3
#
# An implementation of Wordle.
# Inspired by: https://www.mongodb.com/developer/how-to/wordle-bash-data-api/
#
# Tested on macOS Monterey
#
# Author: Justin Cook

from re import (compile, search, IGNORECASE)
from random import choice

word_length = 5

class Wordle():
    
    dictionary = "/usr/share/dict/words"
    guess_lst = ['1st', '2nd', '3rd', '4th', '5th', '6th']
    wordle = game_word = srch_str = user_word = potential_words = unknown_chars = None

    def __init__(self):
        # Get a word six characters in length
        with open(self.dictionary, 'r') as d:
            the_words = [line.strip() for line in d.readlines() 
                         if len(line) == word_length+1]
            self.game_word = choice(the_words)
        self.srch_str = ["."] * word_length
        self.potential_words = []
        self.wordle = [None] * word_length
        self.num_guess = 0

    def __user_guess(self):
        """Prompt the user for input and increment num_guess"""
        while True:
            self.user_word = input("Enter {} word: ".format(self.guess_lst[self.num_guess]))
            if len(self.user_word) != word_length:
                print("Word must be {} characters.".format(word_length))
                continue
            self.num_guess += 1
            break
    
    def __search_dictionary(self):
        """Consult known matched characters `self.srch_str` to narrow down
        word candidates.
        """
        self.potential_words = []
        temp_str = ''.join(self.srch_str)
        regex = compile(rf"^{temp_str}$", flags=IGNORECASE)
        with open(self.dictionary, 'r') as d:
            tl = self.unknown_chars.values()
            required_letters = [item for tl in tl for item in tl]
            for line in d.readlines():
                word = regex.search(line)
                if word:
                    commit = True
                    the_word = word.group()
                    if required_letters:
                        for res in [c in the_word for c in required_letters]:
                            if not res: commit = False
                    if commit:
                        self.potential_words.append(the_word)

    def __check_guess(self):
        if self.user_word == self.game_word.lower():
            print("Good job!")
            return True
        self.__gen_wordle()
        self.__search_dictionary()
    
    def __gen_wordle(self):
        """Enumerate through `self.user_word` anc compare each character with
        `self.game_word`. Update self.wordle with the appropriate character and
        recreate the search string based on the results."""
        self.unknown_chars = {}
        blacked_out = []
        self.srch_str = ["."] * len(self.game_word)
        for i, v in enumerate(self.user_word):
            if self.game_word[i].lower() == v:
                self.wordle[i] = "🟩"
                self.srch_str[i] = v
            elif search(rf"{v}", self.game_word, flags=IGNORECASE):
                self.wordle[i] = "🟨"
                self.unknown_chars[i] = v
            else:
                self.wordle[i] = "⬛️"
                blacked_out.append(v)
        
        for i, v in enumerate(self.srch_str):
            if v != '.': continue
            chars = []
            for k in self.unknown_chars:
                if i == k:
                    chars.extend(self.unknown_chars[k])
            if chars or blacked_out:
                self.srch_str[i] = "(?:(?![{}])[a-z]){{1}}".format(''.join(chars+blacked_out))

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
            print("Suggestions: {}".format(", ".join(self.potential_words)))
        else:
            print("Sorry, the answer is: {}".format(self.game_word))

if __name__ == "__main__":
    # Create game
    wordle = Wordle()
    # Play game
    try:
        wordle.play()
    except KeyboardInterrupt:
        print()