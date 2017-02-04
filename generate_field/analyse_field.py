from common import convert, is_correct_cell
from ship_data import ship_size


def analyse_field(battlefield):
    """
    dict(tuple(int, int): None or bool) -> bool

    analyses dictionary - representation of the battlefield in battleship
    returns True if placement of the ships like that in battlefield is possible
    returns False otherwise
    in particular:
        1) some of ships touch each other
        ***  or  ***
        *           ****
        2) there is wrong number of each ships of different size
        like 5 * ships or 2 **** ships

    dictionary structure:
        - the key is (int, int) - number of row and column respectively
        - numbers in key are in [1; 10] inclusive
        - the value can be:
            1) None - there is nothing in that cell
            2) False - there is undamaged ship in that cell
            3) True - there is damaged ship in that cell
    """
    ships = {}
    visited = set()
    diagonal_neighbours = set([(-1, -1), (-1, 1), (1, 1), (1, -1)])
    connected_neighbours = set([(0, -1), (1, 0), (0, 1), (-1, 0)])
    for cell in battlefield:
        if cell not in visited:
            current_result = ship_size(battlefield, cell, False)
            if current_result[0] != 0:
                for ship_cell in current_result[1]:
                    for prohibited_neighbour in diagonal_neighbours:
                        neighbour_cell = (ship_cell[0] +
                                          prohibited_neighbour[0],
                                          ship_cell[1] +
                                          prohibited_neighbour[1])
                        if battlefield.get(neighbour_cell, None) is not None:
                            return False
                        if is_correct_cell(neighbour_cell):
                            visited.add(neighbour_cell)
                    for permitted_neighbour in connected_neighbours:
                        neighbour_cell = (ship_cell[0] +
                                          permitted_neighbour[0],
                                          ship_cell[1] +
                                          permitted_neighbour[1])
                        if is_correct_cell(neighbour_cell):
                            visited.add(neighbour_cell)
                ships[current_result[0]] = ships.get(current_result[0], 0) + 1
    if not list(sorted(ships.keys())) == list(range(1, 5)):
        return False
    ship_rules = {1: 4, 2: 3, 3: 2, 4: 1}
    for ship_length in range(1, 5):
        if ship_rules[ship_length] != ships[ship_length]:
            return False
    return True
