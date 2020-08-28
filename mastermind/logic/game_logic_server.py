# todo analyse_guess
# todo inform_state

import logging
from sty import fg, rs
from random import choices, randint
from enum import Enum


class ClientRequest(Enum):
    JOIN_GAME = 1
    SEND_GUESS = 2
    CHECK_STATE = 3


class ServerReply(Enum):
    STATE_WAITING_FOR_JOIN = 1
    STATE_WAINING_FOR_GUESS = 2
    GAME_FULL = 3                   #
    GAME_OVER = 4
    NOT_YOUR_TURN = 5
    PLAYER_ADDED = 6
    PLAYER_ALREADY_EXISTS = 7       #
    WAITING_FOR_SECOND_PLAYER = 8   #
    GAME_STARTED_YOUR_TURN = 9      #
    GAME_STARTED_WAIT_FOR_TURN = 10 #


class GameColors(Enum):
    RESET_FG_COLOR = rs.fg  # represents resetting the foreground color
    ALLOWED_COLORS = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]
    # possible colors: 1 : light red, 2 : light green, 3 : light yellow, 4 : light blue


class Player:
    def __init__(self, name):
        self.player_name = name
        self.num_of_guesses = 0
        self.board = choices(GameColors.ALLOWED_COLORS.value, k=4)  # choose 4 colors, can repeat
        # todo save last guesses and results?

    def __repr__(self):     # todo board representation with color
        player_str = " Player name: " + self.player_name + ", Board: " + self.board.__repr__()
        return player_str


class Game:
    def __init__(self):
        self.players = []
        self.next_turn = None

    def add_player(self, player_name):
        """
        :param      player_name:    name of the player to be added
        :return:    ServerReply.GAME_FULL                       player not added:   already two players
                    ServerReply.WAITING_FOR_SECOND_PLAYER       player added:       waiting for second player
                    ServerReply.PLAYER_ALREADY_EXISTS           player not added:   player already exists
                    ServerReply.GAME_STARTED_YOUR_TURN          player added:       and can begin
                    ServerReply.GAME_STARTED_WAIT_FOR_TURN      player added:       and must wait for his turn
        """

        if len(self.players) == 2:
            logging.error("There are already two players in the game. Cannot add another one.")
            return ServerReply.GAME_FULL

        if len(self.players) == 0:
            player = Player(player_name)
            self.players.append(player)
            logging.info("Created and added player: " + str(player_name))
            return ServerReply.WAITING_FOR_SECOND_PLAYER

        if len(self.players) == 1:
            if player_name == self.players[0].player_name:
                logging.error("Player " + player_name + " already listed in game. Cannot add him again.")
                return ServerReply.PLAYER_ALREADY_EXISTS
            else:
                player = Player(player_name)
                self.players.append(player)
                logging.info("Created and added player: " + player_name)

                self.next_turn = randint(0, 1)
                logging.info("Game started. First turn goes to " + self.players[self.next_turn].player_name)

                if player_name == self.players[self.next_turn].player_name:
                    return ServerReply.GAME_STARTED_YOUR_TURN
                else:
                    return ServerReply.GAME_STARTED_WAIT_FOR_TURN

    def analyse_guess(request):
        reply = request  # todo remove
        return reply

    def inform_state(request):
        reply = request  # todo remove
        return reply


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
