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

def p12(gram_node, tableptr, offset, three_addr_code):
    # and or 语句
    # 先类型检查，检查子节点的类型是否匹配
    if gram_node.children[0].TYPE != 'bool' or gram_node.children[2].TYPE != 'bool':
        raise Exception('参与逻辑语句的变量不是bool. (line: %d)'%(gram_node.get_current_line()))
    # 然后TYPE从子节点传到父节点
    newTYPE = gram_node.children[0].TYPE
    gram_node.TYPE = newTYPE   # 可能会类型转换，但是这里先不转

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

def p14(gram_node, tableptr, offset, three_addr_code):
    # not语句
    # 先类型检查，检查子节点的类型是否匹配
    if gram_node.children[1].TYPE != 'bool':
        raise Exception('!后面的变量不是bool. (line: %d)'%(gram_node.get_current_line()))
    # 然后TYPE从子节点传到父节点
    newTYPE = gram_node.children[1].TYPE
    gram_node.TYPE = newTYPE   # 可能会类型转换，但是这里先不转

def p15(gram_node, tableptr, offset, three_addr_code):
    gram_node.TYPE = gram_node.children[1].TYPE

def p16(gram_node, tableptr, offset, three_addr_code):
    # 处理变量，获取TYPE并传递到父节点
    name = gram_node.children[0].content[1]
    item, itemtable = tableptr[-1].lookup(name)
    if item == None:
        raise Exception('使用未声明的标识符 %s. (line: %d)'%(name, gram_node.get_current_line()))
    gram_node.TYPE = item.type

def p17(gram_node, tableptr, offset, three_addr_code):
    # 处理常数，获取TYPE并传递到父节点
    token = gram_node.children[0].content
    type_map = {'int_const': 'int', 'char_const':'char', 
        'float_const':'float', 'true':'bool', 'false':'bool'}
    gram_node.TYPE = type_map[token[0]]

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
    if iditem.type != gram_node.children[2].TYPE:
        raise Exception('不同类型不能赋值. (line: %d)'%(gram_node.get_current_line()))

def p20(gram_node, tableptr, offset, three_addr_code):
    raise Exception('丢失运算符. (line: %d)'%(gram_node.get_current_line()))