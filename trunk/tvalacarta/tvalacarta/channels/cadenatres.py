# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# creado por rsantaella
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cadenatres"
__category__ = "F"
__type__ = "generic"
__title__ = "cadenatres"
__language__ = "ES"
__creationdate__ = "20130321"
__vfanart__ = "http://www.cadenatres.com.mx/sites/www.cadenatres.com.mx/themes/cadena2/images/back.jpg"

DEBUG = config.get_setting("debug")

def isGeneric():

    return True
def mainlist(item):
    logger.info("[cadenatres.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__, title="Noticias" , action="playlists" , url="http://gdata.youtube.com/feeds/api/users/Cadena3Noticias/playlists?v=2&alt=json&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Deportes" , action="playlists" , url="http://gdata.youtube.com/feeds/api/users/Cadena3Deportes/playlists?v=2&alt=json&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Espectaculos" , action="playlists" , url="http://gdata.youtube.com/feeds/api/users/Cadena3Espectaculos/playlists?v=2&alt=json&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Series" , action="playlists" , url="http://gdata.youtube.com/feeds/api/users/Cadena3Series/playlists?v=2&alt=json&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Vida y Hogar" , action="playlists" , url="http://gdata.youtube.com/feeds/api/users/Cadena3VidayHogar/playlists?v=2&alt=json&start-index=1&max-results=30", folder=True) )

    return itemlist

def playlists(item):

    logger.info("[cadenatres.py] playlists")

    # Obtiene el feed segun el API de YouTube
    data=scrapertools.cachePage(item.url)

    #logger.info(data)
    import json
    playlists = json.loads(data)
    if playlists == None : playlists = []

    itemlist = []
    for playlist in playlists['feed']['entry']:
        scrapedtitle = playlist['title']['$t'].encode("utf8","ignore")
        scrapedurl = playlist['content']['src'].encode("utf8","ignore") + '&alt=json'
        scrapedthumbnail = playlist['media$group']['media$thumbnail'][1]['url']
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, folder=True) )

    for link in playlists['feed']['link']:
        if (link['rel'] == 'next'):
            scrapedurl = link['href']
            itemlist.append( Item(channel=__channel__, action="playlists", title="!Página siguiente" , url=scrapedurl, folder=True) ) 

    return itemlist

def videos(item):
    logger.info("[cadenatres.py] videos")

    data = scrapertools.cachePage(item.url)

    #logger.info(data)
    import json
    videos = json.loads(data)
    if videos == None : videos = []

    itemlist = []
    for video in videos['feed']['entry']:
        try:
            scrapedtitle = video['title']['$t'].encode("utf8","ignore")
            scrapedurl = video['media$group']['media$player']['url']
            scrapedthumbnail = video['media$group']['media$thumbnail'][1]['url']
            itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="play", server="youtube" , url=scrapedurl, thumbnail=scrapedthumbnail, folder=False) )
        except:
            continue

    for link in videos['feed']['link']:
        if (link['rel'] == 'next'):
            scrapedurl = link['href']
            itemlist.append( Item(channel=__channel__, action="videos", title="!Página siguiente" , url=scrapedurl, folder=True) ) 

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():

    # Cada elemento de mainlist es un canal de Cadena 3
    mainlist_items = mainlist(Item())

    for mainlist_item in mainlist_items:

        # Si hay algún video en alguna de las listas de reproducción lo da por bueno
        playlist_items = playlists(mainlist_item)
        for playlist_item in playlist_items:
            items_videos = videos(playlist_item)
            if len(items_videos)>0:
                return True

    return False