from . import gramma
class Grammatical_Tree_Node():
    def __init__(self, content):
        '''
        content: token(tuple) or str
        '''
        self.content = content
        self.children = []
        self.parent = None
    
    def is_leaf(self):
        return len(self.children) == 0

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self.content)

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
                except EOFError:
                    token = ('$', None)
            action = self.action.get((stack[-1], token[0]), None)
            if action == None:
                raise Exception('语法错误，语法分析表没有对应action. token: %s. (line: %d)'%(token, lexical_analyzer.reader.current_line))
            elif action[0] == 's':
                # 移进
                stack.append(int(action[1:]))
                sign.append(Grammatical_Tree_Node(token))
                token = None
            elif action[0] == 'r':
                # 归约
                bnf = id2bnf[int(action[1:])]
                print(bnf)
                # print(bnf)
                left = bnf.left
                right = list(bnf.right)
                if 'epsilon' in right:
                    right.remove('epsilon')
                reduce_length = len(right)
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
        parent = Grammatical_Tree_Node(bnf.left)
        parent.children.extend(reduce_sign)
        for sign in reduce_sign:
            sign.parent = parent
        return parent
                

