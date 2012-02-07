# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasflv"
__category__ = "F"
__type__ = "generic"
__title__ = "PeliculasFLV"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"    , action="listado", url="http://www.peliculas-flv.com/"))
    itemlist.append( Item(channel=__channel__, title="Por tags"     , action="tags", url="http://www.peliculas-flv.com/"))
    
    return itemlist

def listado(item):
    logger.info("[peliculasflv.py] listado")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron = '<div class="item"[^<]+<div[^<]+<img src="([^"]+)" alt="([^"]+)".*?<a href="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedthumbnail,scrapedtitle,scrapedurl in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a href='([^']+)'>\&raquo\;</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="listado", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

def tags(item):
    logger.info("[peliculasflv.py] tags")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron = "<a dir='ltr' href='([^']+)'>([^<]+)</a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="listado", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist
