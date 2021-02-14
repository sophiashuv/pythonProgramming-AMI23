from Strategy import *


class Context():
    """
    Class for context representation
    """

    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def generate_list(self, l, pos, n) -> None:
        self._strategy.generate_data(l, pos, n)
