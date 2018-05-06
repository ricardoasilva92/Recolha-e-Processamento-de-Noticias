# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pprint
import os, json
from os import listdir
from os.path import isfile, join

import codecs

pp = pprint.PrettyPrinter(indent=4)
from nltk import FreqDist

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from string import punctuation

from nltk.corpus import floresta

import nltk
#nltk.download()
stopwords = nltk.corpus.stopwords.words('portuguese')

import string


#__________________PARSE de um ficheiro_____________________
"""
tree = ET.parse('obter_colecoes/[PT] Diario de Noticias/noticias/04-28-a-solidariedade-marchou-pelas-ruas-de-santana-DC3073371.xml')
root = tree.getroot()

dict_JA = {}
dict_JA['noticia1'] = {}

for child in root:
    dict_JA['noticia1'][child.tag] = child.text
    

pp.pprint(dict_JA)
"""

#_______________Diario de noticias__________________________
#print(os.path.basename('obter_colecoes/[PT] Diario de Noticias/noticias/04-28-a-solidariedade-marchou-pelas-ruas-de-santana-DC3073371.xml'))

#obter todos os nomes do ficheiros da diretoria
"""
onlyfiles = [f for f in listdir('obter_colecoes/[PT] Diario de Noticias/noticias/') if isfile(join('obter_colecoes/[PT] Diario de Noticias/noticias/',f))]

dict_DN = {}
i=1
for filename in onlyfiles:
    print(filename)
    key_dict = 'noticia' + str(i)
    path= 'obter_colecoes/[PT] Diario de Noticias/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    dict_DN[key_dict] = {}
    for child in root:
        dict_DN[key_dict][child.tag] = child.text
        print(i)
    i+=1
    

pp.pprint(dict_DN)

json = json.dumps(dict_DN)
f=open("DN.json","w")
f.write(json)
f.close()
"""
#_______________Jornal de Angola__________________________

"""
onlyfiles = [f for f in listdir('obter_colecoes/[AGO] jornal angola/noticias/') if isfile(join('obter_colecoes/[AGO] jornal angola/noticias/',f))]

dict_JA = {}
i=1
for filename in onlyfiles:
    print(filename)
    key_dict = 'noticia' + str(i)
    path= 'obter_colecoes/[AGO] jornal angola/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    dict_JA[key_dict] = {}
    for child in root:
        dict_JA[key_dict][child.tag] = child.text
        print(i)
    i+=1

json = json.dumps(dict_JA)
f=open("JA.json","w")
f.write(json)
f.close()
"""

dn = json.load(codecs.open('DN.json', 'r', 'utf-8-sig'))

raw = ""
for key in dn:
    raw += dn[key]["Text"]

palavras = word_tokenize(raw)

a = nltk.pos_tag(palavras)

pontos = ['.', ',', ':','-',';', ' ', '?', '!',')','(']

filtro = []
for w in palavras:
    if w not in stopwords and len(w) > 3:
        filtro.append(w)

fdist = FreqDist(filtro)

#print(fdist.most_common(2))
print(a)