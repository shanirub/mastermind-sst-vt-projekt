from sty import fg, rs
from random import choices, randint
from enum import Enum


class GameColors(Enum):
    RESET_FG_COLOR = rs.fg  # represents resetting the foreground color
    ALLOWED_COLORS = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]
    # possible colors: 1 : light red, 2 : light green, 3 : light yellow, 4 : light blue


class ClientRequest(Enum):
    JOIN_GAME = 1
    SEND_GUESS = 2
    CHECK_STATE = 3


class ServerReply(Enum):
    STATE_WAITING_FOR_JOIN = 1
    STATE_WAINING_FOR_GUESS = 2
    GAME_FULL = 3
    GAME_OVER = 4
    NOT_YOUR_TURN = 5


class Player:
    def __init__(self, name):
        self.player_name = name
        self.num_of_guesses = 0
        self.board = choices(GameColors.ALLOWED_COLORS, k=4)  # choose 4 colors, can repeat
        # todo save last guesses and results?

    def __repr__(self):     # todo board representation with color
        player_str = " Player name: " + self.player_name + ", Board: " + self.board.__repr__()
        return player_str


class Game:
    def __init__(self):
        self.players = []
        self.next_turn = None

    def join_game(self, player):    # todo: start and join together. creates player instance using name. where to save this instance?
        """
        handles join requests from player. three options:
        1. can't join, game is full
        2. can join
        3. can't join, already in
        :param player: player's name to be added to players list
        """
        if len(self.players) < 2:
            if player not in self.players:
                self.players.append(player)
                print("Player added: ")
                print(player)
                print("Current number of players: " + str(len(self.players)))
            else:
                print("this player is already in game")
        else:
            print("already have two players")

        if len(self.players) == 2:
            print("Cannot start game until there are two players")
        else:
            self.next_turn = randint(0, 1)
            print(self.next_turn)
            print("First one to play is " + self.players[self.next_turn].player_name)

    def check_guess(self, guess):

            # correct guess, game ended
            reply = "OLL KORRECT"
            # todo win thing
            return reply
        else:
            # incorrect guess, analyse guess
            full_corrects, half_corrects = self.analyse_guess(guess.pegs)
            reply = "Full Correct: " + str(full_corrects) + "\nHalf Correct: " + str(half_corrects)
            return reply

    def analyse_guess(self, guess):
        """
        helper method for check_guess
        :param self:
        :param guess:
        :return:
        """
        full_corrects = 0  # correct color + place
        half_corrects = 0  # correct color wrong place (after full corrects removed)
        copy_board = self.pegs
        copy_guess = list(guess)

        for peg in copy_board:
            if peg in copy_guess:
                half_corrects += 1
                copy_guess.remove(peg)

        for i in range(4):
            if list(guess)[i] == self.pegs[i]:  # correct color + place counted and then removed
                full_corrects += 1
                half_corrects -= 1

        return full_corrects, half_corrects

    def __repr__(self):
        game_str = ""
        if self.players == 0:
            game_str += "no players"
        elif self.players == 1:
            game_str += "one player. waiting for second player"
        else:
            game_str += "two players.\n"

        for player in self.players:
            game_str += player.__repr__()
            game_str += "\n"

        return game_str
