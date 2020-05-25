from semantic_analysis.Table import Table, TableItem

def get_width(type):
    if type == 'int':
        return 4
    elif type == 'float':
        return 4
    elif type == 'bool':
        return 1
    elif type == 'char':
        return 1

def p1(gram_node, tableptr, offset, three_addr_code):
    '''
    gram_node: left node
    '''
    t = Table(None)
    tableptr.append(t)
    offset.append(0)

def p2(gram_node, tableptr, offset, three_addr_code):
    # var_stmt->var_list.TYPE = var_stmt->type->token[0]
    gram_node.children[1].TYPE = gram_node.children[0].children[0].content[0]

def p3(gram_node, tableptr, offset, three_addr_code):
    gram_node.children[0].TYPE = gram_node.TYPE

def p4(gram_node, tableptr, offset, three_addr_code):
    gram_node.children[2].TYPE = gram_node.TYPE

def p5(gram_node, tableptr, offset, three_addr_code):
    gram_node.children[0].TYPE = gram_node.TYPE

def p6(gram_node, tableptr, offset, three_addr_code):
    name = gram_node.children[0].content[1]
    try:
        tableptr[-1].enter(name, gram_node.TYPE, offset[-1])
    except Exception as e:
        raise Exception(str(e) + (' (line: %d)' % gram_node.children[0].current_line))
    offset[-1] += get_width(gram_node.TYPE)

def p7(gram_node, tableptr, offset, three_addr_code):
    '''函数声明时创建新符号表'''
    t = Table(tableptr[-1])
    tableptr.append(t)
    offset.append(0)

def p8(gram_node, tableptr, offset, three_addr_code):
    '''函数声明完重定位'''
    t = tableptr[-1]
    t.addwidth(offset[-1])
    # t.addtheader()
    tableptr.pop()
    offset.pop()
    name = gram_node.children[1].content[1]
    try:
        tableptr[-1].enterproc(name, t, return_type=gram_node.children[0].children[0].content[0])
    except Exception as e:
        raise Exception(str(e) + (' (line: %d)' % gram_node.children[1].current_line))

def p9(gram_node, tableptr, offset, three_addr_code):
    '''复合语句开始时创建新符号表'''
    t = Table(tableptr[-1])
    tableptr.append(t)
    offset.append(0)

def p10(gram_node, tableptr, offset, three_addr_code):
    '''复合语句结束时重定位'''
    t = tableptr[-1]
    t.addwidth(offset[-1])
    # t.addtheader()
    tableptr.pop()
    offset.pop()
    compound_count = len([i for i in tableptr[-1].items if 'compound' in i.name])
    name = 'compound_sent' + str(compound_count)
    tableptr[-1].enterproc(name, t)





def p11(gram_node, tableptr, offset, three_addr_code):
    gram_node.TYPE = gram_node.children[0].TYPE
    gram_node.ENTRY = gram_node.children[0].ENTRY

def p12(gram_node, tableptr, offset, three_addr_code):
    # and or 语句
    # 先类型检查，检查子节点的类型是否匹配
    if gram_node.children[0].TYPE != 'bool' or gram_node.children[2].TYPE != 'bool':
        raise Exception('参与逻辑语句的变量不是bool. (line: %d)'%(gram_node.get_current_line()))
    # 然后TYPE从子节点传到父节点
    newTYPE = gram_node.children[0].TYPE
    gram_node.TYPE = newTYPE   # 可能会类型转换，但是这里先不转

    # 生成代码
    gram_node.ENTRY = three_addr_code.newtemp()
    E1 = gram_node.children[0]
    E2 = gram_node.children[2]
    three_addr_code.outcode(gram_node.ENTRY, ':=', E1.ENTRY, 
        gram_node.children[1].content[0], E2.ENTRY)

def p13(gram_node, tableptr, offset, three_addr_code):
    # 比较或算术运算语句
    # 先类型检查，检查子节点的类型是否匹配
    if gram_node.children[0].TYPE != gram_node.children[2].TYPE:
        print(gram_node.children[0].TYPE, gram_node.children[2].TYPE)
        raise Exception('运算符两边的类型不同. (line: %d)'%(gram_node.get_current_line()))
    # 蛮横需求之算术运算只支持int和float
    if gram_node.children[1].content[0] in ['+', '-', '*', '/']:
        if gram_node.children[0].TYPE not in ['int', 'float'] or gram_node.children[2].TYPE not in ['int', 'float']:
            raise Exception('非int或float类型参与算术运算. (line: %d)'%(gram_node.get_current_line()))
    # 然后TYPE从子节点传到父节点
    newTYPE = gram_node.children[0].TYPE
    if gram_node.children[1].content[0] in ['>', '>=', '==', '!=', '<=', '<']:
        newTYPE = 'bool'
    gram_node.TYPE = newTYPE   # 可能会类型转换，但是这里先不转

    # 生成中间代码
    gram_node.ENTRY = three_addr_code.newtemp()
    E1 = gram_node.children[0]
    E2 = gram_node.children[2]
    op = gram_node.children[1].content[0]
    if op in ['+', '-', '*', '/']:
        three_addr_code.outcode(gram_node.ENTRY, ':=', E1.ENTRY, op, E2.ENTRY)
    elif op in ['>', '>=', '==', '!=', '<=', '<']:
        label1, label_pointer1 = three_addr_code.newLabel()
        label2, label_pointer2 = three_addr_code.newLabel()
        three_addr_code.outcode('if', E1.ENTRY, op, E2.ENTRY, 'goto', label_pointer1)
        three_addr_code.outcode(gram_node.ENTRY, ':=', 0)
        three_addr_code.outcode('goto', label_pointer2)
        three_addr_code.outcode(gram_node.ENTRY, ':=', 1, label1)
        three_addr_code.outcode(label2)
        

def p14(gram_node, tableptr, offset, three_addr_code):
    # not语句
    # 先类型检查，检查子节点的类型是否匹配
    if gram_node.children[1].TYPE != 'bool':
        raise Exception('!后面的变量不是bool. (line: %d)'%(gram_node.get_current_line()))
    # 然后TYPE从子节点传到父节点
    newTYPE = gram_node.children[1].TYPE
    gram_node.TYPE = newTYPE   # 可能会类型转换，但是这里先不转

    # 生成代码
    gram_node.ENTRY = three_addr_code.newtemp()
    F1 = gram_node.children[1]
    three_addr_code.outcode(gram_node.ENTRY, ':=', 'not', F1.ENTRY)

def p15(gram_node, tableptr, offset, three_addr_code):
    gram_node.TYPE = gram_node.children[1].TYPE
    gram_node.ENTRY = gram_node.children[1].ENTRY

def p16(gram_node, tableptr, offset, three_addr_code):
    # 处理变量，获取TYPE并传递到父节点
    name = gram_node.children[0].content[1]
    item, itemtable = tableptr[-1].lookup(name)
    if item == None:
        raise Exception('使用未声明的标识符 %s. (line: %d)'%(name, gram_node.get_current_line()))
    gram_node.TYPE = item.type

    # 生成代码
    gram_node.ENTRY = (item, itemtable)

def p17(gram_node, tableptr, offset, three_addr_code):
    # 处理常数，获取TYPE并传递到父节点
    token = gram_node.children[0].content
    type_map = {'int_const': 'int', 'char_const':'char', 
        'float_const':'float', 'true':'bool', 'false':'bool'}
    gram_node.TYPE = type_map[token[0]]

    # 生成代码
    if gram_node.children[0].content[0] in ['true', 'false']:
        gram_node.ENTRY = gram_node.children[0].content[0]
    else:
        gram_node.ENTRY = gram_node.children[0].content[1]

def p18(gram_node, tableptr, offset, three_addr_code):
    # 处理函数调用，获取返回值TYPE并传递到父节点
    name = gram_node.children[0].content[1]
    item, itemtable = tableptr[-1].lookup(name)
    if item == None:
        raise Exception('使用未声明的函数标识符 %s. (line: %d)'%(name, gram_node.get_current_line()))
    assert item.return_type != None
    gram_node.TYPE = item.return_type

def p19(gram_node, tableptr, offset, three_addr_code):
    '''类型不同不能赋值'''
    iditem, t = tableptr[-1].lookup(gram_node.children[0].content[1])
    if iditem == None:
        raise Exception('给未声明标识符赋值. (line: %d)'%(gram_node.get_current_line()))
    if iditem.type != gram_node.children[2].TYPE:
        raise Exception('不同类型不能赋值. (line: %d)'%(gram_node.get_current_line()))

    # 赋值语句生成代码
    (p, t) = tableptr[-1].lookup(gram_node.children[0].content[1])
    expr = gram_node.children[2]
    three_addr_code.outcode((p, t), ':=', expr.ENTRY)

def p20(gram_node, tableptr, offset, three_addr_code):
    raise Exception('丢失运算符. (line: %d)'%(gram_node.get_current_line()))





# if语句
def p21(gram_node, tableptr, offset, three_addr_code):
    E = gram_node.children[2]
    label, label_pointer = three_addr_code.newLabel()
    E.JUMPLABEL = label
    three_addr_code.outcode('if', E.ENTRY, '==', '0', 'goto', label_pointer)

def p22(gram_node, tableptr, offset, three_addr_code):
    E = gram_node.children[2]
    three_addr_code.outcode(E.JUMPLABEL)

def p23(gram_node, tableptr, offset, three_addr_code):
    E = gram_node.children[2]
    E_true = gram_node.children[4]
    label, label_pointer = three_addr_code.newLabel()
    E_true.JUMPLABEL = label
    three_addr_code.outcode('goto', label_pointer)
    three_addr_code.outcode(E.JUMPLABEL)

def p24(gram_node, tableptr, offset, three_addr_code):
    E_true = gram_node.children[4]
    three_addr_code.outcode(E_true.JUMPLABEL)



# while
def p25(gram_node, tableptr, offset, three_addr_code):
    E = gram_node.children[2]
    end_label, end_label_pointer = three_addr_code.newLabel()
    gram_node.ENDLABEL = end_label
    three_addr_code.outcode('if', E.ENTRY, '==', '0', 'goto', end_label_pointer)

def p26(gram_node, tableptr, offset, three_addr_code):
    three_addr_code.outcode('goto', gram_node.BEGINLABELPOINTER)
    three_addr_code.outcode(gram_node.ENDLABEL)

def p27(gram_node, tableptr, offset, three_addr_code):
    begin_label, begin_label_pointer = three_addr_code.newLabel()
    gram_node.BEGINLABELPOINTER = begin_label_pointer
    three_addr_code.outcode(begin_label)




def p28(gram_node, tableptr, offset, three_addr_code):
    type = gram_node.children[0].children[0].content[0]
    name = gram_node.children[1].content[1]
    try:
        tableptr[-1].enter(name, type, offset[-1])
    except Exception as e:
        raise Exception(str(e) + (' (line: %d)' % gram_node.get_current_line()))
    print(type)
    offset[-1] += get_width(type)
