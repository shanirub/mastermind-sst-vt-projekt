import zmq
from mastermind.logic import game_logic_server
from enum import Enum


class ClientRequest(Enum):
    JOIN_GAME = 1
    SEND_GUESS = 2
    CHECK_STATE = 3


class ServerReply(Enum):
    STATE_WAITING_FOR_JOIN = 1
    STATE_WAINING_FOR_GUESS = 2
    GAME_FULL = 3
    GAME_OVER = 4
    NOT_YOUR_TURN = 5

def generate_reply():
    pass

def handle_request(request):
    if request.get('op') == ClientRequest.JOIN_GAME:
        return "JOIN_GAME request"
        # return game_logic_server.add_player(request)
    elif request.get('op') == ClientRequest.SEND_GUESS:
        return "SEND_GUESS request"
    elif request.get('op') == ClientRequest.CHECK_STATE:
        return "CHECK_STATE request"
    else:
        return {"invalid request": "nothing done"}


if __name__ == "__main__":
    context = zmq.Context()
    print("Context defined.")
    server = context.socket(zmq.REP)
    print("Socket defined")
    server.bind("tcp://*:5557")
    print("Socket bind tcp://*:5557")

    try:
        while True:
            request = server.recv_pyobj()
            print("Received request: %s" % request)
            # reply = {'op': 'lala'}
            # print("Reply: %s" % reply)
            server.send_pyobj(request)
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
