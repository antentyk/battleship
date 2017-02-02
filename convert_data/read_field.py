def read_field(filename):
    """
    str -> dict[(int, int) : None or bool]
    open file named filename - battlefield representation
    converts this data into dictionary and returns it

    file structure:
        - it consists of 10 strings, length of each string is 10
        - each of the strings contains only from 3 permitted characters:
            1) ' ' - there is nothing in that cell
            2) '*' - there is undamaged ship in that cell
            3) 'X' - there is damaged ship in that cell
    dictionary structure:
        - the key is (int, int) - number of row and column respectively
        - numbers in key are in [1; 10] inclusive
        - the value can be:
            1) None - there is nothing in that cell
            2) False - there is undamaged ship in that cell
            3) True - there is damaged ship in that cell
    """
    file = open(filename, 'r')
    row_number = 0
    convert = {" ": None, "*": False, "X": True}
    battlefield = {}
    for line in file.read().split('\n'):
        row_number += 1
        col_number = 0
        for character in line:
            col_number += 1
            battlefield[(row_number, col_number)] = convert[character]
    return battlefield
