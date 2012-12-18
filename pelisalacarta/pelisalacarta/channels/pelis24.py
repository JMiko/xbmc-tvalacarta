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
    itemlist.append( Item(channel=__channel__, title="Novedades"     , action="peliculas", url="http://pelis24.com/index.php"))
    itemlist.append( Item(channel=__channel__, title="Clasificacion" , action="categorias", url="http://pelis24.com/index.php"))
    
    return itemlist

def peliculas(item):
    logger.info("[pelis24.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <a href="http://www.pelis24.com/hd/13290-the-pirates-band-of-misfits-2012-latino.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/piratasuna.jpg" width="145" height="211" alt="¡Piratas! Una Loca Aventura (2012)" title="¡Piratas! Una Loca Aventura (2012)"/><noscript><img src="http://imgs24.com/images/piratasuna.jpg" width="145" height="211" alt="¡Piratas! Una Loca Aventura (2012)" title="¡Piratas! Una Loca Aventura (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-latino/14402-recreator-2012.html" ><img src="http://imgs24.com/images/recreator3.jpg" width="145" height="211" alt="Recreator (2012)" title="Recreator (2012)"/></a>&nbsp;&nbsp;

    '''
    patron  = '<a href="([^"]+)"[^<]+<img src="([^"]+)" width="\d+" height="\d+" alt="([^"]+)"'
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