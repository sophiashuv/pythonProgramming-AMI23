import doctest

import One_dimensional_arrays as arr


def get_sorted_arr_and_indexes(unsorted_arr, n):
    """
    The function returns a sorted array and indexes of argument in array
    >>> get_sorted_arr_and_indexes([1, 5, 3, 2, 7, 8, 2], 7)
    ([1, 2, 2, 3, 5, 7, 8], [0, 3, 6, 2, 1, 4, 5])
    """
    d = dict(sorted(zip(list(range(n)), unsorted_arr), key=lambda x: x[1]))
    indexes, sorted_arr = list(d.keys()), list(d.values())
    return sorted_arr, indexes


def check_left(array, mid, start):
    """
    The function checks if there are elements same as array[mid] left in sorted array.
    """
    global ind, lst, message
    i = 1
    while mid + i > start and array[mid] == array[mid - i]:
        lst.append(mid - i)
        i += 1
    message += "Check left " + str(i + 1) + " times.\n"
    ind += i + 1


def check_right(array, mid, end):
    """
    The function checks if there are elements same as array[mid] right in sorted array.
    """
    global ind, lst, message
    i = 1
    while mid + i < end and array[mid] == array[mid + i]:
        lst.append(mid + i)
        i += 1
    message += "Check right " + str(i + 1) + " times.\n"
    ind += i + 1


def binary_search(array, element, start, end):
    """
    Binary search recursive algorithm, fills global variable with all necessary information.
    Return: indexes of element in sorted array.
    eg. input: binary_search([1, 2, 3, 3, 3, 4, 5, 5], 3, 0, 7)
    [3, 4, 2]
    eg. input: binary_search([1, 2, 3, 3, 3, 4, 5, 5], 8, 0, 7)
    None
    """
    global ind, lst, message
    if start > end:
        return None

    mid = (start + end) // 2

    ind += 1
    message += str(ind) + ". Check if element is in " + str(mid) + "\n"
    if element == array[mid]:
        lst.append(mid)
        check_right(array, mid, end)
        check_left(array, mid, start)
        return lst

    ind += 1
    message += str(ind) + ". Check if element is between " + str(start) + " " + str(mid-1) + "\n"
    if element < array[mid]:
        return binary_search(array, element, start, mid-1)

    else:
        ind += 1
        message += str(ind) + ". Check if element is between " + str(mid + 1) + " " + str(end) + "\n"
        return binary_search(array, element, mid+1, end)


def output(list_array, sorted_arr, sorted_indexes, indexes, el):
    """
    The function prints results.
    """
    print("ARRAY: " + str(list_array))
    print("SORTED ARRAY: " + str(sorted_arr))
    if indexes is not None:
        print("POSITIONS IN ARRAY OF " + str(el) + ": " + str(indexes) + ".")
        print("POSITIONS IN SORTED ARRAY OF " + str(el) + ": " + str(sorted_indexes) + ".")
    else:
        print("There's no " + str(el) + " in array.")
    print("NUMBER OF OPERATIONS: " + str(ind))
    print("\nOPERATIONS: \n" + message)


def get_indexes(list_array, el):
    """
    The function returns sorted array, indexes of el in argument array and indexes of el in sorted array.
    """
    n = len(list_array)
    sorted_arr, indexes = get_sorted_arr_and_indexes(list_array, n)

    sorted_indexes = binary_search(sorted_arr, el, 0, n-1)
    if sorted_indexes is None:
        real_indexes = None
    else:
        real_indexes = list(map(indexes.__getitem__, sorted_indexes))
    return sorted_arr, real_indexes, sorted_indexes


def func(list_array):
    """
    The main function that outputs all info.
    """
    global ind, lst, message
    ind, lst, message = 0, [], ""
    el = arr.n_input("Enter element to search: ", "none")
    sorted_arr, indexes, sorted_indexes = get_indexes(list_array, el)
    output(list_array, sorted_arr, sorted_indexes, indexes, el)


if __name__ == "__main__":
    arr.menu(func)

    doctest.testmod()
