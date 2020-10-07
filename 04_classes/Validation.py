
from datetime import datetime


class Validation:
    """Class for Validation representation."""

    @staticmethod
    def validateStr(value):
        if any(map(str.isdigit, value)):
            raise ValueError("Title must not contain integers.")
        return value

    @staticmethod
    def validatePrice(value):
        try:
            float(value)
        except ValueError:
            raise ValueError("Price must be float of int.")
        return float(value)

    @staticmethod
    def validateDate(date):
        datetime.strptime(date, '%Y-%m-%d')
        return date

    @staticmethod
    def validateImage_url(value):
        VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
        if not any([value.endswith(e) for e in VALID_IMAGE_EXTENSIONS]):
            raise ValueError("Not valid image URL.")
        return value

    @staticmethod
    def isBiggerDate(date1, date2):
        if date1 > date2:
            raise ValueError("Incorrect data, created_at must be lover than updated_at.")

    @staticmethod
    def validateTxtFileName(filename, end=".txt"):
        if not filename.endswith(end):
            raise ValueError("Incorrect filename, should end with .txt.")
        return filename

    @staticmethod
    def validate_inp(func, m):
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
