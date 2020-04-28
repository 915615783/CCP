
class BNF():
    id_count = 0
    id2BNF = {}
    def __init__(self, left, right):
        '''
        :param left: str
        :param right: list or tuple of str
        '''
        self.id = BNF.id_count
        BNF.id_count += 1
        BNF.id2BNF[self.id] = self
        self.left = left
        self.right = tuple(right) # tuple of str

    def __str__(self):
        return self.left + ' -> ' + ' '.join(self.right)

    def __repr__(self):
        return self.left + ' -> ' + ' '.join(self.right)

    def __eq__(self, other):
        return (self.left == other.left) and (self.right == other.right)

class Gramma():
    def __init__(self, gramma_path, vocab_table, is_augmented_gramma=True):
        self.BNFs = self.load_gramma_from_file(gramma_path)
        # 增广文法
        if is_augmented_gramma:
            self.S = self.BNFs[0].left
            self.BNFs.insert(0, BNF(self.S+'\'', [self.S]))
        self.S = self.BNFs[0].left
        self.vocab_table = vocab_table
        self.Vt, self.Vn = self.get_Vt_and_Vn()
        self.FIRST_cache = {}
        self.FOLLOW_stack = set([]) # 用来防止不断递归，标记正在算的符号，不会再次访问

    def FIRST(self, x):
        '''
        x: list of str or str
        return a set of vt
        '''
        if isinstance(x, str):
            if self.FIRST_cache.get(x, None) != None:
                return self.FIRST_cache[x]
            elif x in self.Vt:
                self.FIRST_cache[x] = set([x])
            elif x in self.Vn:
                result = set([])
                left_recursion = []
                for bnf in self.BNFs:
                    if bnf.left == x:
                        if bnf.right[0] == x:
                            left_recursion.append(bnf.right[1:])   # 处理直接左递归情况
                            continue
                        result = result | self.FIRST(bnf.right)
                if 'epsilon' in result:
                    for i in left_recursion:
                        result = result | self.FIRST(i)
                self.FIRST_cache[x] = result
            return self.FIRST(x)
        else:
            x = tuple(x)
            if self.FIRST_cache.get(x, None) != None:
                return self.FIRST_cache[x]
            else:
                result = set([])
                for i in x:
                    first_i = self.FIRST(i)
                    if 'epsilon' in first_i:
                        first_i.remove('epsilon')
                        result = result | first_i
                    else:
                        result = result | first_i
                        self.FIRST_cache[x] = result
                        return result
                result.add('epsilon')
                self.FIRST_cache[x] = result
                return result

    def FOLLOW(self, x):
        '''x是一个符号'''
        self.FOLLOW_stack.add(x)
        result = set([])
        if x == self.S:
            result.add('$')
        for bnf in self.BNFs:
            if x in bnf.right:
                right = bnf.right
                while x in right:    # 这里之前有个bug，一个生成式右部可能同时有几个相同的符号，list.index只能提取出一个。必须把他们都找出来！
                    index = right.index(x)
                    first_i = []
                    if index < len(right)-1:
                        first_i = self.FIRST(right[index+1:])
                        result.update(first_i - {'epsilon'})
                    right = right[index+1:]
                if ('epsilon' not in first_i) and (len(right)!=0):
                    continue
                    
                if bnf.left not in self.FOLLOW_stack:
                    result.update(self.FOLLOW(bnf.left))
        self.FOLLOW_stack.remove(x)
        return result

    def get_Vt_and_Vn(self):
        '''epsilon is a special Vt'''
        V = set([])
        for i in self.BNFs:
            V.add(i.left)
            V.update(i.right)
        Vt = V & (set(self.vocab_table) | set(['epsilon']))
        Vn = V - Vt
        return Vt, Vn
        
    def load_gramma_from_file(self, gramma_path):
        with open(gramma_path, 'r') as f:
            lines = f.readlines()
        BNFs = []
        for line in lines:
            left, rights = line.strip().split('->')
            left = left.strip()
            rights = rights.strip()
            for right in rights.split('|'):
                BNFs.append(BNF(left, right.strip().split(' ')))
        return BNFs
