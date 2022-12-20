from regexpy.utils.stack import Stack
import subprocess
from abc import ABC

class AbstractFSM(ABC):
    """Abstract class representing a generic FSM"""
    
    def __init__(self, fsm, initialState, finalState, alphabeth, states):
        """Shared constructor"""
        self._fsm = fsm
        self._initialState = initialState
        self._finalStates = finalState
        self._alphabeth = alphabeth
        self._states = states
        
    def __str__(self):
        """Shared string representation"""
        tostr = "\n{\n"
        tostr += "\n".join([f"\t{k}: {v}," for k, v in self._fsm.items()])
        return tostr + "\n}\n"

class FSMNotDeterministic(AbstractFSM):
    """Class describing a not deterministic FSM
    
    This FSM can use eps-transitions and multiple edges with same input exiting from same node.
    A regex string can be easly transformed into a NDFSM using some basics rules,
    instead creating a deterministic FSM from a string is very difficult, so this intermediary
    representation is used to achieve a DFSM for simulating regex validation.
    """
    def __init__(self, fsm, initialState, finalState, alphabeth, states, lastState = None):
        """Constructor"""
        AbstractFSM.__init__(self, fsm, initialState, finalState, alphabeth, states)
        self._lastState = lastState # only used in fromRegex construction

    def closure(self, state):
        """Returns the closure of a node
        
        The closure of a node is represented by all the reachable nodes using only 
        eps-transitions exiting from that node.
        """
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
        """Returns the deterministic FSM representing this NDFSM
        
        Subset construction is an algorithm that using a graph visit can reduce a NDFSM 
        to a DFSM, that can be used for regex validation.
        """
        fsmd = {}
        
        statesId = {}
        lastStateId = 0
        
        # starting from q0 -> closure of initialState
        q0 = self.closure(self._initialState)
        statesId[q0] = lastStateId
        
        unmarkedStates = [q0]
        foundStates = [q0]
    
        # while still having unexplored possibilites try every possible input from the current node
        # and compact every eps-reachable state in a new state
        while unmarkedStates:
            q = unmarkedStates.pop()
            for s in q:
                for c in self._alphabeth:
                    t = {}
                    newState = ()
                    if (s, c) in self._fsm:
                        t = self._fsm[(s, c)]
                    for el in t:
                        newState += self.closure(el)
                    if newState not in foundStates:     # avoid looping in explored states
                        foundStates.append(newState)
                        lastStateId += 1
                        statesId[newState] = lastStateId
                        unmarkedStates.append(newState)
                    if newState:
                        fsmd[(statesId[q], c)] = statesId[newState]
        
        # Every new state containing an original final state is a new final state
        finalStates = []
        for (state, idx) in statesId.items():
            if any(item in state for item in self._finalStates):
                finalStates.append(idx)

        return FSMDeterministic(fsmd, 0, finalStates, self._alphabeth, statesId.values())

                
class FSMDeterministic(AbstractFSM):
    """Class describing a not deterministic FSM
    
    This FSM cannot use eps-transitions or multiple edges with same input exiting from same node.
    But it's very usefull for regex validation, it can be easly visited as a graph
    with string to be validated as the input
    """
    def __init__(self, fsm, initialState, finalState, alphabeth, states):
        """Constructor"""
        AbstractFSM.__init__(**locals())
    
    def checkRegex(self, inputString):
        """Returns whether the visit of graph ends on a finalState
        
        If so the string can be considered matched by the regex represented
        """
        currentState = self._initialState
        for char in inputString:
            if (currentState, char) not in self._fsm: 
                return False
            currentState = self._fsm[(currentState, char)]

        return currentState in self._finalStates
    
