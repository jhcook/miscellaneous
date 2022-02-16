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

from re import compile

word_length = 5

class WordleSolver():
    
    dictionary = "words"
    letters = ['1st', '2nd', '3rd', '4th', '5th']
    srch_str = potential_words = blacked_out = unknown_chars = None

    def __init__(self):
        self.potential_words = []
        self.blacked_out = set()
        self.unknown_chars = {i: set() for i in range(word_length)}
        self.srch_str = ['[a-z]'] * word_length

    def __user_prompt(self):
        for i, l in enumerate(self.letters):
            known = input(f"{l} known letter: ")
            if known.startswith('!'):
                [self.unknown_chars[i].add(c) for c in known[1:]]
            elif known:
                self.srch_str[i] = known
        self.blacked_out.add(input("Known duds: "))
    
    def __gen_search(self):
        for i, v in enumerate(self.srch_str):
            if v != '[a-z]': continue
            chars = []
            for k in self.unknown_chars:
                if i == k:
                    chars.extend(self.unknown_chars[k])
            if chars or self.blacked_out:
                self.srch_str[i] = "(?:(?![{}])[a-z]){{1}}".format(''.join(chars+[c for c in self.blacked_out]))

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
                    if required_letters: # This should be replaced with lookaheads
                        for res in [c in the_word for c in required_letters]:
                            if not res: commit = False
                    if self.blacked_out: # This should be replaced with lookaheads
                        for bo in [c in the_word for c in self.blacked_out]:
                            if bo: commit = False
                    if commit:
                        self.potential_words.append(the_word)

    def play(self):
        self.__user_prompt()
        self.__gen_search()
        self.__search_dictionary()

if __name__ == "__main__":
    # Create solver
    wordle = WordleSolver()
    # Generate words
    try:
        wordle.play()
        print("Suggestions: {}".format(', '.join(wordle.potential_words)))
    except KeyboardInterrupt:
        pass
