from Validation import Validation


class Memento:
    """
    Class for Memento representation
    """
    def __init__(self, lst, ms) -> None:
        self._lst = lst
        self._message = ms

    def get_lst(self):
        return self._lst

    def get_name(self) -> str:
        return self._message


class Caretaker:
    """
    Class for Caretaker representation
    """
    SIZE = 6

    def __init__(self, lst) -> None:
        self._mementos = []
        self._lst = lst
        self._current = 0

    def backup(self, ms) -> None:
        if len(self._mementos) == Caretaker.SIZE:
            self._mementos.pop(0)
            self._current -= 1
        self._mementos.append(self._lst.save(ms))
        self._current += 1

    @Validation.validateUndo
    def undo(self) -> None:
        self._current -= 1
        memento = self._mementos[self._current-1]
        self._lst.restore(memento)

    @Validation.validateRedo
    def redo(self) -> None:
        self._current += 1
        memento = self._mementos[self._current-1]
        self._lst.restore(memento)

    @Validation.validateInt
    @Validation.validateMove
    def move_on_moment(self, moment) -> None:
        self._current = moment
        memento = self._mementos[moment-1]
        self._lst.restore(memento)

    def show_history(self) -> None:
        print("The list of mementos:")
        for i, memento in enumerate(self._mementos):
            print(str(i + 1) + ". " + memento.get_name())
        print("You're on " + str(self._current) + " moment.")
