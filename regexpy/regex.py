from regexpy.utils.fsmutils import *

class Regex:
    def __init__(self, regex):
        self._REGEXFSM_ = FSMUtils.fromRegex(regex).subsetConstruction()
    
    def validate(self, string):
        return self._REGEXFSM_.checkRegex(string)
    
    @staticmethod
    def match(string, regex):
        if not regex:
            return False
        
        try:
            return FSMUtils.fromRegex(regex).subsetConstruction().checkRegex(string)
        except:
            return False
        
        
if __name__ == "__main__":
    from time import time  
  
    def timeit(func):
        def wrap_func(*args, **kwargs):
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            print(f'Function {func.__name__} executed in {t2-t1}s')
            return result
        return wrap_func
    
    @timeit
    def testStatic(n):
        for _ in range(n):
            Regex.match("abcdfffff", "((a|b)*c*)(d|f)*")
    
    @timeit        
    def testInstance(n, regexObj):
        for _ in range(n):
            regexObj.validate("abcdfffff")
            

    testStatic(100)
    
    regex = Regex("((a|b)*c*)(d|f)*")
    testInstance(100, regex)