#referencias a Paises de cada Jornal

import xml.etree.ElementTree as ET
import pprint
import os, json
from os import listdir
from os.path import isfile, join

import codecs, re, getopt, sys, string, csv
import nltk
sys.excepthook = sys.__excepthook__

from itertools import tee, islice, chain
pp = pprint.PrettyPrinter(indent=4)
import unidecode as ud

from collections import Counter

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


#___________________CRIACAO DE dicionario Pais:[cidade]_____________
	#nomes proprios
cidadesFicheiro = open('nomes_e_palavras/cidades_mundo.tsv',encoding="utf8")
cidadesReader = csv.DictReader(cidadesFicheiro,delimiter='\t',fieldnames=['cidade','pais'])

cidades_dict = {}
for row in cidadesReader:
	cidades_dict[row['cidade']] = row['pais']


listaJornais = ["[PT] Diario de Noticias",
				"[AGO] jornal angola",
				"[CV] A_Semana",
				"[ST] Tela_Non",
				"[TL] Governo Timor-Leste"]
listaJornaisAcr = ["DN","JA","AS","TN","TLEST"]




#sem datas
dict_ocoPaises = {}
for jornal,jornalAcr in zip(listaJornais,listaJornaisAcr):
	onlyfiles = [f for f in listdir("obter_colecoes/"+ jornal + "/noticias/") if isfile(join("obter_colecoes/"+ jornal + "/noticias/",f))]
	dict_ocoPaises[jornalAcr] = {}
	

	for filename in onlyfiles:
		path= "obter_colecoes/"+ jornal + "/noticias/" + filename
		tree = ET.parse(path)
		root = tree.getroot()
		for child in root:

			if child.tag == "Text":
				tokens = nltk.word_tokenize(child.text)
				for word in tokens:
					word = ud.unidecode(word)
					if len(word)>1:
						if word in cidades_dict and word[0].isupper():
							#para dicionario sem datas
							#print(jornalAcr + '\t' + word + '\t' + cidades_dict[word])
							if cidades_dict[word] in dict_ocoPaises[jornalAcr]:
								dict_ocoPaises[jornalAcr][cidades_dict[word]]+=1
							else:
								dict_ocoPaises[jornalAcr][cidades_dict[word]] = 1

pp.pprint(dict_ocoPaises)
#a estrutura de dict_ocopaises permite integrar o tipo Counter
countDN = Counter(dict_ocoPaises["DN"])
countAS = Counter(dict_ocoPaises["AS"])
countJA = Counter(dict_ocoPaises["JA"])
countTLEST = Counter(dict_ocoPaises["TLEST"])
countTN = Counter(dict_ocoPaises["TN"])

jDN = countDN.most_common(5)
jAS = countAS.most_common(5)
jJA = countJA.most_common(5)
jTLEST = countTLEST.most_common(5)
jTN = countTN.most_common(5)

paisesDN = []
for elem in jDN:
    paisesDN.append(elem[0])

paisesAS = []
for elem in jAS:
    paisesAS.append(elem[0])

paisesJA = []
for elem in jJA:
    paisesJA.append(elem[0])

paisesTLEST = []
for elem in jTLEST:
    paisesTLEST.append(elem[0])

paisesTN = []
for elem in jTN:
    paisesTN.append(elem[0])

paises = [paisesDN,paisesAS,paisesJA,paisesTLEST,paisesTN]
counters = [countDN,countAS,countJA,countTLEST,countTN]
#lista com nomes dos jornais
nomesJornais = ["Diário de Noticias",
         "A semana (Cabo Verde)",
         "Jornal Angola",
         "Jornal Timor Leste",
         "Jornal Tela Non (S. Tomé)"]

for pais, count, jornal in zip(paises, counters,nomesJornais):
    y_pos = np.arange(len(pais))
    performance = [count[k] for k in pais]
    plt.barh(y_pos, performance, align='center', alpha=0.4)
    plt.yticks(y_pos, pais)
    plt.xlabel('Ocorrências de paises') 
    plt.title('Paises Mais comuns: ' + jornal)
    plt.show()


"""json = json.dumps(dict_ocoPaises)
f=open("oco_paises.json","w")
f.write(json)
f.close()
"""
