#!/usr/bin/env python3
# Run unit tests for reader.py
#
# Usage: $ python3 -m unittest discover -s .
#
# Author: Justin Cook <jhcook@secnix.com>

import unittest
import parsers

class TestMyTextParser(unittest.TestCase):

    def setUp(self) -> None:
        """Setup the app for each test."""
        with open('stuff.txt', 'r') as stuff:
            self.app = parsers.MyTextParser(stuff.read())
        return super().setUp()

    def test_word_count(self):
        """Check if word count is accurate."""
        self.assertEqual(len(self.app.words)-1, 260)

    def test_sentence_count(self):
        """Check if sentence count is accurate."""
        self.assertEqual(len(self.app.sentences)-1, 22)

    def test_longest_word_len(self):
        """Check if longest word length is accurate."""
        self.assertEqual(self.app.longest_word_len, 15)

    def test_six_most_occuring_words(self):
        """Check if six most occuring words are accurate."""
        self.assertListEqual(self.app.sorted_word_count[0:6],
            [('non', 7), ('est', 6), ('enim', 6), ('mihi', 5), ('ut', 5), 
             ('quid', 5)])

class TestKaluzaTextParserNoInit(unittest.TestCase):

    def setUp(self) -> None:
        """Setup the app for each test."""
        self.app = parsers.MyTextParser()
        with open('stuff.txt', 'r') as stuff:
            self.app.text = stuff.read()
        return super().setUp()

    def test_word_count(self):
        """Check if word count is accurate."""
        self.assertEqual(len(self.app.words)-1, 260)

    def test_sentence_count(self):
        """Check if sentence count is accurate."""
        self.assertEqual(len(self.app.sentences)-1, 22)

    def test_longest_word_len(self):
        """Check if longest word length is accurate."""
        self.assertEqual(self.app.longest_word_len, 15)

    def test_six_most_occuring_words(self):
        """Check if six most occuring words are accurate."""
        self.assertListEqual(self.app.sorted_word_count[0:6],
            [('non', 7), ('est', 6), ('enim', 6), ('mihi', 5), ('ut', 5), 
             ('quid', 5)])

if __name__ == "__main__":
    unittest.main()