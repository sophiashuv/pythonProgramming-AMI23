from Validation_Date import ValidationDate
from datetime import date

class Date(object):
    """Class for Booking representation."""

    def __init__(self, day, month, year):
        self.year = year
        self.month = month
        self.day = day

    @property
    def day(self):
        return self._day

    @day.setter
    @ValidationDate.validateDay
    def day(self, value):
        self._day = value

    @property
    def month(self):
        return self._month

    @month.setter
    @ValidationDate.validateMonth
    def month(self, value):
        self._month = value

    @property
    def year(self):
        return self._year

    @year.setter
    @ValidationDate.validateYear
    def year(self, value):
        self._year = value

    def greater(self, date):
        if self.year > date.year: return True
        elif self.year == date.year:
            if self.month > date.month:
                return True
            elif self.month == date.month:
                if self.day > date.day:
                    return True
                else:
                    return False
            else: return False
        else: return False

    def __get_dictionary(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__')
                    and not name.startswith('_') and name != "input_product")

    def DaysCount(self, an_date):
        f_date = date(self.year, self.month, self.day)
        l_date = date(an_date.year, an_date.month, an_date.day)
        delta = l_date - f_date
        return int(delta.days)

    def __str__(self):
        return str(self.day) + "." + str(self.month) + "." + str(self.year)

