import unittest
from regexpy.regex import Regex

class InterfaceTests(unittest.TestCase):
    def test_0_regexMatching(self):
        self.assertTrue(Regex.match("abcdfffff", "((a|b)*c*)(d|f)*c*"))
        self.assertFalse(Regex.match("abcdfffff", "a*"))
    
    def test_1_regexValidation(self):
        regex = Regex("((a|b)*c*)(d|f)*c*")
        self.assertTrue(regex.validate("abcdfffff"))
        self.assertFalse(regex.validate("z"))
        
    @staticmethod
    def runTests():
        unittest.main()