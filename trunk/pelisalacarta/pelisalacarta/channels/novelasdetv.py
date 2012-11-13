# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para novelasdetv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Novelas de TV"
__channel__ = "novelasdetv"
__language__ = "ES"
__creationdate__ = "20121112"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[novelasdetv.py] mainlist")
    item.url="http://www.novelasdetv.com"
    return series(item)

def series(item):
    logger.info("[novelasdetv.py] series")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    
    patron = "<li><a href='(http.//www.novelasdetv.com/20[^']+)'>([^<]+)</a></li>"
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    itemlist = sorted(itemlist, key=lambda item: item.title.lower())

    return itemlist

def episodios(item):
    logger.info("[novelasdetv.py] episodios")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    try:
        data = scrapertools.get_match(data,"<div class='post-body entry-content'>(.*?)<div id='sidebar-wrapper'>")
    except:
        pass
    patron = '<a href="([^"]+)" target="_blank">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, viewmode="movie_with_plot"))

    if len(itemlist)==0:
        itemlist.append( Item(channel=__channel__, action="" , title="No hay episodios de esta serie en la web"))
    
    return itemlist

def findvideos(item):
    data = scrapertools.cache_page(item.url)
    
    #http://content4.catalog.video.msn.com/e2/ds/69c13d8c-913e-42d7-bf43-fa157e16e97d.mp4& 
    patron='(http:\//[a-z0-9\.]+msn.com/[a-z0-9\/\-]+\.mp4)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for scrapedurl in matches:
        itemlist.append( Item(channel=__channel__, action="play" , server="directo", title="Ver en msn.com" , url=scrapedurl, folder=False))

    #http://content4.catalog.video.msn.com/e2/ds/69c13d8c-913e-42d7-bf43-fa157e16e97d.flv& 
    patron='(http:\//[a-z0-9\.]+msn.com/[a-z0-9\/\-]+\.flv)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for scrapedurl in matches:
        itemlist.append( Item(channel=__channel__, action="play" , server="directo", title="Ver en msn.com" , url=scrapedurl, folder=False))

    listavideos = servertools.findvideos(data=data)
    for video in listavideos:
        scrapedurl = video[1]
        server = video[2]
        scrapedtitle = "Ver en "+server
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, folder=False) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                mirrors = findvideos(item=itemlist[0])
                if len(mirrors)>0:
                    return True

    return False