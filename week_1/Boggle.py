import random
import string

words = []
board = []
boardSize = 4
found_words = []

with open('words_NL.txt', 'r') as file:
    for line in file:
        for word in line.split():
           words.append(word)

for i in range(boardSize):
   row = []
   for r in range(boardSize):
      row.append(random.choice(string.ascii_lowercase))
   board.append(row)

def format_row(row):
   return '|' + '|'.join('{0:^3s}'.format(x) for x in row) + '|'

def format_board(board):
   return '\n\n'.join(format_row(row) for row in board)

def word_valid(new_word):
   for word in words:
      if(new_word in word):
         return True
   return False

def word_not_found(new_word):
   for word in found_words:
      if(word == new_word):
         return False
   return True

def word_exists(new_word):
   for word in words:
      if((word == new_word) and word_not_found(new_word)):
         return True
   return False

def neighbour_valid(x, y, word):
   if(x == boardSize):
      x = 0
   elif(x == -1):
      x = boardSize - 1
   elif(y == boardSize):
      y = 0
   elif(y == -1):
      y = boardSize - 1

   if not (word_valid(word + board[x][y])):
      if (word_exists(word)):
         found_words.append(word)
         print(word)
      return False
   word += board[x][y]
   find_words(x, y, word)

def find_words(x, y, word):
   neighbour_valid(x - 1, y, word)
   neighbour_valid(x + 1, y, word)
   neighbour_valid(x, y - 1, word)
   neighbour_valid(x, y + 1, word)

print(format_board(board))

for x in range(boardSize):
   for y in range(boardSize):
      find_words(x, y, board[x][y])

# Timecomplexity: O(b^D)

# b = 16 bij boardsize 4 want boardSize x boardSize = 4 x 4 = 16
# D = 25 want het langste woord is 25 characters lang 

# 16^25 = 1.267.650.600.228.229.401.496.703.205.376