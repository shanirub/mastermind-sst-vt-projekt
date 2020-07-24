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

def handle_request(message):
    if message['op'] == ClientRequest.JOIN_GAME:
        return game_logic_server.add_player(request)
    elif message['op'] == ClientRequest.SEND_GUESS:
        pass
    elif message['op'] == ClientRequest.CHECK_STATE:
        pass
    else:
        return "invalid request - nothing done"

    reply = message # todo temp remove
    return {reply}


if __name__ == "__main__":
    context = zmq.Context()
    print("Context defined.")
    socket = context.socket(zmq.REP)
    print("Socket defined")
    socket.bind("tcp://*:5557")
    print("Socket bind tcp://*:5557")

    while True:
        try:
            #  Wait for next request from client
            request = socket.recv_pyobj()
            print("Received request: %s" % request)
            reply = handle_request(request)
            print("Reply: %s" % reply)
            socket.send_pyobj(reply)
        finally:
            socket.close()
            context.term()
