from semantic_analysis import SDTFunctions
from semantic_analysis import code_generator

class SDT():
    key2SDT = {}
    def __init__(self, left, right):
        '''
        :param left: str
        :param right: list or tuple of str
        '''
        self.left = left
        self.right = tuple(right) # tuple of str
        self.key = (left, self.right_without_proc())
        SDT.key2SDT[self.key] = self

    def right_without_proc(self):
        return tuple([i for i in self.right if i[:2] != '__'])

    def __str__(self):
        return self.left + ' -> ' + ' '.join(self.right)

    def __repr__(self):
        return self.left + ' -> ' + ' '.join(self.right)

    @classmethod
    def get_SDT_by_gram_node(cls, gram_node):
        '''gram_node: gramma tree node (root of a subtree)'''
        key = (gram_node.content, tuple([i.content[0] if isinstance(i.content, tuple) else i.content for i in gram_node.children]))
        return cls.key2SDT.get(key)

class SDTs():
    def __init__(self, SDTs_path):
        '''
        SDTs_path 翻译方案的路径
        '''
        self.SDTs = self.load_SDTs_from_file(SDTs_path)

    def load_SDTs_from_file(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
        mySDTs = []
        for line in lines:
            left, rights = line.strip().split('->')
            left = left.strip()
            rights = rights.strip()
            for right in rights.split('|'):
                mySDTs.append(SDT(left, right.strip().split(' ')))
        return mySDTs

class SemanticAnalyzer():
    def __init__(self):
        self.tableptr = []
        self.offset = []
        self.three_addr_code = code_generator.ThreeAddressCode()

    def analysis(self, gram_node):
        '''return the root table'''
        self.DFS(gram_node)
        return self.tableptr[0]

    def DFS(self, gram_node):
        '''递归DFS遍历并执行翻译方案中的函数'''
        if gram_node.is_leaf():
            return
        sdt = SDT.get_SDT_by_gram_node(gram_node)
        index = 0
        for i in sdt.right:
            if i[:2] == '__':
                '''遇到翻译方案的函数，要执行它'''
                func_name = i.split('__')[1]
                func = SDTFunctions.__dict__[func_name]
                func(gram_node, self.tableptr, self.offset, self.three_addr_code)
            else:
                self.DFS(gram_node.children[index])
                index += 1


