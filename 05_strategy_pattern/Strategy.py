from LinkedList.LinkedList import LinkedList
from Iteration.Iterator import Coprime_pairs_iter
import abc


class Strategy(LinkedList):
    """
    Class for strategy representation
    """
    @abc.abstractmethod
    def generate_data(self, data: LinkedList, pos, param):
        pass


class FirstStrategy(Strategy):
    """
    First type strategy that generates data using iterator.
    """
    def generate_data(self, data: LinkedList, pos, n) -> None:
        for c in Coprime_pairs_iter(3, n, 2):
            data.insert(c[0], pos)
            data.insert(c[1], pos+1)
            pos += 2


class SecondStrategy(Strategy):
    """
    Second type strategy that reads data from txt file.
    """
    def generate_data(self, data: LinkedList, pos, filename) -> None:
        with open(filename, "r") as infile:
            for line in infile:
                for x in line.split():
                    data.insert(int(x), pos)
                    pos += 1
        infile.close()
