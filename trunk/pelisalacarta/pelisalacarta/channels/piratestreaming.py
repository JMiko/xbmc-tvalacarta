# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "piratestreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "piratestreaming"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[piratestreaming.py] mainlist")
    itemlist = []

    '''
    <a href="#">Film</a> 
    <ul> 
    <li><a href="http://www.piratestreaming.com/film-aggiornamenti.php">AGGIORNAMENTI</a></li> 
    <li><a href="http://www.web-streaming-mania.net/" target=_blank><strong><font color="red">&#171;FILM PORNO&#187;</font></a></strong></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/animazione.html">ANIMAZIONE</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/avventura.html">AVVENTURA</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/azione.html">AZIONE</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/biografico.html">BIOGRAFICO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/comico.html">COMICO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/commedia.html">COMMEDIA</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/documentario.html">DOCUMENTARIO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/drammatico.html">DRAMMATICO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/erotico.html">EROTICO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/fantascienza.html">FANTASCIENZA</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/fantasy.html">FANTASY</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/giallo.html">GIALLO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/grottesco.html">GROTTESCO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/guerra.html">GUERRA</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/horror.html">HORROR</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/musical.html">MUSICAL</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/poliziesco.html">POLIZIESCO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/romantico.html">ROMANTICO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/romanzo.html">ROMANZO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/sentimentale.html">SENTIMENTALE</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/storico.html">STORICO</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/thriller.html">THRILLER</a></li> 
    <li><a href="http://www.piratestreaming.com/categoria/film/western.html">WESTERN</a></li> 
    </ul>
    '''
    item.url = "http://www.piratestreaming.com/"
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<a href="#">Film</a>[^<]+<ul>(.*?)</ul>' )
    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("[piratestreaming.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class="featuredItem"> <a href=http://www.imagerip.net/images/ilregnodig.jpg class="featuredImg img" rel="featured"><img src=http://www.imagerip.net/images/ilregnodig.jpg alt="featured item" style="width: 80.8px; height: 109.6px;" /></a>
    <div class="featuredText">
    <b><a href=http://www.piratestreaming.com/film/il-regno-di-gia-la-leggenda-dei-guardiani-streaming-ita.html>Il Regno di Ga' Hoole La leggenda dei guardiani  Ita </a></b> <br /><g:plusone size="small" href=http://www.piratestreaming.com/film/il-regno-di-gia-la-leggenda-dei-guardiani-streaming-ita.html></g:plusone>
    <div id="fb-root"></div><fb:like href="http://www.piratestreaming.com/film/il-regno-di-gia-la-leggenda-dei-guardiani-streaming-ita.html" send="false" layout="button_count" show_faces="false" action="like" colorscheme="dark" font=""></fb:like>    </b>      
    </div>
    </div>
    '''
    patron  = '<div class="featuredItem">\s*'
    patron += '<a href=(.*?) class="featuredImg img" rel="featured">'
    patron += '<img[^<]+</a>[^<]+'
    patron += '<div class="featuredText">[^<]+'
    patron += '<b><a href=([^>]+)>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<td align="center">[^<]+</td>[^<]+<td align="center">\s*<a href="([^"]+)">[^<]+</a>'
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