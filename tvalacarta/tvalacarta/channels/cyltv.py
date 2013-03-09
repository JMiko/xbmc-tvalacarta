# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para cyltv (youtube)
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib
import os

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "cyltv"
YOUTUBE_CHANNEL_ID = "cyltelevision"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cyltv.py] mainlist")
    return programas(item)

def programas(item):
    logger.info("[cyltv.py] programas")

    itemlist = []

    # Descarga la página
    if item.url=="":
        item.url="http://gdata.youtube.com/feeds/api/users/"+YOUTUBE_CHANNEL_ID+"/playlists?v=2&start-index=1&max-results=12"
    data = scrapertools.cache_page(item.url)

    patron = "<entry(.*?)</entry>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for entry in matches:
        logger.info("entry="+entry)
        title = scrapertools.get_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = "" #scrapertools.get_match(entry,"<summary>([^<]+)</summary>")
        thumbnail = scrapertools.get_match(entry,"<media\:thumbnail url='([^']+)'")
        url = scrapertools.get_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")

        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , action="episodios" , show = item.title , folder=True) )

    # Calculates next page URL from actual URL
    start_index = int( scrapertools.get_match( item.url ,"start-index=(\d+)") )
    max_results = int( scrapertools.get_match( item.url ,"max-results=(\d+)") )
    next_page_url = item.url.replace("start-index="+str(start_index),"start-index="+str(start_index+max_results))

    itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , url=next_page_url, action="programas" , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[cyltv.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    
    patron = "<entry(.*?)</entry>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for entry in matches:
        logger.info("entry="+entry)
        
        title = scrapertools.get_match(entry,"<titl[^>]+>([^<]+)</title>")
        try:
            plot = scrapertools.get_match(entry,"<media\:desc[^>]+>([^<]+)")
        except:
            plot = ""
        thumbnail = scrapertools.get_match(entry,"<media\:thumbnail url='([^']+)'")
        url = scrapertools.get_match(entry,"(http\://www.youtube.com/watch\?v\=[0-9A-Za-z_-]{11})")

        # Appends a new item to the xbmc item list
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , action="play" , server="youtube", show = item.title , folder=False) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    items_programas = mainlist(Item())
    if len(items_programas)==0:
        return False

    items_episodios = episodios(items_programas[0])
    if len(items_episodios)==0:
        return False

    return bien