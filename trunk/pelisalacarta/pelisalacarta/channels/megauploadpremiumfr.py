# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para megauploadpremiumfr
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "megauploadpremiumfr"
__category__ = "S"
__type__ = "generic"
__title__ = "Megaupload Premium (FR)"
__language__ = "FR"
__creationdate__ = "20111014"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[megauploadpremiumfr.py] mainlist")
    
    itemlist=[]
    itemlist.append( Item(channel=__channel__, title="TV Shows - Full listing"   , action="completo" , url="http://www.megaupload-premium.com/toutes-les-series/"))

    return itemlist

def completo(item):
    logger.info("[megauploadpremiumfr.py] completo")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="azindex">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)==0:
        return itemlist
    
    data = matches[0]
    patron = '<li[^>]*><a href="([^"]+)"><span class="head">([^<]+)</span></a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist
