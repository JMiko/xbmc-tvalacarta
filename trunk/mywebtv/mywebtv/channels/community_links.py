# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal community-links
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "community_links"
__type__ = "generic"
__title__ = "Community-Links"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.community_links.mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="theStreamDB", url="https://community-links.googlecode.com/svn/trunk/theStreamDB.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="theStreamDB.for.Apple.TV", url="https://community-links.googlecode.com/svn/trunk/theStreamDB.for.Apple.TV.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="hamradio", url="https://community-links.googlecode.com/svn/trunk/hamradio.TV.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="divingmulesStreams", url="https://community-links.googlecode.com/svn/trunk/divingmulesStreams.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="arabic", url="https://community-links.googlecode.com/svn/trunk/arabic.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="SidhuTV", url="https://community-links.googlecode.com/svn/trunk/SidhuTV.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="Radio", url="https://community-links.googlecode.com/svn/trunk/Radio.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="Live-CAMs", url="https://community-links.googlecode.com/svn/trunk/Live-CAMs.xml",action="lista"))
    itemlist.append( Item(channel=__channel__, title="AxisCCTV", url="https://community-links.googlecode.com/svn/trunk/AxisCCTV.xml",action="lista"))
    return itemlist

def lista(item):
    logger.info("mywebtv.channels.community_links.lista")

    itemlist = []
    data = scrapertools.cachePage(item.url)

    # Extrae los paises
    patron  = '<channel>[^<]+'
    patron += '<name>([^<]+)</name>[^<]+'
    patron += '<thumbnail>([^<]+)</thumbnail>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for name,thumbnail in matches:
        scrapedtitle = name
        scrapedurl = name+"|#|"+item.url
        scrapedthumbnail = thumbnail
        if scrapedthumbnail=="none":
            scrapedthumbnail=""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl,thumbnail=scrapedthumbnail,action="videos"))

    return itemlist

def videos(item):
    logger.info("mywebtv.channels.community_links.videos")
    itemlist = []

    # Descarga la página
    channel_id = item.url.split("|#|")[0]
    item.url = item.url.split("|#|")[1]
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las cadenas
    patron  = '<channel>[^<]+'
    patron += '<name>'+channel_id.replace("\\","\\\\")+'</name>(.*?)</channel'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        data = matches[0]

        patron  = '<title>([^<]+)</title>.*?'
        patron += '<link>([^<]+)</link>.*?'
        patron += '<thumbnail>([^<]+)</thumbnail>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        for match in matches:
            scrapedtitle = match[0]
            scrapedurl = match[1]
            scrapedthumbnail = match[2]
            scrapedplot = scrapedurl
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl,thumbnail=scrapedthumbnail,plot=scrapedplot,action="play", folder=False))

    return itemlist
