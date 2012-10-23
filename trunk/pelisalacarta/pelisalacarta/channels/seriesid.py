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
    itemlist.append( Item(channel=__channel__, title="En Emisión", action="series"   , url="http://seriesid.com/series-en-emision/", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg"))
    itemlist.append( Item(channel=__channel__, title="Todas"     , action="menucompleto"   , url="http://seriesid.com/", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"    , action="search", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )
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
        itemlist.extend(series(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def menucompleto(item):
    logger.info("[seriesid.py] menucompleto")
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
        itemlist.append( Item(channel=__channel__, action="scrappingTemp", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle, fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )

    return itemlist

def series(item,paginacion=True):
    logger.info("[seriesid.py] series")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    '''
    <!--ITEM-->
    <div class="item">
    <div class="item-title">
    <h1><a title="Alcatraz 1ra Temporada" href="http://seriesid.com/alcatraz-1ra-temporada/">Alcatraz 1ra Temporada</a></h1>
    </div>
    <div class="item-contenido">
    <div class="caratula" style="background:url(http://seriesid.com/series/alcatraz1.jpg);">
    <a title="Ver Serie Alcatraz 1ra Temporada" href="http://seriesid.com/alcatraz-1ra-temporada/"><span></span></a>
    </div>
    <p>Alcatraz es una Serie de 12 episodios que cuenta la misteriosa historia de la prisión mas famosa del mundo “Alcatraz” narra las
    investigaciones de Rebecca Madsen, un agente de policía, y de Dr. Diego Soto, un "hippie geek" que es el mayor experto del
    mundo en Alcatraz. Ambos investigan la reaparición de guardias y presos de Alcatraz en la actualidad, después de su misteriosa
    desaparición hace cincuenta años. Producida por J.J. Abrams (Si, uno de los productores de “Lost").  
    
    
    Lista de Episodios
    Alcatraz 1ra Temporada - Episodio 1
    Alcatraz 1ra Temporada - Episodio 2
    Alcatraz 1ra Temporada - Episodio 3
    Alcatraz 1ra Temporada - ...</p>
    </div>
    <div class="item-footer"></div>
    </div>
    <!--ITEM-->
    '''
    patron  = 'div class="item"[^<]+'
    patron += '<div class="item-title"[^<]+'
    patron += '<h1><a title="([^"]+)" href="([^"]+)">[^>]+</a></h1[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="item-contenido"[^<]+'
    patron += '<div class="caratula" style="background:url\(([^\)]+)\);">[^<]+'
    patron += '<a[^<]+<span[^<]+</span[^<]+</a[^<]+'
    patron += '</div[^<]+'
    patron += '<p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[0]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = match[3]
        scrapedurl = match[1]
        scrapedthumbnail = match[2]
        if "temporada" in scrapedurl:
            action = "scrappingTemp"
        else:
            action = "findvideos"
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action=action, title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie_with_plot", extra=scrapedtitle, fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )

    return itemlist

def scrappingTemp(item,paginacion=True):
    logger.info("[seriesid.py] scrappingTemp")
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
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle, fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguna de las series "En emisión" devuelve mirrors
    series_items = series(mainlist_items[0])
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