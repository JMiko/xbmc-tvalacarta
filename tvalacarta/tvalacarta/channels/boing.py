# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para boing.es
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[boing.py] init")

DEBUG = True
CHANNELNAME = "boing"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[boing.py] mainlist")
    itemlist = programas(Item(channel=CHANNELNAME,url="http://www.boing.es/series?order=title&sort=asc") )
    return itemlist

def programas(item):
    logger.info("[boing.py] series")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las series
    patron  = '<div id="item-[^<]+'
    patron += '<div class="title"><a href="([^"]+)">([^<]+)</a></div>.*?'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    destacadas = 4
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        destacadas = destacadas - 1
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if destacadas>=0:
            logger.info("ignorando, es de la caja de destacadas")
        else:
            itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="episodios" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail , show = scrapedtitle, folder=True) )
    patron = '<li class="pager-next"><a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        itemlist.append( Item(channel=item.channel, title="Página siguiente >>" , action="programas" , url=urlparse.urljoin(item.url,matches[0]), folder=True) )

    return itemlist

def episodios(item):
    logger.info("[boing.py] episodios")

    # Descarga la página
    #http://www.boing.es/serie/hora-de-aventuras
    #http://www.boing.es/videos/hora-de-aventuras
    data = scrapertools.cachePage(item.url.replace("/serie/","/videos/"))
    #logger.info(data)

    # Extrae los videos
    patron = '<div id="item-.*?'
    patron += '<div class="pic3">[^<]+<a href="([^"]+)">.*?'
    patron += '<img style="[^"]+" height="[^"]+" width="[^"]+" src="([^"]+)".*?'
    patron += '<div class="title"><a[^>]+>([^<]+)</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    destacadas = 4
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        destacadas = destacadas - 1
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if destacadas>=0:
            logger.info("ignorando, es de la caja de destacadas")
        else:
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="Directo" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail, page=item.url, show = item.show, folder=True) )

    return itemlist

def test():
    itemsmainlist = mainlist(None)
    for item in itemsmainlist: print item.tostring()

    itemsseries = series(itemsmainlist[1])
    itemsepisodios = episodios(itemsseries[4])

if __name__ == "__main__":
    test()
