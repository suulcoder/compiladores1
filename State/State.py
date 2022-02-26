import itertools

class State():
    new_id = itertools.count()
    def __init__(self):
        super(State, self).__init__()
        self.id = next(State.new_id)
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, State):
            return self.id == other.id
        return False
        
        
        