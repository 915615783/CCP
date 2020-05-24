from . import gramma
from graphviz import Digraph
class Grammatical_Tree_Node():
    def __init__(self, content):
        '''
        content: token(tuple) or str
        '''
        self.content = content
        self.children = []
        self.parent = None
        self.current_line = None

    def get_current_line(self):
        if self.current_line != None:
            return self.current_line
        else:
            return self.children[0].get_current_line()
    
    def is_leaf(self):
        return len(self.children) == 0

    def __str__(self):
        if isinstance(self.content, tuple):
            if self.content[1] == None:
                return str(self.content[0])
        return str(self.content)

    def __repr__(self):
        if isinstance(self.content, tuple):
            if self.content[1] == None:
                return str(self.content[0])
        return str(self.content)

    def view(self):
        dot = Digraph('Grammar Tree')
        dot.node(str(id(self)), self.__str__())
        self.recursive_view(dot)
        dot.view()

    def recursive_view(self, dot):
        if self.is_leaf() == False:
            for child in self.children:
                dot.node(str(id(child)), str(child))
                dot.edge(str(id(self)), str(id(child)))
                child.recursive_view(dot)

class Grammatical_Analyzer():
    '''LR Grammatical Analyzer'''
    def __init__(self, action, goto):
        self.action = action
        self.goto = goto

    def analysis(self, lexical_analyzer, C):
        get_token = lexical_analyzer.get_token
        id2bnf = gramma.BNF.id2BNF
        stack = [0]
        sign = []
        token = None
        while True:
            if token == None:
                try:
                    token = get_token()
                    current_line = lexical_analyzer.reader.current_line
                except EOFError:
                    token = ('$', None)
            action = self.action.get((stack[-1], token[0]), None)
            if action == None:
                print(sign)
                raise Exception('语法错误，语法分析表没有对应action. token: %s. (line: %d)'%(token, lexical_analyzer.reader.current_line))
            elif action[0] == 's':
                # 移进
                stack.append(int(action[1:]))
                sign.append(Grammatical_Tree_Node(token))
                sign[-1].current_line = current_line
                token = None
            elif action[0] == 'r':
                # 归约
                bnf = id2bnf[int(action[1:])]
                left = bnf.left
                right = list(bnf.right)
                if 'epsilon' in right:
                    right.remove('epsilon')
                reduce_length = len(right)
                if reduce_length != 0:
                    stack = stack[:-reduce_length]
                stack.append(self.goto[(stack[-1], left)])
                reduce_sign = sign[-reduce_length:]
                sign = sign[:-reduce_length]
                sign.append(self.reduce(reduce_sign, bnf))
            elif action == 'acc':
                # 接受
                if len(sign) != 1:
                    raise Exception('语法错误，接受时符号栈不止一个符号。(line %d)'%(lexical_analyzer.reader.current_line))
                return sign[0]
            

    def reduce(self, reduce_sign, bnf):
        '''归约'''
        parent = Grammatical_Tree_Node(bnf.left)
        parent.children.extend(reduce_sign)
        for sign in reduce_sign:
            sign.parent = parent
        return parent
                

