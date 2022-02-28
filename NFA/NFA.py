#A Nondeterministic finite automaton
from State.State import State
from Transitions.Transitions import Transitions

class NFA(object):
    """NFA:A Nondeterministic finite automaton

    Args:
        states (_list<State>_): 
            This must be a list of States
        
        initial (<State>): This must be the initial state, and should be included
            in the states list
        
        finals (_list<State>_): This must be the final states, and should be included
            in the states list
            
        alphabet (_list<char>_): 
            This must be a list of strings, with the characters
            ex: ['a','b','c']
            
        transitions (<Transitions>) :
            This must be a Transitions object
        
    """
    def __init__(self, states, initial, finals, alphabet, transitions):
        super(NFA, self).__init__()
        self.alphabet = alphabet
        self.current = [initial]
        self.initial = initial
        self.finals = finals
        self.states = states
        self.transitions = transitions
        
        def __is_current_a_final(self):
            #bool function, return true if the current state is a final state
            for state in self.current:
                if state in self.finals:
                    return True
            return False
        
        def make_trasition(self, character):
            #bool function, character must be a string memember of alphabet
            #It checks if the new states are final states, and it return
            #true if is like that
            new_state = []
            for state in self.current:
                new_state += self.transitions.get(state, character)
            self.current = new_state
            return self.__is_current_a_final()
        
            
        