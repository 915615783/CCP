from semantic_analysis.Table import TableItem
class ThreeAddressCode():
    def __init__(self):
        self.code = []   # list of str(line)
        self.temp_count = 0
        self.label_count = 0

    def newLabel(self):
        '''返回标记和指针'''
        label = '__label%d__' % (self.label_count)
        label_pointer = '__->label%d__' % (self.label_count)
        self.label_count += 1
        return label, label_pointer

    def is_exist_pointer(self):
        for i in self.code:
            for j in i:
                if '__->label' in str(j):
                    return True
        return False
    
    def find_a_label(self):
        '''找到一个label'''
        for i, line in enumerate(self.code):
            for j in line:
                if '__label' in str(j):
                    label_line = i + 1
                    label_pointer = j
                    label_pointer = j[:2] + '->' + j[2:]
                    return label_line, label_pointer, j
        return None, None, None

    def fill_pointer(self):
        while self.is_exist_pointer():
            label_line, label_pointer, label = self.find_a_label()
            for i in self.code:
                for j in range(len(i)):
                    if i[j] == label_pointer:
                        i[j] = label_line
            self.code[label_line-1].remove(label)

    def newtemp(self):
        self.temp_count += 1
        return 't%d' % (self.temp_count - 1)

    def outcode(self, *args):
        self.code.append(list(args))

    def merge_single_label(self):
        '''如果某行只有一个label，指针重定位之后label会被删掉，则那一行会啥都没有'''
        '''因此需要把只有label的行和下一行合并'''
        single_labels = []
        for i in self.code:
            if len(i) == 1 and '__label' in str(i[0]):
                single_labels.append(i)
        for i in single_labels:
            index = self.code.index(i)
            if index+1 < len(self.code):
                self.code[index + 1].extend(i)
                self.code.pop(index)


    def show(self):
        self.merge_single_label()
        self.fill_pointer()
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
                
                
# a = ThreeAddressCode()
# l, p = a.newLabel()
# l2, p2 = a.newLabel()
# a.outcode(123, 124214)
# a.outcode('add', l2, 'ffff')
# a.outcode('goto', p)

# a.outcode('goto', p2, 'hahaha')
# a.outcode('asdf')
# a.outcode(l)
# a.show()
