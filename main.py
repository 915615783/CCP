from lexical_analysis import lexical_analysis
from grammatical_analysis import gramma, SLR1

G = gramma.Gramma('grammatical_analysis/gramma.txt', lexical_analysis.vocab_table)

print(gramma.BNF.id_count)
a = SLR1.Item.from_BNF(G.BNFs[13], 4)
print(a)

