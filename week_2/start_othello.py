"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""
import copy
import random

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)


def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board


def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep


# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.


def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()


def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE


def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)


def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


# Monitoring players


# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player],
                                                self.move)


def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]


def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())


# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.


def gameover(board):
    return not any_legal_move(BLACK, board) and not any_legal_move(
        WHITE, board)


def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score
    board = initial_board()
    player = BLACK
    while not gameover(board):
        print(print_board(board))
        if legal_moves(player, board):
            move = black_strategy(
                board, player) if player == BLACK else white_strategy(
                    board, player)
            print(move, player)
            make_move(move, player, board)
        player = opponent(player)
    print("winner is: ",get_winner(board))

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    pass

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    pass

def evaluate(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    score = 0
    for piece in board:
        if (piece == player):
            score += 1
    return score

def get_winner(board):
    # compute player's score (number of player's pieces minus opponent's)
    black_score = 0
    white_score = 0
    for piece in board:
        if (piece == BLACK): black_score += 1 
        if (piece == WHITE): white_score += 1 
    return BLACK if black_score > white_score else WHITE

def get_random_move(board, player):
    moves = legal_moves(player, board)
    return random.choice(moves)


def get_minimax_move(board, player):
    return minimax(board, 1, player)['action']


def minimax(board, depth, player):
    #print(depth,len(legal_moves(player, board)))
    if depth == 0 or len(legal_moves(player, board)) == 0:
        return {
            'score':
            evaluate(player, board) - evaluate(opponent(player), board),
            'action': 0
        }

    moves = legal_moves(player, board)
    if player == BLACK:
        max_score = {'score': -float("inf"), 'action': 0}
        for i in range(len(moves)):
            score = minimax(make_move(moves[i], player, copy.deepcopy(board)),
                            depth - 1, WHITE)
            if score['score'] >= max_score['score']:
                max_score = score
                max_score['action'] = moves[i]
        return max_score
    else:  #player == WHITE
        min_score = {'score': float("inf"), 'action': 0}
        for i in range(len(moves)):
            score = minimax(make_move(moves[i], player, copy.deepcopy(board)),
                            depth - 1, WHITE)
            if score['score'] <= min_score['score']:
                min_score = score
                min_score['action'] = moves[i]
        return min_score

        #else:  #player == WHITE
        # for child in node.children:
        #     value = min(value, minimax(child, depth - 1, BLACK))
        # return value


#initial call
play(get_minimax_move, get_random_move)

# print(minimax(board, 4, BLACK))

# board = initial_board()

# print(print_board(board))
# make_move(65, BLACK, board)
# print(print_board(board))

# print(legal_moves(BLACK, board))

# make_move(34, BLACK, board)

# print(print_board(board))

# print(score(BLACK, board))

# def max(value, compare_value):
#     return value if value >= compare_value else compare_value

# def min(value, compare_value):
#     return value if value <= compare_value else compare_value

# def max(value, moves):
#     max_value, move, best_move = 0,0,0
#     for m in value:
#         move += 1
#         if (m >= max_value):
#             max_value = m
#             best_move = move
#     return max_value, moves[best_move]

# def min(value, moves):
#     min_value, move, best_move = 0,0,0
#     for m in value:
#         print(m)
#         move += 1
#         if (m <= min_value):
#             min_value = m
#             best_move = move
#     return min_value, moves[best_move]