from time import time
from regexpy.regex import Regex
  
def timeit(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__} executed in {t2-t1:4f} s')
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