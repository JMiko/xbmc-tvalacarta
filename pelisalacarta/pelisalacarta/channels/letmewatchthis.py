# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para letmewatchthis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "letmewatchthis"
__category__ = "F,S"
__type__ = "generic"
__title__ = "LetMeWatchThis"
__language__ = "EN"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[letmewatchthis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Movies"   ,url="http://www.letmewatchthis.com/watch-movies"))
    itemlist.append( Item(channel=__channel__, action="series"    , title="TV Shows" ,url="http://www.letmewatchthis.com/watch-tv-shows"))
    #itemlist.append( Item(channel=__channel__, action=""search"     , category , "Buscar"                           ,"","","")

    return itemlist

def peliculas(item):
    logger.info("[letmewatchthis.py] peliculas")

    return listaconcaratulas(item,"listmirrors")

def series(item):
    logger.info("[letmewatchthis.py] peliculas")

    return listaconcaratulas(item,"listepisodes")

def listaconcaratulas(item,action):

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    '''
    <div class="index_item index_item_ie">
    <a href="http://www.watchfreemovies.ch/watch-movies/2011/watch-fathers-day-222717/" title="Watch Father's Day (2011)"><img src="http://static.watchfreemovies.ch/thumbs/fathers-day-222717.jpg" border="0" width="150" height="225" alt="Watch Father's Day"><h2>Father's Day (2011)</h2></a>
    '''
    patronvideos  = '<div class="index_item index_item_ie">[^<]+<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[1]
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action=action, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" rel="last">\&gt\;\&gt\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="!Next page >>" , url=scrapedurl , folder=True) )
    
    return itemlist

def listepisodes(item):
    logger.info("[letmewatchthis.py] listepisodes")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''
    <div class="tv_episode_item">
    <a href="http://www.watchfreemovies.ch/watch-tv-shows/2007/watch-gossip-girl-13842/season-1/episode-8/" title="Watch Gossip Girl Season 1 Episode 8 - Seventeen Candles for FREE">Episode 8
    <span class="tv_episode_name"> - Seventeen Candles</span>
    </a>
    '''
    patronvideos  = '<div class="tv_episode_item">[^<]+<a href="([^"]+)" title="([^"]+)'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="listmirrors", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def listmirrors(item):
    logger.info("[letmewatchthis.py] listmirrors")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''
    <tr>
    <td align="center" width="40" valign="middle"><span class=quality_dvd></span></td>
    <td align="left" valign="middle">
    <span class="movie_version_link"><a href="/external.html?url=aHR0cDovL3d3dy5oZHBsYXkub3JnL3hHeWx6OA==" onClick="return addHit('1647242', '1')" rel="noindex, nofollow" title="Watch Version 2 of The Lie" target="_blank"><span style="font-size:9px">Watch <u>The Lie</u> Online</span> | Version 2</a></span>
    </td>
    <td align="center" width="115" valign="middle">
    <span class="version_host">
    <script type="text/javascript">document.writeln('hdplay.org');</script>
    '''

    patronvideos  = '<a href="(/external[^"]+)" rel="noindex, nofollow" title="([^"]+)".*?'
    patronvideos += '<span class="version_host">(.*?)</span>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Servidor
        servidor = match[2].strip()
        # Titulo
        scrapedtitle = scrapertools.htmlclean(match[1])+" ("+servidor+")"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

    return itemlist

def play(item):
    logger.info("[letmewatchthis.py] play")
    
    itemlist=[]
    
    location = scrapertools.get_header_from_response(url=item.url, header_to_get="location")
    if location!="":
        itemlist = servertools.find_video_items(data=location)
    
    return itemlist