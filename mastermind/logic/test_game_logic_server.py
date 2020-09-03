from mastermind.logic.game_logic_server import Game, ServerReply


def test_add_player():
    game = Game()
    # adding first player
    assert game.add_player("Sha") == ServerReply.WAITING_FOR_SECOND_PLAYER
    # first player cannot be added twice
    assert game.add_player("Sha") == ServerReply.PLAYER_ALREADY_EXISTS
    # second player added
    assert game.add_player("ni") == ServerReply.GAME_STARTED_YOUR_TURN or ServerReply.GAME_STARTED_WAIT_FOR_TURN
    # trying to add a third player
    assert game.add_player("Ru") == ServerReply.GAME_FULL


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
