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
    <li><a href='#'>peliculas por genero</a>
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
    <li><a href='http://www.cine-online.eu/search/label/romance'>Romance</a></li>
    <li><a href='http://www.cine-online.eu/search/label/terror'>Terror</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Thriller'>Thriller</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Western'>Western</a></li>
    </ul>
    '''
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<li><a href='#'>peliculas por genero</a>[^<]+<ul>(.*?)</ul>" )
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
    <div class='post bar hentry'>
    <a name='2511198152059281144'></a>
    <h3 class='post-title entry-title'>
    <a href='http://www.cine-online.eu/2012/08/los-inmortales.html'>Los inmortales</a>
    </h3>
    <div class='post-header-line-1'></div>
    <div class='post-body entry-content'>
    <div id='summary2511198152059281144'><a href="http://1.bp.blogspot.com/-sVlgrMa-8NA/UB5D5mSueeI/AAAAAAAAJNo/BGREaZVHNQs/s1600/Los_inmortales-365360791-large.jpg"><img style="float:left; margin:0 10px 10px 0;cursor:pointer; cursor:hand;width: 229px; height: 320px;" src="http://1.bp.blogspot.com/-sVlgrMa-8NA/UB5D5mSueeI/AAAAAAAAJNo/BGREaZVHNQs/s320/Los_inmortales-365360791-large.jpg" border="0" alt=""id="BLOGGER_PHOTO_ID_5773126429146249698" />
    </a><br /><br />Los Inmortales son seres de una raza especial que sólo pueden morir decapitados entre sí. Viven desde hace siglos entre los hombres, pero ocultando su identidad. Unos defienden el Bien, otros, el Mal. Una maldición los obliga a luchar entre sí hasta que sólo quede uno de ellos. El escocés Connor MacLeod (Christopher Lambert) es uno de los supervivientes del clan de los Inmortales que ha llegado hasta nuestros días.<br /><iframe src="http://vk.com/video_ext.php?oid=146263567&id=163615214&hash=911afd3b1cb4b789&hd=1" width="607" height="360" frameborder="0"></iframe></div>
    '''
    patron  = "<div class='post bar hentry'>[^<]+"
    patron += "<a name='[^']+'></a>[^<]+"
    patron += "<h3 class='post-title entry-title'>[^<]+"
    patron += "<a href='([^']+)'>([^<]+)</a>[^<]+"
    patron += "</h3>.*?"
    patron += "<div id='summary[^']+'>[^<]*"
    patron += '<a[^<]+<img style="[^"]+" src="([^"]+)"[^>]+>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail,scrapedplot in matches:
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , fanart = scrapedthumbnail , plot=plot , folder=True) )

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