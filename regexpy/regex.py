from regexpy.utils.fsmutils import FSMUtils

class Regex:
    """Class representing the high level interface presented to the final user.

    This abstract the internal details and provide a simple minimal API.
    A Regex can be both instantiated for multiple uses or used statically and generated on fly.
    """
    
    def __init__(self, regex):
        """Regex constructor"""
        self._REGEXFSM_ = FSMUtils.fromRegex(regex).subsetConstruction()
    
    def validate(self, string):
        """Returns whether the matching is true or false
        Must be called on an instance of Regex, it's the not static variant of match()
        """
        return self._REGEXFSM_.checkRegex(string)
    
    @staticmethod
    def match(string, regex):
        """Returns whether the matching is true or false
        Can be called without an instance of Regex, it's the static variant of validate()
        """
        if not regex:
            return False
        
        try:
            return FSMUtils.fromRegex(regex).subsetConstruction().checkRegex(string)
        except:
            return False

