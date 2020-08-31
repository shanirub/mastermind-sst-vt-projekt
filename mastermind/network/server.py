import logging

import zmq

from mastermind.logic.game_logic_server import Game, ClientRequest


def generate_reply():
    pass


def handle_request(request):
    if request.get('op').name == ClientRequest.JOIN_GAME.name:
        op = game.add_player(request.get('user'))
        return {'op': op.name}
    elif request.get('op').name == ClientRequest.SEND_GUESS.name:
        return {"op": "SEND_GUESS request"}     # todo
    elif request.get('op').name == ClientRequest.CHECK_STATE.name:
        return {"op": "CHECK_STATE request"}        # todo
    else:
        return {"op": "nothing done"}           # todo


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    game = Game()
    logging.info("created a new Game instance")
    logging.info("number of players: " + str(len(game.players)))

    context = zmq.Context()
    logging.info("Context created")
    server = context.socket(zmq.REP)
    logging.info("Socket created")
    logging.info("Binding to tcp://*:5557 ...")
    server.bind("tcp://*:5557")

    try:
        while True:
            request = server.recv_pyobj()
            logging.info("Received request from: " + request.get('user'))
            logging.info("Request op code: " + str(request.get('op')))
            # print("Reply: %s" % reply)
            reply = handle_request(request)
            logging.info("Reply generated, op code: " + str(reply.get('op')))
            server.send_pyobj(reply)
            logging.info("Reply send: %s" % str(reply.get('op')))

    finally:
        server.close()
        context.term()



#
#  Lazy Pirate server
#  Binds REQ socket to tcp://*:5555
#  Like hwserver except:
#   - echoes request as-is
#   - randomly runs slowly, or exits to simulate a crash.
#
#   Author: Daniel Lundin <dln(at)eintr(dot)org>
#
# from random import randint
# import itertools
# import logging
# import time
# import zmq
#
# logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
#
# context = zmq.Context()
# server = context.socket(zmq.REP)
# server.bind("tcp://*:5555")
#
# for cycles in itertools.count():
#     request = server.recv()
#
#     # Simulate various problems, after a few cycles
#     if cycles > 3 and randint(0, 3) == 0:
#         logging.info("Simulating a crash")
#         break
#     elif cycles > 3 and randint(0, 3) == 0:
#         logging.info("Simulating CPU overload")
#         time.sleep(2)
#
#     logging.info("Normal request (%s)", request)
#     time.sleep(1)  # Do some heavy work
#     server.send(request)
