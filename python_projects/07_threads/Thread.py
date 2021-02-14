from threading import Thread
import time


class ExceptionThread(Thread):
    """
    Class representing ExceptionThread
    """

    def run(self):
        self.exc = None
        print("Starting " + self.name)
        self.start = time.clock()

        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout=None):
        super(ExceptionThread, self).join(timeout)

        self.end = time.clock()
        print("Exiting " + self.name)
        print("{}  time was {}".format(self.name, self.end - self.start))

        if self.exc:
            raise self.exc
        return self.ret
