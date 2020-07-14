from sty import fg, rs
from random import choices, randint
import time, zmq

RESET_FG_COLOR = rs.fg  # represents resetting the foreground color
# possible colors: 1 : light red, 2 : light green, 3 : light yellow, 4 : light blue
ALLOWED_COLORS = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]


class Board:

    def __init__(self, value_list=None):
        """

        :type value_list: list
        """
        if value_list is None:
            self.pegs = choices(ALLOWED_COLORS, k=4)  # choose 8 colors, can repeat
        else:
            # todo check value_list validity
            self.pegs = value_list

    def check_guess(self, guess):
        if guess.pegs == self.pegs:
            # correct guess, game ended
            print("OLL KORRECT")
        else:
            # incorrect guess, analyse guess
            full_corrects, half_corrects = self.analyse_guess(guess.pegs)
            print("Full Correct: " + str(full_corrects))
            print("Half Correct: " + str(half_corrects))

    def __repr__(self):
        board_str = ""
        for i in range(4):
            board_str += (self.pegs[i] + str(ALLOWED_COLORS.index(self.pegs[i])) + RESET_FG_COLOR)

        return board_str

    def analyse_guess(self, guess):
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


class Player:

    def __init__(self, name):
        self.player_name = name
        self.board = Board()

    def __repr__(self):
        player_str = " Player name: " + self.player_name + ", Board: " + self.board.__repr__()
        return player_str


class Game:

    def __init__(self):
        self.players = []
        self.next_turn = None
        #context = zmq.Context()
        #socket = context.socket(zmq.REP)
        #socket.bind("tcp://*:5555")
        #print(" Game server started at tcp://localhost:5555 .")
        #print(" To join a game, use: player.py")

    def join_game(self, player):
        if len(self.players) < 2:
            if player not in self.players:
                self.players.append(player)
                print("player added: ")
                print(player)
                print("Number of players: " + str(len(self.players)))
            else:
                print("this player is already in game")
        else:
            print("already have two players")

    def start_game(self):
        if len(self.players) < 2:
            print("cannot start game until there are two players")
        else:
            self.next_turn = randint(0, 1)
            print(self.next_turn)
            print("first one to play is " + self.players[self.next_turn].player_name)

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


p1 = Player("Sha")
p2 = Player("Ni")
p3 = Player("Rub")
g = Game()
g.join_game(p1)
g.join_game(p1)
g.join_game(p2)
g.join_game(p3)
print(g)
g.start_game()



