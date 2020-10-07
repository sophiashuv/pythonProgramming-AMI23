# Клас ПРОДУКТ з полями: ID, title, image_url, price, created_at (date), updated_at (date), description.

from Validation import Validation


class Product(object):
    """Class for Product representation."""
    def __init__(self, **kwargs):
        for (prop, default) in kwargs.items():
            setattr(self, prop, kwargs.get(prop, default))

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = Validation.validateStr(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = Validation.validatePrice(value)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = Validation.validateDate(value)

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value):
        Validation.isBiggerDate(self._created_at, value)
        self._updated_at = Validation.validateDate(value)

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, value):
        self._image_url = Validation.validateImage_url(value)

    def __get_dictionary(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__')
                    and not name.startswith('_') and name != "input_product")
    @staticmethod
    def input_product(*args):
        d = dict((prop, input(prop + " : ")) for prop in args)
        return d

    def __str__(self):
        """
        (Product)->(str)
        returns a string representing Product.
         """
        return "Product:\n" + '\n'.join("%s : %r" % (key2, str(val2)) for (key2, val2)
                                        in self.__get_dictionary().items()) + "\n"
