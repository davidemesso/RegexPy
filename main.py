import sys
from regexFSM import FSMDeterministic
from regexFSM import FSMNotDeterministic
from regexFSM import FSMUtils
from regexFSM import Regex

if len(sys.argv)!=2:
    print("Error: MISSING PARSED REGEX")
    sys.exit(1)

polish_regex = sys.argv[1]
FSM = FSMUtils.fromCharacter(polish_regex[0])
ndFSM = FSM.subsetConstruction()

# print(ndFSM.checkRegex(polish_regex[0]))    # Expected True
# print(ndFSM.checkRegex("zzz"))              # Expected False

#FSM = FSMUtils.starClosure(FSM)
#ndFSM = FSM.subsetConstruction()

# print(Regex.match("ab", polish_regex))      # Expected True
# print(Regex.match("aab", polish_regex))     # Expected False
# print(Regex.match("", polish_regex))        # Expected True
f = FSMUtils.union(FSMUtils.fromCharacter("b",2), FSMUtils.fromCharacter("a"))
print(f)
r = f.subsetConstruction()
print(r)
print(r.checkRegex(""))
print(r.checkRegex("a"))
print(r.checkRegex("b"))
