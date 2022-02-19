# Introduction

Here are things you may use on the command line on macOS. 

## Games

### Wordle

It took social media by storm, and then NY Times bought it!

This is my ascii terminal version for mere mortals -- or you may like it if 
you're a command-line warrior.

You can see below the command line and options available. By default,
it uses the dictionary available on your system. You can download and use
any dictionary you feel comfortable with. 

```
$ ./wordle.py -h
usage: wordle.py [options]

The game of Wordle.

optional arguments:
  -h, --help            show this help message and exit
  -a, --assistance      give word hints
  -w WORDS, --words WORDS
                        path to dictionary

...is a lot of fun!
```

Here is an invocation using the standard dictionary -- and it adawes you with
stimulating intellectual exercise. 

```
$ ./wordle.py
Enter 1st word: raise
⬛️🟨⬛️⬛️🟩
Enter 2nd word: alone
🟩⬛️⬛️⬛️🟩
Enter 3rd word: acute
🟩⬛️⬛️⬛️🟩
Enter 4th word: amaze
🟩⬛️🟩⬛️🟩
Enter 5th word: awake
🟩🟨🟩⬛️🟩
Enter 6th word: adawe
Good job!
```

If you want a little help, you can use the assist option to provide a list of
words that match the hints provided by the success/failure of your current
guesses.

```
$ ./wordle.py -aw wwords
Enter 1st word: raise
🟨⬛️⬛️⬛️⬛️
Suggestions: flour, glory, growl, prowl, world
Enter 2nd word: flour
⬛️⬛️🟩⬛️🟨
Suggestions: thorn, broth, brown, crony, crown
Enter 3rd word: thorn
⬛️⬛️🟩🟨⬛️
Suggestions: crowd, proxy, brood, brook, broom
Enter 4th word: crowd
⬛️🟩🟩⬛️🟩
Suggestions: brood
Enter 5th word: brood
Good job!
```

## Wordle Solver

This tool uses a dictionary of words with hints provided and suggests possible
answers matching the hints. It's pretty clever indeed.

```
$ ./wsolver.py -h
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
  -i, --interactive     interactive session
  -v, --verbose         increase verbosity
  -w WORDS, --words WORDS
                        path to dictionary
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
[More information](https://www.dictionary.com/e/wordle/) on letter distribution and frequency is used to weigh potential words.

A good list of [words on AoPS Online](https://artofproblemsolving.com/texer/vxeinejf) is a great source.

Below, the first word was _lunch_. The hints provided the following suggestions
and the second word choice was _oculi_. The hints provided fewer suggestions
with _caulk_ selected as the correct final choice. Use `-v` command-line option
for an exhaustive list of potential words.

```
 ./wsolver.py -ivw wwords
first known letter: !l
second known letter: !u
third known letter:
fourth known letter: !c
fifth known letter:
Known duds: nh
Suggestions: cruel, ulcer, clued, caulk, clout, cloud, could, clump

$ ./wsolver.py -i
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
$ ./wsolver.py -i
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
$ ./wsolver.py -a '!l' -b '!uc' -c u -d l -z nhoi
Suggestions: caulk
```