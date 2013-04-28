# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Justin.tv
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "justintv"
__type__ = "generic"
__title__ = "Justin.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")
LANGUAGES_URL = "http://www.justin.tv/directory/dropmenu/language/all?order=hot&amp;lang=es"
CATEGORIES_URL = "http://www.justin.tv/directory/dropmenu/category/featured?lang=%s"
CHANNELS_URL = "http://www.justin.tv/directory/%s?lang=%s"

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.justintv.mainlist")
    itemlist = []

    data = scrapertools.cachePage(LANGUAGES_URL)
    patron = '<li class="language_filter"[^<]+<a href="([^"]+)"><span>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(LANGUAGES_URL,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item( channel=__channel__ , action="categories" , title=title , url=url))

    return itemlist

def categories(item):
    logger.info("[justintv.py] mainlist")
    itemlist = []

    language = scrapertools.get_match(item.url,"lang=([a-z]+)")

    data = scrapertools.cachePage(CATEGORIES_URL % language)
    patron = '<li class="category"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist.append( Item( channel=__channel__ , action="channels" , title="Featured" , url="http://www.justin.tv/directory/featured?lang="+language))

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        thumbnail = ""
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item( channel=__channel__ , action="channels" , title=title , url=url, thumbnail=thumbnail, plot=plot))

    return itemlist

def channels(item):
    logger.info("[justintv.py] mainlist")
    itemlist = []

    try:
        actualpage = scrapertools.get_match(item.url,"page\=(\d+)")
        next_page_url = item.url.replace("page="+actualpage,"page="+str(int(actualpage)+1))
        logger.info("[justintv.py] next_page_url="+next_page_url)
    except:
        actualpage = "1"
        next_page_url = item.url+"&page=2"
        logger.info("[justintv.py] next_page_url="+next_page_url)

    data = scrapertools.cachePage(item.url)
    patron  = '<li id="channel[^<]+<div[^<]+'
    patron += '<a class="thumb" href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '<a[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        thumbnail = scrapedthumbnail
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item( channel=__channel__ , action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, server="justintv", folder=False))

    itemlist.append( Item( channel=__channel__ , action="channels" , title=title , url=">> Página siguiente", thumbnail=thumbnail, plot=plot))

    return itemlist
