from mastermind.logic.game_logic_server import Game, ServerReply


def test_add_player():
    game = Game()

    # adding first player
    reply = game.add_player("Sha")
    assert reply.get('op') == ServerReply.WAITING_FOR_SECOND_PLAYER
    assert reply.get('board').isdigit() is True

    # first player cannot be added twice
    reply = game.add_player("Sha")
    assert reply.get('op') == ServerReply.PLAYER_ALREADY_EXISTS
    assert reply.get('board').isdigit() is False

    # second player added
    reply = game.add_player("ni")
    assert reply.get('op') == ServerReply.GAME_STARTED_YOUR_TURN or ServerReply.GAME_STARTED_WAIT_FOR_TURN
    assert reply.get('board').isdigit() is True

    # trying to add a third player
    reply = game.add_player("Ru")
    assert reply.get('op') == ServerReply.GAME_FULL
    assert reply.get('board').isdigit() is False


def test_check_guess():
    game = Game()
    game.add_player("Sha")
    game.add_player("ni")
    game.players[1].board = 1234    # ni board set to 1234 for testing
    assert game.check_guess("Sha", "1111") == (1, 0)
    assert game.check_guess("Sha", "1212") == (2, 0)
    assert game.check_guess("Sha", "4321") == (0, 4)
    assert game.check_guess("Sha", "1234") == (4, 0)
    assert game.check_guess("Sha", "1324") == (2, 2)


def test_check_state():
    game = Game()

    assert game.check_state("Sha") == ServerReply.STATE_WAITING_FOR_JOIN
    game.add_player("Sha")
    assert game.check_state("Sha") == ServerReply.WAITING_FOR_SECOND_PLAYER
    assert game.check_state("Ni") == ServerReply.STATE_WAITING_FOR_JOIN
    game.add_player("Ni")

    game.next_turn = 1
    assert game.check_state("Sha") == ServerReply.NOT_YOUR_TURN
    assert game.check_state("Ni") == ServerReply.STATE_WAITING_FOR_GUESS
    assert game.check_state("Ru") == ServerReply.GAME_FULL
