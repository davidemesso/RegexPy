from regexpy.utils.fsmutils import FSMUtils

class Regex:
    """Class representing the high level interface presented to the final user.

    This abstract the internal details and provide a simple minimal API.
    A Regex can be both instantiated for multiple uses or used statically and generated on fly.
    """
    
    def __init__(self, regex):
        """Regex constructor"""
        self._regex = FSMUtils.fromRegex(regex).subsetConstruction()
        
    @property
    def regex(self):
        """Property exposing the instantiated regex fsm"""
        return self._regex
    
    @regex.setter
    def regex(self, value):
        """Should not be modified, but if you really want you can use the setter with just a string
        
        This setter abstract the string to FSM transformation and permit direct assignment.
        The correct way is anyway to instantiate a new Regex object
        """
        self._regex = FSMUtils.fromRegex(value).subsetConstruction()
    
    def validate(self, string):
        """Returns whether the matching is true or false
        Must be called on an instance of Regex, it's the not static variant of match()
        """
        return self._regex.checkRegex(string)
    
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
        
    @staticmethod
    def matchAny(string, regexList):
        """Returns true if at least one regex matches"""
        return any(map(lambda r : Regex.match(string, r), regexList))
    
    @staticmethod
    def matchAll(string, regexList):
        """Returns true if all regex matches"""
        return all(map(lambda r : Regex.match(string, r), regexList))

