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
import youtube_channel

__channel__ = "elgourmet"
__category__ = "F"
__type__ = "generic"
__title__ = "elgourmet"
__language__ = "ES"
__creationdate__ = "20121216"
__vfanart__ = "http://elgourmet.com/imagenes/background.jpg"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    return youtube_channel.playlists(item,"elgourmetcomLatam")

def test():
    return youtube_channel.test("elgourmetcomLatam")

'''
def mainlist(item):

    logger.info("[elgourmet.py] getplaylists")

    # Obtiene el feed segun el API de YouTube
    if item.title =="!Página siguiente":
        data=scrapertools.cachePage(item.url)
    else:
        data = scrapertools.cachePage('http://gdata.youtube.com/feeds/api/users/elgourmetcomLatam/playlists?v=2&alt=json&start-index=1&max-results=30')

    #logger.info(data)
    import json
    playlists = json.loads(data)
    if playlists == None : playlists = []

    itemlist = []
    for playlist in playlists['feed']['entry']:
        scrapedtitle = playlist['title']['$t'].encode("utf8","ignore")
        scrapedurl = playlist['content']['src'].encode("utf8","ignore") + '&alt=json'
        try:
            scrapedthumbnail = playlist['media$group']['media$thumbnail'][1]['url']
        except:
            scrapedthumbnail = ""
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="playlist" , url=scrapedurl, thumbnail=scrapedthumbnail, folder=True) )

    for link in playlists['feed']['link']:
        if (link['rel'] == 'next'):
            scrapedurl = link['href']
            itemlist.append( Item(channel=__channel__, action="mainlist", title="!Página siguiente" , url=scrapedurl, folder=True) ) 

    return itemlist

def playlist(item):
    logger.info("[elgourmet.py] playlist")

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
            itemlist.append( Item(channel=__channel__, action="playlist", title="!Página siguiente" , url=scrapedurl, folder=True) ) 

    return itemlist
'''