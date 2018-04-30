rss='http://www.dnoticias.pt/rss/home.xml'
hoje=$(shell date '+%m-%d')
xpath=//div[@class="paragraph"]/p
xpath_time=//div[@class="datefrom small"]
xpath_seccao="Geral"
xpath_autor=//div[@class="byline font-1 small bold"]/a
xpath_titulo=//h1[@class="headline font-1 medium bold"]/span[@class="priority-content"]
$(hoje).rss:
	wget $(rss) -O $(hoje).rss
$(hoje).urls: $(hoje).rss
	xidel $(hoje).rss -e //item/link > $(hoje).urls
$(hoje).files: $(hoje).urls
	mkdir -p $(hoje)
	cd $(hoje); wget -i ../$(hoje).urls
	ls $(hoje) > $(hoje).files
p4: $(hoje).files
	mkdir -p noticias
	cd $(hoje) ; for a in *; do echo \<?xml version=\"1.0\" encoding=\"UTF-8\"?\>\<xml\>  > ../noticias/$(hoje)-$$a.xml; echo \<Date\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_time)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Date\>\\n\<Sec\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_seccao)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Sec\>\\n\<Title\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_titulo)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Title\>\\n\<Text\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Text\>\\n\<Autor\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_autor)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Autor\>\<\/xml\> >> ../noticias/$(hoje)-$$a.xml;done
	
