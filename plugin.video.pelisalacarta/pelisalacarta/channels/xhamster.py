# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xhamster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import scrapertools
from core import config
from core import logger
from core import xbmctools
from core.item import Item
from servers import servertools

from pelisalacarta import buscador

CHANNELNAME = "xhamster"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[yotix.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="novedades" , title="Novedades", url="http://www.xhamster.com/"))

    return itemlist

def novedades(item):
    logger.info("[xhamster.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    # seccion novedades
    '''
    <a href="/movies/496069/the_cheerleader.html" class="hRotator">
    <img src="http://st5.xhamster.com/t/069/2_496069.jpg" height="120" width="160">
    <img class="hSprite" src="http://static.xhamster.com/images/spacer.gif" sprite="http://st5.xhamster.com/t/069/s_496069.jpg" id="496069" onmouseover="hRotator.start2(this);" height="120" width="160">
    </a>
    <div class="moduleFeaturedTitle">
    <a href="/movies/496069/the_cheerleader.html">The Cheerleader</a>
    </div>
    <div class="moduleFeaturedDetails">Runtime: 35m51s<br><span style="color: Green;">
    '''

    #patronvideos  = '<p style="text-align: center;">.*?'
    patronvideos = '<a href="(/movies/[^"]+.html)"[^>]*?>[^<]*?'
    patronvideos += '<img src=\'([^\']+.xhamster.com[^\']+)\'[^>]+>[^<]*?'
    patronvideos += '<img[^<]*?>[^<]*?</a>[^<]*?'
    patronvideos += '<div[^<]*?>[^<]*?'
    patronvideos += '<a href="/movies/[^"]+.html"[^>]*?>([^<]+)</a>[^<]*?'
    patronvideos += '</div[^<]*?>[^<]*?'
    patronvideos += '<div[^<]*?>Runtime: ([^<]+)<'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Titulo
        scrapedtitle = match[2] + " [" + match[3] + "]"
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[1].replace(" ", "%20")
        scrapedplot = scrapertools.htmlclean(match[2].strip())
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<A HREF="/new/2.html">Next</A><
    patronvideos  = '<a href="(\/new\/[^\.]+\.html)"[^>]*?>Next[^<]*?<\/a>'
    matches = re.compile(patronvideos,re.DOTALL | re.IGNORECASE).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        logger.info("[xhamster.py] " + scrapedurl)
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="!Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[xhamster.py] findvideos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    #    'file': '1293721834:6LvlmejCLBs/518596_koy_kizlari_2.flv',
    patron = "'file': '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    if len(matches)>0:
        url = "http://88.208.24.132/flv2/" + matches[0]
        server="Directo"

        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title , url=url, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist
