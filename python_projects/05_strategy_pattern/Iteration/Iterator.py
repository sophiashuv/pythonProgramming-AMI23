from Iteration.coprime_chacks import IsCoprime


class Coprime_pairs_iter:
    def __init__(self, low, high, first_el):
        self.current = low-1
        self.high = high
        self.first_el = first_el

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.high > 0:
            while not IsCoprime.is_coprime(self.first_el, self.current):
                self.current += 1
            self.high -= 1
            return self.first_el, self.current
        raise StopIteration

    def __str__(self):
        return str(self.current)


