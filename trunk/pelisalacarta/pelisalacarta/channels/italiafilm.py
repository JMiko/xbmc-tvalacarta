# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para italiafilm
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "italiafilm"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "Italia film (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")
EVIDENCE = "   "

def isGeneric():
    return True

def mainlist(item):
    logger.info("[gnula.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novità" , action="peliculas", url="http://italia-film.com/"))
    itemlist.append( Item(channel=__channel__, title="Categorie" , action="categorias", url="http://italia-film.com/"))
    itemlist.append( Item(channel=__channel__, title="Cerca Film", action="search"))
    return itemlist

def categorias(item):
    logger.info("[italiafilm.py] categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<h2>Categorie Film</h2>(.*?)</div>")
    patron = '<li class="[^"]+"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedplot = ""
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[italiafilm.py] search "+texto)
    itemlist = []
    texto = texto.replace(" ","%20")
    item.url = "http://italia-film.com/index"
    item.extra = "do=search&subaction=search&story="+texto+"&x=0&y=0"

    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []


def peliculas(item):
    logger.info("[italiafilm.py] peliculas")
    itemlist = []

    # Descarga la página
    if item.extra!="":
        post = item.extra
    else:
        post=None
    data = scrapertools.cachePage(item.url,post)

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="([^"]+)"><img class="news-item-image" title="([^"]+)" alt="[^"]+" src="([^"]+)"></a>[^<]+'
    patronvideos += '<span class="shortstoryintro">[^<]+'
    patronvideos += '<div id="news[^>]+>([^<]+)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for url,title,thumbnail,plot in matches:
        # Atributos
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = plot
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="([^"]+)"><span class="thide pnext">Avanti</span></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedtitle = ">> Pagina seguente"
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def to_ita(text):
    text = text.replace('&amp;', '&')
    text = text.replace('&#224;', 'a\'')
    text = text.replace('&#232;', 'e\'')
    text = text.replace('&#233;', 'e\'')
    text = text.replace('&#236;', 'i\'')
    text = text.replace('&#242;', 'o\'')
    text = text.replace('&#249;', 'u\'')
    text = text.replace('&#215;', 'x')
    text = text.replace('&#039;', '\'')
    return text

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