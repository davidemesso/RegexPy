import sys
from regexFSM import FSMDeterministic
from regexFSM import FSMNotDeterministic
from regexFSM import FSMUtils
from regexFSM import Regex

if len(sys.argv) not in (1,3):
    print("Error: WRONG PARAMS COUNT")
    sys.exit(1)

regex = sys.argv[1].strip()
string = ""
try:
    string = sys.argv[2]
except:
    pass

print(Regex.match("abcdfffff", "((a|b)*c*)(d|f)*"))
print(Regex.match("abcdfffff", "((a|b)*c*)(d|f)*"))
print(Regex.match(string, regex))

