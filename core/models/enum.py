class Enum:
    __val__ = 0

    @classmethod
    def get_members(cls): 
        members = {attr:getattr(cls, attr) for attr in dir(cls) if not(attr.startswith("get_members")) and not attr.startswith("__")}
        return members 
        

class PitchStatus(Enum):
    __val__     = 1000
    open        = 'O'
    pending     = 'P' 
    close       = 'C'
    delete      = 'D'
