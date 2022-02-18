# Introduction

Here are things you may use on the command line in on macOS. 

## Games

### Wordle

It took social media by storm, and then NY Times bought it!

This is my training wheel version for mere mortals.

```
 ./wordle.py
Enter 1st word: chase
⬛️⬛️🟨🟩⬛️
Suggestions: salsa, artsy, abyss, amiss, angst, daisy, gassy, lasso, palsy, pansy, patsy, sassy, waist
Enter 2nd word: daisy
⬛️🟩⬛️🟩🟩
Suggestions: gassy, palsy, pansy, patsy, sassy
Enter 3rd word: patsy
Good job!
```

## Wordle Solver

This tool uses a dictionary of words with hints provided and suggests possible
answers matching the hints. 

```
./wsolver.py -h
usage: wsolver.py [options]

A tool to help solve Wordle.

optional arguments:
  -h, --help            show this help message and exit
  -a FIRST, --first FIRST
                        1st character hint
  -b SECOND, --second SECOND
                        2nd character hint
  -c THIRD, --third THIRD
                        3rd character hint
  -d FOURTH, --fourth FOURTH
                        4th character hint
  -e FIFTH, --fifth FIFTH
                        5th character hint
  -z DUD, --dud DUD     characters not in word

...just like that!
```

In the example below, the `!` character is used to
mark the character as yellow, i.e., used in the word but not that position.
Green characters are marked as just the letter for that position and duds are
known black out or letters known not to be used in the word. The following is a
real-world example with the answer being _caulk_ in Wordle 242. The dictionary
can be found on [Github](https://raw.githubusercontent.com/dwyl/english-words/master/words.txt). 

Potential candidates are sorted by [letter frequency](https://artofproblemsolving.com/news/articles/the-math-of-winning-wordle).

A good list of [words on AoPS Online](https://artofproblemsolving.com/texer/vxeinejf) is a great source.

Below, the first word was _lunch_. The hints provided the following suggestions
and the second word choice was _oculi_. The hints provided fewer suggestions
with _caulk_ selected as the correct final choice.

```
 ./wsolver.py
first known letter: !l
second known letter: !u
third known letter:
fourth known letter: !c
fifth known letter:
Known duds: nh
Suggestions: caulk, cruel, ulcer, clued, cloud, clout, clump, could

 ./wsolver.py
first known letter:
second known letter: !c
third known letter: u
fourth known letter: l
fifth known letter:
Known duds: oi
Suggestions: caulk
```

Multiple round of hints can be provided in one go. For example, the above hints
are combined below. Note that known letters (green) override yellow or unknown
position letters.

```
 ./wsolver.py
first known letter: !l
second known letter: !uc
third known letter: u
fourth known letter: l
fifth known letter:
Known duds: nhoi
Suggestions: caulk
```

The non-interactive command-line argument version:

```
 ./wsolver.py -a '!l' -b '!uc' -c u -d l -z nhoi
Suggestions: caulk
```