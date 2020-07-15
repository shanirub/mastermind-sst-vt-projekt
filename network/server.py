#
#   Game Server

#   Binds REP socket to tcp://*:5555
#
#

import zmq
from logic.game import Game

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

game = Game()

while len(game.players) < 2:
    message = socket.recv()
    print("Player requested to join:" % message)
    game.join_game(message)
