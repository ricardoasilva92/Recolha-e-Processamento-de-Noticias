#!/usr/bin/python3
import json
from dateutil import parser
from collections import Counter


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt




#diario de noticias
nomesDN = json.load(open('pessoas_recolhidas/DN.json'))
#a semana
nomesAS = json.load(open('pessoas_recolhidas/AS.json'))
#jornal angola
nomesJA = json.load(open('pessoas_recolhidas/JA.json'))
#jornal timor lest
nomesTLEST = json.load(open('pessoas_recolhidas/TLEST.json'))
#sao tome jornal TN
nomesTN = json.load(open('pessoas_recolhidas/TN.json'))

listaJornais = [nomesDN, nomesAS, nomesJA, nomesTLEST, nomesTN]

#datas
listDataMin = []
listDataMax = []
listAux = []
for jornal in listaJornais:
    listAux = []
    for key in jornal:
        dt = parser.parse(key)
        listAux.append(dt)
    listDataMin.append(min(listAux))
    listDataMax.append(max(listAux))


#counter
countDN = Counter()
countAS = Counter()
countJA = Counter()
countTLEST = Counter()
countTN = Counter()

for key in nomesDN:
    countDN += Counter(nomesDN[key])

for key in nomesAS:
    countAS += Counter(nomesAS[key])

for key in nomesJA:
    countJA += Counter(nomesJA[key])

for key in nomesTLEST:
    countTLEST += Counter(nomesTLEST[key])

for key in nomesTN:
    countTN += Counter(nomesTN[key])


jDN = countDN.most_common(10)
jAS = countAS.most_common(10)
jJA = countJA.most_common(10)
jTLEST = countTLEST.most_common(10)
jTN = countTN.most_common(10)

keysDN = []
for elem in jDN:
    keysDN.append(elem[0])

keysAS = []
for elem in jAS:
    keysAS.append(elem[0])

keysJA = []
for elem in jJA:
    keysJA.append(elem[0])

keysTLEST = []
for elem in jTLEST:
    keysTLEST.append(elem[0])

keysTN = []
for elem in jTN:
    keysTN.append(elem[0])


chaves = [keysDN,keysAS,keysJA,keysTLEST,keysTN]
counters = [countDN,countAS,countJA,countTLEST,countTN]
nomes = ["Diário de Noticias",
         "A semana (Cabo Verde)",
         "Jornal Angola",
         "Jornal Timor Leste",
         "Jornal Tela Non (S. Tomé)"]

for chave, count, jornal, dataMin, dataMax in zip(chaves, counters,nomes,listDataMin,listDataMax):
    y_pos = np.arange(len(chave))
    performance = [count[k] for k in chave]
    plt.barh(y_pos, performance, align='center', alpha=0.4)
    plt.yticks(y_pos, chave)
    plt.xlabel('Ocorrências de ' + str(dataMin.date()) + ' até ' + str(dataMax.date())) 
    plt.title('Nomes Mais comuns  ' + jornal)
    plt.show()
    
