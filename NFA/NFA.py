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
    
    def __make_trasition(self, character):
        #bool function, character must be a string memember of alphabet
        #It checks if the new states are final states, and it return
        #true if is like that
        newState = []
        empty_path_found = False
        for state in self.current:
            transitions = self.transitions.get(state, character)
            if(isinstance(transitions, list)):
                newState += transitions
            empty_transitions = self.transitions.get(state, 'ε')
            if(isinstance(empty_transitions, list)):
                empty_path_found = True
                newState += empty_transitions
        if(len(newState)>0):
            self.current = newState
        if(empty_path_found):
            self.__make_trasition(character)
        return self.__is_current_a_final()
    
    def simulate(self, string):
        for char in string:
            if(self.__make_trasition(char)):
                return True
        return False   
    