import random
import heapq
import math
import config as cf
import numpy as np

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, id(item), item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[2]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def euclidean_distance(n1, n2):
    """Calculates the euclidian distance between two points using 
       the pythagorean theorem: d(p,q) = sqrt((q1 - p1)^2 + (q2 - p2)^2)
    """
    return math.sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)

def search(app, start, goal):
    total_explored = 0
    total_cost = 0
    alg = app.alg.get()

    start_node = Node(start, goal, alg)
    start_node.total_cost = 0

    # Init grid of nodes
    nodes = np.array([Node((x, y), goal, alg) for x in range(cf.SIZE) for y in range(cf.SIZE)])
    nodes.resize(cf.SIZE, cf.SIZE)

    # Make priority queue with the start node
    queue = PriorityQueue()
    queue.put(start_node, start_node.heuristic)

    # Loop until the goal is the highest priority item in the queue
    while not queue.empty():
        # Pop the queue to get the starting node
        node = queue.get()

        # Reached ending criterion, backtrack to display the results
        if node.x == goal[0] and node.y == goal[1]:
            print('Found a solution!')
            total_cost = node.total_cost
            while node.prev_node != None:
                app.plot_line_segment(node.x, node.y, node.prev_node.x, node.prev_node.y, color=cf.FINAL_C)
                node = node.prev_node
                app.pause()
            break

        # Visit all adjacent nodes
        for adjacent in node.find_adjacent(nodes):
            app.plot_line_segment(node.x, node.y, adjacent.x, adjacent.y, color=cf.PATH_C)
            app.plot_node((adjacent.x, adjacent.y), color=cf.PATH_C)
            total_explored += 1

            # Calculate the total cost to get to this node from start. If the total cost is lower then previously known,
            #  update the score, and put this node in the queue.
            cost = node.total_cost + adjacent.cost
            if cost < adjacent.total_cost:
                adjacent.total_cost = cost
                # If this node is already in the queue, remove it so we can change the priority
                for element in queue.elements:
                    if element[2].x == adjacent.x and element[2].y == adjacent.y:
                        queue.elements.remove(element)

                queue.put(adjacent, cost + adjacent.heuristic)
                adjacent.prev_node = node

        app.pause()

    print('Total explored nodes: ', total_explored)
    print('Total cost to reach goal: ', total_cost)

class Node():
    def __init__(self, node, goal, alg):
        self.x, self.y = node
        self.state = get_grid_value(node)
        self.cost = 1
        self.total_cost = float('inf')
        self.prev_node = None
        self.heuristic = euclidean_distance(node, goal)*2 if alg == 'A*' else 0

    def find_adjacent(self, nodes):
        """Returns all adjacent nodes for node n in a 2d grid of nodes"""

        adjacent = []
        for x in range(-1,2):
            for y in range(-1, 2):
                if abs(x) ^ abs(y) and self.x + x >= 0 and self.x + x < cf.SIZE and self.y + y >= 0 and self.y + y < cf.SIZE:
                    adjacent_node = nodes[self.x + x][self.y + y]
                    if adjacent_node.state != 'b': adjacent.append(adjacent_node)

        return adjacent