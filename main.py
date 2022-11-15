# data = {
#     (0, "e"): {1, 8},
#     (1, "a"): {2, 3},
#     (2, "e"): {4},
#     (3, "b"): {5},
#     (4, "e"): {8},
#     (4, "a"): {2},
#     (5, "e"): {6, 7},
#     (6, "a"): {8},
#     (7, "b"): {5, 8},
# }

# AFND = FSMNotDeterministic(data, 0, {8}, {"a","b"}, {0, 1, 2, 3, 4, 5, 6, 7, 8})
# print(AFND)

# AFD = AFND.subsetConstruction()
# print(AFD)

# print(AFD.checkRegex("abbb"))   # True
# print(AFD.checkRegex("aaaaaa")) # True
# print(AFD.checkRegex("ab"))     # False
import sys
from regexFSM import FSMDeterministic
from regexFSM import FSMNotDeterministic
from regexFSM import FSMUtils

if len(sys.argv)!=2:
    print("Error: MISSING PARSED REGEX")
    sys.exit(1)

polish_regex = sys.argv[1]
FSM = FSMUtils.fromCharacter(polish_regex[0])
ndFSM = FSM.subsetConstruction()

print(ndFSM.checkRegex(polish_regex[0]))    # Expected True
print(ndFSM.checkRegex("zzz"))              # Expected False

FSM = FSMUtils.starClosure(FSM)
ndFSM = FSM.subsetConstruction()

print(ndFSM.checkRegex(polish_regex[0]*3))  # Expected True
print(ndFSM.checkRegex(""))                 # Expected True
print(ndFSM.checkRegex("zzz"))              # Expected False
