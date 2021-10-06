'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
import copy
import itertools
from tkinter.constants import FALSE

# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbours = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    for i in range(len(board)):
        card = board[i]
        neighbour_cards = [board[card] for card in neighbours[i]]
        if card == 'A' and 'K' not in neighbour_cards:
            return False
        if card == 'K' and 'Q' not in neighbour_cards:
            return False
        if card == 'Q' and 'J' not in neighbour_cards:
            return False
        if card == 'A' and 'Q' in neighbour_cards:
            return False
        if card in neighbour_cards:
            return False
    return True

def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('t ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3] 
    print('f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('t ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))

def solve(alg="DFS"):
    # Solves the card puzzle using DFS or brute-force strategies
    if alg == "DFS":
        print(solve_dfs(start_board, cards))
    else:
        print(brute_force())

def brute_force():
    # Solves using a brute-force strategy

    permutation_counter = 0

    # Test all permutations
    for board in itertools.permutations(cards):
        # Increment counter
        permutation_counter += 1

        # Convert the board to a dict with board index as key and card as value
        board_dict = dict(zip(range(len(board)), board))
        if is_valid(board_dict):
            # Return solution if board permutation is a valid solution
            return board_dict, permutation_counter

permutation_counter = 0

def solve_dfs(board, cards):
    # Solves using a DFS strategy

    global permutation_counter

    # If board is full check if the board is a valid solution
    if not any(c == '.' for c in board.values()):
        if is_valid(board):
            # print((board, permutation_counter))
            return (board, permutation_counter)

        # This is not a solution, backtrack
        return False
    
    # Choose a board position. If empty 0 and 5 go first to optimize pruning
    if board[0] == '.': empty_position = 0
    elif board[5] == '.': empty_position = 5
    else: empty_position = list(board.values()).index('.')

    # Get non duplicate cards to avoid unneccesary checking
    non_duplicates = []
    for card in cards:
        if card not in non_duplicates:
            non_duplicates.append(card)

    # Check all possible cards
    for c in non_duplicates:
        permutation_counter += 1

        # Set card on the board
        board[empty_position] = c

        # Remove card from available cards
        cards.remove(c)
        
        # Continue solving
        if solve_dfs(board, cards):
            return (board, permutation_counter)

        # If this is not the solution reset to original state
        board[empty_position] = '.'
        cards.append(c)

    return False

solve("BRUTE_FORCE")
solve("DFS")

# a) 1. Hoeveel verchillende permutaties zijn er?
#           8! = 40320, of
#           8! / (2! * 2! * 2! * 2!) = 2510
#           Afhankelijk van of kaarten van hetzelfde type gerekend word als een identiek element.
#    2. Er zijn 997 iteraties nodig om de eerste oplossing te vinden.
#
# b) Na het toepassen van DFS zijn er nog maar 52 iteraties nodig om een oplossing te vinden.