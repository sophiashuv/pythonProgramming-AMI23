import os

class Validation:

    @staticmethod
    def validateInt(n):
        try:
            n = int(n)
            if n < 0:
                raise ValueError("Input must be a positive integer!")
        except ValueError:
            raise ValueError("Not an integer!")
        return n

    @staticmethod
    def validateLowHeight(pair):
        try:
            if pair[0] > pair[1]:
                raise ValueError("Low int must be lover than height.")
        except IndexError:
            raise ValueError("Low and height mast two be integers.")
        return pair

    @staticmethod
    def validateFileName(filename, end=".txt"):
        if not filename.endswith(end):
            raise ValueError("Incorrect filename, should end with ." + end + ".")
        if not os.path.isfile(filename):
            raise FileNotFoundError("There's no such" + filename + " file")
        return filename

    @staticmethod
    def validateListGeneration(context):
        if context == None:
            raise UnboundLocalError("You need to choose type of generation first.")
        return context

    @staticmethod
    def validate_inp(func):
        def validate_inpWrapper(*l):
            while True:
                try:
                    func(*l)
                    break
                except UnboundLocalError as e:
                    print(e)
                    print("Try one more time!")
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
                except IndexError as e:
                    print(e)
                    print("Try one more time!")
                    continue
        return validate_inpWrapper
