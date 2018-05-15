#!/usr/bin/python3
import json
from collections import Counter


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt




#___________________________OCURRENCIAS DIARIO DE NOTICIAS____________________________________
#a partir dos ficheiros com os nomes já recolhidos

nomesDN = json.load(open('pessoas_recolhidas/PT_DN_encondingCorreto.json'))

c1 = Counter()

for key in nomesDN:
    c1 += Counter(nomesDN[key])

print(c1)

# Counter data, c1 is your c1 object
keys = c1.keys()
y_pos = np.arange(len(keys))
# get the counts for each key, assuming the values are numerical
performance = [c1[k] for k in keys]
# not sure if you want this :S
error = np.random.rand(len(keys))

plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.yticks(y_pos, keys)
plt.xlabel('Counts per key')
plt.title('How fast do you want to go today?')

plt.show()