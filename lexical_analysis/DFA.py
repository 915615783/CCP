from . import NFA
class DFANode():
    id_count = 0
    key2Node = {}
    def __init__(self, key):
        '''
        :param key: A sorted tuple of DFANode.id. 
        '''
        self.id = DFANode.id_count
        DFANode.id_count += 1
        self.key = key
        DFANode.key2Node[self.key] = self
        self.out = {}   # key: str    value: DFANode (not list)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def add_out_edge(self, char, target_node):
        if char == 'epsilon':
            raise TypeError('DFA Node does not allow out edge of epsilon.')
        if self.out.get(char, None) != None:
            raise TypeError('DFA Node does not allow two edge share one char.')
        self.out[char] = target_node

    def is_exist_next(self, char):
        if self.out.get(char, None) == None:
            return False
        return True

    def next(self, char):
        return self.out[char]

    def is_acceptable(self):
        for i in [NFA.NFANode.id2Node[nid].accept_vocab for nid in self.key if NFA.NFANode.id2Node[nid].accept_vocab  != None]:
            if i != None:
                return True
        return False

    def accept(self, vocab_table):
        '''
        :param vocab_table: 确定优先级
        :return:
        '''
        acceptable_vocabs = [NFA.NFANode.id2Node[nid].accept_vocab for nid in self.key if NFA.NFANode.id2Node[nid].accept_vocab  != None]
        for i in vocab_table:
            if i in acceptable_vocabs:
                return i
        raise ValueError('Not acceptable!')



def epsilon_closure_s(nfa_node):
    '''return sorted tuple of nfa node id'''
    result = set([])
    queue = [nfa_node]
    while len(queue) > 0:
        node = queue.pop(0)
        if node.out.get('epsilon', None) != None:
            queue.extend([i for i in node.out['epsilon'] if i.id not in result])
        result.add(node.id)
    result = list(result)
    result.sort()
    return tuple(result)

def epsilon_closure_T(T):
    '''return sorted tuple of nfa node id'''
    result = set([])
    queue = [NFA.NFANode.id2Node[i] for i in T]
    while len(queue) > 0:
        node = queue.pop(0)
        if node.out.get('epsilon', None) != None:
            queue.extend([i for i in node.out['epsilon'] if i.id not in result])
        result.add(node.id)
    result = list(result)
    result.sort()
    return tuple(result)

def move(T, char):
    '''return unsorted tuple of nfa node id'''
    result = set([])
    for i in T:
        if NFA.NFANode.id2Node[i].out.get(char, None) != None:
            for node in NFA.NFANode.id2Node[i].out.get(char, None):
                result.add(node.id)
    return tuple(result)


def NFA2DFA(nfa_start):
    start = DFANode(epsilon_closure_s(nfa_start))
    Dstates = [start]   # using as a queue with DFANode
    while len(Dstates) > 0:
        dfa_node = Dstates.pop(0)
        for char in NFA.get_char_set():
            move_T = move(dfa_node.key, char)
            if len(move_T) == 0:
                continue
            U = epsilon_closure_T(move_T)
            if DFANode.key2Node.get(U, None) != None:
                U = DFANode.key2Node[U]
            else:
                U = DFANode(U)
                Dstates.append(U)
            dfa_node.add_out_edge(char, U)
    return start