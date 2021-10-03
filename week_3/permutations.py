import itertools

cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']

permutations = []
for permutation in itertools.permutations(cards):
    if permutation in permutations:
        print(permutation)
        permutations.append(permutation)

print(len(permutations))