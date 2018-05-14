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


#___________________CRIACAO DE SETs com NOMES, APELIDOS e stopWords PORTUGUESES_____________
    #nomes proprios
nomePortuguesesFicheiro = open('portugues/nomes_proprios.tsv')
nomePtReader = csv.DictReader(nomePortuguesesFicheiro,delimiter='\t',fieldnames=['nome','numero'])

nomesPtSet = set()
for row in nomePtReader:
    nomesPtSet.add(row['nome'])

    #apelidos
apelidosPortuguesesFicheiro = open('portugues/apelidos.tsv')
apelidoPtReader = csv.DictReader(apelidosPortuguesesFicheiro,delimiter='\t',fieldnames=['apelido','numero'])

apelidosPtSet = set()
for row in apelidoPtReader:
    apelidosPtSet.add(row['apelido'])

    #stopwords portuguesas
stopPortuguesesFicheiro = open('portugues/stopwords.txt')
stopPtSet = set()
for row in stopPortuguesesFicheiro:
    stopPtSet.add(row.split('\n')[0])


#_____________________________________________________________________


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)



onlyfiles = [f for f in listdir('obter_colecoes/[PT] Diario de Noticias/noticias/') if isfile(join('obter_colecoes/[PT] Diario de Noticias/noticias/',f))]

conetoresNomes = ['de','da','dos','das','do']

dict_DN = {}
for filename in onlyfiles:
    aux_set = set ()
    #print(filename)
    path= 'obter_colecoes/[PT] Diario de Noticias/noticias/' + filename
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
               

            dataAsKey = (data.split('/')[0]).strip('\n') 
            if dataAsKey in dict_DN: 
                for elem in aux_set:
                    dict_DN[dataAsKey].append(elem)
            else:
                dict_DN[dataAsKey] = []
                for elem in aux_set:
                    dict_DN[dataAsKey].append(elem)
            #print('-------------')
            #print('PERSONS [DN] : ' + data.split('/')[0])
            #for pal in aux_set:
                #print(pal)

print(dict_DN) 
json = json.dumps(dict_DN)
f=open("DN.json","w")
f.write(json)
f.close()