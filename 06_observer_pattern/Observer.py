class Logger:
    """
    Class to log events into file.
    """
    line = 0

    @staticmethod
    def write_to_file(li, file_name="logs.txt"):
        f = open(file_name, 'a')
        f.write(str(Logger.line) + " " + str(li) + '\n')
        f.close()
        Logger.line += 1


class Observer:
    """
    Class for Observer representation
    """
    _observers = []

    def __init__(self):
        self._observers.append(self)
        self._observables = {}

    def observe(self, event_name, callback=Logger.write_to_file):
        self._observables[event_name] = callback


class Event:
    """
    Class for Event representation
    """
    def __init__(self, name, changed, changes, par=None, log=True):
        self.name = name
        self.changed = changed
        self.changes = changes
        self.par = par

        if log:
            self.log_event()

    def log_event(self):
        for observer in Observer._observers:
            if self.name in observer._observables:
                observer._observables[self.name](self)

    def __str__(self):
        return "Event({}, ( {}, {}, {} ))".format(self.name, self.changed, self.changes, self.par)
