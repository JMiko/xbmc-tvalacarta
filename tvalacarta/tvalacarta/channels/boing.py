# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para boing.es
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

try:
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

logger.info("[boing.py] init")

DEBUG = True
CHANNELNAME = "boing"

def isGeneric():
	return True

def mainlist(item):
	logger.info("[boing.py] mainlist")

	itemlist = []
	#itemlist.append( Item(channel=CHANNELNAME, extra=code, title="Novedades" , action="novedades" , url="http://www.boing.es/videos/"+code+".xml", folder=True) )
	itemlist.append( Item(channel=CHANNELNAME, title="Series"    , action="series"    , url="http://www.boing.es/videos/videos_desencriptado2.xml", folder=True) )

	return itemlist

def series(item):
	logger.info("[boing.py] series")

	# Descarga la página
	data = scrapertools.cachePage(item.url)
	logger.info(data)

	# Extrae el bloque donde están las series
	patronvideos = '<series>(.*?)</series>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)
	data = matches[0]
	
	# Extrae las series
	patronvideos = '<item id="([^"]+)" nombre="([^"]+)"[^<]+<imagen>([^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		scrapedtitle = match[1]
		code = match[0]
		scrapedthumbnail = match[2]
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], code=["+code+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado
		itemlist.append( Item(channel=CHANNELNAME, extra=code, title=scrapedtitle , action="episodios" , url=item.url, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist

def episodios(item):
	logger.info("[boing.py] episodios")

	print item.tostring()
	print "extra=#"+item.extra+"#"
	print "url=#"+item.url+"#"
	
	# Descarga la página
	data = scrapertools.cachePage(item.url)
	#logger.info(data)

	# Extrae los videos
	'''
	<video id="ben10af_ep2_01" series="ben10af" extras="" novedad="0">
	<titulo>Episodio 2  (parte 1)</titulo>
	<imagen>/videos/1clips/ben10af/ep/ep.jpg</imagen>
	<url>http://ht.cdn.turner.com/tbseurope/big/toones/protected_auth/b10af/Ben10_Ep02_Sg01.flv</url>
	<stats>http://www.boing.es/videos/stats/episodios_ben10af.html</stats>
	<descripcion><![CDATA[<a href='/microsites/ben10alienforce/index.jsp' target='_self'><font color='#FF0000'>Pincha</font></a> para visitar la página de Ben 10 Alien Force<br/>Episodios solamente disponibles en España]]></descripcion>
	</video>
	'''
	# Extrae las entradas (videos, extra es el id de la serie)
	print "extra=#"+item.extra+"#"
	patronvideos  = '<video id="[^"]+" series="'+item.extra+'"[^>]+>[^<]+'
	patronvideos += '<titulo>([^<]+)</titulo>[^<]+'
	patronvideos += '<imagen>([^<]+)</imagen>[^<]+'
	patronvideos += '<secuencias><item>([^<]+)</item></secuencias>[^<]+'
	patronvideos += '<stats>[^<]+</stats>[^<]+'
	patronvideos += '<descripcion>(.*?)</descripcion>[^<]+'
	patronvideos += '</video>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[0], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[0]
		scrapedurl = urlparse.urljoin(item.url,match[2])
		scrapedthumbnail = urlparse.urljoin(item.url,match[1])
		try:
			scrapedplot = scrapertools.htmlclean(unicode( match[3], "utf-8" ).encode("iso-8859-1"))
		except:
			scrapedplot = scrapertools.htmlclean(match[3])
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="Directo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot) )

	return itemlist

def novedades(item):
	logger.info("[boing.py] novedades")

	print item.tostring()
	
	# Descarga la página
	data = scrapertools.cachePage(item.url)
	#logger.info(data)

	# Extrae los videos
	patronvideos  = '<video id="[^"]+" series="([^\"]+)" novedad="1"[^>]+>[^<]+'
	patronvideos += '<titulo>([^<]+)</titulo>[^<]+'
	patronvideos += '<imagen>([^<]+)</imagen>[^<]+'
	patronvideos += '<url>([^<]+)</url>[^<]+'
	patronvideos += '<stats>[^<]+</stats>[^<]+'
	patronvideos += '<descripcion>(.*?)</descripcion>[^<]+'
	patronvideos += '</video>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[0] + " - " + match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[0] + " - " + match[1]
		scrapedurl = urlparse.urljoin(item.url,match[3])
		scrapedthumbnail = urlparse.urljoin(item.url,match[2])
		try:
			scrapedplot = scrapertools.htmlclean(unicode( match[4], "utf-8" ).encode("iso-8859-1"))
		except:
			scrapedplot = scrapertools.htmlclean(match[4])
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="Directo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot) )

	return itemlist

def test():
	itemsmainlist = mainlist(None)
	for item in itemsmainlist: print item.tostring()

	itemsseries = series(itemsmainlist[1])
	itemsepisodios = episodios(itemsseries[4])

if __name__ == "__main__":
	test()
