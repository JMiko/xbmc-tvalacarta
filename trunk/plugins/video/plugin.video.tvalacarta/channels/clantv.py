# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Clan TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import logger
import scrapertools
from item import Item

logger.info("[clantv.py] init")

DEBUG = True
CHANNELNAME = "clantv"

def isGeneric():
	return True

def mainlist(item):
	logger.info("[clantv.py] mainlist")

	url = 'http://www.rtve.es/infantil/videos-juegos/#/videos/clan/todos/'

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae las categorias (carpetas)
	# --------------------------------------------------------
	patron = '<li.*?><a rel="([^"]+)" title="[^"]+" href="([^"]+)"><strong>([^<]+)</strong><img src="([^"]+)".*?><span>([^<]+)</span>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		try:
			scrapedtitle = unicode( match[2], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2]
		scrapedtitle = scrapedtitle + " ("+match[4].replace("&iacute;","i")+")"
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedurl = "http://www.rtve.es/infantil/components/"+match[0]+"/videos.xml.inc"
		scrapedthumbnail = urlparse.urljoin(url,match[3])
		scrapedplot = ""

		if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist

def episodios(item):
	logger.info("[clantv.py] episodios")

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage2(item.url,[["Referer","http://www.rtve.es/infantil/videos-juegos/#/videos/edebits/todos/"],["User-Agent","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; InfoPath.2)"]])
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los capítulos
	# --------------------------------------------------------
	patron = '<video id="[^"]+" thumbnail="([^"]+)" url="([^"]+)" publication_date="([^T]+)T[^>]+>[^<]+<title>([^<]+)</title>[^<]+<sinopsis([^<]+)<'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		try:
			scrapedtitle = unicode( match[3], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[3]
		scrapedtitle = scrapedtitle + " ("+match[2]+")"
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedurl = urlparse.urljoin(item.url,match[1])
		scrapedthumbnail = urlparse.urljoin(item.url,match[0])
		scrapedplot = match[4]
		if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="Directo", url=scrapedurl, page = item.url, thumbnail=scrapedthumbnail, plot=scrapedplot) )

	return itemlist

def test():
	itemsmainlist = mainlist(None)
	for item in itemsmainlist: print item.tostring()

	itemsepisodios = episodios(itemsmainlist[0])

if __name__ == "__main__":
	test()
