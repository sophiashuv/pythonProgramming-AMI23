import doctest

    # TASK:
        # 2. Сходинками називається набір кубиків, в якому кожен верхній шар містить кубиків менше,
        # ніж попередній. Потрібно написати програму, яка обчислює кількість сходинок, яку можна
        # побудувати з N кубиків.
        #
        #     Вхідні дані:
        #     Ввести з клавіатури натуральне число N (1 ≤ N ≤ 100) - кількість кубиків в сходинках.
        #     Вихідні дані:
        #     Вивести на екран кількість сходинок, які можна побудувати з N кубиків.


def print_matrix(matrix):
    """
    The function that illustrates a matrix used in amount_of_stairs
    """
    [print(*line) for line in matrix]


def amount_of_stairs(n):
    """
    The function that counts amount of stairs that can be build from n cubes.
    >>> amount_of_stairs(7)
    5
    >>> amount_of_stairs(9)
    8
    """

    matrix = [[0] * n for i in range(n)]

    for i in range(0, n):
        for j in range(1, i):
            matrix[i][j] = sum(matrix[i - j - 1][:j])
        matrix[i][i] = 1

    # print_matrix(matrix)
    return sum(matrix[n-1])


def int_input():
    """
    The function that checks user's input and in case it's correct prints
    amount of different stairs, otherwise user can try again to input and integer.
    """
    while True:
        try:
            n = int(input("Enter amount of cubes(n): "))
            if n < 0:
                print("Input must be a positive integer!")
                continue
        except ValueError:
            print("Not an integer!")
            continue

        print("There are %d different stairs that can be build from %d cubes." % (amount_of_stairs(n), n))
        break


if __name__ == "__main__":
    int_input()

    doctest.testmod()
