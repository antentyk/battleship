from common import convert, is_correct_cell


def has_ship(battlefield, cell):
    """
    dict(tuple(int, int), (str, int) -> bool

    returns False if cell cell on the battlefield is empty
    otherwise returns True

    read more about battlefield in ship_size() documentation

    cell format
      A B C D E F F H I J
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    in this function we should write ('B', 5) for example
    """
    return battlefield[(cell[1], convert(cell[0]))] is not None


def ship_size(battlefield, cell, convert):
    """
    dict(tuple(int, int), (str, int) or (int, int), bool -> (int, set((int, int)))

    returns a length of the ship, a part of which is located in cell cell
    and set of coordinates of all the parts of this ship

    if there is not ship in this cell, returns (0, 0)

    convert variable determines format of cell:
        1) if convert is True, cell should be like
            ('A', 2) etc.
            read more in has_ship() documentation
        2) if convert is False, cell should be like
            (1, 2)

    dictionary structure:
        - the key is (int, int) - number of row and column respectively
        - numbers in key are in [1; 10] inclusive
        - the value can be:
            1) None - there is nothing in that cell
            2) False - there is undamaged ship in that cell
            3) True - there is damaged ship in that cell

    it is assumed that all the ships are placed in the battlefield according to all the rules
    of the game
    """
    if convert:
        cell = (cell[1], convert(cell[0]))
    if battlefield[cell] is not None:
        counter = 1
        coordinates = set()
        coordinates.add(cell)
        directions = set([(0, -1), (1, 0), (0, 1), (-1, 0)])
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
