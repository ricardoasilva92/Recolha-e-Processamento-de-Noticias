#recebe como parametros acrinomios de paises. Gera o grafico de ocorrencias nos jornais todos
#por exemplo PT, calcula todas as ocorrencias a portugal (cidades portuguesas incluidas)

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

if len(pais_arg)==0:
	sys.exit("ERRO ARGUMENTOS NÂO DETETADOS. POR EXEMPLO: PT ou US")

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

#recolha de todas as noticias
#criacao de dicionario {"Acrinomio de Jornal":{
# 											"data":{
# 													"País": Int}}
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
#dicionario organizado por paises argumentos
#{Pais:{
# 		dateTime:Int}}
for pais in pais_arg:
	dictOcoData = {}
	for jornal in dict_ocoPaisesDatas:
		print("jornal " +jornal)
		for date in dict_ocoPaisesDatas[jornal]:
			if (parser.parse(date) > parser.parse("01 Jan 2018")):
				if pais in dict_ocoPaisesDatas[jornal][date]:
					dictOcoData[parser.parse(date)] = dict_ocoPaisesDatas[jornal][date][pais]
	dictGrande[pais] = dictOcoData

#lista onde cada elemento é uma lista com as datas referentes a cada país
datasGrande = []
#lista onde cada elemento é uma lista com as ocurrencias, onde cada elemento é um int
ocorrenciasGrande = []
for pais in dictGrande:
    ocorrencias=[]
	#nao ordena automaticamente
    for key in sorted(dictGrande[pais].keys()):
        ocorrencias.append(dictGrande[pais][key])
    datas = sorted(dictGrande[pais].keys())
    datasGrande.append(datas)
    ocorrenciasGrande.append(ocorrencias)


ordem_das_cores = ["azul","laranja","verde","vermelho","roxo"]

#para por mensagem informativa no plot
dict_print = {}
i=0
for c in pais_arg:
    dict_print[pais_arg[i]] = ordem_das_cores[i]
    i+=1

fig = plt.figure()
i=0
#cada iteração corresponde às referencias de um Pais (argumento) por datas
for key in dictGrande:
    #plt.bar(list(dictOcoData.keys()), dictOcoData.values(), color='r')
    plt.plot(datasGrande[i],ocorrenciasGrande[i])
    i+=1




plt.gca().xaxis_date()
fig.autofmt_xdate()
plt.xlabel("\n".join([key + ':' + dict_print[key] for key in dict_print]))
plt.title("Referências a países em jornais portugueses")

plt.show()

