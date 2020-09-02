# todo get_guess
# todo ask_to_join

import logging
from mastermind.logic.game_logic_server import ServerReply, ClientRequest


def should_exit(reply):
    if reply.get('op').name == ServerReply.GAME_FULL.name:
        logging.error("game full. exiting")
        return True
    elif reply.get('op').name == ServerReply.PLAYER_ALREADY_EXISTS.name:
        logging.error("player already exists. exiting")
        return True

    return False


def get_op_new_request(reply):
    if reply.get('op') is ServerReply.NOT_YOUR_TURN or reply.get('op') is ServerReply.GAME_STARTED_WAIT_FOR_TURN \
            or reply.get('op') is ServerReply.WAITING_FOR_SECOND_PLAYER:
        logging.warning("not your turn")
        return ClientRequest.CHECK_STATE
    elif reply.get('op') is ServerReply.STATE_WAITING_FOR_GUESS or reply.get('op') is ServerReply.GAME_STARTED_YOUR_TURN:
        logging.info("your turn to guess")
        return ClientRequest.SEND_GUESS
    elif reply.get('op') is ServerReply.GUESS_RESULT:
        logging.info("got result for the guess")
        return ClientRequest.SEND_GUESS
    elif reply.get('op') is ServerReply.GAME_OVER:
        # game lost
        return ClientRequest.LOST_GAME
    elif reply.get('op') is ServerReply.YOU_WON:
        # game won
        return ClientRequest.WON_GAME
    return ClientRequest.CHECK_STATE # todo not very nice, should be in if? fallback


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
