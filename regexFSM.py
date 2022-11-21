from stack import Stack
import subprocess

class FSMNotDeterministic:
    def __init__(self, fsm, initState, finalState, alphabeth, states, lastState = None):
        self._FSM_ = fsm
        self._INITIALSTATE_ = initState
        self._FINALSTATES_ = finalState
        self._ALPHABETH_ = alphabeth
        self._STATES_ = states
        self._LASTSTATE_ = lastState # only used in fromRegex construction
        
    def __str__(self):
        print(self._FINALSTATES_)
        print(self._STATES_)
        tostr = "\n{\n"
        tostr += "\n".join([f"\t{k}: {v}," for k, v in self._FSM_.items()])
        return tostr + "\n}\n"

    def closure(self, state):
        visited = [state]
        closureStates = [state]
        if (state, "e") in self._FSM_.keys():
            closureStates += list(self._FSM_[(state, "e")])  # all reachable states with e-transitions
        for s in closureStates: 
            if s not in visited:    # prevents infinite cycles
                visited.append(s)
                closureStates += self.closure(s)
        return tuple(set(closureStates))    # remove duplicates
    
    def subsetConstruction(self):
        fsmd = {}
        
        statesId = {}
        lastStateId = 0
        
        q0 = self.closure(self._INITIALSTATE_)
        statesId[q0] = lastStateId
        
        unmarkedStates = [q0]
        foundStates = [q0]
    
        # while still having unexplored possibilites try every possible input from the current node
        # and compact every reachable state in a new state
        while unmarkedStates:
            q = unmarkedStates.pop()
            for s in q:
                for c in self._ALPHABETH_:
                    t = ()
                    newState = ()
                    if (s, c) in self._FSM_.keys():
                        t = self._FSM_[(s, c)]
                    for el in t:
                        newState += self.closure(el)
                    if newState:
                        if newState not in foundStates:     # avoid looping in explored states
                            foundStates.append(newState)
                            lastStateId += 1
                            statesId[newState] = lastStateId
                            unmarkedStates.append(newState)
                        fsmd[(statesId[q], c)] = statesId[newState]
        
        # Every new state containing an original final state is a new final state
        finalStates = []
        for (state, idx) in statesId.items():
            if any(item in state for item in self._FINALSTATES_):
                finalStates.append(idx)
                
        return FSMDeterministic(fsmd, 0, finalStates, self._ALPHABETH_, statesId)   

                
class FSMDeterministic:
    def __init__(self, fsm, initState, finalState, alphabeth, statesDict):
        self._FSM_ = fsm
        self._INITIALSTATE_ = initState
        self._FINALSTATES_ = finalState
        self._ALPHABETH_ = alphabeth
        self._STATESDICT_ = statesDict
        self._STATES_ = statesDict.values()
        
    def __str__(self):
        tostr = "\n{\n"
        tostr += "\n".join([f"\t{k}: {v}," for k, v in self._FSM_.items()])
        return tostr + "\n}\n"
    
    def checkRegex(self, inputString):
        currentState = self._INITIALSTATE_
        for char in inputString:
            if (currentState, char) not in self._FSM_: 
                return False
            currentState = self._FSM_[(currentState, char)]
            
        return True if currentState in self._FINALSTATES_ else False

class Regex:
    def __init__(self, regex):
        notDeterministicFSM = FSMUtils.fromRegex(regex)
        self._REGEXFSM_ = self.notDeterministicFSM.subsetConstruction()
    
    def match(self, string):
        return self._REGEXFSM_.checkRegex(string)
    
    @staticmethod
    def match(string, regex):
        if not regex:
            return False
        
        try:
            return FSMUtils.fromRegex(regex).subsetConstruction().checkRegex(string)
        except:
            return False
        
        
    
class FSMUtils:
    @staticmethod
    def fromCharacter(char, firstIndex = 0):
        return FSMNotDeterministic(
            fsm = {
                (firstIndex, char) : {firstIndex + 1},
            }, 
            initState = firstIndex, 
            finalState = {firstIndex + 1}, 
            alphabeth = {char}, 
            states = {firstIndex, firstIndex + 1},
            lastState = firstIndex + 1,
        )

    @staticmethod
    def starClosure(fsm):
        firstIndex = max(fsm._STATES_) + 1
        
        fsm._FSM_.update({
            (firstIndex, "e") : {fsm._INITIALSTATE_, firstIndex + 1},
            (fsm._LASTSTATE_, "e") : {fsm._INITIALSTATE_, firstIndex + 1},
        })
        fsm._FINALSTATES_.add(firstIndex + 1)
        fsm._STATES_.update({firstIndex, firstIndex + 1})
        return FSMNotDeterministic(
            fsm = fsm._FSM_,
            initState = firstIndex,
            finalState = fsm._FINALSTATES_,
            alphabeth = fsm._ALPHABETH_,
            states = fsm._STATES_,
            lastState = firstIndex + 1
        )
        
    @staticmethod
    def union(firstFsm, secondFsm):
        firstIndex = max(max(firstFsm._STATES_), max(secondFsm._STATES_)) + 1
        
        secondFsm._FSM_.update({
            (firstIndex, "e") : {firstFsm._INITIALSTATE_, secondFsm._INITIALSTATE_},
            (firstFsm._LASTSTATE_, "e") : {firstIndex + 1},
            (secondFsm._LASTSTATE_, "e") : {firstIndex + 1},
        })
        secondFsm._FSM_.update(firstFsm._FSM_)
        secondFsm._ALPHABETH_.update(firstFsm._ALPHABETH_)
        secondFsm._STATES_.update(firstFsm._STATES_),
        secondFsm._STATES_.update({firstIndex, firstIndex + 1}),
        return FSMNotDeterministic(
            fsm = secondFsm._FSM_,
            initState = firstIndex,
            finalState = {firstIndex + 1},
            alphabeth = secondFsm._ALPHABETH_,
            states = secondFsm._STATES_,
            lastState = firstIndex + 1
        )
    
    @staticmethod
    def concat(firstFsm, secondFsm):
        secondFsm._FSM_.update({
            (secondFsm._LASTSTATE_, "e") : {firstFsm._INITIALSTATE_},
        })
        secondFsm._FSM_.update(firstFsm._FSM_)
        secondFsm._ALPHABETH_.update(firstFsm._ALPHABETH_)
        secondFsm._STATES_.update(firstFsm._STATES_),
        return FSMNotDeterministic(
            fsm = secondFsm._FSM_,
            initState = secondFsm._INITIALSTATE_,
            finalState = firstFsm._FINALSTATES_,
            alphabeth = secondFsm._ALPHABETH_,
            states = secondFsm._STATES_,
            lastState = firstFsm._LASTSTATE_
        )

    @staticmethod
    def fromRegex(regex):
        regex = FSMUtils.toPolishNotation(regex)
        stack = Stack()
        lastindex = 0
        for char in regex:
            if char == '|':
                stack.push(FSMUtils.union(stack.pop(), stack.pop()))
            elif char == '*':
                stack.push(FSMUtils.starClosure(stack.pop()))
            elif char == '(':
                stack.push('(')
            elif char == ')':
                fsm = stack.pop()
                try:
                    while stack.peek() != '(':
                        fsm = FSMUtils.concat(fsm, stack.pop())
                except:
                    pass
                stack.pop()
                stack.push(fsm)
            else:
                stack.push(FSMUtils.fromCharacter(char, lastindex))
            lastindex += 2
            
        while stack.size() > 1:
            firstFsm = stack.pop()
            secondFsm = stack.pop()
            fsm = FSMUtils.concat(firstFsm, secondFsm)
            stack.push(fsm)
        
        return stack.peek()
    
    @staticmethod
    def toPolishNotation(regex):
        p1 = subprocess.Popen(["echo", regex], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["./Parser/pparser"], stdin=p1.stdout,  stdout=subprocess.PIPE).communicate()[0]
        regex = p2.decode().strip()
        p1.stdout.close()
        return regex     