import random
from statemachine import StateMachine
from player import Player


class Players:
    def __init__(self):
        pl1 = Player()
        pl2 = Player()
        self.players = [pl1, pl2]

    def get_player(self, not_this_one=None):
        pl_list = self.players
        try:
            pl_list.remove(not_this_one)
        except:
            pass

        try:
            return random.choice(pl_list)
        except:
            return None


class Context:
    def __init__(self):
        self.players = Players()

    def get_players(self):
        return self.players


class Game:
    def __init__(self):
        self.ctx = Context()
        self.m = StateMachine()
        self.m.add_state("init", self.sm_init)
#       m.add_state("idle", sm_idle)
        self.m.add_state("start", self.sm_start)
        self.m.add_state("end", self.sm_end, end_state=1)
        self.m.set_start("init")
        self.m.run(self.ctx)

    def sm_init(self, ctx):
        # initialize
        newState = "start"
        return newState, ctx

    def sm_start(self, ctx):
        # pick two players, start game
        p1, p2 = self.get_random_players()
        p1.init(10)
        p2.init(10)

        p1.print_status()
        p2.print_status()

        res = None
        player = [p1, p2]
        next_move = 0
        while p1.has_ships() or p2.has_ships():
            x, y = player[next_move].get_move(res)
            res = player[next_move ^ 1].set_move(x, y)
            if res not in ["inj", "sink"]:
                next_move ^= 1

        newState = "end"

        return newState, ctx

    def sm_end(self, ctx):
        pass

    def get_random_players(self):
        #ugly:
        players = self.ctx.get_players()
        player1 = players.get_player()
        player2 = players.get_player(not_this_one=player1)
        return player1, player2

    def start_game(self):
        pass




if __name__ == "__main__":
    g = Game()
#    g.start_game()

