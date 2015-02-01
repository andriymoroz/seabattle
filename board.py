
EMPTY = ' '
SHIP = 'X'
DEAD_SHIP = 'x'
CRATER = '.'


class Field:
    field = None
    def __init__(self, size):
        self.size = size
        self.clear()


    def clear(self):
        self.field = [[EMPTY for x in range(self.size)] for x in range(self.size)] #self.size*[self.size*[0]]
        pass

    def get_cell(self, x, y):
        return self.field


class Board:
    OWN = 0
    ENEMY = 1

    def __init__(self):
        pass

    def init(self, size=10):
        self.field = [Field(size), Field(size)]
        pass

    def clear(self):
        pass

    def print_board(self):
        pass

    def get_size(self):
        return self.field[0].size

    def get_cell(self, ownership, x, y):
        return self.field[ownership].get_cell(x, y)

