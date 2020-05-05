#!/usr/bin/env python3
#
# Generate a delimited string of random alphanumeric characters
# sufficient for a complicated password. 
#
# Author: Justin Cook <jhcook@secnix.com>

from random import seed, choices, randrange
from string import ascii_letters, digits
from datetime import datetime

# Seed random
seed(datetime.now())

# Create an alphanumeric string subdivided by a delimiter
freq = randrange(3,6)
print(choices('!@#$%^&*=+')[0].join([''.join(choices(ascii_letters + digits,
                                     k=freq)) for i in range(round(28/freq))]))