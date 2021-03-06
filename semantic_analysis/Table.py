
class TableItem():
    def __init__(self, name, type, addr=None, newtable=None, return_type=None):
        self.name = name   # str
        self.type = type   # str
        self.addr = addr   # int
        self.newtable = newtable   # table object
        self.return_type = return_type

    def __str__(self):
        if self.newtable != None:
            return self.name.ljust(15, ' ') + ' ' + self.type.ljust(10, ' ') + ' ' + str(self.addr).ljust(6, ' ') + ' ' + str(self.newtable.id)
        else:
            return self.name.ljust(15, ' ') + ' ' + self.type.ljust(10, ' ') + ' ' + str(self.addr).ljust(6, ' ') + ' ' + str(self.newtable)

    def __repr__(self):
        if self.newtable != None:
            return self.name.ljust(15, ' ') + ' ' + self.type.ljust(10, ' ') + ' ' + str(self.addr).ljust(6, ' ') + ' ' + str(self.newtable.id)
        else:
            return self.name.ljust(15, ' ') + ' ' + self.type.ljust(10, ' ') + ' ' + str(self.addr).ljust(6, ' ') + ' ' + str(self.newtable)

class Table():
    id_count = 0
    id2Table = {}
    def __init__(self, previous):
        self.id = Table.id_count
        Table.id_count += 1
        Table.id2Table[self.id] = self
        self.previous = previous
        self.items = []
        self.width = None

    def print_all(self):
        '''dfs show all subtable'''
        print(self)
        print()
        for i in self.items:
            if i.type == 'proc':
                i.newtable.print_all()

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def lookup(self, name):
        '''沿着table指针一直往前搜索，返回最近的一个table item 和 table id，找不到则返回None'''
        result = self.find_item_by_name(name)
        if result == None:
            if isinstance(self.previous, Table):
                return self.previous.lookup(name)
            else:
                return None, None
        else:
            return result, self.id
                

    def find_item_by_name(self, name):
        '''return None if can't find, only finding in one table'''
        for i in self.items:
            if name == i.name:
                return i
        return None

    def enter(self, name, type, offset):
        if self.find_item_by_name(name) != None:
            raise Exception('在同一个作用域内重复定义变量。')
        self.items.append(TableItem(name, type, offset))

    def addtheader(self, num, pwth, type, width):
        raise NotImplementedError('Table.addtheader not implemented')

    def addwidth(self, width):
        self.width = width

    def enterproc(self, name, newtable, return_type=None):
        if self.find_item_by_name(name) != None:
            raise Exception('在同一个作用域内重复定义过程。')
        self.items.append(TableItem(name, 'proc', newtable=newtable, return_type=return_type))

    def __str__(self):
        header = 'Name'.ljust(15, ' ') + ' ' + 'Type'.ljust(10, ' ') + ' ' + 'Addr'.ljust(6, ' ') + ' ' + 'New_Talbe_ID' + '\n'
        if isinstance(self.previous, Table):
            return '====  Table id: '+ str(self.id) + ', previous id: ' + str(self.previous.id) + '  ====\n' + header + '\n'.join([str(i) for i in self.items]) + '\n=============================='
        else:
            return '====  Table id: '+ str(self.id) + ', previous id: ' + str(self.previous) + '  ====\n' + header + '\n'.join([str(i) for i in self.items]) + '\n=============================='

    def __repr__(self):
        header = 'Name'.ljust(15, ' ') + ' ' + 'Type'.ljust(10, ' ') + ' ' + 'Addr'.ljust(6, ' ') + ' ' + 'New_Talbe_ID' + '\n'
        if isinstance(self.previous, Table):
            return '====  Table id: '+ str(self.id) + ', previous id: ' + str(self.previous.id) + '  ====\n' + header + '\n'.join([str(i) for i in self.items]) + '\n=============================='
        else:
            return '====  Table id: '+ str(self.id) + ', previous id: ' + str(self.previous) + '  ====\n' + header + '\n'.join([str(i) for i in self.items]) + '\n=============================='

# a = Table('Nil')
# a.enter('a', 'int', 0)
# a.enter('asdf', 'float', 4)
# a.enterproc('myfunc', Table(a))
# a.enterproc('myfunc', Table(a))
# print(a)
