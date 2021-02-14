# A class implementing a node.


class Node:
    def __init__(self, item, next = None):
        """
        Produces a newly constructed empty node.
        __init__: Any -> Node
        Fields: item stores any value
            next points to the next node in the list
        """
        self.item = item
        self.next = next

    def __eq__(self, other):
        """
        Checks if Node.item is is equal to other item.
        __eq__: Node -> Bool
        """
        return self.item == other

    def __str__(self):
        """
        Prints the value stored in self.
        __str__: Node -> Str
        """
        return str(self.item)
