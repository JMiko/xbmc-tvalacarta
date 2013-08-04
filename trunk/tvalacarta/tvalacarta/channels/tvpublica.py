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


__channel__ = "tvpublica"
__category__ = "F"
__type__ = "generic"
__title__ = "tvpublica"
__language__ = "ES"
__creationdate__ = "20130518"
__vfanart__ = ""



DEBUG = config.get_setting("debug")

def isGeneric():

    return True
def mainlist(item):
    logger.info("[tvpublica.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__, title="Listas" , action="playlists" , url="http://gdata.youtube.com/feeds/api/users/TVPublicaArgentina/playlists?v=2&alt=json&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Videos" , action="videos" , url="http://gdata.youtube.com/feeds/api/users/TVPublicaArgentina/uploads?v=2&alt=json&start-index=1&max-results=30", folder=True) )
 
    return itemlist
    
def playlists(item):

    logger.info("[tvpublica.py] playlists")

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
    logger.info("[tvpublica.py] videos")

    data = scrapertools.cachePage(item.url)

    #logger.info(data)
    import json
    videos = json.loads(data)
    if videos == None : videos = []

    itemlist = []
    for video in videos['feed']['entry']:
        scrapedtitle = video['title']['$t'].encode("utf8","ignore")
        scrapedurl = video['media$group']['media$player']['url']
        scrapedthumbnail = video['media$group']['media$thumbnail'][1]['url']
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="play", server="youtube" , url=scrapedurl, thumbnail=scrapedthumbnail, folder=False) )

    for link in videos['feed']['link']:
        if (link['rel'] == 'next'):
            scrapedurl = link['href']
            itemlist.append( Item(channel=__channel__, action="videos", title="!Página siguiente" , url=scrapedurl, folder=True) ) 

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():

    mainlist_items = mainlist(Item())
    playlists_items = playlists(mainlist_items[0])
    if len(playlists_items)==0:
        print "No hay playlists"
        return False

    items_videos = videos(playlists_items[0])
    if len(items_videos)==0:
        print "No hay videos en la primera playlist"
        return False

    return True