# todo get_guess
# todo ask_to_join

import logging


def ask_to_join():
    pass


def get_guess(self, name):
    """
    Reads a new guess from the player
    :param self:
    :param name: player's name to identify him to the server
    # todo where do we save player's name? do we save it?
    :return:
    """
    print("-- Player " + str(self.next_turn)) + ": Please enter your guess in four digits."
    print("(1 : light red, 2 : light green, 3 : light yellow, 4 : light blue)")
    guess = input("...")
    reply = self.check_guess(guess)
    return reply


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
