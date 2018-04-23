rss='https://www.telanon.info/feed/'
hoje=$(shell date '+%m-%d')
xpath_date =//time
xpath_sec=//span[@class="post-head-cat"]
xpath_title=//h1[contains(@class,"post-title")]
xpath_content=//div[contains(@id,"content-main")]
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
	cd $(hoje) ; for a in *; do echo \<?xml version="1.0" encoding="UTF-8"?\> > ../noticias/$(hoje)-$$a.xml; echo \<Date\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_date)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Date\>\\n\<Sec\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_sec)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Sec\>\\n\<Title\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_title)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Title\>\\n\<Text\> >> ../noticias/$(hoje)-$$a.xml; xidel $$a -e '$(xpath_content)' >> ../noticias/$(hoje)-$$a.xml; echo \<\/Text\> >> ../noticias/$(hoje)-$$a.xml; done
