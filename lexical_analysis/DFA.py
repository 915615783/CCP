
class DFANode():
    id_count = 0
    def __init__(self, key):
        '''
        :param key: A sorted tuple of DFANode.id. 
        '''
        self.id = DFANode.id_count
        DFANode.id_count += 1
        self.key = self.sort_key(key)
        self.out = {}   # key: str    value: DFANode (not list)

    def add_out_edge(self, char, target_node):
        if char == 'epsilon':
            raise TypeError('DFA Node does not allow out edge of epsilon.')
        if self.out.get(char, None) != None:
            raise TypeError('DFA Node does not allow two edge share one char.')
        self.out[char] = target_node
        
    def sort_key(self, key):
        key = list(key)
        key.sort()
        return tuple(key)

def NFA2DFA(nfa_start):
