from lexical_analysis import lexical_analysis, lexical_analyzer
from grammatical_analysis import gramma, SLR1, grammatical_analyzer
from semantic_analysis.semantic_analysis import SDT, SDTs, SemanticAnalyzer
from semantic_analysis.check_bracket import check_bracket
# ==========  不知道什么情况，文法还是不太支持有epsilon的情况 ==========

# 词法分析
vocab_table = lexical_analysis.vocab_table
dfa = lexical_analysis.dfa
# 检查括号-------------------
reader = lexical_analyzer.Reader()
reader.set_text_from_file('lexical_analysis/ccode.c')
lex_analyzer = lexical_analyzer.Lexical_Analyzer(reader, dfa, vocab_table)
check_bracket(lex_analyzer)
# -----------------------------
reader = lexical_analyzer.Reader()
reader.set_text_from_file('lexical_analysis/ccode.c')
lex_analyzer = lexical_analyzer.Lexical_Analyzer(reader, dfa, vocab_table)

# count_dict = {}
# try:
#     while True:
#         token = lex_analyzer.get_token()
#         print(token)
#         if token[0] in count_dict:
#             count_dict[token[0]] += 1
#         else:
#             count_dict[token[0]] = 1

# except Exception:
#     pass

# print('行数:', lex_analyzer.reader.current_line)
# print('字符数:', lex_analyzer.reader.text.__len__())
# print('====== 各类单词出现次数统计表 ======')
# count_list = list(count_dict.items())
# count_list.sort(key=lambda x: x[1], reverse=True)
# for x, y in count_list:
#     print(x.ljust(14, ' '), y)
# print('===================================')


# 语法分析
# 获得增广文法对象
G = gramma.Gramma('grammatical_analysis/gramma.txt', vocab_table, is_augmented_gramma=True)
# 生成SLR(1)分析表
slr1 = SLR1.SLR1(G)
action, goto = slr1.get_action_goto()
# print(G.FOLLOW('assignment'))
# LR分析器
slr1_analyzer = grammatical_analyzer.Grammatical_Analyzer(action, goto)

# 进行语法分析
gramma_tree = slr1_analyzer.analysis(lex_analyzer, slr1.C)
# print(gramma_tree)
# gramma_tree.view()

# while True:
#     print(lex_analyzer.get_token())


# 语义分析
sdts = SDTs(r'semantic_analysis\SDT.txt')
semantic_analyzer = SemanticAnalyzer()
table = semantic_analyzer.analysis(gramma_tree)
table.print_all()
semantic_analyzer.three_addr_code.show()
semantic_analyzer.three_addr_code.show(True)
