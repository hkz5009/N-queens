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


############################################################
# Section 1: N-Queens
############################################################
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

############################################################
# Section 2: Lights Out
############################################################
class LightsOutPuzzle(object):
    def __init__(self, board):
        self.board = board
        self.row = len(board)
        self.col = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        tups = ((row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        for tup in tups:
            if tup[0] < self.row and tup[1] < self.col and tup[0] >= 0 and tup[1] >= 0:
                self.board[tup[0]][tup[1]] = not self.board[tup[0]][tup[1]]

    def scramble(self):
        for i in range(self.row):
            for j in range(self.col):
                if random.random() < 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        for row in self.board:
            for i in row:
                if i:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors2(self):
        p = self.copy()
        for i in range(self.row):
            for j in range(self.col):
                p.perform_move(i, j)
                yield ((i, j), p)
                p.perform_move(i, j)

    def successors(self):
        for i in range(self.row):
            for j in range(self.col):
                p = self.copy()
                p.perform_move(i, j)
                yield ((i, j), p)

    def find_solution(self):
        myQueue = deque()
        tup = tuple(tuple(x) for x in self.board)
        movement = deque()
        myQueue.append(tup)
        movement.append([])
        visited = {tup}
        while len(myQueue) != 0:
            front = myQueue.popleft()
            newFront = LightsOutPuzzle([[i for i in x] for x in front])
            path = movement.popleft()
            for move, puzzle in newFront.successors2():
                newPuzzle = tuple(tuple(x) for x in puzzle.board)
                if puzzle.is_solved():
                    return path + [move]
                if newPuzzle not in visited:
                    myQueue.append(newPuzzle)
                    movement.append(path + [move])
                    # visited |= {newPuzzle} long set plus long is fastt
                    visited.add(newPuzzle)
        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for i in range(cols)] for j in range(rows)])



############################################################
# Section 3: Linear Disk Movement
############################################################

def help1(tup):
    grid = list(tup)
    l = len(tup)
    for i in range(l):
        if tup[i]:
            if i + 1 < l and not tup[i + 1]:
                grid[i] = False
                grid[i + 1] = True
                yield ((i, i + 1), tuple(grid))
                grid[i] = True
                grid[i + 1] = False

            elif i + 2 < l and not tup[i + 2]:
                grid[i] = False
                grid[i + 2] = True
                yield ((i, i + 2), tuple(grid))
                grid[i] = True
                grid[i + 2] = False


def solve_identical_disks(length, n):
    start = tuple([True] * n + [False] * (length - n))
    end = start[-1::-1]

    myQueue = deque()
    movement = deque()
    myQueue.append(start)
    movement.append([])
    visited = {start}
    while len(myQueue) != 0:
        front = myQueue.popleft()
        path = movement.popleft()
        for move, puzzle in help1(front):
            if puzzle == end:
                return path + [move]
            if puzzle not in visited:
                myQueue.append(puzzle)
                movement.append(path + [move])
                visited.add(puzzle)
    return None



############################################################

def help2(tup):
    grid = list(tup)
    l = len(tup)
    for i, val in enumerate(tup):
        if val is not None:
            if i + 1 < l and tup[i + 1] is None:
                grid[i] = None
                grid[i + 1] = val
                yield ((i, i + 1), tuple(grid))
                grid[i] = val
                grid[i + 1] = None
            elif i + 2 < l and tup[i + 2] is None:
                grid[i] = None
                grid[i + 2] = val
                yield ((i, i + 2), tuple(grid))
                grid[i] = val
                grid[i + 2] = None

            if i > 0 and tup[i - 1] is None:
                grid[i] = None
                grid[i - 1] = val
                yield ((i, i - 1), tuple(grid))
                grid[i] = val
                grid[i - 1] = None
            elif i > 1 and tup[i - 2] is None:
                grid[i] = None
                grid[i - 2] = val
                yield ((i, i - 2), tuple(grid))
                grid[i] = val
                grid[i - 2] = None


def solve_distinct_disks(length, n):
    start = tuple(list(range(n)) + [None] * (length - n))
    end = start[-1::-1]

    myQueue = deque()
    movement = deque()
    myQueue.append(start)
    movement.append([])
    visited = {start}
    while len(myQueue) != 0:
        front = myQueue.popleft()
        path = movement.popleft()
        for move, puzzle in help2(front):
            if puzzle == end:
                return path + [move]
            if puzzle not in visited:
                myQueue.append(puzzle)
                movement.append(path + [move])
                visited.add(puzzle)
    return None


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
24 hours
"""

feedback_question_2 = """
I think the most challenging part for me was to figure out the implementation of BFS.
"""

feedback_question_3 = """
it allowed me to review basic python and learn how to do tree search methods.
"""
