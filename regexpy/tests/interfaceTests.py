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
        regex.regex = "a*"
        self.assertTrue(regex.validate("aaa"))
        self.assertFalse(regex.validate("z"))
        
    def test_2_matchAny(self):
        self.assertTrue(Regex.matchAny("aaa", ["a*", "b*"]))
        self.assertFalse(Regex.matchAny("aaa", ["b*", "c*"]))
    
    def test_2_matchAll(self):
        self.assertTrue(Regex.matchAll("aaa", ["a*", "(a|b)*"]))
        self.assertFalse(Regex.matchAll("aaa", ["a*", "b*"]))
        
    @staticmethod
    def runTests():
        unittest.main()