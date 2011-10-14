# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para animeflv (por MarioXD)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "animeflv"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[animeflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="ListA" , title="Listado Alfabetico"       , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=CHANNELNAME, action="newlist"   , title="Ultimos Capitulos" , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=CHANNELNAME, action="addlist"   , title="Series Agregadas recientemente" , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=CHANNELNAME, action="airlist"   , title="En emision" , url="http://animeflv.net/" ))
  
    return itemlist

def ListA(item):
    logger.info("[animeflv.py] ListA")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="0-9", url="http://animeflv.net/letra/0-9.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="A"  , url="http://animeflv.net/letra/a.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="B"  , url="http://animeflv.net/letra/b.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="C"  , url="http://animeflv.net/letra/c.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="D"  , url="http://animeflv.net/letra/d.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="E"  , url="http://animeflv.net/letra/e.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="F"  , url="http://animeflv.net/letra/f.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="G"  , url="http://animeflv.net/letra/g.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="H"  , url="http://animeflv.net/letra/h.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="I"  , url="http://animeflv.net/letra/i.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="J"  , url="http://animeflv.net/letra/j.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="K"  , url="http://animeflv.net/letra/k.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="L"  , url="http://animeflv.net/letra/l.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="M"  , url="http://animeflv.net/letra/m.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="N"  , url="http://animeflv.net/letra/n.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="O"  , url="http://animeflv.net/letra/o.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="P"  , url="http://animeflv.net/letra/p.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="Q"  , url="http://animeflv.net/letra/q.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="R"  , url="http://animeflv.net/letra/r.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="S"  , url="http://animeflv.net/letra/s.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="T"  , url="http://animeflv.net/letra/t.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="U"  , url="http://animeflv.net/letra/u.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="V"  , url="http://animeflv.net/letra/v.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="W"  , url="http://animeflv.net/letra/w.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="X"  , url="http://animeflv.net/letra/x.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="Y"  , url="http://animeflv.net/letra/y.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="ListAlfabetico" , title="Z"  , url="http://animeflv.net/letra/z.html"))

    return itemlist


def ListAlfabetico(item):
    logger.info("[animeflv.py] ListAlfabetico")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas 
    patronvideos  = '<div class="anime_box"> <a href="([^<]+)" title="([^<]+)"><img src="([^<]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[1]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))        
    return itemlist

def newlist(item):
    logger.info("[animeflv.py] newlist")

    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  
    patronvideos  = '<div class="abso"><iframe src="([^<]+)"></iframe><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[2]
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = match[3]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def serie(item):
    logger.info("[animeflv.py] serie")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Saca el argumento
    patronvideos  = '<div class="sinop">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        scrapedplot = scrapertools.htmlclean( matches[0] )
    
    # Saca enlaces a los episodios
    patronvideos  = '<li class="lcc"><a href="([^"]+)" class="lcc">([^<]+)</a></li>'
    scrapertools.printMatches(matches)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    itemlist = []
    
    for match in matches:
        scrapedtitle = scrapertools.entityunescape( match[1] )
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        #scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show))
    
    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="serie", show=item.show) )

    return itemlist

def addlist(item):
    logger.info("[animeflv.py] serie")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas 
    patronvideos  = '<div class="cont_anime"><div class="anime_box"> <a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" '
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def airlist(item):
    logger.info("[animeid.py] airlist")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  
    patronvideos  = '<div class="caja_cont"> <h3>Animes en Emision</h3><div class="dm">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)" title="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    itemlist = []

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist
