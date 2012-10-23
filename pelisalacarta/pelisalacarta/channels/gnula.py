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

__channel__ = "gnula"
__category__ = "F"
__type__ = "generic"
__title__ = "Gnula"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[gnula.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"            , action="peliculas", url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="A-Z"                  , action="menupelisaz"))
    itemlist.append( Item(channel=__channel__, title="Años"                  , action="menupelisanos"))
    itemlist.append( Item(channel=__channel__, title="Generos"                  , action="generos", url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    return itemlist

def generos(item):
    logger.info("[gnula.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    patron = '<a href="(genero/[^"]+)">[^<]+<span class="tit">([^<]+)</span></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,title in matches:
        scrapedtitle =  title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def menupelisaz(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="A"        , action="peliculas"   , url="http://gnula.biz/letra/a/"))
    itemlist.append( Item(channel=__channel__, title="B"        , action="peliculas"   , url="http://gnula.biz/letra/b/"))
    itemlist.append( Item(channel=__channel__, title="C"        , action="peliculas"   , url="http://gnula.biz/letra/c/"))
    itemlist.append( Item(channel=__channel__, title="D"        , action="peliculas"   , url="http://gnula.biz/letra/d/"))
    itemlist.append( Item(channel=__channel__, title="E"        , action="peliculas"   , url="http://gnula.biz/letra/e/"))
    itemlist.append( Item(channel=__channel__, title="F"        , action="peliculas"   , url="http://gnula.biz/letra/f/"))
    itemlist.append( Item(channel=__channel__, title="G"        , action="peliculas"   , url="http://gnula.biz/letra/g/"))
    itemlist.append( Item(channel=__channel__, title="H"        , action="peliculas"   , url="http://gnula.biz/letra/h/"))
    itemlist.append( Item(channel=__channel__, title="I"        , action="peliculas"   , url="http://gnula.biz/letra/i/"))
    itemlist.append( Item(channel=__channel__, title="J"        , action="peliculas"   , url="http://gnula.biz/letra/j/"))
    itemlist.append( Item(channel=__channel__, title="K"        , action="peliculas"   , url="http://gnula.biz/letra/k/"))
    itemlist.append( Item(channel=__channel__, title="L"        , action="peliculas"   , url="http://gnula.biz/letra/l/"))
    itemlist.append( Item(channel=__channel__, title="M"        , action="peliculas"   , url="http://gnula.biz/letra/m/"))
    itemlist.append( Item(channel=__channel__, title="N"        , action="peliculas"   , url="http://gnula.biz/letra/n/"))
    itemlist.append( Item(channel=__channel__, title="O"        , action="peliculas"   , url="http://gnula.biz/letra/o/"))
    itemlist.append( Item(channel=__channel__, title="P"        , action="peliculas"   , url="http://gnula.biz/letra/p/"))
    itemlist.append( Item(channel=__channel__, title="Q"        , action="peliculas"   , url="http://gnula.biz/letra/q/"))
    itemlist.append( Item(channel=__channel__, title="R"        , action="peliculas"   , url="http://gnula.biz/letra/r/"))
    itemlist.append( Item(channel=__channel__, title="S"        , action="peliculas"   , url="http://gnula.biz/letra/s/"))
    itemlist.append( Item(channel=__channel__, title="T"        , action="peliculas"   , url="http://gnula.biz/letra/t/"))
    itemlist.append( Item(channel=__channel__, title="U"        , action="peliculas"   , url="http://gnula.biz/letra/u/"))
    itemlist.append( Item(channel=__channel__, title="V"        , action="peliculas"   , url="http://gnula.biz/letra/v/"))
    itemlist.append( Item(channel=__channel__, title="W"        , action="peliculas"   , url="http://gnula.biz/letra/w/"))
    itemlist.append( Item(channel=__channel__, title="X"        , action="peliculas"   , url="http://gnula.biz/letra/x/"))
    itemlist.append( Item(channel=__channel__, title="Y"        , action="peliculas"   , url="http://gnula.biz/letra/y/"))
    itemlist.append( Item(channel=__channel__, title="Z"        , action="peliculas"   , url="http://gnula.biz/letra/z/"))
    return itemlist

def menupelisanos(item):
    itemlist = []

    for anyo in range(2012,1921,-1):
        itemlist.append( Item(channel=__channel__, title=str(anyo), action="peliculas" , url="http://gnula.biz/ano/"+str(anyo)+"/") )

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[gnula.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://gnula.biz/buscar.php?q=%s"
        item.url = item.url % texto
        itemlist.extend(peliculas(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item,paginacion=True):
    logger.info("[gnula.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    patron  = '<span>[^<]+'
    patron += '<div[^<]+'
    patron += '<a href="([^"]+)"><img class="[^"]+" title="([^"]+)" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,title,thumbnail in matches:
        scrapedtitle =  title
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = thumbnail
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", extra=scrapedtitle) )

    patron = "<span \"\">[^<]+</span><a href='([^']+)'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action='peliculas', title=">> Página siguiente" , url=urlparse.urljoin(item.url,match)) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien