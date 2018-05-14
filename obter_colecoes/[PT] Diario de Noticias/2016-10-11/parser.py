import xml.etree.ElementTree as ET
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '\n', raw_html)
  return cleantext

tree = ET.parse("arq.xml")

root = tree.getroot()

channel = tree.find('channel')

i = 0

enc = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
sec = '<Sec>\nGeral\n</Sec>'

for child in channel:
    for tag in child:
        if(tag.tag=='title'):
            title='<Title>\n'+tag.text+'\n</Title>\n'
        if(tag.tag=='pubDate'):
            date='\n<xml>\n<Date>\n'+tag.text+'\n</Date>\n'
        if(tag.tag=='description'):
            description='<Text>\n'+cleanhtml(tag.text)+'\n</Text>\n</xml>\n'

            f=open('2016-12-31_'+str(i)+'.xml','w+')
            f.write(enc)
            f.write(date)
            f.write(sec)
            f.write(title)
            f.write(description)
            f.close()

            i=i+1
