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
    data = scrapertools.get_match(data,"<div id='dle-content'>(.*?)</div>")

    # Extrae las entradas (carpetas)
    '''
    <a href="http://www.pelis24.com/pelicula-ca/13617-el-amor-de-tony-2010-castellano.html" ><img src="http://www.pelis24.com/uploads/posts/2012-06/1339789029_cartel_el_amor_de_tony_0.jpg" width="145" height="211" alt="el amor de tony (2010) - Castellano" title="el amor de tony (2010) - Castellano"/></a>&nbsp;&nbsp;
    '''
    patron  = '<a.*?href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)".*?alt="([^"]+)"'
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


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien