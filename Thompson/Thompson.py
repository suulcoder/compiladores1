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
        
    def __process_NFA(self,nodes):
        while(len(nodes)!=1 or nodes[0].value != self.regex):
            #Parenthesis is first on hierarchy
            #If the value of the current node its enclosed by parenthesis.
            new_nodes = []
            index = 0
            change_was_made = False
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start - 1: node.index_end + 1] == "(" + node.value + ")"):
                    new_nodes.append(Node(
                        self.regex[node.index_start - 1: node.index_end + 1],
                        node.nfa,
                        node.index_start - 1,
                        node.index_end + 1
                    ))
                    change_was_made = True
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
            if(change_was_made):
                nodes = self.__process_NFA(nodes)
                    
            #Positive clousure is a Kleene Clousure with a concatenation a+ = a*a
            new_nodes = []
            index = 0
            change_was_made = False
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start: node.index_end + 1] == node.value + "+"):
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__Positive_Clousure(node.nfa),
                        node.index_start,
                        node.index_end + 1
                    ))
                    change_was_made = True
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes   
            if(change_was_made):
                nodes = self.__process_NFA(nodes)   
            
            #Kleene is second on hierarchy
            #If the value of the current node its previous to a Kleene sign.
            new_nodes = []
            index = 0
            change_was_made = False
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start: node.index_end + 1] == node.value + "*"):
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__Kleene(node.nfa),
                        node.index_start,
                        node.index_end + 1
                    ))
                    change_was_made = True
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
            if(change_was_made):
                nodes = self.__process_NFA(nodes)
                    
            #Concatenation is third on hierarchy
            #If the value of a node and its followed node are next to the other
            new_nodes = []
            index = 0
            change_was_made = False
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
                    change_was_made = True
                    index += 2
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
            if(change_was_made):
                nodes = self.__process_NFA(nodes)
                    
            #Or is last on hierarchy
            #If the value of a node and its followed node are divided by a OR sign: |
            new_nodes = []
            index = 0
            change_was_made = False
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
                    change_was_made = True 
                    index += 2
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
            if(change_was_made):
                nodes =  self.__process_NFA(nodes)
            
            #Nullable ?
            #If the value has nullable following value|??
            new_nodes = []
            index = 0
            change_was_made = False
            while(index<len(nodes)):
                node = nodes[index]
                if(self.regex[node.index_start: node.index_end + 1] == node.value + "?"):
                    new_nodes.append(Node(
                        self.regex[node.index_start: node.index_end + 1],
                        self.__Nuballe(node.nfa),
                        node.index_start,
                        node.index_end + 1
                    ))
                    change_was_made = True
                    index += 1
                else:
                    new_nodes.append(node)
                    index += 1
            nodes = new_nodes
            if(change_was_made):
                nodes =  self.__process_NFA(nodes)
        return nodes       
    
    def generate_NFA(self):
        #This fucntion return an NFA based on the regular
        #expression provided 
        nodes = self.__get_inital_nodes()
        nodes = self.__process_NFA(nodes)
        return nodes[0].nfa
        
    def __Nuballe(self, a):
        initial = State()
        final = State()
        transitions = a.transitions
        transitions.add_transition(initial, '??', a.initial)
        transitions.add_transition(initial, '??', final)
        for state in a.finals:
            transitions.add_transition(state, '??', final)
        return NFA(
            a.states + [initial, final],
            initial, 
            [final],
            a.alphabet,
            transitions
        )
    
    def __Positive_Clousure(self, a):
        n = a
        b = n.duplicate()
        final=State()
        intermidate=State()
        transitions = a.transitions
        transitions.combine(b.transitions)
        for state in a.finals:
            transitions.add_transition(state, '??', intermidate)
        transitions.add_transition(intermidate, '??', b.initial)
        transitions.add_transition(intermidate, '??', final)
        for state in b.finals:
            transitions.add_transition(state, '??', b.initial)
            transitions.add_transition(state, '??', final)
        return NFA(
            a.states + [final, intermidate],
            a.initial,
            [final],
            a.alphabet,
            transitions
        )
         
            
    def __OR(self, a, b):
        #This returns a new NFA equivalent to a|b where a and b are both NFAs
        initial = State()
        final = State()
        transitions = a.transitions
        transitions.combine(b.transitions)                  #Join trasitions
        transitions.add_transition(initial, '??', a.initial)
        transitions.add_transition(initial, '??', b.initial)
        for state in  a.finals:                                             
            transitions.add_transition(state, '??', final)   
        for state in  b.finals:                                             
            transitions.add_transition(state, '??', final)   
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
            transitions.add_transition(state, '??', b.initial)          
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
        transitions.add_transition(initial, '??', a.initial)
        transitions.add_transition(initial, '??', final)
        for state in  a.finals:                                             
            transitions.add_transition(state, '??', a.initial)                 
            transitions.add_transition(state, '??', final)   
        return NFA(
            a.states + [initial,final],
            initial,
            [final],
            a.alphabet,
            transitions
        )
        
        
        