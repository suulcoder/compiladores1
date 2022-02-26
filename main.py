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

if __name__ == "__main__":
    regex, string = main(sys.argv[1:])  #Read regex and string
    nfa = generate_NFA(regex)
    for transition in nfa.transitions.transitions:
        print(transition[0].id, transition[1])
        for state in transition[2]:
            print(state.id)
    