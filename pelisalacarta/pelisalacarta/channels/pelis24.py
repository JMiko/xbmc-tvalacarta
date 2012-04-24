# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelis24"
__category__ = "F,S"
__type__ = "xbmc"
__title__ = "Pelis24"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelis24.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"    , action="peliculas", url="http://pelis24.com/"))
    itemlist.append( Item(channel=__channel__, title="Estrenos"    , action="peliculas", url="http://pelis24.com/estrenos/"))
    itemlist.append( Item(channel=__channel__, title="Castellano"    , action="peliculas", url="http://pelis24.com/pelicula-ca/"))
    itemlist.append( Item(channel=__channel__, title="Latino"    , action="peliculas", url="http://pelis24.com/pelicula-latino/"))
    itemlist.append( Item(channel=__channel__, title="Subtituladas"    , action="peliculas", url="http://pelis24.com/peliculasvose/"))
    itemlist.append( Item(channel=__channel__, title="Recomendadas"    , action="peliculas", url="http://pelis24.com/pelicula-re/"))
    
    return itemlist

def peliculas(item):
    logger.info("[pelis24.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    '''
    <a class="" href="http://www.pelis24.com/estrenos/13156-lorax-en-busca-de-la-trfula-perdida-2012-ruso.html" ><img src="http://www.pelis24.com/uploads/posts/2012-03/1331437256_lorax_en_busca_de_la_trufula_perdida-322812684-large.jpg" width="145" height=211" alt="Lorax, en busca de la trúfula perdida (2012) - Latino, Castellano" /></a>&nbsp;&nbsp;
    '''
    patron  = '<a class="" href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)".*?alt="([^"]+)" /></a>\&nbsp\;\&nbsp\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )


    # Extrae el paginador
    patronvideos  = '<span>[^<]+</span>[^<]+<a href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist
