# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmpertutti"
__category__ = "F"
__type__ = "generic"
__title__ = "filmpertutti"
__language__ = "IT"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.filmpertutti mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Film Del Cinema", action="peliculas", url="http://filmxtutti.net/news_film/"))
    itemlist.append( Item(channel=__channel__, title="Aggiornamenti Serie TV", action="peliculas", url="http://filmxtutti.net/ultime_serie/"))
    itemlist.append( Item(channel=__channel__, title="Film per genere" , action="categorias", url="http://filmxtutti.net/"))
    itemlist.append( Item(channel=__channel__, title="Cerca Film", action="search"))
    return itemlist
    
def search(item,texto):
    logger.info("pelisalacarta.filmpertutti search "+texto)
    itemlist = []
    texto = texto.replace(" ","%20")
    item.url = "http://filmxtutti.net/?s="+texto
    item.extra = ""

    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def categorias(item):
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h4><span[^>]+>Genere Film</span></h4>(.*?)</div[^<]+</div[^<]+</div')

    patron  = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.filmpertutti peliculas")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class="xboxcontent">
    <h2><a href="http://filmpertutti.tv/il-padrino-di-chinatown/" rel="bookmark" title="Il padrino di Chinatown" target=""><img width="192" height="262" src="http://filmpertutti.tv/wp-content/uploads/2012/06/IlpadrinodiChinatown.jpeg" class="attachment-post-thumbnail wp-post-image" alt="IlpadrinodiChinatown" title="IlpadrinodiChinatown">              Il padrino di Chinatown              </a>  </h2> 
    <p>  ...  </p>
    </div>
    '''
    patron  = '<div class="xboxcontent">\s*'
    patron += '<h2><a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?<img.*?src="([^>"]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<div class=\'Navi\'>.*?<a href="([^"]+)" ><strong>&raquo;</strong></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Next Page >>" , url=scrapedurl , folder=True) )

    return itemlist

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si est� ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien