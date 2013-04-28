# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Delicast
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "delicast"
__type__ = "generic"
__title__ = "Delicast"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.delicast.mainlist")

    itemlist = []
    # Añade al listado de XBMC
    itemlist.append( Item( channel=__channel__ , action="paises" , title="Todos los canales por paises" , url="http://es.delicast.com"))
    return itemlist

def paises(item):
    logger.info("mywebtv.channels.delicast.paises")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae los paises
    patron = '<a class=v href=([^>]+)>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl,thumbnail=scrapedthumbnail,action="videos"))

    return itemlist

def videos(item):
    logger.info("mywebtv.channels.delicast.videos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las cadenas
    patron = '<a class=s1 href="([^"]+)">([^<]+)</a></TD><TD width=100%><a class=s href="[^"]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[2]+" ("+match[1]+")"
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = scrapedurl
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl,thumbnail=scrapedthumbnail,action="play", folder=False))

    # Página siguiente
    patron = "<a class=n href='([^']+)'><U>Siguiente .raquo.</U></a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Página siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl,thumbnail=scrapedthumbnail,action="videos"))

    return itemlist

def play(item):
    logger.info("mywebtv.channels.delicast.play")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las cadenas
    try:
        item.url = scrapertools.get_match(data,'setTimeout\(.location.replace\("([^"]+)"\)')
        itemlist.append(item)
    except:
        import traceback
        logger.info(traceback.format_exc())

    return itemlist

