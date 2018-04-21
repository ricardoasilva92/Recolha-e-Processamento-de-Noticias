#!/usr/bin/python3

import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
import sys
texto = "O secretário-geral dos ACP, Patrick Gomes, manteve, no último fim-de-semana, encontros com alguns dirigentes africanos, a fim de os informar sobre a organização da Cimeira, em que devem estar representados 79 Estados membros e convidados parceiros do desenvolvimento. Numa altura em que se intensificam os preparativos para o encontro, o secretário-geral dos ACP e o subsecretário-geral encarregado das Questões Políticas e do Desenvolvimento Humano, embaixador Leonardo Ognimba, participaram, como convidados, na 26.ª Cimeira da União Africana. À margem da recente Cimeira da UA, realizada na sede da organização continental, em Addis Abeba, Patrick Gomes e Leonardo Ognimba tiveram encontros com diferentes delegações, a fim de preparar a próxima Cimeira dos ACP.A 8.ª Cimeira constitui  uma viragem para o Grupo dos Estados ACP, após um ano de 2015 particularmente determinante para a comunidade internacional, que assistiu à adopção histórica dos Objectivos de Desenvolvimento Sustentável e do Acordo de Paris sobre as mudanças climáticas”, declarou Patrick Gomes.  O secretário-geral disse que o tema da Cimeira, “Reposicionar o grupo ACP para responder aos desafios do desenvolvimento sustentável”, vai permitir aos dirigentes se debruçarem sobre o papel que pode desempenhar o grupo a fim de apoiar a implementação do Programa de Desenvolvimento Sustentável ao horizonte 2030 nos países membros, bem como a nível regional e continental. Os futuros domínios estratégicos do grupo ACP vão ser igualmente examinados ao mais alto nível na Cimeira de Porto Moresby, acrescentou Patrick Gomes. Após a comemoração, no ano passado, do 40.º aniversário do Acordo de Georgetown, disse, o grupo prossegue as suas reflexões internas sobre a maneira como se deve transformar, a fim de se tornar um actor mundial mais eficaz no século XXI. Esse processo comporta uma avaliação crítica da valiosa parceria que existe com a União Europeia, no quadro do Acordo de Cotonou e que expira em 2020. Patrick Gomes informou que o Grupo de Personalidades Eminentes   dos ACP,  vai submeter à apreciação dos Chefes de Estado e de Governo propostas sobre o reposicionamento futuro do grupo."

a = sys.argv
if len(a) > 1 :
    f = open(a[1],"r").read()
else: 
    exit(1)

lista_palavras = (word_tokenize(f))

print(nltk.trigrams(f))