import random
import string

words = []
board = []
boardSize = 4
with open('words_NL.txt','r') as file:
    for line in file:
        for word in line.split():
           words.append(word)

for i in range(boardSize):
   row = []
   for r in range(boardSize):
      row.append(random.choice(string.ascii_lowercase))
   board.append(row)

def FormatRow(row):
   return '|' + '|'.join('{0:^3s}'.format(x) for x in row) + '|'

def FormatBoard(board):
   return '\n\n'.join(FormatRow(row) for row in board)

print(FormatBoard(board))
foundWords = []

def wordIsValid(newWord):
   for word in words:
      if(newWord in word):
         return True
   return False

def wordNotFound(newWord):
   for word in foundWords:
      if(word == newWord):
         return False
   return True

def wordExists(newWord):
   for word in words:
      if((word == newWord) and wordNotFound(newWord)):
         return True
   return False

def NeighbourIsValid(x,y,word):
   if(x == boardSize):
      x = 0
   if(x == -1):
      x = boardSize - 1
   if(y == boardSize):
      y = 0
   if(y == -1):
      y = boardSize - 1
   if not (wordIsValid(word + board[x][y])):
      if (wordExists(word)):
         foundWords.append(word)
         print(word)
      return False
   word += board[x][y]
   NeighboursValidCharacter(x,y,word)

def NeighboursValidCharacter(x,y,word):
   NeighbourIsValid(x - 1,y,word)
   NeighbourIsValid(x + 1,y,word)
   NeighbourIsValid(x,y - 1,word)
   NeighbourIsValid(x,y + 1,word)

for x in range(boardSize):
   for y in range(boardSize):
      NeighboursValidCharacter(x,y,board[x][y])

# Timecomplexity: O(b^D)

# b = 16 bij boardsize 4 want boardSize x boardSize = 4 x 4 = 16
# D = 25 want het langste woord is 25 characters lang 

# 16^25 = 1.267.650.600.228.229.401.496.703.205.376