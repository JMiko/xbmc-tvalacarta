# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Private XML channel
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "xmlchannel"
__type__ = "generic"
__title__ = "XML Channel"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.xmlchannels.mainlist")

    return lista(item)

def lista(item):
    logger.info("mywebtv.channels.xmlchannels.lista")

    itemlist = []

    # Si es una URL la descarga
    if item.url.startswith("http://") or item.url.startswith("https://"):
        data = scrapertools.cache_page(item.url)

    # Si es un fichero local, lo abre
    else:
        infile = open( item.url )
        data = infile.read()
        infile.close()

    # Extrae los paises
    patron  = '<channel>[^<]+'
    patron += '<name>([^<]+)</name>.*?'
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
    logger.info("mywebtv.channels.xmlchannels.videos")
    itemlist = []

    # Descarga la página
    channel_id = item.url.split("|#|")[0]
    item.url = item.url.split("|#|")[1]

    # Si es una URL la descarga
    if item.url.startswith("http://") or item.url.startswith("https://"):
        data = scrapertools.cache_page(item.url)

    # Si es un fichero local, lo abre
    else:
        infile = open( item.url )
        data = infile.read()
        infile.close()
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
