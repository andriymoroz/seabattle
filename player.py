import os
import random
from board import Board
import board
import abc
import pyjsonrpc
import sys
import threading
import Queue
import socket
import time
import functools
import traceback
import signal
import optparse


def debug(foo):
    @functools.wraps(foo)
    def wrapper(*args, **kwargs):
        try:
            print "*" * 10, foo.__name__, "*" * 10
            r = foo(*args, **kwargs)
            print "*" * 10, "end", foo.__name__, "*" * 10
            return r
        except Exception as e:
            print type(e), e
            traceback.print_exc()
            raise e
    return wrapper

class IPlayers(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def get_player(self, not_this_one=None):
        pass


class IPlayer(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def init(self):
        pass


    @abc.abstractmethod
    def finalize(self):
        pass


    @abc.abstractmethod
    def get_move(self, prev_res):
        pass


    @abc.abstractmethod
    def set_move(self, x, y):
        pass


    @abc.abstractmethod
    def print_status(self):
        pass


    @abc.abstractmethod
    def has_ships(self):
        pass

class Players(IPlayers):
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


class PlayerInfo(object):
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port

    def __str__(self):
        return "%s %s %s" % (self.name, self.address, self.port)


class NetworkPlayersService(pyjsonrpc.HttpRequestHandler):
    def __init__(self, *args, **kwargs):
        self.msgqueue = None
        super(NetworkPlayersService, self).__init__(*args, ** kwargs)


    @pyjsonrpc.rpcmethod
    def register_player(self, name, address, port):
        self.msgqueue.put(PlayerInfo(name, address, port))
        return ""


class NetworkPlayersServiceWrapper(object):
    def __init__(self, msgqueue):
        self.msgqueue = msgqueue


    def __call__(self, *args, **kwargs):
        s = NetworkPlayersService(*args, **kwargs)
        s.msgqueue = self.msgqueue
        return s


class NetworkPlayers(IPlayers):
    MAX_PLAYERS = 50

    def __init__(self):
        self.msgqueue = Queue.Queue(self.MAX_PLAYERS)

        self.http_server = pyjsonrpc.ThreadingHttpServer(
                server_address=("localhost", 9393),
                RequestHandlerClass=NetworkPlayersServiceWrapper(self.msgqueue)
                )

        self.server_thread = threading.Thread(
                target=self.http_server.serve_forever
                )

        self.server_thread.daemon = True
        self.server_thread.start()


    def get_player(self, not_this_one=None, wait_sec=15):
        msg = self.msgqueue.get()
        player = NetworkPlayerClient(msg.name, msg.address, msg.port)

        end_time = time.time() + wait_sec
        while 1:
            try:
                player.ping()
            except Exception:
                if time.time() <= end_time:
                    time.sleep(1)
                    continue
                else:
                    return None

            return player


class Player(IPlayer):
    def __init__(self):
        self.name = "Player" + chr(random.randint(0, 9))
        self.board = Board()
        self.x = 0
        self.y = 0


    def init(self, size):
        # set up board, etc
        self.board.init(size)
        self.init_ships()


    def finalize(self):
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
        # self.board.print_board()
        print self.board.is_placement_complete()


    def get_move(self, prev_res):
        x = self.x
        y = self.y
        if self.x == (self.board.get_size() - 1):
            self.x = 0
        else:
            self.x += 1

            if self.y == (self.board.get_size() - 1):
                self.y = 0
            else:
                self.y += 1

        return x, y


    def set_move(self, x, y):
        if self.board.get_cell(self.board.OWN, x, y) == board.SHIP:
            self.board.set_cell(self.board.OWN, x, y, board.DEAD_SHIP)
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


class NetworkPlayerService(pyjsonrpc.HttpRequestHandler, IPlayer):
    player = Player()


    @pyjsonrpc.rpcmethod
    def init(self, *args, **kwargs):
        try:
            print self.player
            r = self.player.init(*args, **kwargs)
            return r if r is not None else ""
        except Exception as e:
            print e

    @pyjsonrpc.rpcmethod
    def finalize(self):
        # Temporary solution. Should be changed
        os.kill(0, signal.SIGINT)


    @pyjsonrpc.rpcmethod
    def get_move(self, *args, **kwargs):
        r = self.player.get_move(*args, **kwargs)
        return r if r is not None else ""


    @pyjsonrpc.rpcmethod
    def set_move(self, *args, **kwargs):
        r = self.player.set_move(*args, **kwargs)
        return r if r is not None else ""


    @pyjsonrpc.rpcmethod
    def print_status(self, *args, **kwargs):
        r = self.player.print_status(*args, **kwargs)
        return r if r is not None else ""


    @pyjsonrpc.rpcmethod
    def has_ships(self, *args, **kwargs):
        r = self.player.has_ships(*args, **kwargs)
        return r if r is not None else ""


    @pyjsonrpc.rpcmethod
    def ping(self):
        return ""


class NetworkPlayerServiceWrapper(object):
    def __init__(self, player):
        self.player = player


    def __call__(self, *args, **kwargs):
        s = NetworkPlayerService(*args, **kwargs)
        s.player = self.player
        return s


class NetworkPlayerClient(IPlayer):
    def __init__(self, name, address, port):
        url = "http://%s:%s" % (address, port)
        self.server = pyjsonrpc.Server(url)


    def init(self, size):
        return self.server.call("init", size)


    def finalize(self):
        return self.server.notify("finalize")


    def get_move(self, prev_res):
        return self.server.call("get_move", prev_res)


    def set_move(self, x, y):
        return self.server.call("set_move", x, y)


    def print_status(self):
        pass


    def has_ships(self):
        return self.server.call("has_ships")


    def ping(self):
        return self.server.call("ping")


def argparse():
    parser = optparse.OptionParser()
    parser.add_option("-a", "--address",
                      dest="address", help="Server address")
    parser.add_option("-p", "--port", type="int",
                      dest="port", help="Server port")

    options, _ = parser.parse_args()
    return options


def main(argv):
    try:
        options = argparse()
        hostname = socket.gethostname()
        service_port = random.randint(20000, 65000)

        server_url = "http://%s:%s" % (options.address, options.port)
        server = pyjsonrpc.Server(server_url)

        service_address = hostname
        if options.address in ("localhost", "127.0.0.1"):
            service_address = options.address

        for _ in xrange(10):
            try:
                server.call("register_player", hostname, service_address, service_port)
                break
            except pyjsonrpc.InternalError:
                time.sleep(1)

        http_server = pyjsonrpc.ThreadingHttpServer(
                    server_address=("localhost", service_port),
                    RequestHandlerClass=NetworkPlayerService
                    )

        http_server.serve_forever()

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        print type(e), e


if __name__ == "__main__":
    main(sys.argv)

