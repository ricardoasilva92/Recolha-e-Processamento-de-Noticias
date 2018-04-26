rss='http://feeds.feedburner.com/expresso-geral'
hoje=$(shell date '+%m-%d')
xpath_date=//p[@class="timeStamp publishedDate"]
xpath_sec=//html/body//div/main/article//div/section/div/header/p/a
xpath_title=//title
xpath_descript=//h2[@class="lead"]
xpath_content=//div[@class="articleContent"]
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
	cd $(hoje) ; for a in *; do echo \<?xml version="1.0" encoding="UTF-8"?\> > ../noticias/$(hoje)-$$a.xml; echo \<Date\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_date)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Date\>\\n\<Sec\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_sec)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Sec\>\\n\<Title\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_title)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Title\>\\n\<Description\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_descript)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Description\>\\n\<Text\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_content)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Text\> >> ../noticias/$(hoje)-$$a.xml; done
