from regexpy.fsm import *
from functools import lru_cache
from subprocess import Popen

class FSMUtils:
    """An interface collecting as static methods all the functions used for regex implementation
    
    This class contains usefull abstractions for stack operations and data structures manipulations
    needed to achieve the correct construction of a deterministic FSM starting from a regex string.
    """
    @staticmethod
    def fromCharacter(char, firstIndex = 0):
        """Returns a not deterministic FSM representing on a character"""
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
        """Returns a not deterministic FSM representing a block that can repeated 0, 1 or more times"""
        firstIndex = max(fsm._STATES_) + 1
        
        fsm._FSM_.update({
            (firstIndex, "eps") : {fsm._INITIALSTATE_, firstIndex + 1},
            (fsm._LASTSTATE_, "eps") : {fsm._INITIALSTATE_, firstIndex + 1},
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
        """Returns a not deterministic FSM representing the union of 2 blocks (OR operation)"""
        firstIndex = max(max(firstFsm._STATES_), max(secondFsm._STATES_)) + 1
        
        secondFsm._FSM_.update({
            (firstIndex, "eps") : {firstFsm._INITIALSTATE_, secondFsm._INITIALSTATE_},
            (firstFsm._LASTSTATE_, "eps") : {firstIndex + 1},
            (secondFsm._LASTSTATE_, "eps") : {firstIndex + 1},
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
        """Returns a not deterministic FSM representing the concatenation of 2 blocks"""
        secondFsm._FSM_.update({
            (secondFsm._LASTSTATE_, "eps") : {firstFsm._INITIALSTATE_},
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
    @lru_cache(typed=False)
    def fromRegex(regex):
        """Returns a not deterministic FSM representing a regex
        
        lru_cache decorator is used to considerably speed up repeated matches of the same pattern
        The process is achieved by:
        - Getting polish notation of regex string
        - Interpreting it on fly constructing sequentials not determinist FSM using a stack
        (characters are pushed and special symbols represents custom pop logics)
        """
        regex = FSMUtils.toPolishNotation(regex)
        if regex is None:
            raise Exception()
        
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
                while stack.peek() != '(':
                    fsm = FSMUtils.concat(fsm, stack.pop())
                stack.pop() # remove last (
                stack.push(fsm)
            else:
                # Only normal characters here
                stack.push(FSMUtils.fromCharacter(char, lastindex))
            lastindex += 2
        
        # everything left on stack must be concatenated
        while stack.size() > 1:
            firstFsm = stack.pop()
            secondFsm = stack.pop()
            fsm = FSMUtils.concat(firstFsm, secondFsm)
            stack.push(fsm)
        
        return stack.peek()
    
    @staticmethod
    def toPolishNotation(regex):
        """Returns the regex string parsed and converted to polish notation
        
        This is done by calling a c++ compiled parser via subprocess.
        """
        try:
            with Popen(["echo", regex], stdout=subprocess.PIPE, shell=False) as p1:
                with Popen(["./Parser/pparser"], stdin=p1.stdout, stdout=subprocess.PIPE, shell=False) as p2:
                    regex = p2.communicate()[0].decode().strip()
                    p1.stdout.close()
        except:
            return None
        
        return regex     