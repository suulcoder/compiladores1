from State.State import State
from Transitions.Transitions import Transitions

def is_done(transitions):
    for transition in transitions:
        if isinstance(transition, list):
            return False
    return True

def clousure(transitions, states):
    for transition in transitions:
            #If a combination state-character lead to many states
            if isinstance(transition[2], list):
                newState = State()
                finals = transition[2]
                new_transitions = []
                for transition in transitions:
                    if(transition[0] in finals):
                        new_transitions.append(
                            newState, 
                            transition[1], 
                            [newState if state in finals else state for state in transition[2]])
                    else: 
                        new_transitions.append(
                            transition
                        )
                break

def SubsetConstructionAlgorythm(nfa):
    transitions = nfa.transitions
    while(not is_done(transitions)):
        transitions, state = clousure(transitions, nfa.states)
        
