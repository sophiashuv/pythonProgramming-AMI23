class IsCoprime:
    @staticmethod
    def gcd(x, y):
        if y == 0:
            return x
        else:
            return IsCoprime.gcd(y, x % y)

    @staticmethod
    def is_coprime(x, y):
        return IsCoprime.gcd(x, y) == 1
