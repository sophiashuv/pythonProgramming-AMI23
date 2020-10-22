from calendar import monthrange
import re
from Date import Date

# Створити клас Employee, який містить такі поля
#  1. Name (Тільки літери)
#  2. Salary (Число з 2 знаками після коми)
#  3. FirstWorkingDate (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: 05.08.2015
#  4. LastWorkingDate Null or (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: StartDate + 3 months

class Validation:
    """Class for Validation representation."""

    @staticmethod
    def validateName(func):
        def validateStrWrapper(emp, value):
            if any(map(str.isdigit, value)):
                raise ValueError("Name must not contain integers.")
            return func(emp, value)
        return validateStrWrapper

    @staticmethod
    def validateSalary(func):
        def validateSalaryWrapper(emp, value):
            try:
                v = float(value)
                a = value.split('.')
                if len(a) == 2:
                    if len(a[1]) > 2: raise ValueError("Salary must have two digits after coma.")
            except ValueError:
                raise ValueError("Salary must be float of int and must have two digits after coma!")
            return func(emp, v)
        return validateSalaryWrapper

    @staticmethod
    def validateDate(func):
        def validateDateWrapper(emp, date):
            try:

                day, month, year = date.split(".")
                date = Date(day, month, year)
            except ValueError:
                raise ValueError("Incorrect date format.")
            return func(emp, date)
        return validateDateWrapper

    @staticmethod
    def validateLastDate(func):
        def validateDateWrapper(emp, date):
            if date != "Null":
                try:
                    day, month, year = date.split(".")
                    date = Date(day, month, year)
                except ValueError:
                    raise ValueError("Incorrect date format.")

            return func(emp, date)

        return validateDateWrapper


    @staticmethod
    def isBiggerDate(func):
        def isBiggerDateWrapper(emp, date2):
            if date2 != "Null":
                if emp.FirstWorkingDate.DaysCount(date2) < 3*31:
                    raise ValueError("Incorrect data, FirstWorkingDate must be lover than LastWorkingDate.")
            func(emp, date2)
        return isBiggerDateWrapper

    @staticmethod
    def validateFileName(end=".txt"):
        def validateFileNameDecorator(func):
            def validateFileNameWrapper(L, filename):
                if not filename.endswith(end):
                    raise ValueError("Incorrect filename, should end with ." + end + ".")
                return func(L, filename)
            return validateFileNameWrapper
        return validateFileNameDecorator



    @staticmethod
    def validateDiapazonWrapper(L, b, date1, date2):
        day, month, year = date1.split(".")
        date1 = Date(day, month, year)
        day, month, year = date2.split(".")
        date2 = Date(day, month, year)
        res = {}
        for v in L:
            try:
                res[str(v.FirstWorkingDate.month) + "." + str(v.FirstWorkingDate.year)] += 1
            except KeyError:
                res[str(v.FirstWorkingDate.month) + "." + str(v.FirstWorkingDate.year)] = 1
        print(res)
        try:
            res[str(b.FirstWorkingDate.month) + "." + str(b.FirstWorkingDate.year)] += 1
        except KeyError:
            res[str(b.FirstWorkingDate.month) + "." + str(b.FirstWorkingDate.year)] = 1

        if res[str(b.FirstWorkingDate.month) + "." + str(b.FirstWorkingDate.year)] > (len(res) + 1)*0.2:
            raise ValueError("You can't add employee with this FirstWorkingDate")

        for v in L:
            if (v.LastWorkingDate != "Null"):
                try:
                    res[str(v.LastWorkingDate.month) + "." + str(v.LastWorkingDate.year)] += 1
                except KeyError:
                    res[str(v.LastWorkingDate.month) + "." + str(v.LastWorkingDate.year)] = 1

        if b.LastWorkingDate != "Null":
            try:
                res[str(b.LastWorkingDate.month) + "." + str(b.LastWorkingDate.year)] += 1
            except KeyError:
                res[str(b.LastWorkingDate.month) + "." + str(b.LastWorkingDate.year)] = 1

            if res[str(b.LastWorkingDate.month) + "." + str(b.LastWorkingDate.year)] > (len(res) + 1)*0.2:
                raise ValueError("You can't add employee with this LastWorkingDate")

        return b


    @staticmethod
    def chack_diapasone(l, date1, date2):
        for i in l:
            if i.FirstWorkingDate.greater(date1) and date2.greater(i.EndDate):
                return True

    @staticmethod
    def validate_inp(func):
        def validate_inpWrapper(m):
            while True:
                try:
                    func(m)
                    break
                except ValueError as e:
                    print(e)
                    print("Try one more time!")
                    continue
                except AttributeError as e:
                    print(e)
                    print("Try one more time!")
                    continue
                except NameError as e:
                    print(e)
                    print("Try one more time!")
                    continue
                except FileNotFoundError as e:
                    print(e)
                    print("Try one more time!")
                    continue

        return validate_inpWrapper
