class Transitions(object):
    """Transitions

    Args:
        Transitions List<(<State>, <char>, List<State>)>: 
        This must be a list with the state as first and the 
        char as second, and the final state as third.
    """
    def __init__(self, transitions=None):
        super(Transitions, self).__init__()
        self.transitions = [transitions] if transitions is not None else []
        
    def get(self, state, character):
        for transition in self.transitions:
            initial = transition[0]
            char = transition[1]
            final = transition[2]
            if(initial == state and char == character):
                return final
        return []
    
    def add_transition(self, initial_state, character, final_state):
        for transition in self.transitions:
            initial = transition[0]
            char = transition[1]
            final = transition[2]
            if(initial == initial_state and char == character):
                final += [final_state]
                return
        self.transitions.append([initial_state, character, [final_state]])
        
    def combine(self, other):
        if isinstance(other, Transitions):
            self.transitions += other.transitions 