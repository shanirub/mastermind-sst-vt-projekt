from sty import fg, rs
from random import choices
RESET_FG_COLOR = rs.fg  # represents resetting the foreground color


class Board:

    def __init__(self, value_list=None):
        """

        :type value_list: list
        """
        # possible colors: 1 : light red, 2 : light green, 3 : light yellow, 4 : light blue
        allowed_colors = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]

        if value_list is None:
            self.pegs = choices(allowed_colors, k=4)  # choose 8 colors, can repeat
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
            board_str += (self.pegs[i] + 'O ' + RESET_FG_COLOR)

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

    def __init__(self, player):
        self.num_of_players = 1
        self.players = [player]

    def join_game(self, player):
        self.num_of_players += 1
        self.players += player


p1 = Player("Sha")
p2 = Player("Ni")

print(p1)
print(p2)

