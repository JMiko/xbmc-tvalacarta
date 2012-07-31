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

__channel__ = "shurweb"
__category__ = "F,S,D,A"
__type__ = "generic"
__title__ = "Shurweb"
__language__ = "ES"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True

def mainlist(item):
    logger.info("[shurweb.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"                , action="scrapping"   , url="http://www.shurweb.es/"))
    itemlist.append( Item(channel=__channel__, title="Peliculas"                , action="menupeliculas"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="series"  , url="http://www.shurweb.es/series/"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="scrapping"   , url="http://www.shurweb.es/videoscategory/documentales/"))
    itemlist.append( Item(channel=__channel__, title="Anime"                    , action="scrappingS"  , url="http://www.shurweb.es/anime/"))
#    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    return itemlist

def menupeliculas(item):
    logger.info("[shurweb.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - A-Z"              , action="menupelisaz"))
    itemlist.append( Item(channel=__channel__, title="Películas - Decadas"          , action="menupelisanos"))
    itemlist.append( Item(channel=__channel__, title="Películas - Animación"        , action="scrapping"   , url="http://www.shurweb.es/videoscategory/animacion/") )
    return itemlist

def menupelisaz(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="A"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/a/"))
    itemlist.append( Item(channel=__channel__, title="B"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/b/"))
    itemlist.append( Item(channel=__channel__, title="C"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/c/"))
    itemlist.append( Item(channel=__channel__, title="D"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/d/"))
    itemlist.append( Item(channel=__channel__, title="E"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/e/"))
    itemlist.append( Item(channel=__channel__, title="F"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/f/"))
    itemlist.append( Item(channel=__channel__, title="G"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/g/"))
    itemlist.append( Item(channel=__channel__, title="H"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/h/"))
    itemlist.append( Item(channel=__channel__, title="I"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/i/"))
    itemlist.append( Item(channel=__channel__, title="J"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/j/"))
    itemlist.append( Item(channel=__channel__, title="K"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/k/"))
    itemlist.append( Item(channel=__channel__, title="L"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/l/"))
    itemlist.append( Item(channel=__channel__, title="M"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/m/"))
    itemlist.append( Item(channel=__channel__, title="N"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/n/"))
    itemlist.append( Item(channel=__channel__, title="O"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/o/"))
    itemlist.append( Item(channel=__channel__, title="P"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/p/"))
    itemlist.append( Item(channel=__channel__, title="Q"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/q/"))
    itemlist.append( Item(channel=__channel__, title="R"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/r/"))
    itemlist.append( Item(channel=__channel__, title="S"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/s/"))
    itemlist.append( Item(channel=__channel__, title="T"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/t/"))
    itemlist.append( Item(channel=__channel__, title="U"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/u/"))
    itemlist.append( Item(channel=__channel__, title="V"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/v/"))
    itemlist.append( Item(channel=__channel__, title="W"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/w/"))
    itemlist.append( Item(channel=__channel__, title="X"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/x/"))
    itemlist.append( Item(channel=__channel__, title="Y"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/y/"))
    itemlist.append( Item(channel=__channel__, title="Z"        , action="scrapping"   , url="http://www.shurweb.es/lista-de-peliculas/z/"))
    return itemlist

def menupelisanos(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="10's"        , action="scrapping"   , url="http://www.shurweb.es/peliculas/10s/"))
    itemlist.append( Item(channel=__channel__, title="00's"        , action="scrapping"   , url="http://www.shurweb.es/peliculas/00s/"))
    itemlist.append( Item(channel=__channel__, title="90's"        , action="scrapping"   , url="http://www.shurweb.es/peliculas/90s/"))
    itemlist.append( Item(channel=__channel__, title="80's"        , action="scrapping"   , url="http://www.shurweb.es/peliculas/80s/"))
    itemlist.append( Item(channel=__channel__, title="70's"        , action="scrapping"   , url="http://www.shurweb.es/peliculas/70s/"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[shurweb.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.shurweb.es/?s=%s"
        item.url = item.url % texto
        itemlist.extend(scrappingSearch(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def scrappingSearch(item,paginacion=True):
    logger.info("[shurweb.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" style="display:none;" rel="nofollow"><img src="([^"]+)" width="100" height="144" border="0" alt="" /><br/><br/>[^<]+<b>([^<]+)</b></a>[^<]+<a href="([^"]+)">([^#]+)#888"><b>([^<]+)</b>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        if match[5] == 'Peliculas' or match[5] == 'Series':
            scrapedtitle =  match[2]
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            scrapedplot = ""
            scrapedurl = match[3]
            scrapedthumbnail = match[1]
            if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    return itemlist

def series(item,paginacion=True):
    logger.info("[shurweb.py] series")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    '''
    <li class="clearfix">
    <a class="video_thumb" href="http://www.shurweb.es/serie/anatomia-de-grey/" rel="bookmark" title="Anatomía de Grey">
    <img width="123" height="100" src="http://www.shurweb.es/wp-content/uploads/2012/02/Greys-Anatomy4.jpg" class="wp-post-image">             
    </a>
    <p class="title"><a href="http://www.shurweb.es/serie/anatomia-de-grey/" rel="bookmark" title="Anatomía de Grey">Anatomía de Grey</a></p>
    </li>
    '''
    patron  = '<li class="clearfix">[^<]+'
    patron += '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)">[^<]+'
    patron += '<img width="[^"]+" height="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,title,thumbnail in matches:
        scrapedtitle = title.replace("&amp;","&")
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = url
        scrapedthumbnail = thumbnail
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='episodios', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , show=scrapedtitle, context="4|5") )
    return itemlist

def episodios(item):
    logger.info("[shurweb.py] episodios")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    '''
    <li>
    <div class="video">
    <a class="video_title" href="http://www.shurweb.es/videos/alcatraz-1x10/">Alcatraz 1x10</a>
    </div>
    </li>
    '''
    patron  = '<li>[^<]+'
    patron += '<div class="video">[^<]+'
    patron += '<a class="video_title" href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,title in matches:
        scrapedtitle = title
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = url
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , show=item.show, context="4|5") )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def scrapping(item,paginacion=True):
    logger.info("[shurweb.py] scrapping")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)">[^<]+<img width="123" height="100" src="([^"]+)" class=" wp-post-image" alt="[^"]+"  />[^<]+<span class="time">([^<]+)</span>[^<]+</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[1] + " (" + match[3] +")"
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    peliculas_items = scrapping(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien