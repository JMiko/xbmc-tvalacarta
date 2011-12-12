# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para serieshentai
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "serieshentai"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[serieshentai.py] mainlist")

    item.url="http://series-hentai.net/hentai-online"
    return series(item)

def series(item):
    logger.info("[serieshentai.py] series")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<td class="tijav"  ><a href="([^"]+)">([^<]+)</a></td>[^<]+<td> xxx </td>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        itemlist.append( Item( channel=item.channel, action="findvideos", title=scrapedtitle, url=scrapedurl, folder=True))

    return itemlist