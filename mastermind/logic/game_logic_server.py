# todo analyse_guess
# todo inform_state

import logging
from enum import Enum
from random import choices, randint, randrange


class ClientRequest(Enum):
    JOIN_GAME = 1  # generates a request
    SEND_GUESS = 2  # generates a request
    CHECK_STATE = 3  # generates a request
    WON_GAME = 4  # generates no request
    LOST_GAME = 5  # generates no request


class ServerReply(Enum):
    STATE_WAITING_FOR_JOIN = 1  # reply for ClientRequest.CHECK_STATE
    STATE_WAITING_FOR_GUESS = 2  # reply for ClientRequest.CHECK_STATE
    GAME_FULL = 3  # reply for ClientRequest.JOIN_GAME
    GAME_OVER = 4  # reply for ClientRequest.CHECK_STATE
    NOT_YOUR_TURN = 5  # reply for ClientRequest.CHECK_STATE
    PLAYER_ALREADY_EXISTS = 7  # reply for ClientRequest.JOIN_GAME
    WAITING_FOR_SECOND_PLAYER = 8  # reply for ClientRequest.JOIN_GAME
    GAME_STARTED_YOUR_TURN = 9  # reply for ClientRequest.JOIN_GAME
    GAME_STARTED_WAIT_FOR_TURN = 10  # reply for ClientReuqest.JOIN_GAME
    GUESS_RESULT = 11  # reply for ClientRequest.SEND_GUESS
    YOU_WON = 12  # reply for ClientRequest.SEND_GUESS


class Player:
    def __init__(self, name):
        self.player_name = name
        self.num_of_guesses = 0
        # board: 4 digits of 1-4
        self.board = int(str(randrange(3) + 1) + str(randrange(3) + 1) + str(randrange(3) + 1) + str(randrange(3) + 1))
        # todo save last state?
        # todo save last guesses and results?

    def __repr__(self):  # todo board representation with color
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
            logging.info("Board: " + str(self.players[0].board))
            return ServerReply.WAITING_FOR_SECOND_PLAYER

        if len(self.players) == 1:
            if player_name == self.players[0].player_name:
                logging.error("Player " + player_name + " already listed in game. Cannot add him again.")
                return ServerReply.PLAYER_ALREADY_EXISTS
            else:
                player = Player(player_name)
                self.players.append(player)
                logging.info("Created and added player: " + player_name)
                logging.info("Board: " + str(self.players[1].board))
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
        other_player_index = abs(players_names.index(user) - 1)  # user 1 -> other player 0, user 0 -> other player 1
        other_player_board = self.players[other_player_index].board

        copy_board = str(other_player_board)
        copy_guess = list(str(guess))

        for digit in copy_board:
            if digit in copy_guess:
                half_corrects += 1
                copy_guess.remove(digit)

        for i in range(4):
            if list(str(guess))[i] == copy_board[i]:  # correct color + place counted and then removed
                full_corrects += 1
                half_corrects -= 1

        # changing turns
        if self.next_turn == 1:
            self.next_turn = 0
        else:
            self.next_turn = 1

        return full_corrects, half_corrects


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
