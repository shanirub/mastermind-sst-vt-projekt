#
#   Player

#   Connects REQ socket to tcp://localhost:5555
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to game server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

name = input("please enter your name:")

socket.send(name)
