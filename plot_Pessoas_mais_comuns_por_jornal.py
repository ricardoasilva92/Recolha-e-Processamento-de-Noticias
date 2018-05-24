#pessoas mais faladas em cada jornal

import xml.etree.ElementTree as ET
import pprint
import os, json
from os import listdir
from os.path import isfile, join
from dateutil import parser
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



#___________________CRIACAO DE SETs com NOMES, APELIDOS e stopWords PORTUGUESES_____________
    #nomes proprios
nomePortuguesesFicheiro = open('nomes_e_palavras/nomes_proprios.tsv',encoding="utf8")
nomePtReader = csv.DictReader(nomePortuguesesFicheiro,delimiter='\t',fieldnames=['nome','numero'])

nomesPtSet = set()
for row in nomePtReader:
    nomesPtSet.add(row['nome'])

    #apelidos
apelidosPortuguesesFicheiro = open('nomes_e_palavras/apelidos.tsv',encoding="utf8")
apelidoPtReader = csv.DictReader(apelidosPortuguesesFicheiro,delimiter='\t',fieldnames=['apelido','numero'])

apelidosPtSet = set()
for row in apelidoPtReader:
    apelidosPtSet.add(row['apelido'])

    #stopwords portuguesas
stopPortuguesesFicheiro = open('nomes_e_palavras/stopwords.txt')
stopPtSet = set()
for row in stopPortuguesesFicheiro:
    stopPtSet.add(row.split('\n')[0])
conetoresNomes = ['de','da','dos','das','do']

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


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

jornais_arg = []
i=0
for args in sys.argv:
	i+=1
	if i>1:
		jornais_arg.append(args)

dictJornais={"DN":"[PT] Diario de Noticias",
			"JA":"[AGO] jornal angola",
			"AS":"[CV] A_Semana",
			"TN":"[ST] Tela_Non",
			"TLEST":"[TL] Governo Timor-Leste"
			}


listaJornais = ["[PT] Diario de Noticias",
				"[AGO] jornal angola",
				"[CV] A_Semana",
				"[ST] Tela_Non",
				"[TL] Governo Timor-Leste"]
listaJornaisAcr = ["DN","JA","AS","TN","TLEST"]

#recolha de todos os nomes em todas as noticias
#criacao de dicionario {"Acrinomio de Jornal":{
# 											"data":[lista de nomes]
# 													}}
dictPessoas = {}
counterPessoas = {}
for jornalAcr in dictJornais:
	onlyfiles = [f for f in listdir("obter_colecoes/"+ dictJornais[jornalAcr] + "/noticias/") if isfile(join("obter_colecoes/"+ dictJornais[jornalAcr] + "/noticias/",f))]
	if (jornalAcr in jornais_arg) or len(jornais_arg)==0:
		print("A recolher " + dictJornais[jornalAcr])
		dictPessoas[jornalAcr] = {}
		for filename in onlyfiles:
			aux_set = set ()

			path= 'obter_colecoes/' + dictJornais[jornalAcr] + '/noticias/' + filename
			tree = ET.parse(path)
			root = tree.getroot()
			data = "data Null"
			for child in root:
				if child.tag == "Date":
					data = child.text

				if child.tag == "Text":
					tokens = nltk.word_tokenize(child.text)
					#for pal in tokens:
					for previous, item, nxt in previous_and_next(tokens):
						if item[0].isupper() and item.upper() in nomesPtSet:
							#nomeProprio + (nomeProprio || apelido)
							if nxt != None:
								if nxt.upper() in apelidosPtSet or nxt.upper() in nomesPtSet:
									nome_completo = item + ' ' + nxt
									aux_set.add(nome_completo)					   
								else:
									#se nao tem nome nem atras nem à frente
									if previous:
										if previous.upper() not in nomesPtSet:
											aux_set.add(item)
								
						#se anterior for nome e seguinte tambem nome_completo
						else:
							if item in conetoresNomes:
								if previous.upper() in nomesPtSet and (nxt.upper() in nomesPtSet or nxt.upper() in apelidosPtSet) and previous[0].isupper():
									nome_completo = previous + ' ' + item + ' ' + nxt
									aux_set.add(nome_completo)
					
					dataAsKey = convertDate(jornalAcr,data)

					if dataAsKey in dictPessoas[jornalAcr]: 
						for elem in aux_set:
							dictPessoas[jornalAcr][dataAsKey].append(elem)
					else:
						dictPessoas[jornalAcr][dataAsKey] = []
						for elem in aux_set:
							dictPessoas[jornalAcr][dataAsKey].append(elem)
		#counter com as ocorrencias de nomes
		count = Counter()
		for date in dictPessoas[jornalAcr]:
			count += Counter(dictPessoas[jornalAcr][date])
		counterPessoas[jornalAcr] = count.most_common(10)


#data minima e data maxima para cada jornal (para por informacao no plot)
datasMinMax = {}
listAux = []
for jornal in dictPessoas:
	datasMinMax[jornal] = {}
	listAux = []
	for key in dictPessoas[jornal]:
		#por formato datatime
		dt = parser.parse(key)
		listAux.append(dt)
	datasMinMax[jornal]["dataMin"]= min(listAux)
	datasMinMax[jornal]["dataMax"]=max(listAux)
	
res_list = [x[0] for x in counterPessoas["DN"]]
pp.pprint(res_list)


for jornal in counterPessoas:
	count = counterPessoas[jornal]
	pessoaTop = [x[0] for x in counterPessoas[jornal]]
	print(pessoaTop)
	y_pos = np.arange(len(pessoaTop))
	performance = [x[1] for x in counterPessoas[jornal]]
	plt.barh(y_pos, performance, align='center', alpha=0.4)
	plt.yticks(y_pos, pessoaTop)
	plt.xlabel('Ocorrências de ' + str(datasMinMax[jornal]["dataMin"].date()) + ' até ' + str(datasMinMax[jornal]["dataMax"].date())) 
	plt.title('Nomes Mais comuns  ' + jornal)
	plt.show()
    