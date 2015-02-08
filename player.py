from random import randint
from board import Board
import board


class Player:
    def __init__(self):
        self.name = "Player" + chr(randint(0, 9))
        self.board = Board()
        pass

    def init(self, size):
        # set up board, etc
        self.board.init(size)
        self.init_ships()

        pass

    def init_ships(self):
        self.board.place_ship(4, 1, 1, board.RIGHT)
        self.board.place_ship(3, 1, 8, board.DOWN)
        self.board.place_ship(3, 3, 8, board.DOWN)
        self.board.place_ship(2, 5, 8, board.DOWN)
        self.board.place_ship(2, 7, 8, board.DOWN)
        self.board.place_ship(2, 9, 8, board.DOWN)
        self.board.place_ship(1, 4, 4, board.DOWN)
        self.board.place_ship(1, 4, 6, board.DOWN)
        self.board.place_ship(1, 6, 4, board.DOWN)
        self.board.place_ship(1, 6, 6, board.DOWN)
        self.board.print_board()
        print self.board.is_placement_complete()

        pass

    def get_move(self, prev_res):
        return 1, 1

    def set_move(self, x, y):
        #if self.board[x][y] == board.SHIP:
        if self.board.get_cell(self.board.OWN, x, y) == board.SHIP:
            return "inj"
        else:
            return "miss"


    def print_status(self):
        pass

    def has_ships(self):
        size = self.board.get_size()
        for x in range(size):
            for y in range(size):
                if self.board.get_cell(self.board.OWN, x, y) == board.SHIP:
                    return True

        return False
