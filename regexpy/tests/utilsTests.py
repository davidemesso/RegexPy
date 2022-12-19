import unittest
from regexpy.utils.fsmutils import *

class UtilsTests(unittest.TestCase):
    def test_0_fromCharacter(self):
        matchesA = FSMUtils.fromCharacter("a").subsetConstruction()
        self.assertTrue(matchesA.checkRegex("a"))
        self.assertFalse(matchesA.checkRegex("b"))
        
    def test_1_starClosure(self):
        matchesA = FSMUtils.fromCharacter("a")
        matchesAStar = FSMUtils.starClosure(matchesA).subsetConstruction()
        self.assertTrue(matchesAStar.checkRegex(""))
        self.assertTrue(matchesAStar.checkRegex("aaa"))
        self.assertFalse(matchesAStar.checkRegex("b"))
        
    def test_2_union(self):
        matchesA = FSMUtils.fromCharacter("a")
        matchesB = FSMUtils.fromCharacter("b")
        matchesAorB = FSMUtils.union(matchesA, matchesB).subsetConstruction()
        self.assertTrue(matchesAorB.checkRegex("a"))
        self.assertTrue(matchesAorB.checkRegex("b"))
        self.assertFalse(matchesAorB.checkRegex("c"))
        
    def test_3_concat(self):
        matchesA = FSMUtils.fromCharacter("a")
        matchesB = FSMUtils.fromCharacter("b")
        matchesAorB = FSMUtils.concat(matchesA, matchesB).subsetConstruction()
        self.assertTrue(matchesAorB.checkRegex("ab"))
        self.assertFalse(matchesAorB.checkRegex("c"))
        
    def test_4_fromRegex(self):
        matchesRegex = FSMUtils.fromRegex("((a|b)*c*)(d|f)*").subsetConstruction()
        self.assertTrue(matchesRegex.checkRegex("abcdfffff"))
        
    @staticmethod
    def runTests():
        unittest.main()