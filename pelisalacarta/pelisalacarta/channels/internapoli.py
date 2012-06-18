# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para internapoli
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "internapoli"
__category__ = "F"
__type__ = "generic"
__title__ = "Internapoli City (IT)"
__language__ = "IT"
__creationdate__ = "20110516"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[internapoli.py] mainlist")
    item.url = "http://www.internapoli-city.org/"
    return novedades(item)

def novedades(item):
    logger.info("[robinfilm.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class='post hentry'>
    <a name='415866315917457690'></a>
    <h3 class='post-title entry-title'>
    <a href='http://www.internapoli-city.org/2011/11/hero-wanted-megaupload-ita.html'>Hero wanted Streaming Download ITA</a>
    </h3>
    <div class='post-header-line-1'>
    <span class='post-comment-link' style='Float:right;'>
    <a class='comment-link' href='http://www.internapoli-city.org/2011/11/hero-wanted-megaupload-ita.html#comment-form' onclick='' style='background:url(http://2.bp.blogspot.com/_kMUpUqMmduA/SVU81uUMS4I/AAAAAAAAA6E/OApf_zOXfC8/s1600/icon_comments.gif) no-repeat;Padding-left:20px;'>0
    commenti</a>
    </span>
    <br/>
    <span class='post-icons'>
    </span>
    </div>
    <div class='post-body entry-content'>
    <div id='summary415866315917457690'><div class="separator" style="clear: both; text-align: center;">
    </div>
    <div class="separator" style="margin-left: 1em; margin-right: 1em; text-align: center;">
    <img border="0" height="320" src="http://4.bp.blogspot.com/-CPGx23xboJ0/Tsx-1EpLzCI/AAAAAAAAAb8/RwXcAefGqxc/s320/89.jpeg" width="217" /></div>
    <br />
    '''
    patronvideos  = "<div class='post hentry'>[^<]+"
    patronvideos += "<a name='[^']+'></a>[^<]+"
    patronvideos += "<h3 class='post-title entry-title'>[^<]+"
    patronvideos += "<a href='([^']+)'>([^<]+)</a>.*?"
    patronvideos += '<img border="[^"]+" height="[^"]+" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    #<a class='blog-pager-older-link' href='http://www.internapoli-city.org/search?updated-max=2012-05-15T23:54:00%2B02:00&amp;max-results=10' id='Blog1_blog-pager-older-link' title='Post più vecchi'><img height='38' src='http://1.bp.blogspot.com/-duUmcoXvqN8/T3uMWNT32hI/AAAAAAAAD4Q/EJ7MUmU1F90/s1600/desno.png' width='50'/></a>
    patron = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Página siguiente"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools

    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = mainlist(Item())
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien