from regexpy.utils.stack import Stack
import subprocess
from abc import ABC

class AbstractFSM(ABC):
    def __init__(self, fsm, initialState, finalState, alphabeth, states):
        self._fsm = fsm
        self._initialState = initialState
        self._finalStates = finalState
        self._alphabeth = alphabeth
        self._states = states
        
    def __str__(self):
        tostr = "\n{\n"
        tostr += "\n".join([f"\t{k}: {v}," for k, v in self._fsm.items()])
        return tostr + "\n}\n"

class FSMNotDeterministic(AbstractFSM):
    def __init__(self, fsm, initialState, finalState, alphabeth, states, lastState = None):
        AbstractFSM.__init__(self, fsm, initialState, finalState, alphabeth, states)
        self._lastState = lastState # only used in fromRegex construction

    def closure(self, state):
        visited = [state]
        closureStates = [state]
        if (state, "eps") in self._fsm.keys():
            closureStates += list(self._fsm[(state, "eps")])  # all reachable states with e-transitions
        for s in closureStates: 
            if s not in visited:    # prevents infinite cycles
                visited.append(s)
                closureStates += self.closure(s)
        return tuple(set(closureStates))    # remove duplicates
    
    def subsetConstruction(self):
        fsmd = {}
        
        statesId = {}
        lastStateId = 0
        
        q0 = self.closure(self._initialState)
        statesId[q0] = lastStateId
        
        unmarkedStates = [q0]
        foundStates = [q0]
    
        # while still having unexplored possibilites try every possible input from the current node
        # and compact every reachable state in a new state
        while unmarkedStates:
            q = unmarkedStates.pop()
            for s in q:
                for c in self._alphabeth:
                    t = ()
                    newState = ()
                    if (s, c) in self._fsm.keys():
                        t = self._fsm[(s, c)]
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
            if any(item in state for item in self._finalStates):
                finalStates.append(idx)

        return FSMDeterministic(fsmd, 0, finalStates, self._alphabeth, statesId.values())

                
class FSMDeterministic(AbstractFSM):
    def __init__(self, fsm, initialState, finalState, alphabeth, states):
        AbstractFSM.__init__(**locals())
    
    def checkRegex(self, inputString):
        currentState = self._initialState
        for char in inputString:
            if (currentState, char) not in self._fsm: 
                return False
            currentState = self._fsm[(currentState, char)]

        return currentState in self._finalStates
    
