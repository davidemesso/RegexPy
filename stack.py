class Stack():
    def __init__(self, list = []):
        self._stack = list
        
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

