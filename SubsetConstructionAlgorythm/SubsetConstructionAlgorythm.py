from pickle import FALSE
from re import L
from sympy import false
from State.State import State
from Transitions.Transitions import Transitions
from DFA.DFA import DFA
from utils.clousure import clousure
class SubsetConstructionAlgorythm(object):
    def __init__(self, nfa):
        super(SubsetConstructionAlgorythm, self).__init__()
        self.nfa = nfa
        self.states = []
        
    def verify_state(self, state):
        for _state in self.states:
            if _state.clousure == state.clousure:
                return (False, _state)
        return (True, None)
    
    def getFinals(self):
        finals = []
        for state in self.states:
            for _state in state.clousure:
                if(_state in self.nfa.finals):
                    if (state not in finals):
                        finals.append(state) 
        return finals
        
    def isDone(self):
        for __state in self.states:
                if(not __state.marked):
                    __state.mark()
                    return (True, __state) 
        return (False, None)
    
    def isInStates(self, state):
        for _state in self.states:
            for _clousure_state in state.clousure:
                if(_clousure_state in _state.clousure):
                    return (True, _state)
        return (False, None)
        
    def getDFA(self):
        newState = State(clousure=clousure([self.nfa.initial], self.nfa.transitions.transitions))
        self.states.append(newState)
        transitions = Transitions()
        done, T  = self.isDone()
        while(done):
            for char in self.nfa.alphabet:
                old_transition = []
                for clousure_state in T.clousure:
                    state_old_transition = self.nfa.transitions.get(clousure_state, char)
                    for state_transition in state_old_transition:
                        if(state_transition not in old_transition):
                            old_transition.append(state_transition)
                if(len(old_transition)!=0):
                    U = State(clousure=clousure(old_transition, self.nfa.transitions.transitions))
                    UinStates = self.isInStates(U)
                    if(not UinStates[0]):
                        self.states.append(U)
                    else:
                        U = UinStates[1]
                    transitions.add_transition(T, char, U)
            done, T  = self.isDone()
        finals = self.getFinals()
        if(len(finals)==0):
            finals = [newState]
        return DFA(
            self.states,
            newState,
            finals,
            self.nfa.alphabet,
            transitions
        )
                    
