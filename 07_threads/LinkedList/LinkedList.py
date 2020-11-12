from LinkedList.Node import *

# A class implementing LinkedList as a linked list.


class LinkedList:
    def __init__(self):
        """
        Produces a newly constructed empty LinkedList.
        __init__: -> LinkedList
        Field: _head points to the first node in the linked list
        """
        self._head = None

    def IsEmpty(self):
        """
        Checks emptiness of LinkedList.
        empty: LinkedList -> Bool
        :return: True if LinkedList is empty and False otherwise.
        """
        return self._head is None

    def __iter__(self):
        """
        Iterates through LinkedList
        __iter__: -> LinkedList
        """
        current = self._head
        while current:
            yield current
            current = current.next

    def __contains__(self, value):
        """
        Checks existence of value in the LinkedList.
        __contains__: LinkedList Any -> Bool
        :param value: the value to be check.
        :return: True if LinkedList is in the LinkedList and False otherwise.
        """
        current = self._head
        while current:
            if current.item == value:
                return True
            else:
                current = current.next
        return False

    def __len__(self):
        """
        Returns len of list
        __len__: LinkedList -> int
        :return: amount of elements in list
        """
        current = self._head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def __getitem__(self, index):
        """
        Returns element on index
        __getitem__: LinkedList, int -> Node
        :return: amount of elements in list
        """
        pos = 0
        current = self._head
        if self.__len__() <= index:
            raise IndexError('Not such index in LinkedList')
        while pos is not index:
            current = current.next
            pos += 1
        return current

    def __setitem__(self, index, item):
        """
        Sets item on index
        __setitem__: LinkedList, int, item ->
        """
        pos = 0
        current = self._head
        if self.__len__() <= index:
            raise IndexError('Not such index in LinkedList')
        while pos is not index:
            current = current.next
            pos += 1
        current.item = item

    def __str__(self):
        """
        Prints tLinkedList.
        __str__: LinkedList -> Str
        """
        result = "["
        current = self._head
        if current:
            result += str(current.item)
            current = current.next
            while current:
                result += ", " + str(current.item)
                current = current.next
        result += "]"
        return result

    def index(self, item):
        """
        Search last for element in LinkedList
        index: LinkedList item -> int
        :return: index of element in LinkedList
        """
        pos = 0
        current = self._head
        found = False
        while current and not found:
            if current.item == item:
                found = True
            else:
                current = current.next
                pos += 1
        if not found:
            raise ValueError('Value not present in the LinkedList')
        return pos

    def addFront(self, other):
        """
        Adds the value to begin of the LinkedList.
        addFront: LinkedList other ->
        """
        if self._head is None:
            self._head = Node(other)
        else:
            rest = self._head
            self._head = Node(other)
            self._head.next = rest

    def append(self, other):
        """
        Adds the value to the end of the LinkedList.
        append: LinkedList other ->
        """
        current = self._head
        if current:
            while current.next:
                current = current.next
            current.next = Node(other)
        else:
            self._head = Node(other)

    def insert(self, item, position):
        """
        Inserts element on position.
        insert: LinkedList item int ->
        """
        if position > self.__len__() or position < 0:
            raise IndexError('Not such index in LinkedList')
        if position == 0:
            self._head = Node(item, self._head)
        elif position == self.__len__():
            self.append(item)
        else:
            i = 0
            current = self._head
            while current.next:
                if i == position - 1:
                    current.next = Node(item, current.next)
                current = current.next
                i += 1

    def count_amount(self, search_for):
        """
        Counts the amount of times element occurs in LinkedList
        count_amount: LinkedList search_for -> int
        :return: amount of search_for
        """
        current = self._head
        count = 0
        while current:
            if current.item == search_for:
                count += 1
            current = current.next
        return count

    def copy(self):
        """
        Copies a LinkedList
        copy: LinkedList -> LinkedList
        :return: copied LinkedList
        """
        result = LinkedList()
        buffer = self._head
        while buffer:
            result.append(buffer.item)
            buffer = buffer.next
        return result

    def reverse(self):
        """
        Reverse a LinkedList
        reverse: LinkedList ->
        """
        previous = None
        current = self._head

        while current.next:
            tmp = current.next
            current.next = previous
            previous = current
            current = tmp
        current.next = previous
        self._head = current

    def delete(self, value):
        """
        Deletes first entrance of value in LinkedList.
        delete: LinkedList value->
        """
        current = self._head
        previous = None
        while current and current.item != value:
            previous = current
            current = current.next
        if current:
            if previous is None:
                self._head = self._head.next
            else:
                previous.next = current.next
        else:
            raise ValueError('Value not present in the LinkedList')

    def delete_index(self, index):
        """
        Deletes by index
        delete_index: LinkedList index->
        """
        i = 0
        current = self._head
        previous = None
        while current and i != index:
            previous = current
            current = current.next
            i += 1
        if current:
            if previous is None:
                self._head = self._head.next
            else:
                previous.next = current.next
        else:
            raise ValueError('Index not present in the LinkedList')

    def delete_between_pos(self, index1, index2):
        """
        Deletes between two positions
        delete_between_pos: LinkedList index1, index2->
        """
        if index2 > self.__len__() or index1 > index2:
            raise ValueError('Index2 not present in the LinkedList and index2 mast be bigger than index1.')
        for i in range(index2 - index1 + 1):
            self.delete_index(index1)

    def pop(self):
        """
        Deletes last element in LinkedList.
        pop: LinkedList->
        """
        current = self._head
        if current is None:
            raise IndexError('Empty LinkedList')
        if current.next is None:
            self.clear()
            return
        while current.next:
            if current.next.next is None:
                current.next = None
            else:
                current = current.next

    def clear(self):
        """
        Clears all LinkedList.
        clear: LinkedList ->
        """
        temp = self._head
        if temp is None:
            raise IndexError('Empty LinkedList')
        while temp:
            self._head = temp.next
            temp = self._head

    def listMethod(self):
        """
        Method that changes all integers that occur once by zero, all first and second entrances all integers that
        occur more than once by 1 and others by 0.
        """
        occurrences = dict(map(lambda num: (num.item, [i for i in range(len(self)) if self[i] == num]), self))
        for el, occur in occurrences.items():
            if len(occur) == 1:
                self[occur[0]] = 0
            else:
                self[occur[0]] = 1
                self[occur[-1]] = 1
                for i in range(1, len(occur) - 1):
                    self[occur[i]] = 0