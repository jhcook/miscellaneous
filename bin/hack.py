#!/usr/bin/env python
# encoding: utf-8
"""This little script uses the passlib module to attempt looping through
an array of characters odometer style and tries to match a hash generated
by either a password or hash given.

Tested: Mac OS X Yosemite
        Mac OS X El Capitan
        RHEL7

Author: Justin Cook <jhcook@gmail.com>
"""

# Use multiple processors so sidestep the GIL
from multiprocessing import Pool
from sys import exit
# Crypt is not portable
from passlib.hash import sha512_crypt
# Very useful for producing odometer-like iterables
from itertools import product

def verify_hash(wrd):
    # An easy pass 'aaaaaabz'
    # hashed_pass = "$6$1wz2nRjA$z9tZ1JvBzx658MZrj7osVDbk86UOjHcL2O58JGJ.iBD3iFYy7hoc6yhOLHBmqyjaZhq6E8jg9gbpM7n9Ogj/d."

    if sha512_crypt.verify(wrd, hashed_pass):
        return wrd

# The ordinals for alphanums
chars = []
[chars.extend(l) for l in [range(97, 123), range(65, 91), range(48, 58)]]

# Create a pool of subprocesses to sidestep the GIL and iterate through in 
# chunks of 1000
p = Pool(8)

# Loop through alphanums odometer style
for i in range(8, len(chars) + 1):
    wrds = []
    for wrd in product(chars, repeat=i):
        wrds.append(''.join([chr(c) for c in wrd]))
        if len(wrds) >= 1000:
            try:
                results = p.map(verify_hash, wrds)
                for result in results:
                    if result:
                        print(result)
                        raise KeyboardInterrupt
                print(wrds[-1])
                wrds = []
            except KeyboardInterrupt:
                break
        else:
            continue
    p.terminate()
    break
