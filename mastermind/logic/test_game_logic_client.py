from mastermind.logic.game_logic_server import ServerReply, ClientRequest
from mastermind.logic.game_logic_client import get_op_new_request, should_exit


def test_get_op_new_request():
    assert get_op_new_request({'op': ServerReply.GAME_STARTED_YOUR_TURN}) is ClientRequest.SEND_GUESS
    assert get_op_new_request({'op': ServerReply.NOT_YOUR_TURN}) is ClientRequest.CHECK_STATE
    assert get_op_new_request({'op': ServerReply.STATE_WAITING_FOR_GUESS}) is ClientRequest.SEND_GUESS
    assert get_op_new_request({'op': ServerReply.GAME_STARTED_WAIT_FOR_TURN}) is ClientRequest.CHECK_STATE
    assert get_op_new_request({'op': ServerReply.WAITING_FOR_SECOND_PLAYER}) is ClientRequest.CHECK_STATE


def test_should_exit():
    assert should_exit({'op': ServerReply.GAME_OVER}) is True
    assert should_exit({'op': ServerReply.GAME_FULL}) is True
    assert should_exit({'op': ServerReply.PLAYER_ALREADY_EXISTS}) is True
    assert should_exit({'op': ServerReply.GAME_STARTED_YOUR_TURN}) is False
    assert should_exit({'op': ServerReply.GAME_STARTED_WAIT_FOR_TURN}) is False
    assert should_exit({'op': ServerReply.STATE_WAITING_FOR_GUESS}) is False
    assert should_exit({'op': ServerReply.WAITING_FOR_SECOND_PLAYER}) is False
    assert should_exit({'op': ServerReply.NOT_YOUR_TURN}) is False

