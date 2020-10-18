from Context import Context
from Strategy import *
from Validation import Validation


def menu():
    """
    The menu function.
    """
    l = LinkedList()
    context = None
    while True:
        help_message = get_help_message()
        task = input(help_message)
        if task == "1":
            context = Context(FirstStrategy())
        elif task == "2":
            context = Context(SecondStrategy())
        elif task == "3":
            generate_list(l, context)
        elif task == "4":
            del_index(l)
        elif task == "5":
            del_between_indexes(l)
        elif task == "6":
            l.listMethod()
        elif task == "7":
            print(l)
        elif task == "8":
            print("GOODBYE!")
            break
        else:
            print("WRONG INPUT!")
            continue
        print()


@Validation.validate_inp
def generate_list(l, context):
    """
    The function that generates list according to context type.
    """
    context = Validation.validateListGeneration(context)
    if isinstance(context.strategy, FirstStrategy):
        par = Validation.validateInt(input("Enter amount of elements: "))
    else:
        par = Validation.validateFileName(input("Enter file name: "))
    pos = Validation.validateInt(input("Enter position: "))
    context.generate_list(l, pos, par)


@Validation.validate_inp
def del_index(l):
    """
    The function deletes element by index.
    """
    index = Validation.validateInt(input("Enter index to delete: "))
    l.delete_index(index)


@Validation.validate_inp
def del_between_indexes(l):
    """
    The function deletes elements between two indexes.
    """
    index1, index2 = Validation.validateLowHeight(
        tuple(map(Validation.validateInt, input("Enter index1 and index2: ").split())))
    l.delete_between_pos(index1, index2)


def get_help_message():
    """
    The function that returns help message.
    """
    help_message = "*" * 51
    help_message += "\n*  HELP:" + 42 * " " + "*\n*  Possible commands:" + 29 * " " + \
                    "*\n*  1 - to use strategy 1;" + 25 * " " + \
                    "*\n*  2 - to use strategy 2; " + 24 * " " + \
                    "*\n*  3 - to generate elements;  " + 20 * " " + \
                    "*\n*  4 - to delete element by position " + 13 * " " + \
                    "*\n*  5 - to delete elements between positions;  " + 4 * " " + \
                    "*\n*  6 - to use list method;  " + 22 * " " + \
                    "*\n*  7 - to print list;  " + 27 * " " + \
                    "*\n*  8 - to exit.  " + 33 * " " + "*\n"
    help_message += "*" * 51 + "\n"
    return help_message


if __name__ == "__main__":
    menu()
