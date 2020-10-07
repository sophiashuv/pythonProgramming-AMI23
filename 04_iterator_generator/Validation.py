class Validation:
    @staticmethod
    def validateInt(n):
        try:
            n = int(n)
            if n < 0:
                raise ValueError("Input must be a positive integer!")
        except ValueError:
            raise ValueError("Not an integer!")
        return n

