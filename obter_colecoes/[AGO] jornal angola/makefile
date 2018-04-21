rss='http://jornaldeangola.sapo.ao/feeds/articles?format=xml'
hoje=$(shell date '+%m-%d')
xpath=//p[4]
xpath_time=(//time[@class="date-time"])[1]
xpath_seccao=//div[@class="categoria"]
xpath_autor=//p[@class="info-autor"]
xpath_titulo=//article[@class="half-bottom-space"]/h1
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
	cd $(hoje) ; for a in *; do xidel $$a -e '$(xpath)' -e '$(xpath_time)' -e '$(xpath_seccao)' -e '$(xpath_autor)' -e '$(xpath_titulo)' --xml > ../noticias/$(hoje)-$$a.xml; done
