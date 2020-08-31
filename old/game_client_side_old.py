from enum import Enum

from sty import fg, rs


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


def get_guess(self, name):
    print("-- Player " + str(self.next_turn)) + ": Please enter your guess in four digits."
    print("(1 : light red, 2 : light green, 3 : light yellow, 4 : light blue)")
    guess = input("...")
    reply = self.check_guess(guess)
    return reply
