# -*- coding: utf-8 -*-

import nltk
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

#from nltk.tag.stanford import StanfordNERTagger
#st = StanfordNERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

from geotext import GeoText

from nltk.tag.stanford import StanfordNERTagger
# First we set the direct path to the NER Tagger.
_model_filename = r'/home/ricardo/Desktop/SPLN/projeto_spln/stanford-ner/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz'
_path_to_jar = r'/home/ricardo/Desktop/SPLN/projeto_spln/stanford-ner/stanford-ner-2015-04-20/stanford-ner.jar'

# First we set the direct path to the NER Tagger.
_model_filename_l = r'/home/fontao/Desktop/SPLN/tp/spln_2018/stanford-ner/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz'
_path_to_jar_l = r'/home/fontao/Desktop/SPLN/tp/spln_2018/stanford-ner/stanford-ner-2018-02-27/stanford-ner.jar'
# Then we initialize the NLTK's Stanford NER Tagger API with the DIRECT PATH to the model and .jar file.
st = StanfordNERTagger(model_filename=_model_filename_l, path_to_jar=_path_to_jar_l)

texto = "O secretário-geral dos ACP, Patrick Gomes, manteve, no último fim-de-semana, encontros com alguns dirigentes africanos, a fim de os informar sobre a organização da Cimeira, em que devem estar representados 79 Estados membros e convidados parceiros do desenvolvimento. Numa altura em que se intensificam os preparativos para o encontro, o secretário-geral dos ACP e o subsecretário-geral encarregado das Questões Políticas e do Desenvolvimento Humano, embaixador Leonardo Ognimba, participaram, como convidados, na 26.ª Cimeira da União Africana. À margem da recente Cimeira da UA, realizada na sede da organização continental, em Addis Abeba, Patrick Gomes e Leonardo Ognimba tiveram encontros com diferentes delegações, a fim de preparar a próxima Cimeira dos ACP.A 8.ª Cimeira constitui  uma viragem para o Grupo dos Estados ACP, após um ano de 2015 particularmente determinante para a comunidade internacional, que assistiu à adopção histórica dos Objectivos de Desenvolvimento Sustentável e do Acordo de Paris sobre as mudanças climáticas”, declarou Patrick Gomes.  O secretário-geral disse que o tema da Cimeira, “Reposicionar o grupo ACP para responder aos desafios do desenvolvimento sustentável”, vai permitir aos dirigentes se debruçarem sobre o papel que pode desempenhar o grupo a fim de apoiar a implementação do Programa de Desenvolvimento Sustentável ao horizonte 2030 nos países membros, bem como a nível regional e continental. Os futuros domínios estratégicos do grupo ACP vão ser igualmente examinados ao mais alto nível na Cimeira de Porto Moresby, acrescentou Patrick Gomes. Após a comemoração, no ano passado, do 40.º aniversário do Acordo de Georgetown, disse, o grupo prossegue as suas reflexões internas sobre a maneira como se deve transformar, a fim de se tornar um actor mundial mais eficaz no século XXI. Esse processo comporta uma avaliação crítica da valiosa parceria que existe com a União Europeia, no quadro do Acordo de Cotonou e que expira em 2020. Patrick Gomes informou que o Grupo de Personalidades Eminentes dos ACP,  vai submeter à apreciação dos Chefes de Estado e de Governo propostas sobre o reposicionamento futuro do grupo."

texto2 = "O João Fictício, o Manuel Fictício e o Jaime Fictício, conduziram um BMW de Guimarães, em Portugal, até Paris, na França (France)."

tokens = nltk.word_tokenize(texto2)

tagged = nltk.pos_tag(tokens)

entities = nltk.chunk.ne_chunk(tagged)

print('-------------')
print('PERSONS: ')
for entity in entities:
	if type(entity) is nltk.Tree:
		if entity.label()=='PERSON':
			print(entity.leaves())

print('-------------')
print('ORGANIZATIONS: ')
for entity in entities:
	if type(entity) is nltk.Tree:
		if entity.label()=='ORGANIZATION':
			print(entity.leaves())

print('-------------')
print('GPE: ')
for entity in entities:
	if type(entity) is nltk.Tree:
		if entity.label()=='GPE':
			print(entity.leaves())

print('-------------')
print('Stanford-Ner: ')
for token in tokens:
    token_aux = nltk.tokenize.word_tokenize(token)
    tags = st.tag(token_aux)
    for tag in tags:
        if tag[1]=='PERSON': print(tag)

#GEOTEXT
places = GeoText(texto2)
print('-------------')
print('CIDADES:')
print(places.cities)
print('PAÍSES:')
print(places.countries)
