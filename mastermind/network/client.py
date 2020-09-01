#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#
import logging
import sys
import zmq
from mastermind.logic.game_logic_client import should_exit, generate_request
from mastermind.logic.game_logic_server import ClientRequest, ServerReply


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
                    if should_exit(reply):
                        clean_exit()

                    # generating a new request
                    request = generate_request(user, reply)
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
