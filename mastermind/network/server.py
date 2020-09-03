import logging
import zmq
from mastermind.logic.game_logic_server import Game, ClientRequest, ServerReply


def handle_request(request):
    if request.get('op').name == ClientRequest.JOIN_GAME.name:
        op, board = game.add_player(request.get('user'))
        return {'op': op, 'board': board}
    elif request.get('op').name == ClientRequest.SEND_GUESS.name:
        full_c, half_c = game.check_guess(request.get('user'), request.get('guess'))
        if full_c == 4:
            return {'op': ServerReply.YOU_WON}
        return {"op": ServerReply.GUESS_RESULT, 'full_corrects': full_c, 'half_corrects': half_c}
    elif request.get('op').name == ClientRequest.CHECK_STATE.name:
        op = game.check_state(request.get('user'))
        return {'op': op}
    else:
        return {"op": "nothing done"}  # todo


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
            logging.info(
                "<-- Received request from: " + request.get('user') + ", request op code: " + str(request.get('op')))
            reply = handle_request(request)
            server.send_pyobj(reply)
            logging.info("--> Reply send: %s" % str(reply.get('op')))

    finally:
        server.close()
        context.term()
