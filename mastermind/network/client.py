#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#
import logging
import sys
from time import sleep

import zmq
from mastermind.logic.game_logic_client import should_exit, get_op_new_request
from mastermind.logic.game_logic_server import ClientRequest, ServerReply


def get_guess(name):
    """
    Reads a new guess from the player
    :param name: player's name to identify him to the server
    :return: the guess unchecked todo
    """
    print("-- Player " + name + ": Please enter your guess in four digits.")
    print("(1 : light red, 2 : light green, 3 : light yellow, 4 : light blue)")
    guess = input("...")
    return guess  # todo check guess


def clean_exit():
    logging.info("preforming clean exit")
    client.close()
    context.term()
    sys.exit()


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
    logging.info("Generating first request... (join)")
    request = {'op': ClientRequest.JOIN_GAME,
               'user': user,
               'guess': ""}
    client.send_pyobj(request)
    logging.info("--> Request sent")

    try:
        retries_left = REQUEST_RETRIES
        # logging.info("zmq.POLLIN == " + str(zmq.POLLIN))
        # logging.info("client.poll(REQUEST_TIMEOUT) == " + str(client.poll(REQUEST_TIMEOUT)))

        while True:
            sleep(1)
            # is there a reply waiting?
            logging.info("waiting for reply")
            if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                reply = client.recv_pyobj()
                # does the reply have a content?
                if reply is not None:
                    logging.info("<-- Received reply " + str(reply.get('op')))
                    retries_left = REQUEST_RETRIES

                    # checking to see if need to exit
                    if should_exit(reply):  # 3
                        clean_exit()

                    new_op = get_op_new_request(reply)
                    # check for a win or lost situation
                    if new_op == ClientRequest.WON_GAME:
                        # do some nice printing
                        clean_exit()
                    elif new_op == ClientRequest.LOST_GAME:
                        # do some nice printing
                        clean_exit()

                    # asking for a guess only when needed
                    if new_op == ClientRequest.SEND_GUESS:
                        # show player guess results, if there are any
                        if 'full_corrects' in reply:
                            logging.info("Your guess contains " + str(reply.get('full_corrects')) + " full corrects and " +
                                         str(reply.get('half_corrects')) + " half corrects.")
                        guess = get_guess(user)
                    else:
                        guess = ""

                    # generating a new request
                    request = {"op": new_op,
                               "user": user,
                               "guess": guess}
                else:
                    logging.error("!-- No reply received")
                    retries_left -= 1
                    logging.warning("!-- No response from server")
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
                logging.info("--> Resending (%s)", request)
            else:
                logging.info("--> Sending (%s)", request)

            # sending a request (rerequest or new request)
            client.send_pyobj(request)

    except zmq.ZMQError as ze:
        logging.error("ZMQError: " + ze.strerror)
    finally:
        client.close()
        context.term()
