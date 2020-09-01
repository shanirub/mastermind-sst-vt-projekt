from mastermind.logic.game_logic_server import ServerReply, ClientRequest
from mastermind.logic.game_logic_client import get_op_new_request, should_exit, generate_request


def test_get_op_new_request():
    assert False


def test_generate_request():
    assert False


def test_should_exit():
    assert should_exit(ServerReply.GAME_OVER) is True
    assert should_exit(ServerReply.GAME_FULL) is True
    assert should_exit(ServerReply.PLAYER_ALREADY_EXISTS) is True
    assert should_exit(ServerReply.GAME_STARTED_YOUR_TURN) is False
    assert should_exit(ServerReply.GAME_STARTED_WAIT_FOR_TURN) is False
    assert should_exit(ServerReply.STATE_WAINING_FOR_GUESS) is False
    assert should_exit(ServerReply.WAITING_FOR_SECOND_PLAYER) is False
    assert should_exit(ServerReply.NOT_YOUR_TURN) is False

