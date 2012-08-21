# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mejortorrent
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "mejortorrent"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Mejor Torrent"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[mejortorrent.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"    , action="peliculas"   , url="http://www.mejortorrent.com/torrents-de-peliculas.html"))
    itemlist.append( Item(channel=__channel__, title="Series"       , action="series"      , url="http://www.mejortorrent.com/torrents-de-series.html"))
    itemlist.append( Item(channel=__channel__, title="Documentales" , action="documentales", url="http://www.mejortorrent.com/torrents-de-documentales.html"))

    return itemlist

def peliculas(item):
    logger.info("[mejortorrent.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<a href="(/peli-descargar-torrent[^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^<]+</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail in matches:
        title = scrapertools.get_match(scrapedurl,"/peli-descargar-torrent-\d+-(.*?)\.html")
        title = title.replace("-"," ")
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=False) )


    # Extrae el paginador
    patronvideos  = "<a href='([^']+)' class='paginar'> Siguiente >>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

def play(item):
    logger.info("[mejortorrent.py] play")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron  = "<a href='(secciones.php\?sec\=descargas[^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl in matches:
        title = item.title
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = item.thumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        torrent_data = scrapertools.cache_page(url)
        logger.info("torrent_data="+torrent_data)
        #<a href='/uploads/torrents/peliculas/los-juegos-del-hambre-brrip.torrent'>
        link = scrapertools.get_match(torrent_data,"<a href='(/uploads/torrents/peliculas/.*?\.torrent)'>")
        link = urlparse.urljoin(url,link)

        logger.info("link="+link)
        
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , url=link , thumbnail=thumbnail , plot=plot , folder=False) )

    return itemlist