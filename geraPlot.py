#!/usr/bin/python3
import json
from dateutil import parser
from collections import Counter


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import heapq


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
        #por formato datatime
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

pessoasDN = []
for elem in jDN:
    pessoasDN.append(elem[0])

pessoasAS = []
for elem in jAS:
    pessoasAS.append(elem[0])

pessoasJA = []
for elem in jJA:
    pessoasJA.append(elem[0])

pessoasTLEST = []
for elem in jTLEST:
    pessoasTLEST.append(elem[0])

pessoasTN = []
for elem in jTN:
    pessoasTN.append(elem[0])


pessoas = [pessoasDN,pessoasAS,pessoasJA,pessoasTLEST,pessoasTN]
counters = [countDN,countAS,countJA,countTLEST,countTN]
nomes = ["Diário de Noticias",
         "A semana (Cabo Verde)",
         "Jornal Angola",
         "Jornal Timor Leste",
         "Jornal Tela Non (S. Tomé)"]

for pessoa, count, jornal, dataMin, dataMax in zip(pessoas, counters,nomes,listDataMin,listDataMax):
    y_pos = np.arange(len(pessoa))
    print(pessoa)
    performance = [count[k] for k in pessoa]
    print(performance)
    plt.barh(y_pos, performance, align='center', alpha=0.4)
    plt.yticks(y_pos, pessoa)
    plt.xlabel('Ocorrências de ' + str(dataMin.date()) + ' até ' + str(dataMax.date())) 
    plt.title('Nomes Mais comuns  ' + jornal)
    plt.show()
    
