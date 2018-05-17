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

#___________________CRIACAO DE dicionario Pais:[cidade]_____________
    #nomes proprios
cidadesFicheiro = open('nomes_e_palavras/cidades_mundo.tsv',encoding="utf8")
cidadesReader = csv.DictReader(cidadesFicheiro,delimiter='\t',fieldnames=['cidade','pais'])

cidades_dict = {}
for row in cidadesReader:
    cidades_dict[row['cidade']] = row['pais']


listaJornais = ["[PT] Diario de Noticias",
                "[AGO] jornal angola",
                "[BR] UOL",
                "[CV] A_Semana",
                "[PT] Expresso",
                "[ST] Tela_Non",
                "[TL] Governo Timor-Leste"]
listaJornaisAcr = ["DN","JA","UOL","AS","EXP","TN","TLEST"]

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
                    if word in cidades_dict:
                        if cidades_dict[word] in dict_ocoPaises[jornalAcr]:
                            dict_ocoPaises[jornalAcr][cidades_dict[word]]+=1
                        else:
                            dict_ocoPaises[jornalAcr][cidades_dict[word]] = 1
                




json = json.dumps(dict_ocoPaises)
f=open("oco_paises.json","w")
f.write(json)
f.close()



