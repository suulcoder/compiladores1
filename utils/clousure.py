def clousure(state, transitions):
    stack = []
    e_clousure = [] + state
    for _state in state:
        stack.append(_state)
    while (len(stack)!=0):
        t = stack.pop()
        for transition in transitions:
            if(transition[0]==t and transition[1]=='ε'):
                u = transition[2]
                for _state in u:
                    if(_state not in e_clousure):
                        e_clousure.append(_state)
                stack.append(u)
    return e_clousure
    