class Stack():
    """Stack implementation specific for Regex use case.
    None is used as return instead of explicit error for implementation choice.
    In this case it's implicit it will never be pushed
    """
    
    def __init__(self):
        """Stack constructor"""
        self._stack = []
        
    def push(self, item):
        """Pushes one item to the stack"""
        self._stack.append(item)
        
    def isEmpty(self):
        """Returns whether the stack is empty or not"""
        return not self._stack

    def pop(self):
        """Returns and removes the first item in the stack"""
        if(self.isEmpty()):
            return None
        return self._stack.pop()

    def peek(self):
        """Returns the first item in the stack without removing it"""
        if(self.isEmpty()):
            return None
        return self._stack[-1]

    def size(self):
        """Returns the number of items in the stack"""
        return len(self._stack)

    def __str__(self):
        """To string"""
        toString = ""
        for el in self._stack:
            toString += f"{el} "
        return toString