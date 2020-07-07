from sty import fg, rs
from random import choices
RESET_FG_COLOR = rs.fg  # represents resetting the foreground color


class Board:

    def __init__(self):
        self.colors = generate_new_board()

    def check_guess(self, colors):
        if colors == self.colors:
            # correct guess, game ended
            return True
        else:
            # incorrect guess, analyse guess
            self.analyse_guess(colors)
            return False

    def print_board(self):
        board_str = ""
        for i in range(8):
            board_str += (self.colors[i] + 'O ' + RESET_FG_COLOR)

        print(board_str)

    def analyse_guess(self, colors):
        pass


def generate_new_board():
    # allowed_letters = "ABCDEFGH"
    # possible colors: light red, light green, light yellow, light blue
    allowed_colors = [fg.li_red, fg.li_green, fg.li_yellow, fg.li_blue]
    # letters = choices(allowed_letters, k=8)     # choose 8 letters, can repeat
    colors = choices(allowed_colors, k=8)       # choose 8 colors, can repeat

    return colors


b = Board()
print(b)
b.print_board()