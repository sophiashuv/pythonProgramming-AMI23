# Варіант 2
# Створити клас Employee, який містить такі поля
#  1. Name (Тільки літери)
#  2. Salary (Число з 2 знаками після коми)
#  3. FirstWorkingDate (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: 05.08.2015
#  4. LastWorkingDate Null or (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: StartDate + 3 months
# Створити такі методи:
#  1. Зчитати масив (клас для роботи з масивом екземплярів класу Employee) Employee з файла (1)
#  2. Додати новий Employee. В один місяць може влаштуватись на роботу і звільнитись не більше, ніж 20% всього персоналу(3)
#  3. Додати валідацію на поля Name, Salary, FirstWorkingDate, LastWorkingDate (2.5)
#  4. Обрахувати витрати компанії на заробітню платню сумарно всіх працівників (вважається, що кожних 6 місяців працівник отримує заробітню платню вищу на 15%) (1.5)
#  5. Всіх працівників, які відпрацювали рівно 1, 2, … років потрібно записати в інший файл: Ім’я працівника, 1 рік і так далі  (1.5)
#  6. Вивести всі Employee на екран (0.5)

import json
from Validation import Validation
from Employee import Employee


def menu():
    """
    The menu function.
    """
    lst = []
    while True:
        help_message = get_help_message()
        task = input(help_message)
        if task == "1":
            read_file(lst)
        elif task == "2":
            addEmployee(lst)
        elif task == "3":
            print(comp_price(lst))
        elif task == "4":
            write_file(lst)
        elif task == "5":
            print_lst(lst)
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
    help_message = "*" * 61
    help_message += "\n*  HELP:" + 52 * " " + "*\n*  Possible commands:" + 39 * " " + \
                    "*\n*  1 - to read from file." + 35 * " " + \
                    "*\n*  2 - to add new employee. " + 32 * " " + \
                    "*\n*  3 - to calculate the company's costs.  " + 18 * " " + \
                    "*\n*  4 - to write to file employees who worked 1, 2, … years. " + 0 * " " + \
                    "*\n*  5 - to print employee." + 35 * " " + \
                    "*\n*  exit - to exit.  " + 40 * " " + "*\n"
    help_message += "*" * 61 + "\n"
    return help_message


@Validation.validateFileName(end='.json')
def read_json_file(lst, file_name="data.json"):
    f = open(file_name, encoding='utf-8')
    file = json.load(f)
    for i, employee in enumerate(file):
        try:
            lst.append(Employee(**employee))
        except ValueError as e:
            print("Line" + str(i * (len(employee) + 1) + 3) + ": " + str(e))
            continue
        except AttributeError as e:
            print("Line" + str(i * (len(employee) + 1) + 3) + ": " + str(e))
            continue
    f.close()


@Validation.validate_inp
def read_file(l):
    file_name = input("Enter FileName: ")
    read_json_file(l)

@Validation.validate_inp
def addEmployee(l):

    d = Employee.input_product("Name", "FirstWorkingDate", "LastWorkingDate", "Salary")
    # d["PricePerDay"] = price
    d = Employee(**d)
    l.append(Validation.validateDiapazonWrapper(l, d))


def comp_price(l):
    sum = 0
    for i in l:
        sum += i.pricePer()
    return sum

@Validation.validateFileName('.txt')
def write_in_txt_file(L, file_name="hj.txt"):
    f = open(file_name, mode='w', encoding="utf-8")
    d = []
    for i in L:
        if i.FirstWorkingDate.DaysCount(i.LastWorkingDate):
            d.append(i)
            y = i.years()
            d.append("years : " + str(y//365))

    f.writelines(str(i) + "\n" for i in d)
    f.close()


@Validation.validate_inp
def read_file(l):
    read_json_file(l, "data.json")


@Validation.validate_inp
def write_file(l):
    file_name = input("Enter FileName: ")
    write_in_txt_file(l, file_name)


def print_lst(l):
    for i in l:
        print(i)

if __name__ == "__main__":
    menu()

