import string

class NFANode():
    id_count = 0
    id2Node = {}
    def __init__(self):
        self.id = NFANode.id_count
        NFANode.id_count += 1
        NFANode.id2Node[self.id] = self
        self.out = {}   # key: str    value: list of node
        self.accept_vocab = None

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def add_out_edge(self, char, target_node):
        if self.out.get(char, None) == None:
            self.out[char] = [target_node]
        else:
            self.out[char].append(target_node)

def get_char_set():
    '''get all char.(not include epsilon)'''
    chars = []
    for i in NFANode.id2Node.values():
        chars.extend(list(i.out.keys()))
    chars = set(chars)
    chars.remove('epsilon')
    return list(chars)

def union(list_of_pair):
    # list_of_pair [(start_node, end_node), (...)...]
    # return (start, end)
    start = NFANode()
    end = NFANode()
    for pair in list_of_pair:
        start.add_out_edge('epsilon', pair[0])
        pair[1].add_out_edge('epsilon', end)
    return (start, end)

def link(list_of_pair):
    for i in range(len(list_of_pair)-1):
        list_of_pair[i][1].add_out_edge('epsilon', list_of_pair[i+1][0])
    return (list_of_pair[0][0], list_of_pair[-1][1])

def closure(pair):
    start = NFANode()
    end = NFANode()
    start.add_out_edge('epsilon', pair[0])
    pair[1].add_out_edge('epsilon', pair[0])
    pair[1].add_out_edge('epsilon', end)
    start.add_out_edge('epsilon', end)
    return (start, end)

def closure_plus(pair):
    start = NFANode()
    end = NFANode()
    start.add_out_edge('epsilon', pair[0])
    pair[1].add_out_edge('epsilon', pair[0])
    pair[1].add_out_edge('epsilon', end)
    return (start, end)

def make_pair(char):
    start = NFANode()
    end = NFANode()
    start.add_out_edge(char, end)
    return (start, end)

def make_pair_from_string(s):
    (start, end) = make_pair(s[0])
    for i in s[1:]:
        new_end = NFANode()
        end.add_out_edge(i, new_end)
        end = new_end
    return (start, end)

def letter():
    # Return a start node and a end node
    list_of_pair = [make_pair(l) for l in string.ascii_letters]
    return union(list_of_pair)

def letter_and_():
    list_of_pair = [make_pair(l) for l in (string.ascii_letters + '_')]
    return union(list_of_pair)

def digit():
    list_of_pair = [make_pair(d) for d in string.digits]
    return union(list_of_pair)

def digit_1to9():
    list_of_pair = [make_pair(d) for d in string.digits[1:]]
    return union(list_of_pair)

def intiger():
    return union([digit(), link([digit_1to9(), closure(digit())])])

def Float():
    return link([union([digit(), link([digit_1to9(), closure(digit())])]), make_pair('.'), closure(digit())])

def ID():
    return link([letter_and_(), closure(union([letter_and_(), digit()]))])

def charactor():
    return link([make_pair("'"), letter(), make_pair("'")])

def delim():
    # 空格或者换行符
    return union([make_pair(' '), make_pair('\t'), make_pair('\n')])

def ws():
    return closure_plus(delim())

def make_NFA(list_of_pair, vocab_table):
    # 合并所有分支，并且把分支最后一个Node改成accept状态
    # return 一个start Node
    start = NFANode()
    if len(list_of_pair) != len(vocab_table):
        raise Exception('List of pair and vocab not match with length')
    for i in range(len(list_of_pair)):
        list_of_pair[i][1].accept_vocab = vocab_table[i]
        start.add_out_edge('epsilon', list_of_pair[i][0])
    return start

