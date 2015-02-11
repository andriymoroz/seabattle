import copy

"""
    A   B   C   D   E   F   G   H   I   J       A   B   C   D   E   F   G   H   I   J
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
1 |   |   |   |   |   |   |   |   |   |   | 1 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
2 |   |   |   |   |   |   |   |   |   |   | 2 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
3 |   |   |   |   |   |   |   |   |   |   | 3 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
4 |   |   |   |   |   |   |   |   |   |   | 4 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
5 |   |   |   |   |   |   |   |   |   |   | 5 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
6 |   |   |   |   |   |   |   |   |   |   | 6 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
7 |   |   |   |   |   |   |   |   |   |   | 7 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
8 |   |   |   |   |   |   |   |   |   |   | 8 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
9 |   |   |   |   |   |   |   |   |   |   | 9 |   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+
10|   |   |   |   |   |   |   |   |   |   | 10|   |   |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+

"""

EMPTY = ' '
SHIP = 'X'
DEAD_SHIP = 'x'
CRATER = '.'

RIGHT = 0
DOWN = 1


class Field:
    field = None

    def __init__(self, size):
        self.size = size
        self.clear()

    def get_field(self):
        return self.field

    def set_field(self, field):
        self.field = copy.deepcopy(field)

    def clear(self):
        self.field = [[EMPTY for x in range(self.size)] for x in range(self.size)]  # self.size*[self.size*[0]]
        pass

    def get_cell(self, x, y):
        return self.field[x][y]

    def set_cell(self, x, y, val):
        self.field[x][y] = val


class Board:
    OWN = 0
    ENEMY = 1
    ships_init = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self):
        self.field = None
        self.ships = {}
        pass

    def init(self, size=10):
        self.field = [Field(size), Field(size)]
        self.ships = copy.deepcopy(self.ships_init)

    def clear(self):
        pass

    def get_size(self):
        return self.field[0].size

    def get_cell(self, ownership, x, y):
        return self.field[ownership].get_cell(x, y)

    def set_cell(self, ownership, x, y, val):
        self.field[ownership].set_cell(x, y, val)

    def place_ship(self, size, x, y, orientation):
        sx = x - 1
        sy = y - 1
        field_backup = copy.deepcopy(self.field[self.OWN].get_field())
        try:
            if self.ships[size] == 0:
                raise Exception

            for i in range(0, size):
                self.field[self.OWN].set_cell(sx, sy, SHIP)
                if orientation == RIGHT:
                    sx += 1
                elif orientation == DOWN:
                    sy += 1
                else:
                    raise Exception

#                if sx >= self.field[self.OWN].size or sy >= self.field[self.OWN].size:
#                    raise Exception
        except:
            self.field[self.OWN].set_field(field_backup)
            return False

        self.ships[size] -= 1

        return True

    def is_placement_complete(self):
        for ship_size in self.ships:
            if self.ships[ship_size] > 0:
                return False

        return True

    def print_board(self):
        print "    A   B   C   D   E   F   G   H   I   J       A   B   C   D   E   F   G   H   I   J"
        print "  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+"
        for y in range(0, self.get_size()):
            row1 = ""
            row2 = ""
            for x in range(0, self.get_size()):
                row1 += " " + self.field[self.OWN].get_cell(x, y) + " |"
                row2 += " " + self.field[self.ENEMY].get_cell(x, y) + " |"
            print "%2d|%s %2d|%s" % (y + 1, row1, y + 1, row2)
            print "  +---+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+---+---+"

