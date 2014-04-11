#!/usr/bin/env python3.4

from sys import exit
from re import search, IGNORECASE

tries = 1

while True:
    if tries > 3:
        print("Too many tries")
        exit(1)
    try:
        temp, umeas = search(r'(\d+)([cf]{1})', 
                             input("Temp, e.g. 32F: "), 
                             flags=IGNORECASE).group(1, 2)
        break
    except:
        pass
    finally:
        tries += 1

if umeas in 'fF':
    print(round((int(temp) - 32) * 5/9., 2), "C")
elif umeas in 'cC':
    print(round(int(temp) * 9/5. + 32, 2), "F")
else:
    print("If you got here you are super special")
