from datetime import datetime
import re


class Validation:
    """Class for Validation representation."""

    @staticmethod
    def validateStr(func):
        def validateStrWrapper(product, value):
            if any(map(str.isdigit, value)):
                raise ValueError("Title must not contain integers.")
            return func(product, value)
        return validateStrWrapper

    @staticmethod
    def validatePrice(func):
        def validatePriceWrapper(product, value):
            try:
                v = float(value)
                if re.match(r'[0-9]*\.[0-9]{2}', value):
                    raise ValueError("Price must have two digits after coma.")
            except ValueError:
                raise ValueError("Price must be float of int and must have two digits after coma!")
            return func(product, value)
        return validatePriceWrapper

    @staticmethod
    def validateDate(func):
        def validateDateWrapper(product, date):
            datetime.strptime(date, '%Y-%m-%d')
            return func(product, date)
        return validateDateWrapper

    @staticmethod
    def validateImage_url(func):
        def validateImage_urlWrapper(product, value):
            VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
            if not any([value.endswith(e) for e in VALID_IMAGE_EXTENSIONS]):
                raise ValueError("Not valid image URL.")
            return func(product, value)
        return validateImage_urlWrapper

    @staticmethod
    def isBiggerDate(func):
        def isBiggerDateWrapper(product, date2):
            if product.created_at > date2:
                raise ValueError("Incorrect data, created_at must be lover than updated_at.")
            func(product, date2)
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
    def validateInt(func):
        def validateIntWrapper(moment, value):
            try:
                v = int(value)
            except ValueError:
                raise ValueError("Not an integer.")
            return func(moment, v)
        return validateIntWrapper

    @staticmethod
    def validateMail(func):
        def validateMailWrapper(_self, val):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", val):
                raise ValueError('Incorrect Email')
            func(_self, val)
        return validateMailWrapper

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
                    break
                except NameError as e:
                    print(e)
                    print("Try one more time!")
                    continue
                except FileNotFoundError as e:
                    print(e)
                    print("Try one more time!")
                    continue

        return validate_inpWrapper
