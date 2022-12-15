from regexFSM import FSMUtils

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
        