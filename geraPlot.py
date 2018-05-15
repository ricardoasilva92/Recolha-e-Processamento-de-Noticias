#!/usr/bin/python3
import json
from collections import Counter


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt




#___________________________OCURRENCIAS DIARIO DE NOTICIAS____________________________________
#a partir dos ficheiros com os nomes já recolhidos

nomesDN = json.load(open('pessoas_recolhidas/PT_DN.json'))

c1 = Counter()


for key in nomesDN:
    c1 += Counter(nomesDN[key])


print(c1)

c2 = c1.most_common(10)
# Counter data, c1 is your c1 object
keys = []
for elem in c2:
    keys.append(elem[0])
    

y_pos = np.arange(len(keys))
# get the counts for each key, assuming the values are numerical
performance = [c1[k] for k in keys]

plt.barh(y_pos, performance, align='center', alpha=0.4)
plt.yticks(y_pos, keys)
plt.xlabel('Counts per key')
plt.title('Nomes Mais comuns')

plt.show()