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

criminalidadeFicheiro = open('nomes_e_palavras/criminalidade.txt')
crimes_set = set()


#set com palavras de criminalidade
for row in criminalidadeFicheiro:
	crimes_set.add(row.split('\n')[0])


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
				crime = False
				tokens = nltk.word_tokenize(child.text)
				for word in tokens:
					word = ud.unidecode(word)
					if word in crimes_set:
						crime = True
						#para dicionario sem datas
				
					if word in cidades_dict and crime==True:
						if cidades_dict[word] in dict_ocoPaises[jornalAcr]:
							dict_ocoPaises[jornalAcr][cidades_dict[word]]+=1
						else:
							dict_ocoPaises[jornalAcr][cidades_dict[word]] = 1

						

pp.pprint(dict_ocoPaises)

dictOcoCrimes = {}
#join dos dicionarios
for jornal in dict_ocoPaises:
	for pais in dict_ocoPaises[jornal]:
		if pais in dictOcoCrimes:
			dictOcoCrimes[pais] += dict_ocoPaises[jornal][pais]
		else:
			dictOcoCrimes[pais] = dict_ocoPaises[jornal][pais]

pp.pprint(dictOcoCrimes)


#a estrutura de dict_ocopaises permite integrar o tipo Counter
countAll = Counter(dictOcoCrimes)


#top 5 paises
jDN = countAll.most_common(5)

print(jDN)


paisesDN = []
for elem in jDN:
	paisesDN.append(elem[0])



y_pos = np.arange(len(paisesDN))
performance = [countAll[k] for k in paisesDN]
plt.barh(y_pos, performance, align='center', alpha=0.4)
plt.yticks(y_pos, paisesDN)
plt.xlabel('Ocorrências de paises') 
plt.title('Criminalidade Paises ' )
plt.show()


