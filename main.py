import sys
from regexpy.regex import Regex

if len(sys.argv) != 3:
    print("Error: WRONG PARAMS COUNT")
    sys.exit(1)

regex = sys.argv[2].strip()
string = ""
try:
    string = sys.argv[1]
except:
    pass

#print(Regex.match("abcdfffff", "((a|b)*c*)(d|f)*"))
print(Regex("((a|b)*c*)(d|f)*")._REGEXFSM_)
print(Regex.match(string, regex))

