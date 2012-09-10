# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tucinecom
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tucinecom"
__category__ = "F"
__type__ = "generic"
__title__ = "tucinecom"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tucinecom.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas"         , title="Novedades"    , url="http://www.tucinecom.com/" ))
    itemlist.append( Item(channel=__channel__ , action="tags"         , title="Tags"    , url="http://www.tucinecom.com/" ))

    return itemlist

def peliculas(item):
    logger.info("[tucinecom.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <a href="http://www.tucmegavideo-2/" rel="bookmark" title="Permanent liDEEGAVIDEO">Ver Campanilla: El secreto de las hadas (Tinker Bell: Secret of the Wings (A Winter Story)) (2012) Y SIN CORTES DE MEGAVIDEO</a></h2>
    <span class="teaser_author">by <span class="author vcard fn">josemora</span></span>
    <img style="width:100px" src="http://2.bp.blogspot.com/-NEYH5ZkXNgw/UEP_FRT4KdI/AAAAAAAARWg/RHdgBeJy6YA/s200/Campanilla_El_secreto_de_las_hadas-456425049-large.jpg"><a class="teaser_comments" href="http://www.tucinecom.com/2012/09/ver-campanilla-el-secreto-de-las-hadas-tinker-bell-secret-of-the-wings-a-winter-story-2012-y-sin-cortes-de-megavideo-2/#comments" rel="nofollow"><span>0</span> comments</a>
    </div
    '''
    patron  = '<a href="([^"]+)"[^>]+>([^<]+)</a></h2>.*?'
    patron += '<img style="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )


    '''
    <a href="http://www.tucinecom.com/2011/09/ver-red-state-2011-y-sin-cortes-de-megavideo/"><img alt="Red State (2011) " border="0" src="http://www.tucinecom.com/wp-content/uploads/2011/09/Red-State-2011-movie-194x300-e1315817203816.jpg" style="cursor: pointer; height: 210px; margin: 0pt 1px 0px 0pt; width: 159px;" title="Red State (2011)   (BLURAY S) (BLURAY S720P) (DVD R) (VS) (VC) Y SIN CORTES DE MEGAVIDEO-Thriller | Religión. Cine independiente USA " /></a>
    '''
    patron  = '<a href="([^"]+)">'
    patron += '<img alt="[^"]+" border="0" src="([^"]+)" style="[^"]+" title="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def tags(item):
    logger.info("[tucinecom.py] tags")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)
    data = scrapertools.get_match(data,'<div class="st-tag-cloud">(.*?)</div>')
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    '''
    <a href="http://www.tucinecom.com/2011/09/ver-red-state-2011-y-sin-cortes-de-megavideo/"><img alt="Red State (2011) " border="0" src="http://www.tucinecom.com/wp-content/uploads/2011/09/Red-State-2011-movie-194x300-e1315817203816.jpg" style="cursor: pointer; height: 210px; margin: 0pt 1px 0px 0pt; width: 159px;" title="Red State (2011)   (BLURAY S) (BLURAY S720P) (DVD R) (VS) (VC) Y SIN CORTES DE MEGAVIDEO-Thriller | Religión. Cine independiente USA " /></a>
    '''
    patron  = '<a href="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    itemlist = servertools.find_video_items(item)

    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.title
        videoitem.title = "Ver en ["+videoitem.server+"]"
    
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