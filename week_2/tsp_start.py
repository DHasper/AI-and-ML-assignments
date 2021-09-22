import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def orientation(p1, q1, p2):
    return (q1.y-p1.y) * (p2.x-q1.x) > (q1.x-p1.x) * (p2.y-q1.y);

def intersect(e1, e2):
    o1 = orientation(e1[0], e1[1], e2[0])
    o2 = orientation(e1[0], e1[1], e2[1])
    o3 = orientation(e2[0], e2[1], e1[0])
    o4 = orientation(e2[0], e2[1], e1[1])
    return o1 != o2 and o3 != o4

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def tour_nn(cities):
    # Return a tour (list of City tuples) found using the nearest neighbour strategy
    # Time complexity: O((n^2 + n) / 2)
    tour = []
    cities = list(cities)
    curr = cities[0]
    
    while len(cities) > 0:
        # Find nearest neighbouring city in list of remaining cities
        nn = min((distance(city, curr), city) for city in cities)[1]
        tour.append(nn)

        # Remove city so it can't be visited again.
        cities.remove(nn)
        curr = nn

    return tour

def two_opt(tour):
    tour = tour.copy()
    print(tour)

    for _ in range(len(tour)-3):
        # Remove city from tour so it will not be considered again
        edge1 = (tour[0], tour[1])
        tour.pop(0)

        for i in range(len(tour)-2):
            # Check if intersect
            # Switch edge1[0] and edge2[0]
            edge2 = (tour[i+1], tour[i+2])
            print(edge1, edge2)
            if intersect(edge1, edge2):
                print('intersect!')

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(0) # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.clf()
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    two_opt(tour)
    # two_opt(tour)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# give a demo with 10 cities using brute force
# plot_tsp(try_all_tours, make_cities(10))
plot_tsp(tour_nn, make_cities(10))
# two_opt(list(range(10)))
# print(intersect((City(750,250), City(250,750)), (City(250,250), City(750,750))))

plt.show()
