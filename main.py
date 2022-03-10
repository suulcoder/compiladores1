""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Compilers: Project 1
# Saul Contreras
# Code made by @Suulcoder
# This code verifies if a provided string belongs to a regular
# expression building a NFA or DFA with different algorythoms
#
#  - Thompson Algorythm 
#  - Sub
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from Thompson.Thompson import Thompson
from NFA.NFA import NFA
import sys, getopt

from SubsetConstructionAlgorythm.SubsetConstructionAlgorythm import SubsetConstructionAlgorythm
from Direct.Direct import DirectToDFA
from utils.tree import generate_Tree

def generate_NFA(regex):
    return Thompson(regex).generate_NFA()


def main(argv):
    regex = ''
    string = ''
    try:
        opts, _ = getopt.getopt(argv,"hr:w",["regex=","string="])
    except getopt.GetoptError:
        print ('main.py -r <Regular Expression> -w <String>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -r <Regular Expression> -w <String>')
            sys.exit()
        elif opt in ("-r", "--regex"):
            regex = arg
        elif opt in ("-w", "--string"):
            string = arg
    return regex, string


def parse_regex(regex):
    regex = regex.replace('?','|ε')
    while('+' in regex):
        print(regex)
        index = regex.index('+')
        if(index>1):
            if(regex[index-1]!=')'):
                regex = regex[:index] + '(' + regex[index-1] + ")*" + regex[index+1:]
            else:
                new_index = index
                while(regex[new_index]!='('):
                    new_index -= 1
                    if(index==0):
                        raise SyntaxError        
                regex = regex[:new_index] + regex[new_index:index] + regex[new_index:index]  + "*"  + regex[index+1:]
        else:
            raise SyntaxError
    return regex

if __name__ == "__main__":
    regex, string = main(sys.argv[1:])  #Read regex and string
    regex = parse_regex(regex)
    
    
    print("--------------Regex-------------------")
    print(regex)
            
    
    nfa = generate_NFA(regex)
    
    print("----------------NFA-------------------")
    for transition in nfa.transitions.transitions:
        print(transition[0].id, transition[1])
        for state in transition[2]:
            print(state.id)
    
    print("-------Simulating... with NFA-------")
    if(nfa.simulate(string)):
        print("Pertenece al lenguje")
    else:
        print("No pertenece")
        
    subsetConstructionAlgorythm = SubsetConstructionAlgorythm(nfa)
    dfa = subsetConstructionAlgorythm.getDFA()
    
    print("----------------DFA-------------------")
    for transition in dfa.transitions.transitions:
        print(transition[0].id, transition[1])
        for state in transition[2]:
            print(state.id)
    
    print("-------Simulating... with DFA-------")
    if(dfa.simulate(string)):
        print("Pertenece al lenguje")
    else:
        print("No pertenece")
    
    
    root, alphabet = generate_Tree(regex)
    dfa = DirectToDFA(root, alphabet)
    
    print("--------------Direct-------------------")
    for transition in dfa.transitions.transitions:
        print(transition[0].id, transition[1])
        for state in transition[2]:
            print(state.id)
    
    print("-----Simulating... with DIRECT-----")
    if(dfa.simulate(string)):
        print("Pertenece al lenguje")
    else:
        print("No pertenece")