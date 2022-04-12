"""
Tic Tac Toe Player
"""
from copy import deepcopy
from queue import Empty
from random import choice
import numpy as np
import math


# possible moves of the board
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    temp = 0
    for row in board:
        for value in row:
            if value != EMPTY:
                temp += 1

    if temp % 2:
        return O
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j, j_value in enumerate(board[i]):
            if j_value is EMPTY:
                possible_actions.add((i, j))

    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (x, y) = action

    if (x < 0 or x >= len(board)) or (y < 0 or y >= len(board)):
        raise IndexError()

    #actionArray = board
    actionBoard = deepcopy(board)
    move = player(actionBoard)
    actionBoard[action[0]][action[1]] = move
    
    return actionBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # if there is no winner, returns 0
    next_player = player(board)
    if next_player is X:
        last_player = O
    else:
        last_player = X

    if vertical_check(board, last_player) or horizontal_check(board, last_player) or diagonal_check(board, last_player):
        return last_player
    else:
        return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is X or winner(board) is O:
        return True
    elif is_draw(board):
        return True
    else:
        return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    choice = None
    if player(board) == X:
        v = -2
        for action in actions(board):
            a = min_value(result(board, action))
            if a > v:
                v = a
                choice = action
    elif player(board) == O:
        v = 2
        for action in actions(board):
            a = max_value(result(board, action))
            if a < v:
                v = a
                choice = action
    
    return choice

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):

    if terminal(board):
        return utility(board)
    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def horizontal_check(board, player):
    counter = 0
    for row in board:
        for value in row:
            if value == player:
                counter += 1

                if counter == 3:
                    return 1
        counter = 0

    return 0


def diagonal_check(board, player):

    # getting both diagonals
    major_diagonal = np.diagonal(board)
    # np.rot90 flip board, so that it is rotated by 90 degrees
    minor_diagonal = np.diagonal(np.rot90(board))

    if np.all(major_diagonal == player) or np.all(minor_diagonal == player):
        return 1
    else:
        return 0


def vertical_check(board, player):
    transposed_board = np.transpose(board)
    counter = 0
    for row in transposed_board:
        for value in row:
            if value == player:
                counter += 1

                if counter == 3:
                    return 1
        counter = 0

    return 0


def is_draw(board):

    if EMPTY in board:
        return 0
    else:
        return 1
