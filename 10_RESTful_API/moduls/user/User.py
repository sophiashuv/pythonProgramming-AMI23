from Validation import Validation


class User(object):
    """Class for User representation."""
    def __init__(self, **kwargs):
        for (prop, default) in kwargs.items():
            setattr(self, prop, kwargs.get(prop, default))

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    @Validation.validateStr
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    @Validation.validateStr
    def last_name(self, value):
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    @Validation.validateMail
    def email(self, value):
        self._email = value

    def __get_dictionary(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__')
                    and not name.startswith('_'))

    def __str__(self):
        return "User:\n" + '\n'.join("%s : %r" % (key2, str(val2)) for (key2, val2)
                                        in self.__get_dictionary().items()) + "\n"
