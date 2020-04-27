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
        self.right = tuple(right)
        self.BNF_id = BNF_id
        self.dot = dot

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
    