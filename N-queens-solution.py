############################################################
# Imports
############################################################
# Include your imports here, if any are used.
import math, copy, random
try:
    from queue import PriorityQueue #py3
except ImportError:
    from Queue import PriorityQueue #py2
    range = xrange

import random
from collections import deque

def num_placements_all(n):
    return (math.factorial(n ** 2)) / (math.factorial(n ** 2 - n) * math.factorial(n))


def num_placements_one_per_row(n):
    return n ** n

def n_queens_valid(board):
    n = len(board)
    if len(set(board)) != n:
        return False
    for i in range(n):
        dangerList = {y - x - 1 for x, y in enumerate(board[i + 1:])}
        dangerList |= {y + x + 1 for x, y in enumerate(board[i + 1:])}
        if board[i] in dangerList:
            return False
    return True


def n_queens_helper(n, board):
    for i in range(n):
        if n_queens_valid(board + [i]):
            yield board + [i]


def n_queens_solutions(n):
    myStack = [[]]
    visited = set()
    while (myStack):
        front = myStack.pop()
        for newFront in n_queens_helper(n, front):
            if len(newFront) == n:
                yield newFront
            tup = tuple(newFront)
            if tup not in visited:
                visited |= {tup}
                myStack.append(newFront)
