import random
from common import is_correct_cell


def possible_direction(ship_length, allowed_cells, start_cell):
    """
    int, set(tuple(int, int)), tuple(int, int) -> list(tuple(int, int))

    returns list of all possible directions in which ship with length
    ship_length can be placed

    allowed cells is a set of cells which can be used

    if we cannot build the ship in any direction, returns None

    structure of directions:
        1) (0, 1) - to the right
        2) (0, -1) - to the left
        3) (1, 0) - to the bottom
        4) (-1, 0) - to the top
    """
    possible_directions = set([(0, 1), (0, -1), (1, 0), (-1, 0)])
    result = []
    for current_direction in possible_directions:
        is_ok = True
        for i in range(1, ship_length):
            current_cell = (start_cell[0] + current_direction[0] * i,
                            start_cell[1] + current_direction[1] * i)
            if (not is_correct_cell(current_cell) or
                    current_cell not in allowed_cells):
                is_ok = False
                break
        if is_ok:
            result.append(current_direction)
    if len(result) == 0:
        return None
    return result


def write_ship(allowed_cells,
               current_battlefield,
               start_cell,
               ship_length,
               direction=(0, 0)):
    """
    set(tuple(int, int)),
    dict(tuple(int, int): None or bool),
    tuple(int, int), int,
    tuple(int, int) -> None

    updates allowed cells and current_battlefield writing
    a ship with length ship_length
    from start_cell in direction direction

    read more about direction in possible_direction() documentation
    read more about current_battlefield in generate_field() documentation
    """
    for i in range(ship_length):
        current_cell = (start_cell[0] + i * direction[0],
                        start_cell[1] + i * direction[1])
        current_battlefield[current_cell] = False
    end_cell = (start_cell[0] + (ship_length - 1) * direction[0],
                start_cell[1] + (ship_length - 1) * direction[1])
    delete_start_cell = (min(start_cell[0], end_cell[0]) - 1,
                         min(start_cell[1], end_cell[1]) - 1)
    delete_end_cell = (max(start_cell[0], end_cell[0]) + 1,
                       max(start_cell[1], end_cell[1]) + 1)
    for row in range(delete_start_cell[0], delete_end_cell[0] + 1):
        for col in range(delete_start_cell[1], delete_end_cell[1] + 1):
            if (row, col) in allowed_cells:
                allowed_cells.remove((row, col))


def generate_field():
    """
    () -> dict(tuple(int, int): None or bool)

    generates random battlefield and returns it
    it is guaranteed that the placement of all the ships is according
    to all the rules in battleship game

    dictionary structure:
        - the key is (int, int) - number of row and column respectively
        - numbers in key are in [1; 10] inclusive
        - the value can be:
            1) None - there is nothing in that cell
            2) False - there is undamaged ship in that cell
            3) True - there is damaged ship in that cell
    """
    allowed_cells = set()
    ship_rules = {4: 1, 3: 2, 2: 3, 1: 4}
    current_battlefield = {}
    for i in range(1, 11):
        for j in range(1, 11):
            allowed_cells.add((i, j))
            current_battlefield[(i, j)] = None
    for ship_length in range(4, 1, -1):
        allowed_guess = allowed_cells.copy()
        for i in range(ship_rules[ship_length]):
            while allowed_guess:
                random_cell = random.sample(allowed_guess, 1)[0]
                current_result = possible_direction(ship_length,
                                                    allowed_cells,
                                                    random_cell)
                if current_result is None:
                    allowed_guess.remove(random_cell)
                else:
                    write_ship(allowed_cells,
                               current_battlefield,
                               random_cell,
                               ship_length,
                               random.choice(current_result))
                    allowed_guess = allowed_cells.copy()\
                        .intersection(allowed_guess)
                    break
    for i in range(4):
        write_ship(allowed_cells,
                   current_battlefield,
                   random.sample(allowed_cells, 1)[0],
                   1)
    return current_battlefield
