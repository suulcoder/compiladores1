from NFA.NFA import NFA

class Node(object):
    def __init__(self, value, nfa, index_start, index_end):
        super(Node, self).__init__()
        self.value = value
        self.nfa = nfa
        self.index_start = index_start
        self.index_end = index_end
        
    def __str__(self):
        return self.valuexs