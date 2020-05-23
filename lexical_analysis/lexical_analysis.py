from . import NFA
from . import DFA
from . import lexical_analyzer


# 注释直接读入的时候忽略掉

# define lexicon 词汇表
# 空格换行符
ws = NFA.ws()
# reserved 保留字 (str)
reserved = [
'int', 'char', 'bool', 'float', 'true', 'false', '=', ',', 'if', 'else',
'while', 'for', 'return', 'or', 'and', '!',
 '<', '<=', '==', '!=', '>', '>=', ';', '+', '+=', '-', '-=',
 '*', '*=', '/', '/=', '++', '--', '{', '}', '(', ')']
vocab_table = ['ws'] + reserved + ['id', 'int_const', 'char_const', 'float_const']
reserved = [NFA.make_pair_from_string(i) for i in reserved]
# id或者常量等, pair of NFANode
others = [NFA.ID(), NFA.intiger(), NFA.charactor(), NFA.Float()]

all_pairs = [ws] + reserved + others

nfa = NFA.make_NFA(all_pairs, vocab_table)

dfa = DFA.NFA2DFA(nfa)



# reader = lexical_analyzer.Reader()

# reader.set_text_from_file('lexical_analysis/ccode.c')
# lex_analyzer = lexical_analyzer.Lexical_Analyzer(reader, dfa, vocab_table)

# try:
#     while True:
#         print(lex_analyzer.get_token())
# except EOFError:
#     print(lex_analyzer.id_table, lex_analyzer.int_const_table, lex_analyzer.char_const_table)
#     print('EOF')



