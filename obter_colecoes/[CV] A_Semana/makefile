rss='http://www.asemana.publ.cv/spip.php?page=backend&id_mot=1&ak=1'
hoje=$(shell date '+%m-%d')
xpath_date=//span[@class="date"]
xpath_sec=//h2[contains(@class, "grandtitre crayon rubrique-titre")]
xpath_title=//h2[contains(@class, "crayon article-titre-")]
xpath_descript=//h4[contains(@class, "crayon article-descriptif-")]
xpath_content=//div[contains(@class, "crayon article-texte-")]
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
	cd $(hoje) ; for a in *; do echo \<?xml version=\"1.0\" encoding=\"UTF-8\"?\>\<xml\> > ../noticias/$(hoje)-$$a.xml; echo \<Date\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_date)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Date\>\\n\<Sec\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_sec)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Sec\>\\n\<Title\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_title)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Title\>\\n\<Description\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_descript)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Description\>\\n\<Text\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_content)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Text\>\<\/xml\> >> ../noticias/$(hoje)-$$a.xml; done
	cd noticias ; rename 's/[ \?]/_/g' *