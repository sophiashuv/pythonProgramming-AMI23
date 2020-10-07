from LstCollection import LstCollection
from Product import Product
from Validation import Validation


def menu():
    """
    The menu function.
    """
    p = LstCollection()
    while True:
        help_message = get_help_message()
        task = input(help_message)
        if task == "1":
            Validation.validate_inp(read_file, p)
        elif task == "2":
            Validation.validate_inp(sort_elements, p)
        elif task == "3":
            search_elements(p)
        elif task == "4":
            Validation.validate_inp(add_product, p)
        elif task == "5":
            Validation.validate_inp(del_product, p)
        elif task == "6":
            Validation.validate_inp(edit_product, p)
        elif task == "7":
            Validation.validate_inp(write_in_file, p)
        elif task == "8":
            for product in p:
                print(product)
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
    help_message = "*" * 46
    help_message += "\n*  HELP:" + 37 * " " + "*\n*  Possible commands:" + 24 * " " + \
                    "*\n*  1 - to read from file;" + 20 * " " + \
                    "*\n*  2 - to sort elements; " + 20 * " " + \
                    "*\n*  3 - to to search element.  " + 15 * " " + \
                    "*\n*  4 - to to add Product to collection. " + 5 * " " + \
                    "*\n*  5 - to del element from collection.  " + 5 * " " + \
                    "*\n*  6 - to edit element from collection.  " + 4 * " " + \
                    "*\n*  7 - to write collection elements to file. " \
                    "*\n*  8 - to print collection. " + 17 * " " + \
                    "*\n*  exit - to exit.  " + 25 * " " + "*\n"
    help_message += "*" * 46 + "\n"
    return help_message


def read_file(p):
    p.read_file(Validation.validateTxtFileName(input("Enter file_name: ")))


def sort_elements(p):
    p.sort(input("Enter field for which you want to sort: \n"
                               "POSSIBLE: title, image_url, price, created_at, updated_at, description, ID:\n"))


def search_elements(p):
    parameter = input("Enter parameter which elements you want to find: \n")
    for e in p.search(parameter):
        print(e)


def add_product(p):
    d = Product.input_product("title", "image_url", "price", "created_at", "updated_at", "description", "u_id")
    p.append(Product(**d))


def del_product(p):
    p.delete(input("Enter id to delete: "))


def edit_product(p):
    p.edit(input("Enter id to edit: "), input("Enter atter to edit: "), input("Enter value to change: "))


def write_in_file(p):
    p.write_in_file(Validation.validateTxtFileName(input("Enter file_name: ")))


if __name__ == "__main__":
    menu()
