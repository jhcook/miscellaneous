#!/usr/bin/env python3.4
"""
This is an implementation of Rock-paper-scissors-lizard-Spock that can be 
found http://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-Spock.

Author: Justin Cook <jhcook@gmail.com>
"""

from random import randrange

sig = ['rock', 'Spock', 'paper', 'lizard', 'scissors']

def name_to_number(name):
    """Return the index of sig where name is located.

    >>> name_to_number('rock')
    0
    
    >>> name_to_number('Spock')
    1

    >>> name_to_number('paper')
    2

    >>> name_to_number('lizard')
    3

    >>> name_to_number('scissors')
    4
 
    >>> name_to_number('nonexistent')
    Traceback (most recent call last):
    ...
    ValueError: 'nonexistent' is not in list
    """
    return sig.index(name)

def number_to_name(number):
    """Return the value of sig[number].

    >>> number_to_name(0)
    'rock'

    >>> number_to_name(1)
    'Spock'

    >>> number_to_name(2)
    'paper'

    >>> number_to_name(3)
    'lizard'

    >>> number_to_name(4)
    'scissors'

    >>> number_to_name(5)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    """
    return sig[number]

def rpsls(player_choice, comp_choice=None): 
    """Returns the winner of rock-paper-scissors-lizard-Spock given the
    players choice (players_choice) and the computers choice (comp_choice).
    If not passed comp_choice, one is randomly generated.

    The rules of rock-paper-scissors-lizard-Spock are:

    Scissors cut paper
    Paper covers rock
    Rock crushes lizard
    Lizard poisons Spock
    Spock smashes scissors
    Scissors decapitate lizard
    Lizard eats paper
    Paper disproves Spock
    Spock vaporizes rock
    Rock crushes scissors

    >>> rpsls('scissors', 'paper')
    Player chooses scissors
    Computer chooses paper
    Player wins!

    >>> rpsls('scissors', 'rock')
    Player chooses scissors
    Computer chooses rock
    Computer wins!

    >>> rpsls('scissors', 'lizard')
    Player chooses scissors
    Computer chooses lizard
    Player wins!

    >>> rpsls('scissors', 'Spock')
    Player chooses scissors
    Computer chooses Spock
    Computer wins!

    >>> rpsls('paper', 'rock')
    Player chooses paper
    Computer chooses rock
    Player wins!

    >>> rpsls('paper', 'lizard')
    Player chooses paper
    Computer chooses lizard
    Computer wins!

    >>> rpsls('paper', 'Spock')
    Player chooses paper
    Computer chooses Spock
    Player wins!
   
    >>> rpsls('rock', 'lizard')
    Player chooses rock
    Computer chooses lizard
    Player wins!

    >>> rpsls('rock', 'Spock')
    Player chooses rock
    Computer chooses Spock
    Computer wins!

    >>> rpsls('lizard', 'Spock')
    Player chooses lizard
    Computer chooses Spock
    Player wins!

    >>> rpsls('doesnt', 'exist')
    Traceback (most recent call last):
    ...
    ValueError: 'doesnt' is not in list
    """

    print("Player chooses %s" % player_choice)
    player_number = name_to_number(player_choice)
    if not comp_choice:
        comp_number = randrange(0, 5)
    else:
        comp_number = name_to_number(comp_choice)
    comp_choice = number_to_name(comp_number)
    print("Computer chooses %s" % comp_choice)
    diff = (comp_number - player_number) % 5
    if diff in (1, 2):
        print("Computer wins!")
    elif diff in (3, 4):
        print("Player wins!")
    else:
        print("Player and computer tie!")


if __name__ == '__main__': 
    import doctest
    doctest.testmod()
