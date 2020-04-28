from . import gramma

class Item():
    id_count = 0

    def __init__(self, left, right, BNF_id, dot='dot'):
        '''
        :param left: str
        :param right: list or tuple of str
        '''
        self.id = Item.id_count
        Item.id_count += 1
        self.left = left
        self.right = tuple([i for i in right if i != 'epsilon'])
        self.BNF_id = BNF_id
        self.dot = dot

    def next_item(self):
        '''返回一个新的item对象， dot向后移一格'''
        return Item.from_BNF(gramma.BNF.id2BNF[self.BNF_id], self.dot_index()+1)

    def dot_index(self):
        return self.right.index(self.dot)

    def is_reducible(self):
        '''是否可归约'''
        return self.right.index(self.dot) == len(self.right)-1

    def __hash__(self):
        return hash(self.__str__())

    @classmethod
    def from_BNF(cls, bnf, dot_pos, dot='dot'):
        right = list(bnf.right)
        right.insert(dot_pos, dot)
        return Item(bnf.left, right, bnf.id, dot)

    def __str__(self):
        right = []
        for i in self.right:
            if i == self.dot:
                right.append('·')
            else:
                right.append(i)
        return self.left + ' -> ' + ' '.join(right)

    def __repr__(self):
        right = []
        for i in self.right:
            if i == self.dot:
                right.append('·')
            else:
                right.append(i)
        return self.left + ' -> ' + ' '.join(right)

    def __eq__(self, other):
        return (self.left == other.left) and (self.right == other.right)
    
class SLR1():
    def __init__(self, augment_gramma):
        self.G = augment_gramma
        self.C = self.item_sets()   # LR(0)项集族C list  分析时从第0个item开始

    def item_sets(self):
        '''构建LR(0)项集族C'''
        C = []
        queue = [self.closure({Item.from_BNF(self.G.BNFs[0], 0)})]
        while len(queue) != 0:
            item_set = queue.pop(0)
            if item_set in C:
                continue
            for v in ((self.G.Vt | self.G.Vn) - {'epsilon'}):
                goto_set = self.goto(item_set, v)
                if len(goto_set) == 0:
                    continue
                queue.append(goto_set)
            C.append(item_set)
        return C

    def closure(self, item_set):
        result = set([])
        queue = list(item_set)
        while len(queue) != 0:
            item = queue.pop(0)
            if item in result:
                continue
            if item.is_reducible() == False:
                B = item.right[item.dot_index() + 1]
                for bnf in self.G.BNFs:
                    if B == bnf.left:
                        queue.append(Item.from_BNF(bnf, 0))
            result.add(item)
        return result

    def goto(self, item_set, x):
        '''
        x: str. not include epsilon
        '''
        result = set([])
        for item in item_set:
            if item.is_reducible() == False:
                if x == item.right[item.dot_index() + 1]:
                    result.add(item.next_item())
        return self.closure(result)

    def get_action_goto(self):
        '''
        获取slr1分析表
        return action(dict), goto(dict)
        action: {(int, str): str}
        goto: {(int, str): int}
        '''
        action = {}
        goto = {}
        for i, item_set in enumerate(self.C):
            for item in item_set:
                if item.is_reducible() == False:
                    # 移进项目
                    x = item.right[item.dot_index()+1]
                    if x in self.G.Vt:
                        if action.get((i, x), None) == None:
                            action[(i, x)] = 's' + str(self.C.index(self.goto(item_set, x)))
                        else:
                            if action[(i, x)] != ('s' + str(self.C.index(self.goto(item_set, x)))):
                                raise Exception('不是slr1语法,无法建立分析表')
                    elif x in self.G.Vn:
                        if goto.get((i, x), None) == None:
                            goto[(i, x)] = self.C.index(self.goto(item_set, x))
                        else:
                            if goto[(i, x)] != self.C.index(self.goto(item_set, x)):
                                raise Exception('不是slr1语法,无法建立分析表')
                else:
                    # 归约项目
                    A = item.left
                    if A == self.G.S:
                        action[(i, '$')] = 'acc'
                    else:
                        target = 'r' + str(item.BNF_id)
                        for x in self.G.FOLLOW(A):
                            if action.get((i, x), None) == None:
                                action[(i, x)] = target
                            else:
                                if action[(i, x)] != target:
                                    print(item, x)
                                    raise Exception('不是slr1语法,无法建立分析表')
        return action, goto
                    

                        



    
                        
    




