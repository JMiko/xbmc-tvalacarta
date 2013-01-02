# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para animeid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Animeid"
__channel__ = "animeid"
__language__ = "ES"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[animeid.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades_series"    , title="Últimas series agregadas" , url="http://animeid.tv/" ))
    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos capítulos"        , url="http://animeid.tv/" ))
    itemlist.append( Item(channel=__channel__, action="generos"             , title="Listado por genero"       , url="http://animeid.tv/" ))
    itemlist.append( Item(channel=__channel__, action="letras"              , title="Listado alfabetico"       , url="http://animeid.tv/" ))

    return itemlist

def novedades_series(item):
    logger.info("[animeid.py] novedades_series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<header class="title">Agregado recientemente:</header> <ol>(.*?)</ol>')
    patronvideos  = '<li><a href="([^"]+)"><span class="tipo\d+">([^<]+)</span><strong>([^<]+)</strong>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for url,tipo,title in matches:
        scrapedtitle = title+" ("+tipo+")"
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=title))

    return itemlist

def novedades_episodios(item):
    logger.info("[animeid.py] novedades_episodios")

    # Descarga la pagina
    #<article> <a href="/ver/uchuu-kyoudai-35"> <header>Uchuu Kyoudai #35</header> <figure><img src="http://static.animeid.com/art/uchuu-kyoudai/normal/b4934a1d.jpg" class="cover" alt="Uchuu Kyoudai" width="250" height="140" /></figure><div class="mask"></div> <aside><span class="p"><strong>Reproducciones: </strong>306</span> <span class="f"><strong>Favoritos: </strong>0</span></aside> </a> <p>Una noche en el año 2006, cuando eran jovenes, los dos hermanos Mutta (el mayor) y Hibito (el menor) vieron un OVNI que hiba en dirección hacia la luna. Esa misma noche decidieron que ellos se convertirian en astronautas y irian al espacio exterior. En el año 2050, Hibito se ha convertido en astronauta y que ademas está incluido en una misión que irá a la luna. En cambio Mutta siguió una carrera mas tradicional, y terminó trabajando en una compañia de fabricación de automoviles. Sin embargo, Mutta termina arruinando su carrera por ciertos problemas que tiene con su jefe. Ahora bien, no sólo perdió su trabajo si no que fue incluido en la lista negra de la industria laboral. Pueda ser que esta sea su unica oportunidad que tenga Mutta de volver a perseguir su sueño de la infancia y convertirse en astronauta, al igual que su perqueño hermano Hibito.</p> </article>
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<section class="lastcap">(.*?)</section>')
    patronvideos  = '<article> <a href="([^"]+)"> <header>([^<]+)</header> <figure><img src="([^"]+)"[^<]+</figure><div[^<]+</div[^<]+<aside[^<]+<span class="p"[^<]+<strong[^<]+</strong[^<]+</span[^<]+<span[^<]+<strong[^<]+</strong[^<]+</span[^<]+</aside[^<]+</a[^<]+<p>(.*?)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for url,title,thumbnail,plot in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie_with_plot"))

    return itemlist

def generos(item):
    logger.info("[animeid.py] generos")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="generos">(.*?)</div>')
    patronvideos  = '<li> <a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=title))

    return itemlist

def letras(item):
    logger.info("[animeid.py] letras")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul id="letras">(.*?)</ul>')
    patronvideos  = '<li> <a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=title))

    return itemlist

def series(item):
    logger.info("[animeid.py] series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    '''
    <article class="item"> <a href="/aoi-sekai-no-chuushin-de"><header>Aoi Sekai no Chuushin de</header> <figure><img src="http://static.animeid.com/art/aoi-sekai-no-chuushin-de/cover/0077cb45.jpg" width="116" height="164" /></figure><div class="mask"></div></a> <p>El Reino de Segua ha ido perdiendo la guerra contra el Imperio de Ninterdo pero la situación ha cambiado con la aparición de un chico llamado Gear. Todos los personajes son parodias de protas de videojuegos de Nintendo y Sega respectivamente, como lo son Sonic the Hedgehog, Super Mario Bros., The Legend of Zelda, etc.</p> </article>
    '''
    patron  = '<article class="item"[^<]+'
    patron += '<a href="([^"]+)"[^<]+<header>([^<]+)</header[^<]+'
    patron += '<figure><img src="([^"]+)"[^<]+</figure><div class="mask"></div></a> <p>(.*?)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for url,title,thumbnail,plot in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie_with_plot"))

    try:
        page_url = scrapertools.get_match(data,'<li><a href="([^"]+)">&gt;</a></li>')
        itemlist.append( Item(channel=__channel__, action="series" , title=">> Página siguiente" , url=urlparse.urljoin(item.url,page_url), thumbnail="", plot=""))
    except:
        pass

    return itemlist

def episodios(item):
    logger.info("[animeid.py] episodios")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul id="listado">(.*?)</ul>')
    patron  = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for url,title in matches:
        scrapedtitle = scrapertools.htmlclean(title)
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def findvideos(item):
    logger.info("[animeid.py] findvideos")

    data = scrapertools.cache_page(item.url)
    itemlist=[]
    
    data = data.replace("\\/","/")

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())

    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false

    # Da por bueno el canal si alguno de los vídeos de las series en "Destacados" devuelve mirrors
    series_items = destacados(mainlist_items[0])
    episodios_items = serie(series_items[0])
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien