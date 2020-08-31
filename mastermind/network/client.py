#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#
import logging
import sys
import zmq

from mastermind.logic.game_logic_server import ClientRequest, ServerReply


def generate_request(user, op=ClientRequest.CHECK_STATE):
    return {"op": op,
            "user": user}


def analyse_reply(state):
    global request
    if state is None:
        logging.error("Empty state")
    else:
        if state.get('op') == ServerReply.STATE_WAITING_FOR_JOIN.name:
            logging.info("Server is waiting a join request")
        elif state.get('op') == ServerReply.STATE_WAINING_FOR_GUESS.name:
            logging.info("Server is waiting a guess")
        elif state.get('op') == ServerReply.GAME_FULL.name:
            logging.error("Game is full. Player not added")
            client.close()
            context.term()
            sys.exit()
        elif state.get('op') == ServerReply.GAME_OVER.name:
            logging.warning("Game over")    # todo win and lost
            client.close()
            context.term()
            sys.exit()
        elif state.get('op') == ServerReply.NOT_YOUR_TURN.name:
            logging.warning("Server says it's not your turn")
        elif state.get('op') == ServerReply.PLAYER_ADDED.name:  # not used?
            logging.info("Player was added successfully")
            request = generate_request(user)
        elif state.get('op') == ServerReply.PLAYER_ALREADY_EXISTS.name:
            logging.info("Player already in game. Try a different name")
            client.close()
            context.term()
            sys.exit()
        elif state.get('op') == ServerReply.WAITING_FOR_SECOND_PLAYER.name:
            logging.info("Waiting for a second player to join the game")
            request = generate_request(user)
        elif state.get('op') == ServerReply.GAME_STARTED_YOUR_TURN.name:
            logging.info("Game started: your turn")
            # get new guess
        elif state.get('op') == ServerReply.GAME_STARTED_WAIT_FOR_TURN.name:
            logging.info("Game started: wait for your turn")
        else:
            logging.info("Invalid state")


if __name__ == "__main__":
    user = input("enter username: ")

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    REQUEST_TIMEOUT = 2500
    REQUEST_RETRIES = 3
    SERVER_ENDPOINT = "tcp://localhost:5557"

    context = zmq.Context()
    logging.info("Context created")

    client = context.socket(zmq.REQ)
    logging.info("Socket created")
    logging.info("Connecting to server...")
    client.connect(SERVER_ENDPOINT)

    # first request
    logging.info("Generating request...")
    request = generate_request(user, op=ClientRequest.JOIN_GAME)
    logging.info("Request generated")
    client.send_pyobj(request)

    try:
        retries_left = REQUEST_RETRIES
        logging.info("zmq.POLLIN == " + str(zmq.POLLIN))
        logging.info("client.poll(REQUEST_TIMEOUT) == " + str(client.poll(REQUEST_TIMEOUT)))

        while True:
            # is there a reply waiting?
            if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                reply = client.recv_pyobj()
                # does the reply have a content?
                if reply is not None:
                    logging.info("received reply" + reply.get('op'))
                    retries_left = REQUEST_RETRIES
                    analyse_reply(reply)
                    # todo analyse reply + create new request
                else:
                    logging.error("no reply received")
                    retries_left -= 1
                    logging.warning("No response from server")
                    # Socket is confused. Close and remove it.
                    client.setsockopt(client.LINGER, 0)
                    client.close()
                    logging.info("Reconnecting to server…")
                    client = context.socket(zmq.REQ)
                    client.connect(SERVER_ENDPOINT)

            # after REQUEST_RETRIES tries, we assume the server is down
            if retries_left == 0:
                logging.error("Server seems to be offline, abandoning")
                break

            if retries_left < REQUEST_RETRIES:
                logging.info("Resending (%s)", request)
            else:
                logging.info("Sending (%s)", request)

            # sending a request (rerequest or new request)
            client.send_pyobj(request)

    except zmq.ZMQError as ze:
        logging.error("ZMQError: " + ze.strerror)
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
