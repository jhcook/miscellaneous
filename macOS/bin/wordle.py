#!/usr/bin/env python3
#
# An implementation of Wordle.
# Inspired by: https://www.mongodb.com/developer/how-to/wordle-bash-data-api/
#
# Tested on macOS Monterey
#
# Author: Justin Cook

from re import (compile, finditer, search, IGNORECASE)
from random import choice

word_length = 5

class Wordle():
    
    dictionary = "/usr/share/dict/words"
    guess_lst = ['1st', '2nd', '3rd', '4th', '5th', '6th']
    num_guess = 0
    wordle = [""] * word_length
    game_word = temp_word = user_word = potential_words = None

    def __init__(self):
        # Get a word six characters in length
        with open(self.dictionary, 'r') as d:
            the_words = [line.strip() for line in d.readlines() 
                         if len(line) == word_length+1]
            self.game_word = choice(the_words)
        self.temp_word = ["."] * len(self.game_word)
        self.potential_words = []

    def __user_guess(self):
        """Prompt the user for input and increment num_guess"""
        while True:
            self.user_word = input("Enter {} word: ".format(self.guess_lst[self.num_guess]))
            if len(self.user_word) != word_length:
                print("Word must be {} characters.".format(word_length))
                continue
            self.num_guess += 1
            break

    def __find_matches(self):
        """`matches` is a dict which is populated with each char and a list of
        indexes from guesses that match game_word.
        """
        matches = {}
        for s in self.user_word:
            search = finditer(rf"({s})", self.game_word, flags=IGNORECASE)
            [matches.setdefault(s, []).append(m.span()[0]) for m in search]
        # Update self.temp_word with these findings
        for c in matches:
            for i in matches[c]:
                self.temp_word[i] = c
    
    def __search_dictionary(self):
        """Consult known matched characters `self.temp_word` to narrow down
        word candidates.
        """
        self.potential_words = []
        temp_word = ''.join(self.temp_word)
        regex = compile(rf"^{temp_word}$", flags=IGNORECASE)
        with open(self.dictionary, 'r') as d:
            for line in d.readlines():
                word = regex.search(line)
                if word: self.potential_words.append(word.group())

    def __check_guess(self):
        if self.user_word == self.game_word.lower():
            print("Good job!")
            return True
        self.__find_matches()
        self.__search_dictionary()
    
    def __gen_wordle(self):
        for i, v in enumerate(self.user_word):
            if self.game_word[i] == v:
                self.wordle[i] = "🟩"
            elif search(rf"{v}", self.game_word):
                self.wordle[i] = "🟨"
            else:
                self.wordle[i] = "⬛️"

    def play(self):
        while self.num_guess < len(self.guess_lst):
            # Prompt for user try
            self.__user_guess()
            # Check user's input
            if self.__check_guess():
                return
            # Print Wordle
            self.__gen_wordle()
            print("".join(self.wordle))
            # Print suggested words
            print("Suggestions: {}".format(", ".join(self.potential_words)))
        else:
            print("Sorry, the answer is: {}".format(self.game_word))

if __name__ == "__main__":
    # Create game
    wordle = Wordle()
    # Play game
    wordle.play()