#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#
import logging
import sys
from time import sleep
from mastermind.network.server import ClientRequest, ServerReply
import zmq

def generate_request(user, op= 'FIRST_REQUEST'):
    return {"op": op,
            "user": user}


def analyse_reply(state):
    if state is None:
        print("state is None")
    else:
        if state.get('op') == ServerReply.STATE_WAITING_FOR_JOIN:
            print("state recieved: STATE_WAITING_FOR_JOIN")
        elif state.get('op') == ServerReply.STATE_WAINING_FOR_GUESS:
            print("state recieved: STATE_WAITING_FOR_GUESS")
        elif state.get('op') == ServerReply.GAME_FULL:
            print("state recieved: GAME_FULL")
        elif state.get('op') == ServerReply.GAME_OVER:
            print("state recieved: GAME_OVER")
        elif state.get('op') == ServerReply.NOT_YOUR_TURN:
            print("state recieved: NOT_YOUR_TURN")
        else:
            print("invalid state - nothing done")


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    user = input("enter username: ")

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    REQUEST_TIMEOUT = 2500
    REQUEST_RETRIES = 3
    SERVER_ENDPOINT = "tcp://localhost:5557"
    #
    context = zmq.Context()

    logging.info("Connecting to server…")
    print("Connecting to game server…")
    client = context.socket(zmq.REQ)
    client.connect(SERVER_ENDPOINT)

    # first request
    request = "please_work"
    client.send_string(request)

    try:
        retries_left = REQUEST_RETRIES
        print(zmq.POLLIN)
        print(client.poll(REQUEST_TIMEOUT))
        while True:
            if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                reply = client.recv_string()
                if reply is not None:
                    logging.info("received reply")
                    retries_left = REQUEST_RETRIES
                else:
                    logging.error("no reply received")
            retries_left -= 1
            logging.warning("No response from server")
            # Socket is confused. Close and remove it.
            client.setsockopt(client.LINGER, 0)
            client.close()
            if retries_left == 0:
                logging.error("Server seems to be offline, abandoning")

            logging.info("Reconnecting to server…")
            client = context.socket(zmq.REQ)
            client.connect(SERVER_ENDPOINT)
            logging.info("Resending (%s)", request)
            client.send_string(request)

    except zmq.ZMQError as ze:
        print("ZMQError: " + ze.strerror)
    finally:
        client.close()
        context.term()

    # socket.send_string(name)





#
#  Lazy Pirate client
#  Use zmq_poll to do a safe request-reply
#  To run, start lpserver and then randomly kill/restart it
#
#   Author: Daniel Lundin <dln(at)eintr(dot)org>
# #
# import itertools
# import logging
# import sys
# import zmq
#
# logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
#
# REQUEST_TIMEOUT = 2500
# REQUEST_RETRIES = 3
# SERVER_ENDPOINT = "tcp://localhost:5555"
#
# context = zmq.Context()
#
# logging.info("Connecting to server…")
# client = context.socket(zmq.REQ)
# client.connect(SERVER_ENDPOINT)
#
# for sequence in itertools.count():
#     request = str(sequence).encode()
#     logging.info("Sending (%s)", request)
#     client.send(request)
#
#     retries_left = REQUEST_RETRIES
#     while True:
#         if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
#             reply = client.recv()
#             if int(reply) == sequence:
#                 logging.info("Server replied OK (%s)", reply)
#                 break
#             else:
#                 logging.error("Malformed reply from server: %s", reply)
#                 continue
#
#         retries_left -= 1
#         logging.warning("No response from server")
#         # Socket is confused. Close and remove it.
#         client.setsockopt(zmq.LINGER, 0)
#         client.close()
#         if retries_left == 0:
#             logging.error("Server seems to be offline, abandoning")
#             sys.exit()
#
#         logging.info("Reconnecting to server…")
#         # Create new connection
#         client = context.socket(zmq.REQ)
#         client.connect(SERVER_ENDPOINT)
#         logging.info("Resending (%s)", request)
#         client.send(request)
#
#
