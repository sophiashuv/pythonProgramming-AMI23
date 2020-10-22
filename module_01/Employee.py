# Створити клас Employee, який містить такі поля
#  1. Name (Тільки літери)
#  2. Salary (Число з 2 знаками після коми)
#  3. FirstWorkingDate (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: 05.08.2015
#  4. LastWorkingDate Null or (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: StartDate + 3 months

from Validation import Validation

class Employee(object):
    """Class for Employee representation."""

    def __init__(self, **kwargs):

        for (prop, default) in kwargs.items():
            setattr(self, prop, kwargs.get(prop, default))



    @property
    def Name(self):
        return self._Name

    @Name.setter
    @Validation.validateName
    def Name(self, value):
        self._Name = value

    @property
    def Salary(self):
        return self._Salary

    @Salary.setter
    @Validation.validateSalary
    def Salary(self, value):
        self._Salary = value

    @property
    def FirstWorkingDate(self):
        return self._FirstWorkingDate

    @FirstWorkingDate.setter
    @Validation.validateDate
    def FirstWorkingDate(self, value):
        self._FirstWorkingDate = value

    @property
    def LastWorkingDate(self):
        return self._LastWorkingDate

    @LastWorkingDate.setter
    @Validation.validateLastDate
    @Validation.isBiggerDate
    def LastWorkingDate(self, value):
        self._LastWorkingDate = value

    def __get_dictionary(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__')
                    and not name.startswith('_') and name != "input_product" and name != "pricePer" and name != "years")

    @staticmethod
    def input_product(*args):
        d = dict((prop, input(prop + " : ")) for prop in args)
        return d

    def pricePer(self):
        if self.LastWorkingDate == 'Null': return None
        delta = self.FirstWorkingDate.DaysCount(self.LastWorkingDate)
        ost = (delta%6)
        return self.Salary * (1.15**(delta//6))*(1 + ost)

    def years(self):
        return int(self.FirstWorkingDate.DaysCount(self.LastWorkingDate))

    def __str__(self):
        """
        (Employee)->(str)
        returns a string representing Employee.
         """
        return "Employee:\n" + '\n'.join("%s : %r" % (key2, str(val2)) for (key2, val2)
                                        in self.__get_dictionary().items()) + "\n"
