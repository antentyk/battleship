from __init__ import convert


def ship_size(battlefield, cell):
    """
    dict, (str, int) -> int
    TODO documentation
    """
    cell = (cell[1], convert(cell[0]))
    if battlefield[cell] is not None:
        counter = 1
        directions = set((0, -1), (1, 0), (0, 1), (-1, 0))
        for current_direction in directions:
            current_row = cell[0]
            current_col = cell[1]
            try:
                while True:
                    current_row += current_direction[0]
                    current_col += current_direction[1]
                    if battlefield[current_row, current_col] is not None:
                        counter += 1
                    else:
                        break
            except:
                pass
        return counter
    else:
        return 0
