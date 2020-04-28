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
        self.C = None   # LR(0)项集族C

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
                        




