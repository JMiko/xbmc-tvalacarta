# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Shurweb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools


__channel__ = "seriesid"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriesid"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesid.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="En Emisión"            , action="scrapping"   , url="http://seriesid.com/series-en-emision/"))
    itemlist.append( Item(channel=__channel__, title="Todas"                  , action="menucompleto"   , url="http://seriesid.com/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[seriesid.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://seriesid.com/?s=%s"
        item.url = item.url % texto
        itemlist.extend(scrapping(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def menucompleto(item):
    logger.info("[seriesid.py] scrapping")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    patron = 'Lista Completa de Series(.+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    patronvideos = '<li><a href="([^"]+)" title="[^"]+">([^<]+)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[1]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = match[0]
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="scrappingTemp", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    return itemlist

def scrapping(item,paginacion=True):
    logger.info("[seriesid.py] scrapping")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = 'div class="item">[^>]+<div class="item-title">[^>]+<h1><a title="([^"]+)" href="([^"]+)">[^>]+</a></h1>[^>]+</div>[^>]+<div class="item-contenido">[^>]+<div class="caratula" style="background:url\(([^\)]+)\);">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[0]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = match[1]
        scrapedthumbnail = match[2]
        if "temporada" in scrapedurl:
            action = "scrappingTemp"
        else:
            action = "findvideos"
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action=action, title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    return itemlist

def scrappingTemp(item,paginacion=True):
    logger.info("[seriesid.py] scrapping")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    patronimg = '<div class="caratula-ep" style="background:url\(([^\)]+)\);">'
    matches = re.compile(patronimg,re.DOTALL).findall(data)
    scrapedthumbnail = matches[0]
    # Extrae las entradas
    patronvideos = '<a title="Ver[^"]+" href="([^"]+)" target="_blank">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[1]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = match[0]
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguna de las series "En emisión" devuelve mirrors
    series_items = scrapping(mainlist_items[0])
    bien = False
    
    for serie_item in series_items:
        if serie_item.action=="scrappingTemp":
            episodios_items = scrappingTemp(serie_item)
            for episodio_item in episodios_items:
                mirrors = servertools.find_video_items( item=episodio_item )
                if len(mirrors)>0:
                    return True
        else:
            mirrors = servertools.find_video_items( item=serie_item )
            if len(mirrors)>0:
                return True

    return False