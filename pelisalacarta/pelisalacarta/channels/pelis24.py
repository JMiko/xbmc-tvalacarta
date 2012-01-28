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
    <!--TBegin--><a href="http://www.pelis24.com/uploads/posts/2012-01/1327670351_dime_con_cuantos-301100490-large.jpg" onclick="return hs.expand(this)" ><img align="left" src="http://www.pelis24.com/uploads/posts/2012-01/thumbs/1327670351_dime_con_cuantos-301100490-large.jpg" alt='Dime con cuántos (2011) - Latino' title='Dime con cuántos (2011) - Latino'
    ...
    <div class="mlink">		<span class="argmore"><a href="http://www.pelis24.com/peliculas/12513-dime-con-cubntos-2011castellano-mic.html">
    '''
    patron = '<!--TBegin--><a href="([^"]+)"[^<]+'
    patron += '<img align="left" src="[^"]+" alt=\'([^\']+)\'.*?'
    patron += '<div class="mlink">[^<]+<span class="argmore"><a href="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedtitle,scrapedurl in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )


    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)"><span class="thide pnext">Siguiente</span></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist
