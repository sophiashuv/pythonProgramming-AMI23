from Context import Context
from Strategy import *
from Validation import Validation
from Observer import *
import copy

def menu():
    """
    The menu function.
    """
    l = LinkedList()
    obs = Observer()
    obs.observe('Add', Logger.write_to_file)
    obs.observe('Remove', Logger.write_to_file)
    obs.observe('Change', Logger.write_to_file)

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
            b_l = copy.deepcopy(l)
            l.listMethod()
            Event("Change", l, b_l)
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
    b_l = copy.deepcopy(l)
    context.generate_list(l, pos, par)
    Event("Add", l, b_l, pos)


@Validation.validate_inp
def del_index(l):
    """
    The function deletes element by index.
    """
    index = Validation.validateInt(input("Enter index to delete: "))
    b_l = copy.deepcopy(l)
    l.delete_index(index)
    Event("Remove", l, b_l, index)


@Validation.validate_inp
def del_between_indexes(l):
    """
    The function deletes elements between two indexes.
    """
    index1, index2 = Validation.validateLowHeight(
        tuple(map(Validation.validateInt, input("Enter index1 and index2: ").split())))
    b_l = copy.deepcopy(l)
    l.delete_between_pos(index1, index2)
    Event("Remove", l, b_l, (index1, index2))


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
