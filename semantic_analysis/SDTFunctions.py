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

def p1(gram_node, tableptr, offset):
    '''
    gram_node: left node
    '''
    t = Table(None)
    tableptr.append(t)
    offset.append(0)

def p2(gram_node, tableptr, offset):
    # var_stmt->var_list.TYPE = var_stmt->type->token[0]
    gram_node.children[1].TYPE = gram_node.children[0].children[0].content[0]

def p3(gram_node, tableptr, offset):
    gram_node.children[0].TYPE = gram_node.TYPE

def p4(gram_node, tableptr, offset):
    gram_node.children[2].TYPE = gram_node.TYPE

def p5(gram_node, tableptr, offset):
    gram_node.children[0].TYPE = gram_node.TYPE

def p6(gram_node, tableptr, offset):
    name = gram_node.children[0].content[1]
    try:
        tableptr[-1].enter(name, gram_node.TYPE, offset[-1])
    except Exception as e:
        raise Exception(str(e) + (' (line: %d)' % gram_node.children[0].current_line))
    offset[-1] += get_width(gram_node.TYPE)

def p7(gram_node, tableptr, offset):
    '''函数声明时创建新符号表'''
    t = Table(tableptr[-1])
    tableptr.append(t)
    offset.append(0)

def p8(gram_node, tableptr, offset):
    '''函数声明完重定位'''
    t = tableptr[-1]
    t.addwidth(offset[-1])
    # t.addtheader()
    tableptr.pop()
    offset.pop()
    name = gram_node.children[1].content[1]
    try:
        tableptr[-1].enterproc(name, t)
    except Exception as e:
        raise Exception(str(e) + (' (line: %d)' % gram_node.children[1].current_line))

def p9(gram_node, tableptr, offset):
    '''复合语句开始时创建新符号表'''
    t = Table(tableptr[-1])
    tableptr.append(t)
    offset.append(0)

def p10(gram_node, tableptr, offset):
    '''复合语句结束时重定位'''
    t = tableptr[-1]
    t.addwidth(offset[-1])
    # t.addtheader()
    tableptr.pop()
    offset.pop()
    compound_count = len([i for i in tableptr[-1].items if 'compound' in i.name])
    name = 'compound_sent' + str(compound_count)
    tableptr[-1].enterproc(name, t)

