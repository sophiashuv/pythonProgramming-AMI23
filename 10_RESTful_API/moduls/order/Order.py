from Validation import Validation


class Order(object):
    """Class for Order representation."""
    def __init__(self, **kwargs):
        for (prop, default) in kwargs.items():
            setattr(self, prop, kwargs.get(prop, default))

    @property
    def amount(self):
        return self._amount

    @amount.setter
    @Validation.validateAmount
    def amount(self, value):
        self._amount = value

    def __get_dictionary(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__')
                    and not name.startswith('_'))

    def __str__(self):
        return "User:\n" + '\n'.join("%s : %r" % (key2, str(val2)) for (key2, val2)
                                        in self.__get_dictionary().items()) + "\n"

