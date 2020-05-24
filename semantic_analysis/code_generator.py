from semantic_analysis.Table import TableItem
class ThreeAddressCode():
    def __init__(self):
        self.code = []   # list of str(line)
        self.temp_count = 0

    def newtemp(self):
        self.temp_count += 1
        return 't%d' % (self.temp_count - 1)

    def outcode(self, *args):
        self.code.append(args)

    def show(self):
        count = 0
        for line in self.code:
            count += 1
            out = []
            for i in line:
                if isinstance(i, tuple):   # 标识符的ENTRY是tuple (tableItem, tableid)
                    out.append(str((i[0].name, i[1])))
                else:
                    out.append(str(i))
            print(str(count).rjust(3,' ') + '| ' ,' '.join(out))

    def __len__(self):
        return len(self.code)
                
                
