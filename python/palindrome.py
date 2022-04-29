#!/usr/bin/env python3
# A simple palindrome test implementation.
#
# Main iterates through the platform word dictionary and tests each using the
# very complicated isPalindrome algorithm.
#
# References: https://stackoverflow.com/questions/10140281/how-to-find-out-whether-a-file-is-at-its-eof
#
# Author: Justin Cook

def isPalindrome(word):
    """Return True if word is a palindrome.

    Word must be greater than two characters or raises ValueError. 

    >>> for word in ["racecar", "developer", "447500005744", str(8675309)]:
    ...     print("{}: {}".format(word, isPalindrome(word)))
    racecar: True
    developer: False
    447500005744: True
    8675309: False
    >>> isPalindrome("aa")
    Traceback (most recent call last):
        ...
    ValueError: word must be greater than two characters
    """
    if len(word) < 3:
        raise ValueError("word must be greater than two characters")
    return False not in [word[x].lower() == word[-(x+1)].lower() for x in range(0,len(word)//2)]

if __name__ == "__main__":
    # Open the word dictionary and iterate line by line testing each word
    with open('/usr/share/dict/words') as dict:
        # Get the file size to test for EOF on each iteration
        dict.seek(0, 2)
        file_size = dict.tell()
        dict.seek(0)
        while True:
            word = dict.readline().strip()
            try:
                if isPalindrome(word):
                    print("Palindrome: {}".format(word))
                if dict.tell() == file_size:
                    break
            except ValueError:
                pass
