from NFA.NFA import NFA
from State.State import State
from Node.Node import Node
from Transitions.Transitions import Transitions

class Thompson(object):
    """Thomson

    Args:
        regular_expression (_string_): This is the regular 
            expression that the Thomson algorythm will evaluate
            
    Methods:
        generate_NFA(): This fucntion return an NFA based on the 
        regular expression provided 
    """
    
    def __init__(self, regular_expression):
        super(Thompson, self).__init__()
        self.regex = regular_expression

    def __get_inital_nodes(self):
        #This method returns a list of Node, members of the alphabet
        nodes = []
        for index in range(0,len(self.regex)):
            char = self.regex[index]
            if(char!='*' and char!='(' and char!=')' and char!='|'):
                initial = State()
                final = State()
                nodes.append(
                    Node(
                        char, 
                        NFA(
                            [initial, final],
                            initial,
                            [final],
                            [char],
                            Transitions([initial, char, [final]])
                        ),
                        index,
                        index+1
                    )
                )
            index+=1
        return nodes
                
    def generate_NFA(self):
        #This fucntion return an NFA based on the regular
        #expression provided 
        nodes = self.__get_inital_nodes()
        while(len(nodes)!=1 and nodes[0].value != self.regex):
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                print(self.regex[node.index_start - 1: node.index_end + 2], "asdf")
                if(self.regex[node.index_start - 1: node.index_end + 1] == ("(" + node.value + ")")):
                    #If the parent node is a parenthesis, in other words if the value of the current node its
                    #enclosed by parenthesis.
                    print('ser')
                    new_nodes.append(Node(
                        self.regex[node.index_start - 1: node.index_end + 1],
                        node.nfa,
                        node.index_start - 1,
                        node.index_end + 1
                    ))
                    index += 1
                elif(self.regex[node.index_start: node.index_end + 1] == node.value + "*"):
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__Kleene(node.nfa),
                        node.index_start,
                        node.index_end + 1
                    ))
                    index += 1
                elif(
                    index+1<len(nodes) and
                    self.regex[node.index_start: nodes[index+1].index_end + 1] == node.value + nodes[index+1].value
                ):
                    new_nodes.append(Node(
                        self.regex[node.index_start: nodes[index+1].index_end + 1],
                        self.__Concatenate(node.nfa, nodes[index+1].nfa),
                        node.index_start,
                        nodes[index+1].index_end
                    ))
                    index += 2
                elif(
                    index+1<len(nodes) and
                    self.regex[node.index_start: nodes[index+1].index_end + 2] == node.value + '|' + nodes[index+1].value
                ):
                    new_nodes.append(Node(
                        self.regex[node.index_start: nodes[index+1].index_end + 1],
                        self.__OR(node.nfa, nodes[index+1].nfa),
                        node.index_start,
                        nodes[index+1].index_end
                    )) 
                    index += 2
                else:
                    new_nodes.append(node)
                    index += 1
            for node in nodes:
                print (node.value)
            print('------------------')
            nodes = new_nodes
        for node in nodes:
            print (node.value)
        print('------------------')
        return nodes[0].nfa            
            
    def __OR(self, a, b):
        #This returns a new NFA equivalent to a|b where a and b are both NFAs
        initial = State()
        final = State()
        transitions = a.transitions
        transitions.combine(b.transitions)                  #Join trasitions
        transitions.add_transition(initial, 'ε', a.initial)
        transitions.add_transition(initial, 'ε', b.initial)
        for state in  a.finals:                                             
            transitions.add_transition(state, 'ε', final)   
        for state in  b.finals:                                             
            transitions.add_transition(state, 'ε', final)   
        return NFA(
            a.states + b.states + [initial,final],
            initial,
            [final],
            a.alphabet + b.alphabet,
            transitions
        )
        
    def __Concatenate(self, a, b):
        #This returns a new NFA equivalent to ab where a and b are both NFAs
        transitions = a.transitions
        transitions.combine(b.transitions)                  #Join trasitions
        for state in  a.finals:                                             #Add a transitions to concatenate
            transitions.add_transition(state, 'ε', b.initial)          
        return NFA(
            a.states + b.states,
            a.initial,
            b.finals,
            a.alphabet + b.alphabet,
            transitions
        )
        
    def __Kleene(self, a):  
        #This returns a new NFA equivalent to a* where a is NFA too
        initial = State()
        final = State()
        transitions = a.transitions
        transitions.add_transition(initial, 'ε', a.initial)
        transitions.add_transition(initial, 'ε', final)
        for state in  a.finals:                                             
            transitions.add_transition(state, 'ε', a.initial)                 
            transitions.add_transition(state, 'ε', final)   
        return NFA(
            a.states + [initial,final],
            initial,
            [final],
            a.alphabet,
            transitions
        )
        
        
        