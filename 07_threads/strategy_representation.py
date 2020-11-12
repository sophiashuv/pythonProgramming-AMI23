import copy

from Context import Context
from Strategy import *
from Validation import Validation
from Observer import *
from Thread import ExceptionThread


def menu():
    """
    The menu function.
    """
    l_strategy1 = LinkedList()
    l_strategy2 = LinkedList()

    obs = Observer()
    obs.observe('Add')
    obs.observe('Remove')
    obs.observe('Change')

    while True:
        help_message = get_help_message()
        task = input(help_message)
        if task == "1":
            context = Context(FirstStrategy())
        elif task == "2":
            context = Context(SecondStrategy())
        elif task == "3":
            if isinstance(context._strategy, FirstStrategy):
                generate_list(l_strategy1, context)
            else:
                generate_list(l_strategy2, context)
        elif task == "4":
            del_index(l_strategy1, l_strategy2)
        elif task == "5":
            del_between_indexes(l_strategy1, l_strategy2)
        elif task == "6":
            list_method(l_strategy1, l_strategy2)
        elif task == "7":
            create_thread(print, print, (l_strategy1,), (l_strategy2,))
        elif task == "8":
            print("GOODBYE!")
            break
        else:
            print("WRONG INPUT!")
            continue
        print()


def create_thread(f1, f2, args1=(), args2=()):
    p1 = ExceptionThread(name='Strategy1 list', target=f1, args=args1)
    p2 = ExceptionThread(name='Strategy2 list', target=f2, args=args2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()


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
def del_index(l1, l2):
    """
    The function deletes element by index.
    """
    index = Validation.validateInt(input("Enter index to delete: "))
    b_l1 = copy.deepcopy(l1)
    b_l2 = copy.deepcopy(l2)
    create_thread(l1.delete_index, l2.delete_index, (index,), (index,))
    Event("Remove", l1, b_l1, index)
    Event("Remove", l1, b_l2, index)


@Validation.validate_inp
def del_between_indexes(l1, l2):
    """
    The function deletes elements between two indexes.
    """
    index1, index2 = Validation.validateLowHeight(
        tuple(map(Validation.validateInt, input("Enter index1 and index2: ").split())))
    b_l1 = copy.deepcopy(l1)
    b_l2 = copy.deepcopy(l2)
    create_thread(l1.delete_between_pos, l2.delete_between_pos, (index1, index2), (index1, index2))
    Event("Remove", l1, b_l1, (index1, index2))
    Event("Remove", l2, b_l2, (index1, index2))


def list_method(l1, l2):
    b_l1 = copy.deepcopy(l1)
    b_l2 = copy.deepcopy(l2)
    create_thread(l1.listMethod, l2.listMethod)
    Event("Change", l1, b_l1)
    Event("Change", l2, b_l2)


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
