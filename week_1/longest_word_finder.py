longestWordLength = 0
longestWord = ""

with open('words_NL.txt','r') as file:
    for line in file:
        for word in line.split():
           if (len(word) > longestWordLength):
            longestWordLength = len(word)
            longestWord = word

print(longestWordLength)
print(longestWord)