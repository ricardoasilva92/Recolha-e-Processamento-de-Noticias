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

#___________________CRIACAO DE SETs com NOMES, APELIDOS e stopWords PORTUGUESES_____________
    #nomes proprios
nomePortuguesesFicheiro = open('nomes_e_palavras/nomes_proprios.tsv',encoding="utf8")
nomePtReader = csv.DictReader(nomePortuguesesFicheiro,delimiter='\t',fieldnames=['nome','numero'])

nomesPtSet = set()
i=0
for row in nomePtReader:
    i+=1
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

profissoesPtFicheiro = open('nomes_e_palavras/profissões.txt',encoding="utf8")
profissoesPtSet = set()
for row in profissoesPtFicheiro:
    profissoesPtSet.add(row.split('\n')[0])

worldCitiesFicheiro = open('nomes_e_palavras/cities.txt',encoding="utf8")
worldCitiesSet = set()
for row in worldCitiesFicheiro:
    worldCitiesSet.add(row.split('\n')[0])

temasFicheiro = open('nomes_e_palavras/temas.txt',encoding="utf8")
temasSet = set()
for row in temasFicheiro:
    temasSet.add(row.split('\n')[0])

#_____________________________________________________________________


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


#______________________DIARIO DE NOTICIAS_______________________________
onlyfiles = [f for f in listdir('obter_colecoes/[PT] Diario de Noticias/noticias/') if isfile(join('obter_colecoes/[PT] Diario de Noticias/noticias/',f))]
dict_DN = {}
for filename in onlyfiles:
    aux_set = set ()
    profissoes_set = set()
    #print(filename)
    path= 'obter_colecoes/[PT] Diario de Noticias/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    data = "data Null"
    locals = set()
    temas = set()
    tema = ''
    for child in root:
        if child.tag == "Date":
            data = child.text

        if child.tag == "Text":
            tokens = nltk.word_tokenize(child.text)
            #for pal in tokens:
            for previous, item, nxt in previous_and_next(tokens):
            #for item in tokens:
                decoded = ud.unidecode(item)
                if item[0].isupper() and decoded in worldCitiesSet:
                    locals.add(decoded)

                if item.lower() in temasSet:
                    temas.add(item)

                if item[0].isupper() and item.upper() in nomesPtSet:
                    #nomeProprio + (nomeProprio || apelido)

                    if previous and previous.lower() in profissoesPtSet:
                        profissoes_set.add(previous)
                    else:
                        profissoes_set.add('')

                    if nxt is not None and (nxt.upper() in apelidosPtSet or nxt.upper() in nomesPtSet):
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



            dataAsKey = ((data.split('/')[0]).strip('\n')).strip()
            c = dataAsKey.split(',')
            if len(c)>1:
                c = c[1].strip().split(' ')
                dataAsKey = c[0] + ' ' + c[1] + ' ' + c[2]

            if locals == set():
                locals = ''
            if temas == set():
                temas = ''


            for elem in aux_set:
                if elem in dict_DN:
                    for prof in profissoes_set:
                        dict_DN[elem].append({'prof':prof})
                    dict_DN[elem].append({'locals':locals, 'temas':temas})
                else:
                    dict_DN[elem] = []
                    for prof in profissoes_set:
                        dict_DN[elem].append({'prof':prof})
                    dict_DN[elem].append({'locals':locals, 'temas':temas})

            #print('-------------')
            #print('PERSONS [DN] : ' + data.split('/')[0])
            #for pal in aux_set:
                #print(pal)
encoding="utf8"
print("DIARIO DE NOTICIAS")
#pp.pprint(dict_DN)
i = 0
f=open('DN.html',mode='w')
f.write('<meta charset=\"UTF-8\">')
f.write('<title>DIÁRIO DE NOTÍCIAS</title>')
f.write('<h1>DIÁRIO DE NOTÍCIAS</h1>')
for elem in dict_DN:
    #pp.pprint(dict_DN[elem])
    decoded_elem = ud.unidecode(elem)
    decoded_elem = decoded_elem.replace(' ','_')

    tag = '<a href=dn_html/'+decoded_elem+'.html>'+elem+'</a><br>'

    f.write(tag)

    html=open('dn_html/'+decoded_elem+'.html','w')
    html.write('<meta charset=\"UTF-8\">\n')
    html.write('<title>'+elem+'</title>')
    html.write('<h1>'+elem+'</h1>')
    html.write('<h6>em Diário de Notícias</h6>')
    html.write('<table width=\"100%\" heigth=\"100%\">')
    html.write('<td width=\"33%\" heigth=\"100%\">')
    html.write('PROFISSOES<br>')
    for i in range(0,len(dict_DN[elem]),1):
        if 'prof' in dict_DN[elem][i]:
            if dict_DN[elem][i]['prof'] != '':
                html.write(dict_DN[elem][i]['prof']+'<br>')

    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('LOCAIS<br>')
    for i in range(0,len(dict_DN[elem]),1):
        if 'locals' in dict_DN[elem][i]:
            for local in dict_DN[elem][i]['locals']:
                html.write(local+'<br>')
    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('TEMAS<br>')
    for i in range(0,len(dict_DN[elem]),1):
        if 'temas' in dict_DN[elem][i]:
            for tema in dict_DN[elem][i]['temas']:
                html.write(tema+'<br>')
    html.write('</td>')
    html.write('</table>')
    html.close()

f.close()
'''
json = json.dumps(dict_DN)
f=open("DNprofs.json","w")
f.write(json)
f.close()
'''
#________________________________JORNAL DE ANGOLA_________________________________________-
onlyfiles = [f for f in listdir('obter_colecoes/[AGO] jornal angola/noticias/') if isfile(join('obter_colecoes/[AGO] jornal angola/noticias/',f))]
dict_JA = {}
for filename in onlyfiles:
    aux_set = set ()
    profissoes_set = set()
    #print(filename)
    path= 'obter_colecoes/[AGO] jornal angola/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    data = "data Null"
    locals = set()
    temas = set()
    tema = ''
    for child in root:
        if child.tag == "Date":
            data = child.text

        if child.tag == "Text":
            tokens = nltk.word_tokenize(child.text)
            #for pal in tokens:
            for previous, item, nxt in previous_and_next(tokens):
            #for item in tokens:
                decoded = ud.unidecode(item)
                if item[0].isupper() and decoded in worldCitiesSet:
                    locals.add(decoded)

                if item.lower() in temasSet:
                    temas.add(item)

                if item[0].isupper() and item.upper() in nomesPtSet:
                    #nomeProprio + (nomeProprio || apelido)

                    if previous and previous.lower() in profissoesPtSet:
                        profissoes_set.add(previous)
                    else:
                        profissoes_set.add('')

                    if nxt is not None and (nxt.upper() in apelidosPtSet or nxt.upper() in nomesPtSet):

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



            dataAsKey = ((data.split('/')[0]).strip('\n')).strip()
            c = dataAsKey.split(',')
            if len(c)>1:
                c = c[1].strip().split(' ')
                dataAsKey = c[0] + ' ' + c[1] + ' ' + c[2]

            if locals == set():
                locals = ''
            if temas == set():
                temas = ''


            for elem in aux_set:
                if elem in dict_JA:
                    for prof in profissoes_set:
                        dict_JA[elem].append({'prof':prof})
                    dict_JA[elem].append({'locals':locals, 'temas':temas})
                else:
                    dict_JA[elem] = []
                    for prof in profissoes_set:
                        dict_JA[elem].append({'prof':prof})
                    dict_JA[elem].append({'locals':locals, 'temas':temas})

            #print('-------------')
            #print('PERSONS [DN] : ' + data.split('/')[0])
            #for pal in aux_set:
                #print(pal)

print("JORNAL ANGOLA")
#pp.pprint(dict_JA)
i = 0
f=open('JA.html',mode='w')
f.write('<meta charset=\"UTF-8\">')
f.write('<title>JORNAL ANGOLA</title>')
f.write('<h1>JORNAL ANGOLA</h1>')
for elem in dict_JA:
    #pp.pprint(dict_DN[elem])
    decoded_elem = ud.unidecode(elem)
    decoded_elem = decoded_elem.replace(' ','_')

    tag = '<a href=ja_html/'+decoded_elem+'.html>'+elem+'</a><br>'

    f.write(tag)

    html=open('ja_html/'+decoded_elem+'.html','w')
    html.write('<meta charset=\"UTF-8\">\n')
    html.write('<title>'+elem+'</title>')
    html.write('<h1>'+elem+'</h1>')
    html.write('<h6>em Jornal Angola</h6>')
    html.write('<table width=\"100%\" heigth=\"100%\">')
    html.write('<td width=\"33%\" heigth=\"100%\">')
    html.write('PROFISSOES<br>')
    for i in range(0,len(dict_JA[elem]),1):
        if 'prof' in dict_JA[elem][i]:
            if dict_JA[elem][i]['prof'] != '':
                html.write(dict_JA[elem][i]['prof']+'<br>')

    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('LOCAIS<br>')
    for i in range(0,len(dict_JA[elem]),1):
        if 'locals' in dict_JA[elem][i]:
            for local in dict_JA[elem][i]['locals']:
                html.write(local+'<br>')
    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('TEMAS<br>')
    for i in range(0,len(dict_JA[elem]),1):
        if 'temas' in dict_JA[elem][i]:
            for tema in dict_JA[elem][i]['temas']:
                html.write(tema+'<br>')
    html.write('</td>')
    html.write('</table>')
    html.close()

f.close()

#_________________________CABO VERDE - A semana______________________________-

onlyfiles = [f for f in listdir('obter_colecoes/[CV] A_Semana/noticias/') if isfile(join('obter_colecoes/[CV] A_Semana/noticias/',f))]
dict_AS = {}
for filename in onlyfiles:
    aux_set = set ()
    profissoes_set = set()
    #print(filename)
    path= 'obter_colecoes/[CV] A_Semana/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    data = "data Null"
    locals = set()
    temas = set()
    tema = ''
    for child in root:
        if child.tag == "Date":
            data = child.text

        if child.tag == "Text":
            tokens = nltk.word_tokenize(child.text)
            #for pal in tokens:
            for previous, item, nxt in previous_and_next(tokens):
            #for item in tokens:
                decoded = ud.unidecode(item)
                if item[0].isupper() and decoded in worldCitiesSet:
                    locals.add(decoded)

                if item.lower() in temasSet:
                    temas.add(item)

                if item[0].isupper() and item.upper() in nomesPtSet:
                    #nomeProprio + (nomeProprio || apelido)

                    if previous and previous.lower() in profissoesPtSet:
                        profissoes_set.add(previous)
                    else:
                        profissoes_set.add('')

                    if nxt is not None and (nxt.upper() in apelidosPtSet or nxt.upper() in nomesPtSet):
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



            dataAsKey = ((data.split('/')[0]).strip('\n')).strip()
            c = dataAsKey.split(',')
            if len(c)>1:
                c = c[1].strip().split(' ')
                dataAsKey = c[0] + ' ' + c[1] + ' ' + c[2]

            if locals == set():
                locals = ''
            if temas == set():
                temas = ''


            for elem in aux_set:
                if elem in dict_AS:
                    for prof in profissoes_set:
                        dict_AS[elem].append({'prof':prof})
                    dict_AS[elem].append({'locals':locals, 'temas':temas})
                else:
                    dict_AS[elem] = []
                    for prof in profissoes_set:
                        dict_AS[elem].append({'prof':prof})
                    dict_AS[elem].append({'locals':locals, 'temas':temas})

print("A SEMANA (CABO VERDE)")
#pp.pprint(dict_AS)
i = 0
f=open('AS.html',mode='w')
f.write('<meta charset=\"UTF-8\">')
f.write('<title>A SEMANA (CABO VERDE)</title>')
f.write('<h1>A SEMANA (CABO VERDE)</h1>')
for elem in dict_AS:
    #pp.pprint(dict_AS[elem])
    decoded_elem = ud.unidecode(elem)
    decoded_elem = decoded_elem.replace(' ','_')

    tag = '<a href=as_html/'+decoded_elem+'.html>'+elem+'</a><br>'

    f.write(tag)

    html=open('as_html/'+decoded_elem+'.html','w')
    html.write('<meta charset=\"UTF-8\">\n')
    html.write('<title>'+elem+'</title>')
    html.write('<h1>'+elem+'</h1>')
    html.write('<h6>em A Semana</h6>')
    html.write('<table width=\"100%\" heigth=\"100%\">')
    html.write('<td width=\"33%\" heigth=\"100%\">')
    html.write('PROFISSOES<br>')
    for i in range(0,len(dict_AS[elem]),1):
        if 'prof' in dict_AS[elem][i]:
            if dict_AS[elem][i]['prof'] != '':
                html.write(dict_AS[elem][i]['prof']+'<br>')

    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('LOCAIS<br>')
    for i in range(0,len(dict_AS[elem]),1):
        if 'locals' in dict_AS[elem][i]:
            for local in dict_AS[elem][i]['locals']:
                html.write(local+'<br>')
    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('TEMAS<br>')
    for i in range(0,len(dict_AS[elem]),1):
        if 'temas' in dict_AS[elem][i]:
            for tema in dict_AS[elem][i]['temas']:
                html.write(tema+'<br>')
    html.write('</td>')
    html.write('</table>')
    html.close()

f.close()
'''
json = json.dumps(dict_AS)
f=open("AS.json","w")
f.write(json)
f.close()
'''


#______________________________S.TOME - Tela_Non________________________
onlyfiles = [f for f in listdir('obter_colecoes/[ST] Tela_Non/noticias/') if isfile(join('obter_colecoes/[ST] Tela_Non/noticias/',f))]
dict_TN = {}
for filename in onlyfiles:
    aux_set = set ()
    #print(filename)
    path= 'obter_colecoes/[ST] Tela_Non/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    data = "data Null"
    locals = set()
    temas = set()
    tema = ''
    for child in root:
        if child.tag == "Date":
            data = child.text

        if child.tag == "Text":
            tokens = nltk.word_tokenize(child.text)
            #for pal in tokens:
            for previous, item, nxt in previous_and_next(tokens):
            #for item in tokens:
                decoded = ud.unidecode(item)
                if item[0].isupper() and decoded in worldCitiesSet:
                    locals.add(decoded)

                if item.lower() in temasSet:
                    temas.add(item)

                if item[0].isupper() and item.upper() in nomesPtSet:
                    #nomeProprio + (nomeProprio || apelido)

                    if previous and previous.lower() in profissoesPtSet:
                        profissoes_set.add(previous)
                    else:
                        profissoes_set.add('')

                    if nxt is not None and (nxt.upper() in apelidosPtSet or nxt.upper() in nomesPtSet):
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



            dataAsKey = ((data.split('/')[0]).strip('\n')).strip()
            c = dataAsKey.split(',')
            if len(c)>1:
                c = c[1].strip().split(' ')
                dataAsKey = c[0] + ' ' + c[1] + ' ' + c[2]

            if locals == set():
                locals = ''
            if temas == set():
                temas = ''


            for elem in aux_set:
                if elem in dict_TN:
                    for prof in profissoes_set:
                        dict_TN[elem].append({'prof':prof})
                    dict_TN[elem].append({'locals':locals, 'temas':temas})
                else:
                    dict_TN[elem] = []
                    for prof in profissoes_set:
                        dict_TN[elem].append({'prof':prof})
                    dict_TN[elem].append({'locals':locals, 'temas':temas})

print("TELA NON (S. TOMÉ E PRÍNCIPE)")
#pp.pprint(dict_TN)
i = 0
f=open('TN.html',mode='w')
f.write('<meta charset=\"UTF-8\">')
f.write('<title>TELA NON (S. TOMÉ E PRÍNCIPE)</title>')
f.write('<h1>TELA NON (S. TOMÉ E PRÍNCIPE)</h1>')
for elem in dict_TN:
    #pp.pprint(dict_TN[elem])
    decoded_elem = ud.unidecode(elem)
    decoded_elem = decoded_elem.replace(' ','_')

    tag = '<a href=tn_html/'+decoded_elem+'.html>'+elem+'</a><br>'

    f.write(tag)

    html=open('tn_html/'+decoded_elem+'.html','w')
    html.write('<meta charset=\"UTF-8\">\n')
    html.write('<title>'+elem+'</title>')
    html.write('<h1>'+elem+'</h1>')
    html.write('<h6>em Tela-Non</h6>')
    html.write('<table width=\"100%\" heigth=\"100%\">')
    html.write('<td width=\"33%\" heigth=\"100%\">')
    html.write('PROFISSOES<br>')
    for i in range(0,len(dict_TN[elem]),1):
        if 'prof' in dict_TN[elem][i]:
            if dict_TN[elem][i]['prof'] != '':
                html.write(dict_TN[elem][i]['prof']+'<br>')

    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('LOCAIS<br>')
    for i in range(0,len(dict_TN[elem]),1):
        if 'locals' in dict_TN[elem][i]:
            for local in dict_TN[elem][i]['locals']:
                html.write(local+'<br>')
    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('TEMAS<br>')
    for i in range(0,len(dict_TN[elem]),1):
        if 'temas' in dict_TN[elem][i]:
            for tema in dict_TN[elem][i]['temas']:
                html.write(tema+'<br>')
    html.write('</td>')
    html.write('</table>')
    html.close()

f.close()

'''
print(dict_TN)
json = json.dumps(dict_TN)
f=open("ST_TN.json","w")
f.write(json)
f.close()
'''

#___________________________________TIMOR LESTE _______________________________________-
onlyfiles = [f for f in listdir('obter_colecoes/[TL] Governo Timor-Leste/noticias/') if isfile(join('obter_colecoes/[TL] Governo Timor-Leste/noticias/',f))]
dict_TLEST = {}
for filename in onlyfiles:
    aux_set = set ()
    #print(filename)
    path= 'obter_colecoes/[TL] Governo Timor-Leste/noticias/' + filename
    tree = ET.parse(path)
    root = tree.getroot()
    data = "data Null"
    locals = set()
    temas = set()
    tema = ''
    for child in root:
        if child.tag == "Date":
            data = child.text

        if child.tag == "Text":
            tokens = nltk.word_tokenize(child.text)
            #for pal in tokens:
            for previous, item, nxt in previous_and_next(tokens):
            #for item in tokens:
                decoded = ud.unidecode(item)
                if item[0].isupper() and decoded in worldCitiesSet:
                    locals.add(decoded)

                if item.lower() in temasSet:
                    temas.add(item)

                if item[0].isupper() and item.upper() in nomesPtSet:
                    #nomeProprio + (nomeProprio || apelido)

                    if previous and previous.lower() in profissoesPtSet:
                        profissoes_set.add(previous)
                    else:
                        profissoes_set.add('')

                    if nxt is not None and (nxt.upper() in apelidosPtSet or nxt.upper() in nomesPtSet):
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



            dataAsKey = ((data.split('/')[0]).strip('\n')).strip()
            c = dataAsKey.split(',')
            if len(c)>2:
                c = c[1].strip().split(' ')
                dataAsKey = c[0] + ' ' + c[1] + ' ' + c[2]

            if locals == set():
                locals = ''
            if temas == set():
                temas = ''


            for elem in aux_set:
                if elem in dict_TLEST:
                    for prof in profissoes_set:
                        dict_TLEST[elem].append({'prof':prof})
                    dict_TLEST[elem].append({'locals':locals, 'temas':temas})
                else:
                    dict_TLEST[elem] = []
                    for prof in profissoes_set:
                        dict_TLEST[elem].append({'prof':prof})
                    dict_TLEST[elem].append({'locals':locals, 'temas':temas})

print("GOVERNO TIMOR-LESTE")
#pp.pprint(dict_TLEST)
i = 0
f=open('TLEST.html',mode='w')
f.write('<meta charset=\"UTF-8\">')
f.write('<title>GOVERNO TIMOR-LESTE</title>')
f.write('<h1>GOVERNO TIMOR-LESTE</h1>')
for elem in dict_TLEST:
    #pp.pprint(dict_TLEST[elem])
    decoded_elem = ud.unidecode(elem)
    decoded_elem = decoded_elem.replace(' ','_')

    tag = '<a href=tlest_html/'+decoded_elem+'.html>'+elem+'</a><br>'

    f.write(tag)

    html=open('tlest_html/'+decoded_elem+'.html','w')
    html.write('<meta charset=\"UTF-8\">\n')
    html.write('<title>'+elem+'</title>')
    html.write('<h1>'+elem+'</h1>')
    html.write('<h6>em Governo Timor-Leste</h6>')
    html.write('<table width=\"100%\" heigth=\"100%\">')
    html.write('<td width=\"33%\" heigth=\"100%\">')
    html.write('PROFISSOES<br>')
    for i in range(0,len(dict_TLEST[elem]),1):
        if 'prof' in dict_TLEST[elem][i]:
            if dict_TLEST[elem][i]['prof'] != '':
                html.write(dict_TLEST[elem][i]['prof']+'<br>')

    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('LOCAIS<br>')
    for i in range(0,len(dict_TLEST[elem]),1):
        if 'locals' in dict_TLEST[elem][i]:
            for local in dict_TLEST[elem][i]['locals']:
                html.write(local+'<br>')
    html.write('</td><td width=\"33%\" heigth=\"100%\">')
    html.write('TEMAS<br>')
    for i in range(0,len(dict_TLEST[elem]),1):
        if 'temas' in dict_TLEST[elem][i]:
            for tema in dict_TLEST[elem][i]['temas']:
                html.write(tema+'<br>')
    html.write('</td>')
    html.write('</table>')
    html.close()

f.close()

'''
print(dict_TLEST)
json = json.dumps(dict_TLEST)
f=open("TL_TLEST.json","w")
f.write(json)
f.close()
'''
