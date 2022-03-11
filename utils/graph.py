from graphviz import Digraph

def graph(automaton, name):
    _graph = Digraph()
    
    # Adding states in Finite Automaton to diagram
    for state in automaton.states:
        if (state not in automaton.finals):
            _graph.attr('node', shape='circle')
            _graph.node(str(state.id))
        else:
            _graph.attr('node', shape='doublecircle')
            _graph.node(str(state.id))
    
    # Adding initial state
    _graph.attr('node', shape='none')
    _graph.node('')
    _graph.edge('', str(automaton.initial.id))
    
    # Adding transitions
    for transition in automaton.transitions.transitions:
        for state in transition[2]:
            _graph.edge(
                str(transition[0].id),
                str(state.id),
                label=('ε', transition[1])[transition[1] != 'e'])
    
    # Makes a pdf with name nfa.graph.pdf and views the pdf
    _graph.render(name, view=True)