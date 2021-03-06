import time
import copy

#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I

def cross(A, B):
    # concat of chars in string A and chars in string B
    return [a+b for a in A for b in B]

digits = '123456789'
rows   = 'ABCDEFGHI'
cols   = digits
cells  = cross(rows, cols) # 81 cells A1..9, B1..9, C1..9, ... 

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +                             # 9 rows 
             [cross(rows, c) for c in cols] +                             # 9 cols
             [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) # 9 units


units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in cells)

def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print ('All tests pass.')

def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    domains = []
    for r in rows:
        for c in cols:
            v = grid[r+c]
            # avoid the '123456789'
            if len(v) != 1: 
                domains.append(v)
                v = '.'

            print (''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F': 
            print('-------------------')
    print()
    # print(domains)

def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))

def no_conflict(grid, c, val):
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == val:
           return False # conflict
    return True

def candidates(grid, c):
    # Returns list with all candidate values for cell c in grid
    peer_values = [grid[p] for p in peers[c] if grid[p] != digits]
    return [d for d in digits if d not in peer_values]

def make_arc_consistent(grid, c, v):
    grid_changed = False

    for peer in peers[c]:
        peer_value = grid[peer]
        if v in peer_value:
            if len(peer_value) <= 1:
                # Not a solution, backtrack
                return False
            else:
                # Remove v from all peers of c
                grid[peer] = peer_value.replace(v, '')
                grid_changed = True

    if grid_changed:
        # Get all cells where n values is 1 and is not c
        c2_list = [c2 for c2 in cells if len(grid[c2]) == 1 and c2 != c]
        # Get values of c2_list
        v2_list = [grid[c2] for c2 in c2_list]

        # Recursive call, if False is returned this is not a solution
        if any(not make_arc_consistent(grid, c2, v2) for c2, v2 in zip(c2_list, v2_list)):
            return False

    return True

def solve_arc(grid):
    # Backtracking search for a solution (DFS) with variable ordering and arc consistency

    # Check if all cells have exactly one value
    if not any(len(grid[c]) != 1 for c in cells):
        print('Found a solution:')
        display(grid)
        return True

    # Get all cells with n values > 1
    cell_list = [c for c in cells if len(grid[c]) > 1]

    # Choose variable with smallest domain
    var = min(cell_list, key = lambda c: len(grid[c]))
    
    for candidate in grid[var]:
        # Check if value is valid within sudoku constraints
        if no_conflict(grid, var, candidate):
            # Copy grid and make change on copy
            new_grid = copy.deepcopy(grid)
            new_grid[var] = candidate

            # Make arcs consistent
            if make_arc_consistent(new_grid, var, candidate):
                # Continue solving with arc consistent grid
                if solve_arc(new_grid):
                    return True
           
    return False

def solve(grid):
    # Backtracking search for a solution (DFS) with variable ordering and domain consistency

    if not any(grid[c] == digits for c in cells):
        print('Found a solution:')
        display(grid)
        return True

    # Get dict with key = cell and value = valid candidates for cell
    candidates_dict = {c: candidates(grid, c) for c in cells if grid[c] == digits}
    # Choose cell with lowest amount of candidates
    var = min(candidates_dict.items(), key = lambda c: len(c[1]))[0]

    # Check every possible value
    for val in grid[var]:
        # Check if value is valid within constraints
        if no_conflict(grid, var, val):
            grid[var] = val

            if solve(grid):
                return True

            # This is not the solution, undo change
            grid[var] = digits

    return False

# minimum nr of clues for a unique solution is 17
slist = [None for _ in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10]= '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11]= '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12]= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13]= '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14]= '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15]= '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16]= '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17]= '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18]= '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19]= '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'

for i, sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))
    print(sudo)
    d = parse_string_to_dict(sudo)
    start_time = time.time()
    # solve(d)
    solve_arc(d)
    end_time = time.time()
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours),int(minutes),seconds))
    print()
