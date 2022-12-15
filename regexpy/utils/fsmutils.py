from regexpy.fsm import *

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
    @lru_cache(typed=False)
    def fromRegex(regex):
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
        try:
            p1 = subprocess.Popen(["echo", regex], stdout=subprocess.PIPE, shell=False)
            p2 = subprocess.Popen(["./Parser/pparser"], stdin=p1.stdout, stdout=subprocess.PIPE, shell=False).communicate()[0]
        except:
            return None
        regex = p2.decode().strip()
        p1.stdout.close()
        return regex     