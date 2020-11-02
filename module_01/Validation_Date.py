from calendar import monthrange


#  3. FirstWorkingDate (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: 05.08.2015
#  4. LastWorkingDate Null or (Клас Date, що містить 3 поля: день (1-31 / 1-30 / 1-29 / 1-28), місяць (1-12) рік (2020+). Min: StartDate + 3 months


class ValidationDate:
    """Class for Validation representation."""

    @staticmethod
    def validateDay(func):
        def validateDayWrapper(date, day):
            try:
                if int(day) > monthrange(date.year, date.month)[1]:
                    raise ValueError("Incorrect month.")
                if date.year == 2015 and date.month < 8:
                    raise ValueError("Incorrect date.")
                if date.year == 2015 and date.month == 8 and int(day) < 5:
                    raise ValueError("Incorrect date.")
            except ValueError:
                raise ValueError("Incorrect day.")
            return func(date, int(day))
        return validateDayWrapper

    @staticmethod
    def validateMonth(func):
        def validateMonthWrapper(date, month):
            try:
                if int(month) < 1 or int(month) > 12:
                    raise ValueError("Incorrect month.")
            except ValueError:
                raise ValueError("Incorrect month.")
            return func(date, int(month))
        return validateMonthWrapper

    @staticmethod
    def validateYear(func):
        def validateYearWrapper(date, year):
            try:
                if int(year) < 2015:
                    raise ValueError("Incorrect Year.")
            except ValueError:
                raise ValueError("Incorrect Year.")
            return func(date, int(year))
        return validateYearWrapper


