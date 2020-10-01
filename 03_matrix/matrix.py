import random

# Задано дійсні числа  ( – парне). Утворити
# квадратну матрицю порядку :


def menu(func):
    """
    The menu function.
    """
    while True:
        help_message = get_help_message()
        task = input(help_message)

        if task == "1":
            n = n_input("Enter n(size): ")
            low, height = input_low_height()
            list_array = random_arr(n, low, height)

        elif task == "2":
            list_array = user_arr()

        elif task == "exit":
            print("GOODBYE!")
            break

        else:
            print("WRONG INPUT!")
            continue

        func(list_array, len(list_array))
        print()


def get_help_message():
    """
    The function that returns help message.
    """
    help_message = "*" * 31
    help_message += "\n*  HELP:" + 22 * " " + "*\n*  Possible commands:" + 9 * " " + \
                    "*\n*  1 - generate random array; *\n*  2 - user input array; " + 5 * \
                    " " + "*\n*  exit - to finish program.  *\n"
    help_message += "*" * 31 + "\n"
    return help_message


def user_arr():
    """
    The function that returns user input array.
    """
    while True:
        try:
            mas = [float(i) for i in input("Enter numbers of array with whitespaces: ").split()]
            if len(mas)%2:
                print("Array len mast be even!")
                continue
        except ValueError:
            print("Elements of array mast be integers!")
            continue
        break
    return mas


def n_input(message, sign="pos", pr="even"):
    """
    The function that returns user input number and validates it depending whether input should be positive or not.
    """
    while True:
        try:
            n = int(input(message))
            if sign == "pos":
                if n <= 0:
                    print("Input must be a positive integer!")
                    continue
            if pr == "even":
                if n % 2:
                    print("Input must be a even integer!")
                    continue
            elif pr == "odd":
                if not n % 2:
                    print("Input must be a odd integer!")
                    continue
        except ValueError:
            print("Input must be an integer!")
            continue
        break
    return n


def input_low_height():
    """
    The function that returns input low and height values.
    """
    while True:
        low = n_input("Enter lower pos for random num: ", "none", "none")
        height = n_input("Enter higher pos for random num: ", "none", "none")
        if low > height:
            print("Low must be smaller than height.")
            continue
        return low,  height


def random_arr(n, low, height):
    """
    The function that returns a randomly generated array on certain interval.
    """
    mas = [round(random.uniform(low, height), 1) for i in range(n)]
    return mas


def generate_matrix(arr, n):
    """
    The function generates matrix from task.
    """
    matrix = [arr[::-1] if i%2 else arr for i in range(n)]
    print_matrix(matrix)
    return matrix


def print_matrix(matrix):
    """
    The prints beautiful matrix.
    """
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))


if __name__ == "__main__":
    menu(generate_matrix)
