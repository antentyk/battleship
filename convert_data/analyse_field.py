from __init__ import convert, is_correct_cell
from ship_data import ship_size


def analyse_field(battlefield):
    """
    dict -> bool
    """
    ships = {}
    visited = set()
    diagonal_neighbours = set((-1, -1), (-1, 1), (1, 1), (1, -1))
    connected_neighbours = set((0, -1), (1, 0), (0, 1), (-1, 0))
    for cell in battlefield:
        if cell not in visited:
            # немає сенсу добавляти у візітед бо я вже тут не буду
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
