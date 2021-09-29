import random
import itertools
import math
import copy
import numpy as np

MAX_DEPTH = 3

WEIGHT_MAP = [
    [64/64, 60/64, 56/64, 52/64],
    [36/64, 40/64, 44/64, 48/64],
    [32/64, 28/64, 24/64, 20/64],
    [4/64, 8/64, 12/64, 16/64],
]

def merge_left(b):
    # merge the board left
    # this function is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left
        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accu
        if len(row) == 1:
            return acc + [x]
        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accu, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accu, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]

def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]

def merge_down(b):
    # merge the board downward
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]

# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                # if same value or an empty cell
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # check horizontally and vertically
    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b

def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b

def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    # random.seed(0)
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue
            
def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]
    assert (move_exists(b)) == True
    b = [[32, 64, 2, 16], [8, 32, 16, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (move_exists(b)) == False
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    for i in range(11):
        add_two_four(b)
        print(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def get_expectimax_move(b):
    move = expectimax(b, MAX_DEPTH)
    print(move)
    return move['action']

def adjacent_cells(b, row, col):
    # Function that returns all adjacent cells given cell(row, col) on board b
    nodes = []

    if row < len(b) - 1:
        nodes.append(b[row+1][col])
    if row > 0:
        nodes.append(b[row-1][col])
    if col > 0:
        nodes.append(b[row][col-1])
    if col < len(b[row]) - 1:
        nodes.append(b[row][col+1])

    return nodes

def evaluate(b):
    # Returns an evaluation of the board position
    # Largest tile highscore: 8192, MAX_DEPTH = 3

    weighted_board = np.multiply(b, WEIGHT_MAP)
    weighted_score = np.sum(weighted_board)

    return np.sum(b) * weighted_score

def evaluate_old(b):
    # Old algorithm to evaluate a board position.
    # Does not work as well as the new evaluate algorithm
    # Largest tile highscore: 2048, MAX_DEPTH = 3

    n_empty = 0
    smoothness_board = copy.deepcopy(b)
    for row in range(len(b)):
        for col in range(len(b[row])):
            value = b[row][col]

            if value == 0:
                # Count empty cells
                n_empty += 1
            else:
                for adjacent in adjacent_cells(b, row, col):
                    if adjacent == value or adjacent == value / 2 or adjacent == value * 2:
                        smoothness_board[row][col] = 1
                    else:
                        smoothness_board[row][col] = 0

    weighted_board = np.multiply(b, WEIGHT_MAP)
    smoothness_board = np.multiply(b, smoothness_board)

    # Calculate heuristic scores
    weighted_score = np.sum(weighted_board)
    smoothness_score = np.sum(smoothness_board)
    empty_score = n_empty * np.max(weighted_board)

    return weighted_score * smoothness_score * empty_score

def expectimax(b, depth, player="MAX"):
    # When node is terminal
    if depth == 0 or not move_exists(b):
        return {'score': evaluate(b)}

    # Maximizing player
    if player == "MAX":
        max_score = -1
        for action in MERGE_FUNCTIONS.keys():
            new_board = MERGE_FUNCTIONS[action](copy.deepcopy(b))
            score = expectimax(new_board, depth-1, "EXP")['score']
            if score > max_score:
                max_score, best_action = score, action

        return {'score': max_score, 'action': best_action}
    # Chance player
    else:
        n_empty = 0
        value = 0
        for row in range(len(b)):
            for col in range(len(b[row])):
                if b[row][col] == 0:
                    n_empty += 1

                    # 90% chance for a 2 to be placed
                    new_board = copy.deepcopy(b)
                    new_board[row][col] = 2
                    value += 0.9 * expectimax(b, depth-1, "MAX")['score']

                    # 10% chance for a 4 to be placed
                    new_board = copy.deepcopy(b)
                    new_board[row][col] = 4
                    value += 0.1 * expectimax(b, depth-1, "MAX")['score']

        if n_empty == 0: return {'score': expectimax(b, depth-1, "MAX")['score']}
        return {'score': (value * 1 / n_empty)}

# b) De maximale diepte waarbij de performance acceptabel is, is 5. De performance zou met de volgende manieren vebeterd kunnen worden:
#     - Het evaluatie/heuristic algoritme minder complex maken.
#     - Resultaten cachen zodat veel voorkomende situaties niet opnieuw berekend hoeven te worden.
#     - Multithreading toepassen.
#     - Een bitboard gebruiken om het spelbord te representeren. 
