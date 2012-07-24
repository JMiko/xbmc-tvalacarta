# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cineonlineeu
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cineonlineeu"
__category__ = "F"
__type__ = "generic"
__title__ = "cineonlineeu"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cineonlineeu.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas"         , title="Novedades"    , url="http://www.cine-online.eu/" ))
    itemlist.append( Item(channel=__channel__ , action="generos"         , title="Por categorías"    , url="http://www.cine-online.eu/" ))

    return itemlist

def generos(item):
    logger.info("[cineonlineeu.py] mainlist")
    itemlist = []

    '''
    <span>Generos</span>Peliculas por generos</a>
    <ul>
    <li><a href='http://www.cine-online.eu/search/label/accion'>Acción</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Animaci%C3%B3n'>Animacion</a></li>
    <li><a href='http://www.cine-online.eu/search/label/aventuras'>Aventuras</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Belica'>Belica</a></li>
    <li><a href='http://www.cine-online.eu/search/label/ficcion'>Ficcion</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Comedia'>Comedia</a></li>
    <li><a href='http://www.cine-online.eu/search/label/cine%20espa%C3%B1ol'>Cine Español</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Documental'>Documental</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Drama'>Drama</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Fantastico'>Fantastico</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Infantil'>Infantil</a></li>
    <li><a href='http://www.cine-online.eu/search/label/series'>Series</a></li>
    <li><a href='http://www.cine-online.eu/search/label/romance'>Romance</a></li>
    <li><a href='http://www.cine-online.eu/search/label/terror'>Terror</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Thriller'>Thriller</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Western'>Western</a></li>
    </ul>
    '''
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<span>Generos</span>Peliculas por generos</a>[^<]+<ul>(.*?)</ul>' )
    patron  = "<li><a href='([^']+)'>([^<]+)</a></li>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist


def peliculas(item):
    logger.info("[cineonlineeu.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class='post hentry'>
    <a name='5584516536626267731'></a>
    <h3 class='post-title entry-title'>
    <a href='http://www.cine-online.eu/2012/07/mechanic.html'>The Mechanic</a>
    </h3>
    <div class='post-header'>
    <div class='post-header-line-1'></div>
    </div>
    <div class='post-body entry-content' id='post-body-5584516536626267731'>
    <div id='summary5584516536626267731'>
    <a href="http://img833.imageshack.us/img833/9657/themechanic343996468lar.jpg"><img style="float:left; margin:0 10px 10px 0;cursor:pointer; cursor:hand;width: 217px; height: 320px;" src="http://img833.imageshack.us/img833/9657/themechanic343996468lar.jpg" border="0" alt="" /></a><br />Arthur Bishop (Jason Statham) es un asesino profesional de élite, con un estricto código y un talento único para eliminar limpiamente a sus víctimas. La muerte de su amigo y mentor Harry (Donald Sutherland) le obligará a replantearse sus métodos, sobre todo cuando Steve (Ben Foster), el hijo de Harry, le pida ayuda para saciar su sed de venganza. Bishop empieza a entrenar a Steve y a enseñarle sus letales técnicas, pero las mentiras y los engaños amenazan con convertir esta alianza en el mayor de sus errores. Remake del film protagonizado por Charles Bronson en 1972.<br /><br /><br /><iframe src="http://vk.com/video_ext.php?oid=162408313&id=162843006&hash=697b0f71fb4ce6fc&hd=1" width="607" height="360" frameborder="0"></iframe>
    </div>
    '''
    patron  = "<div class='post hentry'>[^<]+"
    patron += "<a name='[^']+'></a>[^<]+"
    patron += "<h3 class='post-title entry-title'>[^<]+"
    patron += "<a href='([^']+)'>([^<]+)</a>[^<]+"
    patron += "</h3>[^<]+"
    patron += "<div class='post-header'>[^<]+"
    patron += "<div class='post-header-line-1'></div>[^<]+"
    patron += "</div>[^<]+"
    patron += "<div class='post-body entry-content' id='post-body[^']+'>[^<]+"
    patron += "<div id='summary[^']+'>[^<]+"
    patron += '<a[^<]+<img style="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien