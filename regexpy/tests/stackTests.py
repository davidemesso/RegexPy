import unittest
from regexpy.utils.stack import Stack

class StackTests(unittest.TestCase):
    def test_0_pushAndPop(self):
        stack = Stack()
        stack.push("pushed")
        stack.push("pushed")
        self.assertEqual(stack.pop(), "pushed")
        self.assertEqual(stack.size(), 1)
        stack.pop()
        self.assertEqual(stack.pop(), None)
        self.assertTrue(stack.isEmpty())
        
    
    def test_1_peek(self):
        stack = Stack()
        stack.push("pushed")
        self.assertEqual(stack.peek(), "pushed")
        self.assertFalse(stack.isEmpty())
        
    @staticmethod
    def runTests():
        unittest.main()