import random
from LinkedList import LinkedList

# Завдання повинно бути виконано з мінімальною кількістю операцій та з використанням функцій.
# Передбачити можливість 2 варіанти введення масивів: ввести кількість елементів та згенерувати
# рандомні елементи, або ввести сам масив. Користувач має мати право вибирати безліч разів один
# чи інший варіант введення та тестувати програму. По закінченню тестування користувач має мати
# змогу вийти з меню.

# Задано масив цілих чисел розмірності n. Створити нову послідовність таким чином,
# що кожне число, яку немає повторень замінити нулями. Всі перші та останні входження
# кожного числа, які мають повторення замінити одиницями, а інші входження - нулями.
# Порахувати кількість нулів та одиниць в утвореній послідовності.


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

        func(list_array)
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
            mas = LinkedList()
            line = input("Enter numbers of array with whitespaces: ")
            for x in line.split():
                mas.append(int(x))
        except ValueError:
            print("Elements of array mast be integers!")
            continue
        break
    return mas


def n_input(message, sign="pos"):
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
        low = n_input("Enter lower pos for random num: ", "none")
        height = n_input("Enter higher pos for random num: ", "none")
        if low > height:
            print("Low must be smaller than height.")
            continue
        return low,  height


def random_arr(n, low, height):
    """
    The function that returns a randomly generated array on certain interval.
    """
    mas = LinkedList()
    for i in range(n):
        mas.append(random.randint(low, height))
    return mas


def occurrence_of_each_elem(nums):
    """
    The function generates dictionary where keys are nums and values are lists of indexes in nums.
    """
    occurrences = dict(map(lambda num: (num.item, [i for i in range(len(nums)) if nums[i] == num]), nums))
    return occurrences


def change_arr(nums, occurrences):
    """
    The function changes array according to rules from task.
    """
    for el, occur in occurrences.items():
        if len(occur) == 1:
            nums[occur[0]] = 0
        else:
            nums[occur[0]] = 1
            nums[occur[-1]] = 1
            for i in range(1, len(occur)-1):
                nums[occur[i]] = 0


def count_zeroes_ones(nums):
    """
    The function counts amount of 0 and 1 in array.
    """
    zeros = nums.count_amount(0)
    ones = nums.count_amount(1)
    return zeros, ones


def output(old_array, new_array):
    """
    The function prints results.
    """
    print("Original array: " + str(old_array))
    print("Changed array: " + str(new_array))
    zeros, ones = count_zeroes_ones(new_array)
    print("Amount of zeroes: " + str(zeros))
    print("Amount of ones: " + str(ones))


def generate_new_array(list_array):
    """
    The function generates new array of changed elements from first one.
    """
    arr_copy = list_array.copy()
    occurrences = occurrence_of_each_elem(arr_copy)
    change_arr(arr_copy, occurrences)
    return arr_copy


def func(list_array):
    """
    The main function that outputs all info.
    """
    changed_arr = generate_new_array(list_array)
    output(list_array, changed_arr)


if __name__ == "__main__":
    menu(func)
