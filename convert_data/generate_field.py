import random
from common import is_correct_cell


def possible_direction(ship_length, allowed_cells, start_cell):
    """
    ship_length > 1 !!!!!
    """
    possible_directions = set((0, 1), (0, -1), (1, 0), (-1, 0))
    result = []
    for current_direction in possible_directions:
        is_ok = True
        for i in range(1, ship_length):
            current_cell = (start_cell[0] + current_direction[0] * i, start_cell[1] + current_direction[1] * i)
            if not is_correct_cell(current_cell) or current_cell not in allowed_cells:
                is_ok = False
                break
        if is_ok:
            result.append(current_direction)
    if len(result) == 0:
        return None
    return result


def write_ship(allowed_cells, battlefield, start_cell, ship_length, direction = None):
    pass

def generate_field():
    """
    якщо довжина корабля 1 то не тре possible_direction
    """
    allowed_cells = set()
    ship_rules = {4: 1, 3: 2, 2: 3, 1: 4}
    current_battlefield = {}
    # allowed_guess = set()
    for i in range(1, 11):
        for j in range(1, 11):
            allowed_cells.add((i, j))
            current_battlefield[(i, j)] = None
    for ship_length in range(4, 1, -1):
        allowed_guess = allowed_cells.copy()
        for i in ship_rules[ship_length]:
            while allowed_guess:
                random_cell = random.choice(allowed_guess)
                current_result = possible_direction(ship_length, allowed_cells, random_cell)
                if current_result is None:
                    allowed_guess.remove(random_cell)
                else:
                    write_ship(allowed_cells, current_battlefield, random_cell, ship_length, random.choice(current_result))
                    # TODO redefine all variables
                    break
    for i in range(4):
        write_ship(allowed_cells, current_battlefield, random.choice(allowed_cells), 1)
        # TODO redefine variables
    return current_battlefield