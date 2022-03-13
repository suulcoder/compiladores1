from State.State import State
from Transitions.Transitions import Transitions
from DFA.DFA import DFA

def isDone(states):
    for __state in states:
        if(not __state.marked):
            __state.mark()
            return (True, __state) 
    return (False, None)

def DirectToDFA(root, alphabet):
    transitions = Transitions()
    initial = State(sorted(root.firstpos, key=lambda x: x.id)) 
    states = [initial]
    final = []
    is_done, state = isDone(states)
    while (is_done):
        state.mark()
        _transitions = {}
        for node in state.clousure:
            if(node.value == "#"):
                final += [state]
                break
            if(node.value in _transitions):
                _transitions[node.value].extend(x for x in node.followpos if x not in _transitions[node.value])
            else:
                _transitions[node.value] = node.followpos
        for char in _transitions:
            state_to_add = None
            sorted_list = sorted(_transitions[char], key=lambda x: x.id)
            for _state in states:
                if(sorted_list == _state.clousure):
                    state_to_add = _state
            if(state_to_add==None):
                state_to_add = State(sorted_list)
                states.append(state_to_add)
            transitions.add_transition(state, char, state_to_add)    
        is_done, state = isDone(states)
    return DFA(
        states, 
        initial,
        final,
        alphabet,
        transitions
    )
                    

    
    