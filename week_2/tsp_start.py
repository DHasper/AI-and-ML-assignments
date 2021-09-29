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
    # Improve a tour by removing all intersections using a 2-opt approach
    # Time complexity: O(n^3)

    tour = tour.copy()

    intersect_remaining = True
    no_intersect_count = 0
    counter = 0
    while intersect_remaining:
        # Use iteration counter as a pointer to the first position of edge 1
        counter += 1
        p1 = counter % (len(tour)-2)

        # If there are no intersections remaining the algorithm is finished
        if no_intersect_count > len(tour):
            intersect_remaining = False

        intersect_found = False
        for p2 in range(p1+2, len(tour)):
            edge1 = (tour[p1], tour[p1+1])

            # q2 can be 0 to include the last edge which has the origin/first position in
            #  the tour list.
            if p2 == len(tour)-1:
                if p1 != 0:
                    q2 = 0
                else: continue
            else:
                q2 = p2 + 1

            edge2 = (tour[p2], tour[q2])

            if intersect(edge1, edge2):
                # If intersection is found, switch the edges. All the nodes inbetween have
                #  to be reversed
                tour[p1+1:p2+1] = tour[p1+1:p2+1][::-1]
                intersect_found = True
        
        # Keep track of iterations since a intersection has been encountered
        if not intersect_found: no_intersect_count += 1
        else: no_intersect_count = 0
    
    return tour

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.clf()
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    tl = tour_length(tour)
    tour = two_opt(tour)
    t1 = time.process_time()
    print('nn: {:.1f}'.format(tl))
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

def test(n):
    deltas = []
    count = 0

    for _ in range(100):
        cities = make_cities(n)
        t0 = time.process_time()
        tour = tour_nn(cities)
        t1 = time.process_time()
        l1 = tour_length(tour)
        print("\n{} city tour with length {:.1f} in {:.3f} secs for using nearest neighbour"
            .format(len(tour), l1, t1 - t0))
        
        t0 = time.process_time()
        tour = try_all_tours(cities)
        t1 = time.process_time()
        l2 = tour_length(tour)
        print("length {:.1f} in {:.3f} secs after optimising tour with 2-opt"
            .format(l2, t1-t0))

        delta = (l2 - l1) / l1 * 100
        print('2-opt difference with normal nn: {:.1f}'.format(delta))

        deltas.append(delta)
        count += 1
        print('Average delta: {:.1f}'.format(sum(deltas) / count))

# give a demo with 10 cities using brute force
# plot_tsp(try_all_tours, make_cities(10))
# plot_tsp(tour_nn, make_cities(50))
test(5)

# a) Hoeveel procent ligt het resultaat van NN af van de optimale route? Uit onze tests blijkt dat bij 10 steden het verschil
#     ongeveer 10% is gemiddeld.
# 



