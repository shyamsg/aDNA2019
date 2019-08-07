import sys
import numpy as np

pops = {}

indfile = open(sys.argv[2])
index = 0
for line in indfile:
    (samp, sex, pop) = line.strip().split()
    if pop not in pops:
        pops[pop] = []
    pops[pop].append(index)
    index += 1
indfile.close()

genofile = open(sys.argv[1])
print("\t".join(pops.keys()))

npops = len(pops)
for line in genofile:
    toks = np.array(line.strip().split(''))
    for pop in pops:
        chosen = toks[pops[pop]]
        chosen = chosen[np.where(chosen != 9)]
        alts = np.sum(chosen)
        print(str(alts)+","+str(2*len(chosen)-alts))
    print("\n")
genofile.close()
