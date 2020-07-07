from sty import fg, rs
from random import choices
RESET_FG_COLOR = "rs.fg"


class Board:

    def __init__(self):
        self.letters, self.colors = generate_new_board()

    def check_guess(self, letters, colors):
        if letters == self.letters and colors == self.colors:
            return True
        else:
            return False

    def print_board(self):
        for i in range(8):
            print(self.colors[i] + self.letters[i] + RESET_FG_COLOR)


def generate_new_board():
    allowed_letters = "ABCDEFGH"
    allowed_colors = ["fg.li_red", "fg.li_green", "fg.li_yellow", "fg.li_blue"]
    letters = choices(allowed_letters, k=8)
    colors = choices(allowed_colors, k=8)

    return letters, colors


b = Board()
print(b)
b.print_board()