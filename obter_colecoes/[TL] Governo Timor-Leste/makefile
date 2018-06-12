rss='http://timor-leste.gov.tl/?f=1&cat=9&langpt'
hoje=$(shell date '+%m-%d')
xpath_date=//span[@class="tit"]
xpath_sec=//html/body//div/main/article//div/section/div/header/p/a
xpath_title=//title
xpath_descript=//h2[@class="lead"]
xpath_content=//p[@style="text-align: justify;"]
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
	cd $(hoje) ; for a in *; do echo \<?xml version=\"1.0\" encoding=\"UTF-8\"?\>\<xml\> > ../noticias/$(hoje)-$$a.xml; echo \<Date\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_date)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Date\>\\n\<Title\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_title)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Title\>\\n\<Text\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_content)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Text\>\<\/xml\> >> ../noticias/$(hoje)-$$a.xml; done
	cd noticias ; rename 's/[ \?]/_/g' *