#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#
from time import sleep
from mastermind.network.server import ClientRequest, ServerReply
import zmq

def check_state(state):
    if state['op'] == ServerReply.STATE_WAITING_FOR_JOIN:
        pass
    elif state['op'] == ServerReply.STATE_WAINING_FOR_GUESS:
        pass
    elif state['op'] == ServerReply.GAME_FULL:
        pass
    elif state['op'] == ServerReply.GAME_OVER:
        pass
    elif state['op'] == ServerReply.NOT_YOUR_TURN:
        pass
    else:
        return "invalid state - nothing done"

    reply = state # todo temp remove
    return reply


context = zmq.Context()

#  Socket to talk to server
print("Connecting to game server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5557")

request = {}

while True:
    try:
        sleep(1)
        request['op'] = ClientRequest.CHECK_STATE
        state = socket.send_pyobj(request)
        print(state)
        # checking state to decide what to do
        check_state(state)
    finally:
        socket.close()
        context.term()

# socket.send_string(name)
