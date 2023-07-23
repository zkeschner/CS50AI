"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
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
    if sum(x.count("X") for x in board) > sum(y.count("O") for y in board):
        return "O"
    else:
        return "X"
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                pass
            else:
                options.add((i, j))
    #   print(options)
    return options
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action in actions(board):
        (i, j) = action
        current_player = player(board)
        new_board = deepcopy(board)
        new_board[i][j] = current_player
        return new_board
    else:
         raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == X:
            return X
        elif board[i][0] == board[i][1] == board[i][2] == O:
            return O
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == X:
            return X
        elif board[0][i] == board[1][i] == board[2][i] == O:
            return O
    count1 = 0
    for i in range(3):
        if board[i][i] == "X":
            count1 += 1
    if count1 == 3:
        return "X"
    count1 = 0
    for i in range(3):
        if board[i][i] == "O":
            count1 += 1
    if count1 == 3:
        return "O"
    diag = 2
    count2 = 0
    for i in range(3):
        if board[i][diag] == "X":
            count2 += 1
            diag -= 1
    if count2 == 3:
        return "X"
    diag = 2 
    count2 = 0
    for i in range(3):
        if board[i][diag] == "O":
            count2 += 1
            diag -= 1
    if count2 == 3:
        return "O"
    return None

        



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == "X" or winner(board) == "O":
        return True
    if EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]:
        return True
    else:
        return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    if winner(board) == "O":
        return -1
    return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    '''
    X tries to maximize score, O minimize
    player 
    '''
    
    current = player(board)
    def max_val(state):
        count = 0
        v = -10000
        act_return = None
        if terminal(state):
            return utility(state), None
        act_list = actions(state)
        for action in act_list:
            #print(count)
            count += 1
            #print(state)
            checkmin, act = min_val(result(state, action))
            if checkmin > v:
                v = checkmin
                act_return = action
            if v == 1:
                return v, act_return
        return v, act_return
    def min_val(state):
        v = 1000
        if terminal(state):
            return utility(state), None
        act_list = actions(state)
        act_return = None
        for action in act_list:
            checkmax, act = max_val(result(state, action))
            if checkmax < v:
                v = checkmax
                act_return = action
                if v == -1:
                    return v, act_return
        return v, act_return
    if current == "X":
        return max_val(board)[1]
    else:
        return min_val(board)[1]
    raise NotImplementedError
