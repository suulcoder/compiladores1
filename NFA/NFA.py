#A Nondeterministic finite automaton
from State.State import State
from Transitions.Transitions import Transitions
from utils.clousure import clousure

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
    
    def __make_trasition(self, S, character):
        #bool function, character must be a string memember of alphabet
        #It checks if the new states are final states, and it return
        #true if is like that
        newState = []
        for _state in S:
            states = clousure(self.transitions.get(_state, character), self.transitions.transitions)
            for __state in states:
                if(__state not in newState):
                    newState.append(__state)
        return newState
    
    def simulate(self, string):
        S = clousure([self.initial], self.transitions.transitions)
        for char in string:
            S =  self.__make_trasition(S, char)
        for state in S:
            if(state in self.finals):
                return True
        return False
    
    def duplicate(self):
        newStates = [State() for _ in self.states]
        index = 0
        initial = None
        finals = [] 
        for state in self.states:
            if(state == self.initial):
                initial = newStates[index]
            if(state in self.finals):
                finals.append(newStates[index])
            index += 1
        transitions = Transitions()
        for transition in self.transitions.transitions:
            for n in transition[2]:
                transitions.add_transition(
                    newStates[self.states.index(transition[0])],
                    transition[1],
                    newStates[self.states.index(n)]
            )
        return NFA(
            newStates,
            initial,
            finals,
            self.alphabet,
            transitions
        )
                            
            
    