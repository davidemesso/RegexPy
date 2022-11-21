class Stack():
    def __init__(self):
        self._stack = []
        
    def push(self, item):
        self._stack.append(item)
        
    def isEmpty(self):
        return not self._stack

    def pop(self):
        if(self.isEmpty()):
            return None
        return self._stack.pop()

    def peek(self):
        if(self.isEmpty()):
            return None
        return self._stack[-1]

    def size(self):
        return len(self._stack)

    def __str__(self):
        toString = ""
        for el in self._stack:
            toString += f"{el} "
        return toString