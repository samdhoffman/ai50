import pytest
import tictactoe as ttt

X = ttt.X
O = ttt.O
EMPTY = ttt.EMPTY

empty_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def test_player_returns_X_when_board_empty():
    cur_player = ttt.player(empty_board)
    assert cur_player == X


def test_player_returns_X():
    board = [[X, O, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    cur_player = ttt.player(board)
    assert cur_player == X


def test_player_returns_O():
    board = [[X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    cur_player = ttt.player(board)
    assert cur_player == O


def test_actions_when_board_empty():
    actions = ttt.actions(empty_board)
    assert len(actions) == 9


def test_result_with_invalid_action():
    invalid_action = (-1, -1)
    msg = f'{invalid_action} is not a valid action'

    with pytest.raises(Exception) as excinfo:
        ttt.result(empty_board, invalid_action)
        assert excinfo.value == msg


def test_result():
    action_1 = (0, 0)
    action_2 = (0, 1)

    new_board_1 = ttt.result(empty_board, action_1)
    assert new_board_1[0][0] == X

    new_board_2 = ttt.result(new_board_1, action_2)
    assert new_board_2[0][1] == O

    with pytest.raises(Exception) as excinfo:
        ttt.result(new_board_1, (0, 0))
        assert excinfo.value == f'(0,0) is not a valid action'


def test_winner():
    board_x_wins_vertically = [
        [X, O, X],
        [X, O, X],
        [O, EMPTY, X]
    ]
    winner_vertically = ttt.winner(board_x_wins_vertically)
    assert winner_vertically == X

    board_x_wins_horizontally = [
        [X, O, EMPTY],
        [X, X, X],
        [O, EMPTY, EMPTY]
    ]
    winner_horizontally = ttt.winner(board_x_wins_horizontally)
    assert winner_horizontally == X

    board_x_wins_diagonally = [
        [X, O, EMPTY],
        [X, X, EMPTY],
        [O, EMPTY, X]
    ]
    winner_diagonally = ttt.winner(board_x_wins_diagonally)
    assert winner_diagonally == X

    # no winner
    assert ttt.winner(empty_board) is None


def test_terminal():
    assert ttt.terminal(empty_board) == False
 
    board_x_wins_diagonally = [
        [X, O, EMPTY],
        [X, X, EMPTY],
        [O, EMPTY, X]
    ]
    assert ttt.terminal(board_x_wins_diagonally) == True

    full_board = [
        [X, O, X],
        [O, X, O],
        [O, X, O]
    ]
    assert ttt.terminal(full_board) == True


def test_utility():
    board_x_wins = [
        [X, O, EMPTY],
        [X, X, EMPTY],
        [O, EMPTY, X]
    ]
    assert ttt.utility(board_x_wins) == 1

    board_o_wins = [
        [O, O, EMPTY],
        [O, X, EMPTY],
        [O, EMPTY, X]
    ]
    assert ttt.utility(board_o_wins) == -1

    board_no_winner = [
        [X, O, X],
        [O, X, O],
        [O, X, O]
    ]
    assert ttt.utility(board_no_winner) == 0


def test_minimax():
    terminal_board = [
        [X, O, X],
        [O, X, O],
        [O, X, O]
    ]
    assert ttt.minimax(terminal_board) == None

    board_1 = [
        [EMPTY, X, O],
        [O, X, X],
        [X, EMPTY, O]
    ]

    assert ttt.minimax(board_1) == (2, 1)

    board_2 = [
        [EMPTY, X, O],
        [O, X, X],
        [EMPTY, EMPTY, O]
    ]

    assert ttt.minimax(board_2) == (2,1)
