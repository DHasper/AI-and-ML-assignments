import random
import itertools
import math
import copy
import numpy as np

MAX_DEPTH = 4

# WEIGHT_MAP = [
#     [15/16, 14/16, 13/16, 12/16],
#     [8/16, 9/16, 10/16, 11/16],
#     [7/16, 6/16, 5/16, 4/16],
#     [0/16, 1/16, 2/16, 3/16],
# ]

WEIGHT_MAP = [
    [32768, 16384, 8192, 4096],
    [2048, 1024, 512, 256],
    [128, 64, 32, 16],
    [8, 4, 2, 1],
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
    # a = input()
    return b

def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
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
    return expectimax(b, MAX_DEPTH)['action']

def adjacent_nodes(b, row, col):
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
    # functie: get_adjacent
    # For node in adjacent:
    #    if node.score == adjacent.score / 2 or * 2:
    #       node.score *= adjacent_weight
    if game_state(b) == 'win': return float('inf')

    n_empty = 0
    smoothness_board = copy.deepcopy(b)
    for row in range(len(b)):
        for col in range(len(b[row])):
            value = b[row][col]
            if value == 0:
                n_empty += 1
            else:
                smoothness = 0
                n_neighbours = 0
                for adjacent in adjacent_nodes(b, row, col):
                    if adjacent != 0:
                        if adjacent == value:
                            smoothness += value
                        else:
                            smoothness += abs(value - adjacent)
                            n_neighbours += 1
                if n_neighbours != 0:
                    smoothness_board[row][col] = smoothness / n_neighbours
                else:
                    smoothness_board[row][col] = 0

    weighted_board = np.multiply(b, WEIGHT_MAP)
    weighted_board = np.multiply(weighted_board, smoothness_board)

    weighted_score = np.sum(weighted_board)
    smoothness_score = np.sum(smoothness_board)
    empty_score = n_empty * np.max(weighted_board)

    # print(n_empty * np.max(weighted_board)/3, weighted_sum)
    # return np.sum(b) * weighted_score * smoothness_score * empty_score
    return np.sum(b) * weighted_score

def expectimax(b, depth, player="MAX"):
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
        # print(max_score)
        return {'score': max_score, 'action': best_action}
    # Average player
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

        # print(value * 1 / n_empty)
        if n_empty == 0: return {'score': expectimax(b, depth-1, "MAX")['score']}
        return {'score': (value * 1 / n_empty)}
