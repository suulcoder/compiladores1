#A Nondeterministic finite automaton
from sympy import true
from State.State import State
from Transitions.Transitions import Transitions

class DFA(object):
    """DFA:A Deterministic finite automaton

    Args:
        states (_list<int>_): 
            This must be a list of States
        
        initial (<State>): This must be the initial state, and should be included
            in the states list
        
        finals (<State>): This must be the final states, and should be included
            in the states list
            
        alphabet (_list<char>_): 
            This must be a list of strings, with the characters
            ex: ['a','b','c']
            
        transitions (<Transitions>) :
            This must be a Transitions object
        
    """
    def __init__(self, states, initial, finals, alphabet, transitions):
        super(DFA, self).__init__()
        self.alphabet = alphabet
        self.current = [initial]
        self.initial = initial
        self.finals = finals
        self.states = states
        self.transitions = transitions
    
    def simulate(self, string):
        S = self.initial
        for char in string:
            transition = self.transitions.get(S, char)
            if(len(transition)!=0):
                S = transition[0]
            else:
                return False
        if(S in self.finals):
            return True
        return False
