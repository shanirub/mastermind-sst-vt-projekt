#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#
import logging
import sys
import zmq
from mastermind.logic.game_logic_client import should_exit, get_op_new_request
from mastermind.logic.game_logic_server import ClientRequest, ServerReply


def get_guess(self, name):
    """
    Reads a new guess from the player
    :param self:
    :param name: player's name to identify him to the server
    :return: the guess unchecked todo
    """
    print("-- Player " + str(self.next_turn)) + ": Please enter your guess in four digits."
    print("(1 : light red, 2 : light green, 3 : light yellow, 4 : light blue)")
    guess = input("...")
    return guess    # todo check guess


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

                    # checking to see if need to exit
                    if should_exit(reply):  # 3
                        clean_exit()

                    new_op = get_op_new_request(reply)
                    # asking for a guess only when needed
                    if new_op == ClientRequest.SEND_GUESS:
                        guess = get_guess(user)
                    else:
                        guess = ""

                    # generating a new request
                    request = {"op": new_op,
                                "user": user,
                                "guess": guess}
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
