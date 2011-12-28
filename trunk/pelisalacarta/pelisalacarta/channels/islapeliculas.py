# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para islapeliculas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "islapeliculas"
__category__ = "F"
__type__ = "generic"
__title__ = "IslaPel�culas"
__language__ = "ES"
__creationdate__ = "20110509"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[islapeliculas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="novedades", url="http://www.islapeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Listado por Categor�as", action="cat", url="http://www.islapeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Estrenos" , action="estrenos", url="http://www.islapeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Buscar por Pel�cula", action="search", url = "http://www.islapeliculas.com/buscar-pelicula-%s") )
    itemlist.append( Item(channel=__channel__, title="Buscar por Actor", action="search", url = "http://www.islapeliculas.com/actor-%s") )

    return itemlist

def search(item,texto):
    logger.info("[islapeliculas.py] busqueda")
    
    if item.url=="":
        item.url = "http://www.islapeliculas.com/buscar-pelicula-%s"
    
    item.url = item.url % texto
    return novedades(item)

def novedades(item):
    logger.info("[islapeliculas.py] novedades")

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = '<div class="content">(.*?)</table>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for elemento in matches:
        patronvideos = '.*?<h2 ><a.*?title="([^"]+)".*?href="([^"]+)".*?></a></h2>'
        patronvideos += '.*?<img src="([^"]+)".*?/>'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin(item.url,match[1])
            scrapedtitle = match[0]
            scrapedthumbnail = match[2]
            scrapedplot = ""
            logger.info(scrapedtitle)

            # A�ade al listado
            itemlist.append( Item(channel=__channel__, action="listapelis", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
              
    # Extrae la marca de siguiente p�gina
    patronvideos = '<td width="69">.*?<table.*?<a href="([^"]+)".*?>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P�gina siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        itemlist.append( Item( channel=__channel__ , title=scrapedtitle , action="novedades" , url=scrapedurl , thumbnail=scrapedthumbnail, folder=True ) )

    return itemlist

    
def listapelis(item):
    logger.info("[islapeliculas.py] listapelis")

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas

    itemlist = []
    patronvideos = '<span class="estilo16"><a.*?href="([^"]+)".*?>.*?Pelicula (.*?)<strong>(.*?)</strong></a>'
    patronvideos += '.*?<img.*?>.*?<img.*?>.*?<strong>(.*?)</strong>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        if match[3]!="fileserve":
            scrapedurl = urlparse.urljoin("http://www.islapeliculas.com/",match[0])
            scrapedtitle = match[1] + match[2] + " - " + match[3]
            scrapedthumbnail = item.thumbnail
            logger.info(scrapedtitle)

            # A�ade al listado
            itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )
            
    return itemlist
            
            
def videos(item):

    logger.info("[islapeliculas.py] videos")
    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    title= item.title
    scrapedthumbnail = item.thumbnail
    listavideos = servertools.findvideos(data)

    itemlist = []
    for video in listavideos:
        scrapedtitle = title.strip() + " - " + video[0]
        videourl = video[1]
        server = video[2]
        #logger.info("videotitle="+urllib.quote_plus( videotitle ))
        #logger.info("plot="+urllib.quote_plus( plot ))
        #plot = ""
        #logger.info("title="+urllib.quote_plus( title ))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+videourl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=videourl , thumbnail=scrapedthumbnail , server=server , folder=False) )

    return itemlist


def cat(item):

    logger.info("[islapeliculas.py] cat")

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = 'G�nero</td>(.*?)</table>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for elemento in matches:
        patronvideos  = '.*?<h2>.*?<a href="(.*?)".*?>(.*?)</a>'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin(item.url,match[0])
            scrapedtitle = match[1]
            scrapedthumbnail = ""
            scrapedplot = ""
            logger.info(scrapedtitle)

            # A�ade al listado
            itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
        
    return itemlist
    
def estrenos(item):
    logger.info("[islapeliculas.py] estrenos")

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = 'Estrenos</td>(.*?)</table>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for elemento in matches:
        patronvideos  = '.*?<td.*?<a href="([^"]+)".*?>(.*?)</a>'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin(item.url,match[0])
            scrapedtitle = match[1]
            scrapedthumbnail = ""
            scrapedplot = ""
            logger.info(scrapedtitle)

            # A�ade al listado
            itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist
