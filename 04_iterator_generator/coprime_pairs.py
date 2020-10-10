from IterCount import Coprime_pairs_iter
from GeneratorCount import coprimes_generator
from Validation import Validation

#       TASK_programming:
#           Згенерувати послідовність N пар взаємно простих чисел. Взаємно
#           прості числа — натуральні або цілі числа, які не мають спільних
#           дільників більших за 1, або, інакше кажучи, якщо їх найбільший
#           спільний дільник дорівнює 1. Таким чином, 2 і 3 — взаємно
#           прості, а 2 і 4 — ні (діляться на 2).


def list_with_generator(n):
    l = [c for c in coprimes_generator(3, n, 2)]
    return l


def list_with_iter(n):
    l = [c for c in Coprime_pairs_iter(3, n, 2)]
    return l


def print_res(func):
    try:
        n = Validation.validateInt(input("Enter n (amount of pairs): "))
        l = func(n)
        print("Sequence of %d coprime pairs is: %s." % (n, l))

    except ValueError as e:
        print(e)


def int_input():
    """
    The function that checks user's input and in case it's correct prints
    pairs of coprime integers, otherwise user can try again to input and integer.
    """
    while True:
        m = "Enter 1 to iterate pairs of coprine integers;\n" \
            "Enter 2 to generate pairs of coprine integers;\n" \
            "Enter sth else to exit;\n"
        task = input(m)
        if task == "1":
            print_res(list_with_iter)
            continue

        elif task == "2":
            print_res(list_with_generator)
            continue
        else:
            print("GOODBYE")
            break


if __name__ == "__main__":
    int_input()


