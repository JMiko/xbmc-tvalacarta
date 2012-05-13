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
MAIN_URL = "http://www.boing.es/series?order=title&sort=asc"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[boing.py] mainlist")
    item.url = MAIN_URL
    return series(item)

def series(item):
    logger.info("[boing.py] series")
    itemlist = []

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
        itemlist.extend( series(Item(channel=item.channel, title="Página siguiente >>" , action="series" , url=urlparse.urljoin(item.url,matches[0]), folder=True) ) )

    return itemlist

def episodios(item):
    logger.info("[boing.py] episodios")

    # Descarga la página
    #http://www.boing.es/serie/hora-de-aventuras
    #http://www.boing.es/videos/hora-de-aventuras
    data = scrapertools.cachePage(item.url.replace("/serie/","/videos/"))
    #logger.info(data)
    bloque = scrapertools.get_match(data,'<div class="Contenedor100">(.*?)<\!-- \/Contenedor100 -->',1)
    logger.info(str(bloque))

    # Extrae los videos
    '''
    <div class="pic"><div class="pic2"><div class="pic3">    
    <a href="/serie/geronimo-stilton/video/top-model">
    <img class="bcvid" height="73" width="130" src="http://i.cdn.turner.com/tbseurope/big/Boing_ES/thumbs/SP_SA_GERSTI0017_01.jpg" />
    </a>
    </div></div></div>
    <div class="series"><a href="/serie/geronimo-stilton">Gerónimo Stilton</a></div>
    <div class="title"><a href="/serie/geronimo-stilton/video/top-model">Top Model</a></div>
    '''
    patron  = '<div class="pic3">[^<]+<a href="([^"]+)">[^<]+'
    patron += '<img class="bcvid" height="[^"]+" width="[^"]+" src="([^"]+)".*?'
    patron += '<div class="title"><a[^>]+>([^<]+)</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="boing" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail, page=item.url, show = item.show, folder=False) )

    return itemlist

def test():
    itemsmainlist = mainlist(None)
    for item in itemsmainlist: print item.tostring()

    itemsseries = series(itemsmainlist[1])
    itemsepisodios = episodios(itemsseries[4])

if __name__ == "__main__":
    test()
