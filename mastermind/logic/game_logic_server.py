# todo analyse_guess
# todo inform_state

import logging
from enum import Enum
from random import choices, randint, randrange

from sty import fg, rs


class ClientRequest(Enum):
    JOIN_GAME = 1
    SEND_GUESS = 2
    CHECK_STATE = 3
    WON_GAME = 4
    LOST_GAME = 5


class ServerReply(Enum):
    STATE_WAITING_FOR_JOIN = 1  #
    STATE_WAITING_FOR_GUESS = 2  #
    GAME_FULL = 3  #
    GAME_OVER = 4
    NOT_YOUR_TURN = 5   #
    PLAYER_ADDED = 6
    PLAYER_ALREADY_EXISTS = 7  #
    WAITING_FOR_SECOND_PLAYER = 8  #
    GAME_STARTED_YOUR_TURN = 9  #
    GAME_STARTED_WAIT_FOR_TURN = 10  #
    GUESS_RESULT = 11 #
    YOU_WON = 12 #


class GameColors(Enum):
    RESET_FG_COLOR = rs.fg  # represents resetting the foreground color
    ALLOWED_COLORS = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]
    # possible colors: 1 : light red, 2 : light green, 3 : light yellow, 4 : light blue


class Player:
    def __init__(self, name):
        self.player_name = name
        self.num_of_guesses = 0
        # self.board = choices(GameColors.ALLOWED_COLORS.value, k=4)  # choose 4 colors, can repeat
        self.board = int(str(randrange(3) + 1) + str(randrange(3) + 1) + str(randrange(3) + 1) + str(randrange(3) + 1))
        # todo save last state?
        # todo save last guesses and results?

    def __repr__(self):  # todo board representation with color
        player_str = " Player name: " + self.player_name + ", Board: " + self.board.__repr__()
        return player_str

    def get_board_numbers(self):
        return [x.value for x in self.board]


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

    def check_state(self, player_name):
        # local var. to make the ifs clearer
        num_of_players = len(self.players)
        players_names = [x.player_name for x in self.players]
        has_player_joined = player_name in players_names

        # todo add clause when the other player wins
        if num_of_players == 0:
            return ServerReply.STATE_WAITING_FOR_JOIN
        elif num_of_players == 1:
            if has_player_joined:
                return ServerReply.WAITING_FOR_SECOND_PLAYER
            else:
                return ServerReply.STATE_WAITING_FOR_JOIN
        elif num_of_players == 2:
            if has_player_joined:
                if self.next_turn == players_names.index(player_name):
                    return ServerReply.STATE_WAITING_FOR_GUESS
                else:
                    return ServerReply.NOT_YOUR_TURN
            else:
                return ServerReply.GAME_FULL

    def check_guess(self, user, guess):
        full_corrects = 0  # correct color + place
        half_corrects = 0  # correct color wrong place (after full corrects removed)

        players_names = [x.player_name for x in self.players]
        other_player_index = abs(players_names.index(user) - 1) # user 1 -> other player 0
                                                                # user 0 -> other player 1
        other_player_board = self.players[other_player_index].board

        # do logic magic

        return full_corrects, half_corrects


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
