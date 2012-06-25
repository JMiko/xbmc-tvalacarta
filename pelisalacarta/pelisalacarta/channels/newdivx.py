# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newdivx.net by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "newdivx"
__category__ = "F,D"
__type__ = "generic"
__title__ = "NewDivx"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[newdivx.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="peliculas", url="http://www.newdivx.net"))
    itemlist.append( Item(channel=__channel__, title="Categorías", action="categorias", url="http://www.newdivx.net"))
    itemlist.append( Item(channel=__channel__, title="Buscar...", action="search") )
    return itemlist

def search(item,texto):
    #POST http://www.newdivx.net/
    #do=search&subaction=search&story=brave&x=0&y=0
    logger.info("[newdivx.py] search")
    if item.url=="":
        item.url="http://www.newdivx.net/"
    texto = texto.replace(" ","+")
    item.extra = "do=search&subaction=search&story="+texto+"&x=0&y=0"
    return peliculas(item)

def peliculas(item):
    logger.info("[newdivx.py] peliculas")
    itemlist=[]

    # Descarga la página
    if item.extra!="":
        data = scrapertools.cachePage( item.url , item.extra )
    else:
        data = scrapertools.cachePage( item.url )
    '''
    <div class="main-news">
    <div class="main-news-content">
    <div id="news-id-5677" style="display:inline;"><!--dle_image_begin:http://www.newdivx.net/uploads/1340575816_YouLuckyDog.jpg|left--><img src="/uploads/1340575816_YouLuckyDog.jpg" align="left" alt="Un perro con suerte (TV) (1994)" title="Un perro con suerte (TV) (1994)"  /><!--dle_image_end--></div><div style="clear: both;"></div>
    <div class="main-news-link"><a href="http://www.newdivx.net/comedia/5677-un-perro-con-suerte-1994i.html"></a></div>
    </div>
    <h2><a href="http://www.newdivx.net/comedia/5677-un-perro-con-suerte-1994i.html">Un perro con suerte (TV) (1994)</a></h2>
    <div class="main-news-hidden"><a href="http://www.newdivx.net/comedia/">Comedia</a>, <a href="http://www.newdivx.net/infantil/">Infantil</a></div>
    </div>
    '''
    '''
    <div class="main-news-content">
    <div id="news-id-1198" style="display:inline;"><div align="center"><!--dle_image_begin:http://www.newdivx.net/uploads/thumbs/1280343827_mr_nobody.jpg|--><img src="/uploads/thumbs/1280343827_mr_nobody.jpg" alt="Las vidas posibles de Mr. Nobody (2009)" title="Las vidas posibles de Mr. Nobody (2009)"  /><!--dle_image_end--></div></div><div style="clear: both;"></div>
    <div class="main-news-link"><a href="http://www.newdivx.net/ciencia-ficcion/1198-las-vidas-posibles-de-mr-nobody-2009.html"></a></div>
    </div>
    <h2><a href="http://www.newdivx.net/ciencia-ficcion/1198-las-vidas-posibles-de-mr-nobody-2009.html">Las vidas posibles de Mr. Nobody (2009)</a></h2>
    '''
    '''
    <div class="main-news">
    <div class="main-news-content">
    <div id='news-id-5097'><!--dle_image_begin:http://www.newhd.org/uploads/thumbs/1332626577_Braveheart-898928745-large.jpg|left--><img src="http://www.newhd.org/uploads/thumbs/1332626577_Braveheart-898928745-large.jpg" align="left" alt="Braveheart (1995)" title="Braveheart (1995)"  /><!--dle_image_end--></div><div style="clear: both;"></div>
    <div class="main-news-link">Ver <a href="http://www.newdivx.net/drama/5097-braveheart-1995.html" ></a> Online</div>
    </div>
    <h2><a href="http://www.newdivx.net/drama/5097-braveheart-1995.html" >Braveheart (1995)</a></h2>
    <div class="main-news-hidden"><a href="http://www.newdivx.net/drama/">Drama</a>, <a href="http://www.newdivx.net/aventuras/">Aventuras</a>, <a href="http://www.newdivx.net/romatico/">Romatico</a></div>
    </div>
    '''

    # Patron de las entradas
    patronvideos = '<div class="main-news-content">[^<]+'
    patronvideos += '<div id=.news-id.*?<img src="([^"]+)".*?'
    patronvideos += '<h2><a href="([^"]+)"\s*>([^<]+)</a></h2>[^<]+'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    # Añade las entradas encontradas
    for thumbnail,url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    #Extrae la marca de siguiente página
    #<span>1</span> <a href="http://www.newdivx.net/peliculas-online/animacion/page/2/">2</a>
    patronvideos  = '</span> <a href="(http://www.newdivx.net.*?page/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente >>"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def categorias(item):
    logger.info("[newdivx.py] categorias")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,"<h4>Categories</h4>(.*?)</div>")
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    # Añade las entradas encontradas
    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

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