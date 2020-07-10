from sty import fg, rs
from random import choices
RESET_FG_COLOR = rs.fg  # represents resetting the foreground color


class Board:

    def __init__(self, value_list=None):
        """

        :type value_list: list
        """
        # possible colors: light red, light green, light yellow, light blue
        allowed_colors = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]

        if value_list is None:
            self.pegs = choices(allowed_colors, k=8)  # choose 8 colors, can repeat
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
        for i in range(8):
            board_str += (self.pegs[i] + 'O ' + RESET_FG_COLOR)

        return board_str

    def analyse_guess(self, guess):
        full_corrects = 0  # correct color + place
        half_corrects = 0  # correct color wrong place (after full corrects removed)
        copy_board = self.pegs

        for i in range(8):
            if guess[i] == self.pegs[i]:     # correct color + place counted and then removed
                full_corrects += 1
                guess[i] = ''
                copy_board[i] = ''

        for peg in guess:
            if peg in copy_board:
                half_corrects += 1
                copy_board.remove(peg)

        return full_corrects, half_corrects



b1 = Board()
b2 = Board()

print(b1)
print(b2)

b1.check_guess(b2)