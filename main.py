from lexical_analysis import lexical_analysis
from grammatical_analysis import gramma, SLR1

G = gramma.Gramma('grammatical_analysis/gramma.txt', lexical_analysis.vocab_table)

# print(gramma.BNF.id_count)
a = SLR1.Item.from_BNF(G.BNFs[2], 0)
print(a)
b = SLR1.Item.from_BNF(G.BNFs[1], 0)
print(b)
slr1 =SLR1.SLR1(G)
close = slr1.closure({b})
print(slr1.closure({a, b}) == close)
print()
for i in close:
    print(i)


# aa = {a}
# bb = {b}
# print(aa == bb)
# for i in range(len(G.BNFs)):
#     print(i, G.BNFs[i])


