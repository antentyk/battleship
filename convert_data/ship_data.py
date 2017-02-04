from common import convert, is_correct_cell


def has_ship(battlefield, cell):
    """
    dict, (str, int) -> bool
    TODO write documentation to the end
    """
    return battlefield[(cell[1], convert(cell[0]))] is not None


def ship_size(battlefield, cell, convert):
    """
    dict, (str, int), bool -> (int, set((int, int)))
    TODO documentation
    """
    if convert:
        cell = (cell[1], convert(cell[0]))
    if battlefield[cell] is not None:
        counter = 1
        coordinates = set()
        coordinates.add(cell)
        directions = set((0, -1), (1, 0), (0, 1), (-1, 0))
        for current_direction in directions:
            current_row = cell[0]
            current_col = cell[1]
            while True:
                current_row += current_direction[0]
                current_col += current_direction[1]
                if is_correct_cell((current_row, current_col)):
                    if battlefield[current_row, current_col] is not None:
                        counter += 1
                        coordinates.add((current_row, current_col))
                    else:
                        break
                else:
                    break
        return counter, coordinates
    else:
        return (0, 0)
