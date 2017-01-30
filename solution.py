assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return[s+t for s in A for t in B]

boxes = cross(rows,cols)
row_units = [cross(r,cols) for r in rows]
column_units = [cross(rows,c) for c in cols]
square_units = [cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

units = dict((s,[u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def str_intersection(str1, str2):
    for i in str1:
        str3=''
        str3 = str3.join(i for i in str1 if i in str2 not in str3)
    return(str3)


def hidden_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the hidden twins eliminated from peers.
    """

    print("Hidden twins")
    # find candidates for naked twin units but check occurs further down to find the twins
    display(values)
    for box in values.keys():
        hidden_twins = []     #Initialize hidden twins list
        hidden_values = []    # Initialize hidden twin values
        if len(values[box]) == 1 :
            continue # return to box loop and set new box
        else :  # Unsolved box
            for unit in units[box]:    # 1 of 3 unitlists
                for peer in set(unit).intersection(set(peers[box])):
                    # Set hidden value with peer FIRST if >=2 common digits, every peer is a candidate to avoid missing
                    # common hidden values by skipping any one peer check with box
                       hidden_twins = []  # Initialize hidden twins list before moving onto next peer
                       hidden_values = []  # Initialize hidden twin values before moving onto next peer
                       hidden_twins.append(box)
                       if len(str_intersection(values[peer], values[box])) >= 2:
                          hidden_values = str_intersection(values[peer], values[box])
                          # for 2 or greater common values initialize hidden values
                          hidden_twins.append(peer)
                          # Add the first peer you found for the common hidden value, now check with all other peers!
                          if len(hidden_values) == 2: #use these values to check other peers
                                                      # for repeats
                             #continue checking with all peers again to discount single digit commonalities ignored
                             # earlier to disqualify twins
                             for digit in hidden_values:
                                  for other_peer in set(unit).intersection(set(peers[box])) - set(hidden_twins):
                                      if digit in values[other_peer]:   # Found in other peer, not a hidden twin, exit
                                                                        # to next unit check
                                         hidden_twins.append(other_peer)
                                         hidden_values = []  # Obsolete these values
                                         # Discount the 2 common digits found with all peers
                                         break
                                  if len(hidden_twins) > 2:
                                      break #break out of this loop, go to next peer to set hidden_values
                          else: # More than 2 common digits, need to reduce to 2 if possible by checking other peers
                                # in unit for repeats
                              for digit in hidden_values:
                                  for other_peer in set(unit).intersection(set(peers[box])) - set(hidden_twins):
                                      if digit in values[other_peer]:   #This common digit will be disqualified with its
                                                                        # check in peers, too many peers
                                         if digit in hidden_values:
                                            hidden_values = hidden_values.replace(digit,'')
                                            # continue to check all the hidden value digits against other peers
                              if len(hidden_values) == 2:  # Now again use these values to check other peers
                                                           # for repeats
                                                           # continue checking with all peers again to discount single
                                                           # digit commonalities ignored earlier to disqualify twins
                                 for digit in hidden_values:
                                     for other_peer in set(unit).intersection(set(peers[box])) - set(hidden_twins):
                                         if digit in values[other_peer]:  # Found in other peer, not a hidden twin, exit
                                                                          # to next unit check
                                            hidden_twins.append(other_peer)
                                            # Discount the 2 common digits found with all peers
                                            hidden_values = [] #Obsolete these values
                                            break
                                 if len(hidden_twins) > 2:
                                    break  # break out of this loop, go to next peer to set hidden_values
                       #possible hidden twin found but need to continue checking peers twin peer of candidate identified
                       # exactly, set candidate digits for elimination in other peers
                       if len(hidden_values) == 2: # hidden_twins found, eliminate digits that are not the hidden twins'
                          for item in hidden_twins:
                              for digit in values[item] :
                                  if not digit in hidden_values:
                                     values = assign_value(values, item, values[item].replace(digit, ''))
                       else:
                          hidden_values = []
                          hidden_twins = []
                          #No hidden twins found for candidate with this peer
            # Loop for remaining units till all hidden twins are found
        # Loop for remaining boxes till all hidden twins are found
    display(values)
    return(values)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # find candidates for naked twin units but check occurs further down to find the twins
    print("Naked twins")
    display(values)
    for box in values.keys():
        if len(values[box]) == 2:
           # set a possible naked twins candidate, but still need to find a twin if available!
           naked_twin_cand = box
           for unit in units[naked_twin_cand]:
               for peer in set(unit).intersection(set(peers[naked_twin_cand])):
                   # check all units with this candidate for peers not including the candidate
                   if not set(values[peer]).difference(set(values[naked_twin_cand])):
                      # twin peer of candidate identified exactly, set candidate digits for elimination in other peers
                       digit0 = values[naked_twin_cand][0]
                       digit1 = values[naked_twin_cand][1]
                       for other_peer in set(unit).difference(set([naked_twin_cand,peer])):
                           # for all other peers, eliminate these two digits if found
                           if digit0 in values[other_peer]:
                              values = assign_value(values, other_peer, values[other_peer].replace(digit0, ''))
                              # similarly check digit1
                           if digit1 in values[other_peer]:
                              values = assign_value(values, other_peer, values[other_peer].replace(digit1, ''))
         # Loop for remaining candidates with two possibilities till all naked twins are found
    return(values)

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'

    for c in grid:
        if c == '.':
           values.append(all_digits)
        elif c in all_digits:
           values.append(c)
    assert len(values) == 81
    return dict(zip(boxes,values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print('.'.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    return

# Add declarations here for diagonal units
# Add diagonal units required for diagonal sudoku solution
diagonal_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows[::-1],cols)]]
unitlist = row_units + column_units + square_units + diagonal_units

def eliminate(values):
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        solved_digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(solved_digit,''))
    return(values)

def only_choice(values):
    new_values = values.copy()  # Original values not to be modified in this function
    for unit in unitlist:
        for digit in '123456789':
            repetition_list = [box for box in unit if digit in values[box]]
            if len(repetition_list) == 1:
                new_values = assign_value(new_values, repetition_list[0], digit)
    return(new_values)

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        #Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        #Eliminate choice strategy
        values = eliminate(values)

        # use only choice strategy
        values = only_choice(values)

        #Check now how many boxes are solved
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        #if nothing new found, update stalled to check
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
        # failed Sudoku because of box with no digit possibility
            return False
            # sanity check
    return values


def search(values):
    # Using depth first search and propogation, create a search tree and solve the Sudoku
    # First reduce the puzzle
    #unitlist = row_units + column_units + square_units + diagonal_units
    values = reduce_puzzle(values)
    if values is False:
        return False # Search failed with unfillable box
    if all(len(values[s]) == 1 for s in boxes):
        # display(values)
        return values ## Solved!
        # Sudoku puzzle solved without DFS required
    # Choose unfilled square with fewest possibilities
    unfill_best_ch, s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)

    for option in values[s]:
        new_sudoku = values.copy()
        # Reproduce current sudoku
        new_sudoku[s] = option
        # Try each option in the selected values
        result = search(new_sudoku)
        if result:
            return result
            # Success!
            # Otherwise for loop sets other option in values[s] selected and retrieves recursive search
            # in new_sudoku for new option
    #DFS success

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return(search(grid_values(grid)))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # Add diagonal units as additional check, set these units in a list
    #unitlist = row_units + column_units + square_units + diagonal_units
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
