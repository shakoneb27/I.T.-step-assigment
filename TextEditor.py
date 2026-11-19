class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, data):
        node = Node(data)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def insert_at(self, index, data):
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        if index == self._size:
            self.append(data)
            return
        node = Node(data)
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            node.next = prev.next
            prev.next = node
        self._size += 1

    def delete_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        if index == 0:
            removed = self.head
            self.head = removed.next
            if self.head is None:
                self.tail = None
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            removed = prev.next
            prev.next = removed.next
            if removed is self.tail:
                self.tail = prev
        self._size -= 1
        return removed.data

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next


class TextEditor:
    def __init__(self):
        self._lines = SinglyLinkedList()
        self._undo_stack = []
        self._redo_stack = []

    def add_line(self, text):
        self.insert_line(len(self._lines), text)

    def insert_line(self, index, text):
        self._lines.insert_at(index, text)  
        self._undo_stack.append(("insert", index, text))
        self._redo_stack.clear()

    def delete_line(self, index):
        text = self._lines.delete_at(index) 
        self._undo_stack.append(("delete", index, text))
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return
        action, index, text = self._undo_stack.pop()
        if action == "insert":
            self._lines.delete_at(index)
        else:
            self._lines.insert_at(index, text)
        self._redo_stack.append((action, index, text))

    def redo(self):
        if not self._redo_stack:
            return
        action, index, text = self._redo_stack.pop()
        if action == "insert":
            self._lines.insert_at(index, text)
        else:
            self._lines.delete_at(index)
        self._undo_stack.append((action, index, text))

    def show(self):
        for i, line in enumerate(self._lines, start=1):
            print(f"{i}: {line}")


if __name__ == "__main__":
    ed = TextEditor()
    ed.add_line("A"); ed.add_line("B"); ed.add_line("C")
    ed.delete_line(1)     
    ed.undo()             
    ed.undo()           
    ed.redo()              
    ed.add_line("D")       
    ed.redo()              
    ed.show()
