from LstCollection import LstCollection
from Product import Product
from Validation import Validation
from memento import *


def menu():
    """
    The menu function.
    """

    p = LstCollection()
    caretaker = Caretaker(p)
    caretaker.backup("Empty collection.")

    while True:
        help_message = get_help_message()
        task = input(help_message)
        if task == "1":
            read_json_file(p)
            caretaker.backup("Read json.")
        elif task == "2":
            sort_elements(p)
            caretaker.backup("Sort elements.")
            write_in_json_file(p)
        elif task == "3":
            search_elements(p)
            write_in_json_file(p)
        elif task == "4":
            add_product(p)
            caretaker.backup("Add Product to collection.")
            write_in_json_file(p)
        elif task == "5":
            del_product(p)
            caretaker.backup("Del element from collection.")
            write_in_json_file(p)
        elif task == "6":
            edit_product(p)
            caretaker.backup("Edit element from collection.")
            write_in_json_file(p)
        elif task == "7":
            write_in_txt_file(p)
        elif task == "8":
            write_in_json_file(p)
        elif task == "9":
            for product in p:
                print(product)
        elif task == "undo":
            undo_moment(caretaker)
            write_in_json_file(p)
        elif task == "redo":
            redo_moment(caretaker)
            write_in_json_file(p)
        elif task == "move":
            move_moment(caretaker)
            write_in_json_file(p)
        elif task == "history":
            caretaker.show_history()
            write_in_json_file(p)
        elif task == "exit":
            print("GOODBYE!")
            break
        else:
            print("WRONG INPUT!")
            continue
        print()


def get_help_message():
    """
    The function that returns help message.
    """
    help_message = "*" * 51
    help_message += "\n*  HELP:" + 42 * " " + "*\n*  Possible commands:" + 29 * " " + \
                    "*\n*  1 - to read from file;" + 25 * " " + \
                    "*\n*  2 - to sort elements; " + 25 * " " + \
                    "*\n*  3 - to to search element.  " + 20 * " " + \
                    "*\n*  4 - to to add Product to collection. " + 10 * " " + \
                    "*\n*  5 - to del element from collection.  " + 10 * " " + \
                    "*\n*  6 - to edit element from collection.  " + 9 * " " + \
                    "*\n*  7 - to write collection elements to txt file.  " \
                    "*\n*  8 - to write collection elements to json file. " \
                    "*\n*  9 - to print collection. " + 22 * " " + \
                    "*\n*  undo - to undo moment. " + 24 * " " + \
                    "*\n*  redo - to redo moment. " + 24 * " " + \
                    "*\n*  move - to move on moment. " + 21 * " " + \
                    "*\n*  history - to show history of moments. " + 9 * " " + \
                    "*\n*  exit - to exit.  " + 30 * " " + "*\n"
    help_message += "*" * 51 + "\n"
    return help_message


@Validation.validate_inp
def read_json_file(p):
    global file_name
    file_name = input("Enter file_name: ")
    p.read_json_file(file_name)

@Validation.validate_inp
def sort_elements(p):
    p.sort(input("Enter field for which you want to sort: \n"
                               "POSSIBLE: title, image_url, price, created_at, updated_at, description, ID:\n"))

@Validation.validate_inp
def search_elements(p):
    parameter = input("Enter parameter which elements you want to find: \n")
    for e in p.search(parameter):
        print(e)

@Validation.validate_inp
def add_product(p):
    d = Product.input_product("title", "image_url", "price", "created_at", "updated_at", "description", "u_id")
    p.append(Product(**d))

@Validation.validate_inp
def del_product(p):
    p.delete(input("Enter id to delete: "))

@Validation.validate_inp
def edit_product(p):
    p.edit(input("Enter id to edit: "), input("Enter atter to edit: "), input("Enter value to change: "))

@Validation.validate_inp
def write_in_txt_file(p):
    p.write_in_file(input("Enter file_name: "))

@Validation.validate_inp
def write_in_json_file(p):
    p.write_in_json_file(file_name)

@Validation.validate_inp
def undo_moment(c):
    c.undo()

@Validation.validate_inp
def redo_moment(c):
    c.redo()

@Validation.validate_inp
def move_moment(c):
    c.show_history()
    mo = input("Enter moment: ")
    c.move_on_moment(mo)


if __name__ == "__main__":
    menu()
