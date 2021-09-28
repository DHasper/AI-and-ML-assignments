import copy

class Node:
    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state

    def game_over(self):
        if len(self.state[0]) == 0:
            return True, True

        cur, tar = self.find('F')
        if ('C' in self.state[tar] and 'G' in self.state[tar]) or ('G' in self.state[tar] and 'W' in self.state[tar]):
            return True, False
        
        return False, False

    def get_valid_moves(self):
        cur, tar = self.find('F')
        moves = self.state[cur]
        return moves

    def play(self, o):
        self.move(o)
        if o != 'F': self.move('F')

    def find(self, o):
        return [0, 1] if o in self.state[0] else [1, 0]

    def move(self, o):
        cur, tar = self.find(o)
        self.state[cur].remove(o)
        self.state[tar].append(o)

    def print_state(self):
        left = "".join(self.state[0])
        right = "".join(self.state[1])
        return left + "|" + right

    def print_history(self):
        string = self.print_state()
        node = self
        while node.parent is not None:
            node = node.parent
            string = node.print_state() + " -> " + string
        print(string)

    def equals(self, node):
        return all(elem in node.state[0] for elem in self.state[0]) and all(elem in node.state[1] for elem in self.state[1])

def dfs(node, visited, depth=0):
    game_over, won = node.game_over()
    
    if won:
        # This is a solution!
        node.print_history()
    elif not game_over and not any(node.equals(visited_node[0]) and depth > visited_node[1] for visited_node in visited):
        # Only keep searching if game is not over and we haven't visited this position yet
        visited.append((node, depth))
        # Explore all moves
        for move in node.get_valid_moves():
            # A deep copy of the state is necessary because list.copy() only copies outer list
            new_node = Node(copy.deepcopy(node.state), node)
            new_node.play(move)
            dfs(new_node, visited, depth+1)

if __name__ == '__main__':
    # Starting state: Farmer, Goat, Cabbage and Wolf on the left side. Right side is empty.
    node = Node([['F', 'G', 'C', 'W'], []])
    # Start searching for solutions
    dfs(node, [], 0)

# Time complexity: O(b^D)
# b = branching factor:  4
# D = max depth: 7