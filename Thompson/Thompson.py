from turtle import done
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
            if(char!='*' and char!='(' and char!=')' and char!='|' and char!='?' and char!='+'):
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
        while(len(nodes)!=1 or nodes[0].value != self.regex):
            #Parenthesis is first on hierarchy
            #If the value of the current node its enclosed by parenthesis.
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start - 1: node.index_end + 1] == "(" + node.value + ")"):
                    new_nodes.append(Node(
                        self.regex[node.index_start - 1: node.index_end + 1],
                        node.nfa,
                        node.index_start - 1,
                        node.index_end + 1
                    ))
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
                    
            #Positive clousure is a Kleene Clousure with a concatenation a+ = a*a
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start: node.index_end + 1] == node.value + "+"):
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__Concatenate(node.nfa, self.__Kleene(node.nfa)),
                        node.index_start,
                        node.index_end + 1
                    ))
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes      
            
            #Kleene is second on hierarchy
            #If the value of the current node its previous to a Kleene sign.
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start: node.index_end + 1] == node.value + "*"):
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__Kleene(node.nfa),
                        node.index_start,
                        node.index_end + 1
                    ))
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
                    
            #Concatenation is third on hierarchy
            #If the value of a node and its followed node are next to the other
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                if(
                    index+1<len(nodes) and
                    self.regex[node.index_start: nodes[index+1].index_end] == node.value + nodes[index+1].value
                ):
                    new_nodes.append(Node(
                        self.regex[node.index_start: nodes[index+1].index_end],
                        self.__Concatenate(node.nfa, nodes[index+1].nfa),
                        node.index_start,
                        nodes[index+1].index_end
                    ))
                    index += 2
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
            
            #Nullable ?
            #If the value has nullable following value|ε
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start: node.index_end + 1] == node.value + "?"):
                    initial = State()
                    final = State()
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__OR(node.nfa, NFA(
                            [initial, final],
                            initial,
                            [final],
                            ['ε'],
                            Transitions([initial, 'ε', [final]])
                        )),
                        node.index_start,
                        node.index_end + 1
                    ))
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
                    
            #Or is last on hierarchy
            #If the value of a node and its followed node are divided by a OR sign: |
            new_nodes = []
            index = 0
            while(index<len(nodes)):
                node = nodes[index]
                if(
                    index+1<len(nodes) and
                    self.regex[node.index_start: nodes[index+1].index_end] == node.value + '|' + nodes[index+1].value
                ):
                    new_nodes.append(Node(
                        self.regex[node.index_start: nodes[index+1].index_end],
                        self.__OR(node.nfa, nodes[index+1].nfa),
                        node.index_start,
                        nodes[index+1].index_end
                    )) 
                    index += 2
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
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
        
        
        