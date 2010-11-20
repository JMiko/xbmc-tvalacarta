# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Clan TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[clantv.py] init")

DEBUG = True
CHANNELNAME = "clantve"
MODO_CACHE=0

def isGeneric():
    return True

def mainlist(item):
    logger.info("[clantv.py] mainlist")
    item = Item(url="http://www.rtve.es/infantil/series/")
    return programas(item)

def programas(item):
    logger.info("[clantv.py] programas")

    # Descarga la página
    data = scrapertools.cachePage(item.url,modoCache=MODO_CACHE)

    # Extrae los programas
    patron  = '<div class="informacion-serie">[^<]+'
    patron += '<h3><a href="([^"]+)">([^<]+)</a></h3><a[^>]+>[^<]+</a><img.*?src="([^"]+)"><div>(.*?)</div>.*?'
    patron += '<div class="videos">.*?'
    patron += '<p class="vertodos"><a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedurl = urlparse.urljoin(item.url,match[4])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = match[3]
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        scrapedplot = scrapertools.entityunescape(scrapedplot)

        scrapedpage = urlparse.urljoin(item.url,match[0])
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] plot=["+scrapedplot+"]")
        #logger.info(scrapedplot)

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , page=scrapedpage, show=scrapedtitle , folder=True) )

    # Añade el resto de páginas
    patron = '<li class="siguiente"><a rel="next" title="Ir a la p&aacute;gina siguiente" href="([^"]+)">Siguiente</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        match = matches[0]
        newitem = Item(channel=CHANNELNAME,url=urlparse.urljoin(item.url,match))
        itemlist.extend(programas(newitem))

    return itemlist

def episodios(item):
    logger.info("[clantv.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url,modoCache=MODO_CACHE)

    # Extrae los capítulos
    patron = '<div class="contenido-serie">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return itemlist
    data2 = matches[0]

    patron = '<ul class="videos">[^<]+'
    patron = '<li>[^<]+'
    patron = '<dl>[^<]+'
    patron = '<dt>[^<]+</dt>[^<]+'
    patron = '<dd><a rel="([^"]+)".*?href="([^"]+)"><img src="([^"]+)"[^>]+>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data2)
    
    # Extrae los items
    for match in matches:
        scrapedtitle = match[3]
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        
        # La página del vídeo
        scrapedpage = urlparse.urljoin(item.url,match[1])
        
        # Código de la serie
        scrapedcode = match[0]
        
        # Url de la playlist
        scrapedurl = "http://www.rtve.es/infantil/components/"+scrapedcode+"/videos.xml.inc"
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], page=["+scrapedpage+"] thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="Directo", page=scrapedpage, url=scrapedurl, thumbnail=scrapedthumbnail, show=item.show , plot=scrapedplot , folder=False) )

    # Ahora extrae el argumento y la url del vídeo
    dataplaylist = scrapertools.cachePage(scrapedurl,modoCache=MODO_CACHE)
    
    for episodeitem in itemlist:
        partes = episodeitem.page.split("/")
        code = partes[len(partes)-2]
        patron  = '<video id="'+code+'".*?url="([^"]+)".*?'
        patron += '<sinopsis>(.*?)</sinopsis>'
        matches = re.compile(patron,re.DOTALL).findall(dataplaylist)

        if len(matches)>0:
            episodeitem.url = urlparse.urljoin(item.url,matches[0][0])
            episodeitem.plot = matches[0][1]

    # Añade el resto de páginas
    patron = '<li class="siguiente"><a rel="next" title="Ir a la p&aacute;gina siguiente" href="([^"]+)">Siguiente</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        match = matches[0]
        item.url = urlparse.urljoin(item.url,match)
        itemlist.extend(episodios(item))

    return itemlist
