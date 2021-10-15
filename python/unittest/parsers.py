#!/usr/bin/env python3

class MyTextParser:

    words = []              # List of words
    sentences = []          # List of sentences
    longest_word_len = 0    # The length of the longest word
    sorted_word_count = []  # A list of each word's appearance in text sorted

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._text = args[0].strip()
            self._words()
            self._sentences()

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value.strip()
        self._words()
        self._sentences()
    
    @text.getter
    def text(self):
        return self._text
    
    def _words(self):
        """Split _text using single whitespace and period delimiters.
        
           The split words will be stored in a list. The longest word's length
           will be stored in longest_word_len. Each word's appearance count
           will be stored as a sorted list of tuples in sorted_word_count.
        """
        from re import split
        self.words = split('\ |\.', self._text)
        self.longest_word_len = 0
        word_count = {}
        for word in self.words:
            try:
                word_count[word] += 1
            except KeyError:
                word_count[word] = 1
            length = len(word)
            if length > self.longest_word_len:
                self.longest_word_len = length
        self.sorted_word_count = sorted(word_count.items(), key=lambda x: x[1],
                                        reverse=True)

    def _sentences(self):
        self.sentences = self._text.split('.')


if __name__ == "__main__":
    with open('stuff.txt', 'r') as stuff:
        text = MyTextParser(stuff.read())

    print("The word count is: {}".format(len(text.words)-1)) # Kludge
    print("The sentence count is: {}".format(len(text.sentences)-1))
    print("The longest word is: {}".format(text.longest_word_len))
    print("The six most occuring words are: {}".format(', '.join(
           [wrd[0] for wrd in text.sorted_word_count[0:6]])))
