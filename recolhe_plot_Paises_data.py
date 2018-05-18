#recebe como parametros acrinomios de paises. Gera o grafico de ocorrencias nos jornais todos
#por exemplo PT, calcula todas as ocorrencias a portugal (cidades portuguesas incluidas)

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
from dateutil import parser
from collections import Counter

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
def convert_months(month):
	orig = month
	return {
		'Jan' : 'Jan',
		'Fev' : 'Feb',
		'Abr' : 'Apr',
		'Mai' : 'May',
		'Ago' : 'Aug',
		'Set' : 'Sep',
		'Out' : 'Oct',
		'Dez' : 'Dec',	   
	}.get(month, orig)

def convertDate(jornal,date):
	if jornal=="DN":
		dataAsKey = ((date.split('/')[0]).strip('\n')).strip()
		c = dataAsKey.split(',')
		if len(c)>1:
			c = c[1].strip().split(' ')
			dataAsKey = c[0] + ' ' + c[1] + ' ' + c[2]
		aux = dataAsKey.split(' ')
		dataAsKey = aux[0] + ' ' + convert_months(aux[1]) + ' ' + aux[2]
	if jornal=="JA":
		aux = (date.split(' '))
		dataAsKey = aux[1] + ' ' + aux[3][:3] + ' ' + aux[4]
		aux = dataAsKey.split(' ')
		dataAsKey = aux[0] + ' ' + convert_months(aux[1]) + ' ' + aux[2]
	if jornal=="AS":
		aux = (date.split(' '))
		dataAsKey = aux[0].strip('\n') + ' ' + aux[1][:3] + ' ' + aux[2].strip('\n')
		aux = dataAsKey.split(' ')
		dataAsKey = aux[0] + ' ' + convert_months(aux[1]) + ' ' + aux[2]
	if jornal=="TN":
		aux = (date.split(' '))
		dataAsKey = aux[0].strip('\n') + ' ' + aux[2][:3] + ' ' + aux[4].strip('\n')
		aux = dataAsKey.split(' ')
		dataAsKey = aux[0] + ' ' + convert_months(aux[1]) + ' ' + aux[2]

	if jornal=="TLEST":
		aux = (date.split(' '))
		dataAsKey = aux[1] + ' ' + (aux[3][:3]).title() + ' ' + aux[5].strip(',')
		aux = dataAsKey.split(' ')
		dataAsKey = aux[0] + ' ' + convert_months(aux[1]) + ' ' + aux[2]
	
	return dataAsKey

pais_arg = []
i=0
for args in sys.argv:
    i+=1
    if i>1:
        pais_arg.append(args)


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


#com datas
dict_ocoPaisesDatas = {}

for jornal,jornalAcr in zip(listaJornais,listaJornaisAcr):
	onlyfiles = [f for f in listdir("obter_colecoes/"+ jornal + "/noticias/") if isfile(join("obter_colecoes/"+ jornal + "/noticias/",f))]
	dict_ocoPaisesDatas[jornalAcr] = {}

	for filename in onlyfiles:
		path= "obter_colecoes/"+ jornal + "/noticias/" + filename
		tree = ET.parse(path)
		root = tree.getroot()
		for child in root:
			if child.tag == "Date":
				#print(jornalAcr + child.text + jornal)
				data = convertDate(jornalAcr,child.text)
			if child.tag == "Text":
				tokens = nltk.word_tokenize(child.text)
				for word in tokens:
					word = ud.unidecode(word)
					if word in cidades_dict and word[0].isupper():
						#para dicionario com datas
						if data in dict_ocoPaisesDatas[jornalAcr]:
							if cidades_dict[word] in dict_ocoPaisesDatas[jornalAcr][data]:
								dict_ocoPaisesDatas[jornalAcr][data][cidades_dict[word]]+=1
							else:
								dict_ocoPaisesDatas[jornalAcr][data][cidades_dict[word]] = 1
						else:
							dict_ocoPaisesDatas[jornalAcr][data]={}
							dict_ocoPaisesDatas[jornalAcr][data][cidades_dict[word]] = 1
	print(jornal + " recolhido")


dictGrande = {}
for pais in pais_arg:
    dictOcoData = {}
    for jornal in dict_ocoPaisesDatas:
        print("jornal " +jornal)
        for date in dict_ocoPaisesDatas[jornal]:
            if pais in dict_ocoPaisesDatas[jornal][date]:
                dictOcoData[parser.parse(date)] = dict_ocoPaisesDatas[jornal][date][pais]
    dictGrande[pais] = dictOcoData

datasGrande = []
ocorrenciasGrande = []
for pais in dictGrande:
    ocorrencias=[]
    for key in sorted(dictGrande[pais].keys()):
        ocorrencias.append(dictGrande[pais][key])
    datas = sorted(dictGrande[pais].keys())
    datasGrande.append(datas)
    ocorrenciasGrande.append(ocorrencias)




fig = plt.figure()
i=0
for key in dictGrande:
    #plt.bar(list(dictOcoData.keys()), dictOcoData.values(), color='r')
    plt.plot(datasGrande[i],ocorrenciasGrande[i])
    i+=1




plt.gca().xaxis_date()
fig.autofmt_xdate()
plt.title('Referências ao país\n  ' + pais_arg[0])

plt.show()


"""
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
    plt.show()"""


"""json = json.dumps(dict_ocoPaises)
f=open("oco_paises.json","w")
f.write(json)
f.close()
"""

