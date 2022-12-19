from regexpy.utils.stack import Stack
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
    