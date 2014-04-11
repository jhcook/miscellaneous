#!/usr/bin/env python3.4
#
# Conway's Game of Life
#
# Author: Justin Cook <jhcook@gmail.com>

from random import randint

class Conway():
    """I would normally write some clever comments here, but everyone knows
       what this does. If you don't know, then it doesn't matter. It may not
       do what it claims -- Conway's game of life. After all, this was written
       in a hurry!
    """
    def __init__(self, size=10, board=None):
        # If no board is passed, create a random board.
        if not board:
            self.size = size
            self.board = [[randint(0, 1) for x in range(size)] 
                          for x in range(size)]
        else:
            # If a board was passed in, assume it is a List and make a copy.
            # Since it is a list of integers, a shallow copy will work just fine.
            self.size = len(board)
            self.board = board.copy()
        self.__alive_cells = self.__collate_alive()

    def __collate_alive(self):
        alive = set()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    alive.add((i, j))
        return alive

    def calculate_board(self):
        """This can probably be done far more efficiently, but since it is
           necessary to calculate both dead and alive cells, that means all
           cells need to be accounted for. I'm no clever mathematician, so
           I will use the power of fast CPU and gigs of RAM at my disposal to
           do so.
        """
        self.new_board = [[0]*self.size for x in range(self.size)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                count = self.__calculate_neighborhood((i, j))
                if self.board[i][j]:
                    # A live cell with fewer than two live neighbours dies.
                    if count < 2:
                        self.new_board[i][j] = 0
                    # A live cell with more than three live neighbours dies.
                    elif count > 3:
                        self.new_board[i][j] = 0
                    # A live cell with two or three live neighbours lives.
                    else:
                        self.new_board[i][j] = 1
                else:
                    # A dead cell with exactly three live neighbours becomes 
                    # alive.
                    if count == 3:
                        self.new_board[i][j] = 1

    def __calculate_neighborhood(self, coord):
        alive_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i or j:
                    if (coord[0]+i, coord[1]+j) in self.__alive_cells:
                        alive_count += 1
        return alive_count

t = Conway()
t.calculate_board()

import pprint
pprint.pprint(t.board)
print()
pprint.pprint(t.new_board)

