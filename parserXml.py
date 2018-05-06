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

#nomes
#from nameparser import HumanName
#outro para nomes
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

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

#texto das noticias do DN
raw = ""
for key in dn:
    raw += dn[key]["Text"]

#lista de palavras
tokens = word_tokenize(raw)

#cada palavra com a sua tag (nome, adjetivo, verbo, etc)
tagged = nltk.pos_tag(tokens)

#obter nomes
nomes= []
for word, pos in tagged:
    if pos in ["NNP"] and word not in stopwords and len(word)>3:
        nomes.append(word)

#nomes mais comuns
freq_nomes = nltk.FreqDist(nomes)
print(freq_nomes.most_common(10))





for sent in nltk.sent_tokenize(raw):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    for tag in tags:
        if tag[1]=='PERSON': print(tag)
