from lexical_analysis import lexical_analysis
from grammatical_analysis import gramma, SLR1

G = gramma.Gramma('grammatical_analysis/gramma.txt', lexical_analysis.vocab_table)

# print(gramma.BNF.id_count)

slr1 =SLR1.SLR1(G)

acction, goto = slr1.get_action_goto()
print(acction, goto)




