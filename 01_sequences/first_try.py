import doctest

#       TASK_programming:
#           Згенерувати послідовність N пар взаємно простих чисел. Взаємно
#           прості числа — натуральні або цілі числа, які не мають спільних
#           дільників більших за 1, або, інакше кажучи, якщо їх найбільший
#           спільний дільник дорівнює 1. Таким чином, 2 і 3 — взаємно
#           прості, а 2 і 4 — ні (діляться на 2).


def gcd(x, y):
    """
    The function that counts gcd 2 integers.
    >>> gcd(7, 5)
    1
    >>> gcd(9, 3)
    3
    >>> gcd(16, 24)
    8
    """
    if y == 0:
        return x
    else:
        return gcd(y, x % y)


def is_coprime(x, y):
    """
    The function checks if to integers are coprime.
    >>> is_coprime(3, 7)
    1
    >>> is_coprime(9, 3)
    0
    """
    return gcd(x, y) == 1


def generate_list_of_coprimes(n):
    """
    The function generates list of coprime pairs of integers.
    """
    l = list()
    a, b = 2, 3
    while len(l) < n:
        if is_coprime(a, b):
            l.append((a, b))
        b += 1
    return l


if __name__ == "__main__":
    n = int(input("Enter n (amount of pairs): "))
    l = generate_list_of_coprimes(n)
    print("Sequence of %d coprime pairs is: %s." % (n, l))

    doctest.testmod()
