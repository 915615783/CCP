def check_bracket(lex_analyzer):
    # 测试丢失括号，顺便把丢失操作数也检查一下
    big_stack = []   # 处理大括号
    small_stack = []   # 处理小括号

    prev_token = (None, None)
    while True:
        try:
            token = lex_analyzer.get_token()
        except EOFError:
            break
        
        # 硬加进来检查操作数丢失
        if prev_token[0] in ['+', '-', '*', '/'] and token[0] == ')':
            raise Exception('丢失操作数。(line: %d)' % lex_analyzer.reader.current_line)

        if token[0] == '(':
            small_stack.append(lex_analyzer.reader.current_line)
        elif token[0] == '{':
            big_stack.append(lex_analyzer.reader.current_line)
        elif token[0] == '}':
            if len(big_stack) == 0:
                raise Exception('丢失左大括号。(line: %d)' % lex_analyzer.reader.current_line)
            big_stack.pop()
        elif token[0] == ')':
            if len(small_stack) == 0:
                raise Exception('丢失左小括号。(line: %d)' % lex_analyzer.reader.current_line)
            small_stack.pop()
        prev_token = token
    
    if len(small_stack) != 0:
        raise Exception('丢失右小括号。(line: %d)' % small_stack[-1])
    if len(big_stack) != 0:
        raise Exception('丢失右大括号。(line: %d)' % big_stack[-1])

    
