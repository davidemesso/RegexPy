from regexpy.utils.fsmutils import FSMUtils

class Regex:
    def __init__(self, regex):
        self._REGEXFSM_ = FSMUtils.fromRegex(regex).subsetConstruction()
    
    def validate(self, string):
        return self._REGEXFSM_.checkRegex(string)
    
    @staticmethod
    def match(string, regex):
        if not regex:
            return False
        
        try:
            return FSMUtils.fromRegex(regex).subsetConstruction().checkRegex(string)
        except:
            return False

