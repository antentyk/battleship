from generate_field.generate_field import generate_field
from generate_field.ship_data import ship_size
from generate_field.common import convert
import string


class Ship:
    def __init__(self, bow, horizontal, length, hit):
        self.bow = bow
        self.horizontal = horizontal
        self.length = length
        self.hit = hit
    def __str__(self):
        result = '----------------------------\n'
        result += "SHIP\n"
        add_line = 0 if self.horizontal else 1
        add_row = 1 if self.horizontal else 0
        for i in range(self.length):
            cell = (self.bow[0] + i*add_line, self.bow[1] + i*add_row)
            result += "cell " + str(cell)
            if self.is_hit(cell):
                result += "hit"
            else:
                result += "healthy"
            result += '\n'
        result += '----------------------------\n'
        return result
    def shoot_at(self, coordinate):
        if self.horizontal:
            self.hit[coordinate[1] - self.bow[1]] = True
        else:
            self.hit[coordinate[0] - self.bow[0]] = True
    def is_hit(self, coordinate):
        if self.horizontal:
            return self.hit[coordinate[1] - self.bow[1]]
        else:
            return self.hit[coordinate[0] - self.bow[0]]
    def is_dead(self):
        return self.hit.count(False) >= 1


class Field:
    def __init__(self):
        self.field = {}
        field = generate_field()
        visited = set()
        for cell in field:
            if cell not in visited:
                length, coordinates = ship_size(field, cell)
                if length == 0:
                    self.field[cell] = False
                else:
                    visited = visited.union(coordinates)
                    horizontal = (max(coordinates)[0] == min(coordinates)[0])
                    ship = Ship(min(coordinates), horizontal, length, [False]*length)
                    for item in coordinates:
                        self.field[item] = ship
    def __str__(self):
        return self.field_with_ships()
    def is_hit(self, coordinate):
        if isinstance(self.field[coordinate], Ship):
            return self.field[coordinate].is_hit(coordinate)
        else:
            return self.field[coordinate]
    def shoot_at(self, coordinate):
        if isinstance(self.field[coordinate], Ship):
            self.field[coordinate].shoot_at(coordinate)
        else:
            self.field[coordinate] = True
    def field_without_ships(self):
        '''
        E - empty you know for sure
        H - ship is hit but not dead
        D - dead ship
        '''
        text_field = [[' ']*10 for i in range(10)]
        for line in range(1, 11):
            for row in range(1, 11):
                cell = (line, row)
                if isinstance(self.field[cell], Ship):
                    if self.field[cell].is_dead():
                        text_field[line - 1][row - 1] = "D"
                    else:
                        if self.field[cell].is_hit(cell):
                            text_field[line - 1][row - 1] = "H"
                else:
                    if self.is_hit(cell):
                        text_field[line - 1][row - 1] = "E"
        return '\n'.join(text_field)
    def field_with_ships(self):
        '''
        I - injured cell of the ship
        D - dead ship
        H - healthy part of the ship
        M - rival mistook and hit empty cell
        '''
        text_field = [[' ']*10 for i in range(10)]
        for line in range(1, 11):
            for row in range(1, 11):
                cell = (line, row)
                if isinstance(self.field[cell], Ship):
                    if self.field[cell].is_dead():
                        text_field[line - 1][row - 1] = "D"
                    else:
                        if self.field[cell].is_hit(cell):
                            text_field[line - 1][row - 1] = "I"
                        else:
                            text_field[line - 1][row - 1] = "H"
                else:
                    if self.is_hit(cell):
                        text_field[line - 1][row - 1] = "M"
        return '\n'.join(text_field)


class Player:
    def __init__(self, name):
        self.name = name
    def read_position(self):
        while True:
            try:
                inp = input("Enter your position for example A4")
                line = int(inp[1])
                row = convert(inp[0])
                if row is not None:
                    return (line, row)
            except:
                print('wrong data! Try again!')


class Game:
    def __init__(self):
        self.fields = [Field(), Field()]
        self.players = [Player('player1'), Player('player2')]
        self.current_player = 1
    #---------------------------------