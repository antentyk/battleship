from generate_field.generate_field import generate_field
from generate_field.ship_data import ship_size
from generate_field.common import convert
import os


class Ship:
    def __init__(self, bow, horizontal, length, hit):
        """
        tuple(int, int), bool, int, list[bool] -> None

        initializes ship

        self.bow - tuple(int, int)
        coordinate of ship's
        left top cell in[(1, 1); (10, 10)] inclusive

        self.horizontal - bool
        it is True when ship is placed horizontally(****)
        otherwise it is False

        self._length - int
        length of the ship in [1;4] inclusive

        self._hit - list[bool]
        element of the list is True when relevant part of the ship is injured
        for example (* - healthy cell, O - injured cell):
        *
        O
        O
        *
        self._hit would be [False, True, True, False]
        """
        self.bow = bow
        self.horizontal = horizontal
        self._length = length
        self._hit = hit

    def shoot_at(self, coordinate):
        """
        tuple(int, int) -> None

        updates self._hit according to the cell that was hit
        it is assumed that coordinate is
        a right coordinate that is in this ship
        """
        if self.horizontal:
            self._hit[coordinate[1] - self.bow[1]] = True
        else:
            self._hit[coordinate[0] - self.bow[0]] = True

    def is_hit(self, coordinate):
        """
        tuple(int, int) -> bool

        checks if coordinate cell in ship was hit or not
        returns True or False respectively

        it is assumed that coordinate is
        a right coordinate that is in this ship
        """
        if self.horizontal:
            return self._hit[coordinate[1] - self.bow[1]]
        else:
            return self._hit[coordinate[0] - self.bow[0]]

    def is_dead(self):
        """
        () -> None

        checks if there are any healthy cells in ship
        """
        return self._hit.count(False) == 0


class Field:
    def __init__(self):
        """
        () -> None

        initializes field

        self._field - dict{(int, int): Ship() or None}
        field representation
            key is (int, int) - number of row and column respectively
                in [(1, 1);(10, 10)] inclusive
            value is None if there is no ship in cells
            otherwise it contains Ship() object


        self.cells_left - number of healthy cells left on the field
        """
        self._field = {}
        self.cells_left = 20
        field = generate_field()
        visited = set()
        for cell in field:
            if cell not in visited:
                length, coordinates = ship_size(field, cell)
                if length == 0:
                    self._field[cell] = False
                else:
                    visited = visited.union(coordinates)
                    horizontal = (max(coordinates)[0] == min(coordinates)[0])
                    ship = Ship(min(coordinates),
                                horizontal,
                                length,
                                [False]*length)
                    for item in coordinates:
                        self._field[item] = ship

    def _get_field(self, displayship):
        """
        bool -> str

        returns text representation of the ship

        if displayship is True,
        function returns a string with ships in this format:
            'I' - injured cell of the ship
            'D' - dead ship
            'H' - healthy part of the ship
            'M' - miss
            ' ' - untouched cell on the field
        example:
        '''
        M        H
            HHHI H
        H  M   MM
                H
              H H
          H     H
        H
        H   H
               HH
         DDD M
        '''

        if displayship is False,
        function returns a string with ships in this format:
            'I' - injured cell of the ship
            'D' - dead ship
            'M' - miss
            ' ' - untouched cell on the field
        example:
        '''
        M
                I
            MM






        DDD M
        '''
        """
        text_field = [[' ']*10 for i in range(10)]
        for line in range(1, 11):
            for row in range(1, 11):
                cell = (line, row)
                if isinstance(self._field[cell], Ship):
                    if self._field[cell].is_dead():
                        text_field[line - 1][row - 1] = "D"
                    else:
                        if self._field[cell].is_hit(cell):
                            text_field[line - 1][row - 1] = "I"
                        elif displayship:
                            text_field[line - 1][row - 1] = "H"
                else:
                    if self.is_hit(cell):
                        text_field[line - 1][row - 1] = "M"
        result = []
        for item in text_field:
            result.append(''.join(item))
        return '\n'.join(result)

    def is_hit(self, coordinate):
        """
        (int, int) -> bool

        returns True if coordinate on the field is hit or not
        it is assumed that coordinate is tuple of 2 ints
        in [(1, 1); (10, 10)] inclusive
        """
        if isinstance(self._field[coordinate], Ship):
            return self._field[coordinate].is_hit(coordinate)
        else:
            return self._field[coordinate]

    def shoot_at(self, coordinate):
        """
        (int, int) -> bool

        tries to shoot in coordinate
        if this coordinate wasn't hit before,
        updates self.field
            if there is no ship in this cell,
                sets field[coordinate] equal to True
            if there is a ship in this cell,
                updates Ship() object
        returns True

        if this coordinate was hit before,
        returns False
        """
        if isinstance(self._field[coordinate], Ship):
            self.cells_left -= 1
            self._field[coordinate].shoot_at(coordinate)
            return True
        else:
            self._field[coordinate] = True
            return False


class Player:
    def __init__(self, number):
        """
        int -> None

        initializes the player and gets his name
        """
        name = 'first' if number == 1 else 'second'
        self._name = input("Enter name of %s player" % name)

    def read_position(self, opponent_field):
        """
        Field() -> (int, int)

        gets from user a correct cell that was not hit before
        and converts it to another format

        if input data is incorrect,
        asks user to write cell again

        intput format: 'F10'
        return value: tuple of 2 ints
        in range[(1,1);(10,10)] inclusive
        """
        while True:
            try:
                inp = input("Enter your position for example A4")
                line = int(inp[1:])
                assert(line >= 1)
                assert(line <= 10)
                row = convert(inp[0])
                if row is not None:
                    if opponent_field.is_hit((line, row)):
                        print('You have already hit in this cell')
                        continue
                    return (line, row)
            except:
                print('wrong data! Try again!')


class Game:
    def __init__(self):
        """
        () -> None

        initializes Game:
            - fields
            - players
            - index of current player
        self._players - list of Player() objects -
            current players that are participating
        self._fields - list of Field() objects - fields of the players
        self._current_player - index of current player (1 or 2)
        """
        self._fields = [Field(), Field()]
        self._players = [Player(1), Player(2)]
        self._current_player = 1

    def increase_player(self):
        """
        () -> None
        updates index of a current player
        sets it to 1 if it is 2
        sets it to 1 if it is 1
        """
        self._current_player = 2 - ((self._current_player + 1) % 2)

    def get_index(self):
        """
        () -> int
        returns an integer - index of the current player
        """
        return self._current_player - 1

    def get_opponent_index(self):
        """
        () -> int
        returns an integer - index of the rival
        of the current player
        """
        return 1 - ((self._current_player + 1) % 2)

    def field_with_ships(self, index):
        """
        int -> str
        returns a text representation of
        the field of a player with index index
        returns string that contains data about all the ships
        """
        return self._fields[index]._get_field(True)

    def field_without_ships(self, index):
        """
            int -> str
            returns a text representation of
            the field of a player with index index
            returns string that contains data only about the cells
            that were hit
        """
        return self._fields[index]._get_field(False)

    def is_winner(self):
        """
        () -> int or bool

        check if the game is over
        if it is, returns index of the player,
        that won the game

        if it is not the end of the game, returns False
        """
        if self._fields[0].cells_left == 0:
            return 2
        if self._fields[1].cells_left == 0:
            return 1
        return False

    def start(self):
        """
        starts the game
        """
        while not self.is_winner():
            os.system('cls')
            print(self._players[self._current_player - 1]._name +
                  ' make your move')
            print('your field')
            print(self._fields[self.get_index()]._get_field(True))
            print('opponent field')
            print(self._fields[self.get_opponent_index()]._get_field(False))
            cell = self._players[self.get_index()].\
                read_position(self._fields[self.get_opponent_index()])
            if not self._fields[self.get_opponent_index()].shoot_at(cell):
                self.increase_player()
        print(self._players[self.is_winner() - 1]._name + ' won')
