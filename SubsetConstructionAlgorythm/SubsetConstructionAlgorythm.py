from State.State import State
from Transitions.Transitions import Transitions
from DFA.DFA import DFA

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
        done = True
        for _state in self.states:
            if _state.marked:
                done = False
        return done
        
    def getDFA(self):
        newState = State([self.nfa.initial])
        self.states.append(newState)
        transitions = Transitions()
        while(self.isDone()):
            for _state in self.states:
                if(not _state.marked):
                    #print("-------------------")
                    #print(_state.id)
                    _state.mark()
                    for char in self.nfa.alphabet + ['ε']:
                        #print(char)
                        nfa_transitions = self.nfa.transitions
                        for __state in _state.clousure:
                            #print(__state.id, self.nfa.initial.id)
                            newStateTransitions = nfa_transitions.get(__state, char)
                            if(isinstance(newStateTransitions, list)):
                                _newState = State(newStateTransitions)
                                verify, ___state = self.verify_state(_newState)
                                if(verify):
                                    #for mystate in newStateTransitions:
                                        #print(mystate.id)
                                    #print("lo agregue")
                                    self.states.append(_newState)
                                    transitions.add_transition(_state, char, _newState)
                                else:
                                    transitions.add_transition(_state, char, ___state)
        finals = self.getFinals()
        return DFA(
            self.states,
            newState,
            finals,
            self.nfa.alphabet,
            transitions
        )
                    
