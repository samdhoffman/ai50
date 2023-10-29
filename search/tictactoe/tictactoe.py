from collections import Counter
from itertools import chain
import copy

"""
Tic Tac Toe Player
"""

import math

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
    empty_board_cells = Counter(chain.from_iterable(board))[None]

    if empty_board_cells % 2 == 0:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    valid_actions = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                valid_actions.add((row, col))

    return valid_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board) or board[action[0]][action[1]] != None:
        raise Exception(f'{action} is not a valid action')

    cur_player = player(board)
    new_board = copy.deepcopy(board)
    row = action[0]
    col = action[1]
    new_board[row][col] = cur_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontally
    for row in range(3):
        moves = set(board[row])
        if len(moves) == 1:
            return board[row][0]

    # check vertically
    for col in range(3):
        moves = set(row[col] for row in board)
        if len(moves) == 1:
            return board[0][col]

    # check diagonally
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return board[1][1]

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    empty_board_cells = Counter(chain.from_iterable(board))[None]
    game_winner = winner(board)

    if game_winner or empty_board_cells == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    cur_player = player(board)
    action = None
    v = None

    if cur_player == X:
        v = max_value(board, None)
    else:
        v = min_value(board, None)

    action = v[1]
    return action


def max_value(board, cur_action):
    if terminal(board):
        return (utility(board), cur_action)

    available_actions = actions(board)
    optimal_action = None
    v = float('-inf')

    for a in available_actions:
        if optimal_action == None:
            optimal_action = a

        new_board = result(board, a)
        opponent_min_value = min_value(new_board, a)
        if opponent_min_value[0] > v:
            v = opponent_min_value[0]
            optimal_action = a

    return (v, optimal_action)


def min_value(board, cur_action):
    if terminal(board):
        return (utility(board), cur_action)

    available_actions = actions(board)
    optimal_action = None
    v = float('inf')

    for a in available_actions:
        if optimal_action == None:
            optimal_action = a

        new_board = result(board, a)
        opponent_min_value = max_value(new_board, a)
        if opponent_min_value[0] < v:
            v = opponent_min_value[0]
            optimal_action = a

    return (v, optimal_action)
