import NFA
# 注释直接读入的时候忽略掉

# define lexicon 词汇表
# 空格换行符
ws = NFA.ws()
# reserved 保留字 (str)
reserved = [
'int', 'char', 'bool', 'true', 'false', '=', ',', 'if', 'else',
'while', 'for',
 '<', '<=', '==', '!=', '>', '>=', ';', '+', '+=', '-', '-=',
 '*', '*=', '/', '/=', '++', '--', '{', '}', '(', ')']
vocab_table = ['ws'] + reserved + ['id', 'int_const', 'char_const']
reserved = [NFA.make_pair_from_string(i) for i in reserved]
# id或者常量等, pair of NFANode
others = [NFA.ID(), NFA.intiger(), NFA.charactor()]

all_pairs = [ws] + reserved + others

nfa = NFA.make_NFA(all_pairs, vocab_table)


