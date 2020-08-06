import pytest
from mastermind.logic.game_logic_server import Game, ServerReply


def test_add_player():
    game = Game()
    assert game.add_player("Sha") == ServerReply.WAITING_FOR_SECOND_PLAYER
    assert game.add_player("Sha") == ServerReply.PLAYER_ALREADY_EXISTS
    assert game.add_player("ni") == ServerReply.GAME_STARTED_YOUR_TURN or ServerReply.GAME_STARTED_WAIT_FOR_TURN
    assert game.add_player("Ru") == ServerReply.GAME_FULL


def test_analyse_guess():
    assert False


def test_inform_state():
    assert False
