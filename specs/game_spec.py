from nimoy.specification import Specification


class BoardSpec(Specification):

    def string_assertion(self):
        with given:
            a = "There's a huge difference"
        with expect:
            a == "There's a small difference"