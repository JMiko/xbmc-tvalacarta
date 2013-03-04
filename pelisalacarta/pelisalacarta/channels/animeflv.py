# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para animeflv (por MarioXD)
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
__title__ = "Animeflv"
__channel__ = "animeflv"
__language__ = "ES"
__creationdate__ = "20111014"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[animeflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades" , title="Últimos episodios"            , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="series"    , title="Ultimas series"               , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="airlist"   , title="Series en emision"            , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="letras"    , title="Listado Alfabetico"           , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="genero"    , title="Listado por Genero"           , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Animes"   , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Ovas"     , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="completo"  , title="Listado Completo de Peliculas", url="http://animeflv.net/" ))
    #itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar"                       , url="http://animeflv.net/buscar/" ))
  
    return itemlist

def search(item,texto):
    logger.info("[animeflv.py] search")
    if item.url=="":
        item.url="http://animeflv.net/buscar/"
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def genero(item):
    logger.info("[animeflv.py] genero")

    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="caja_b3"><div id="genuno">(.*?)</div></div>')

    patron = '<li><a href="([^"]+)"[^>]*>([^"]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def completo(item):
    logger.info("[animeflv.py] completo")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    if "Animes" in item.title:
        patron  = '<ul id="flvanimes"(.*?)</ul>'
    elif "Ovas" in item.title:
        patron  = '<ul id="flvovas"(.*?)</ul>'
    elif "Peliculas" in item.title:
        patron  = '<ul id="flvpelis"(.*?)</ul>'
        
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)" title="([^"]+)">([^"]+)</a></li>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))        
    return itemlist

def letras(item):
    logger.info("[animeflv.py] letras")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="series" , title="0-9", url="http://animeflv.net/letra/0-9.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="A"  , url="http://animeflv.net/letra/a.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="B"  , url="http://animeflv.net/letra/b.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="C"  , url="http://animeflv.net/letra/c.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="D"  , url="http://animeflv.net/letra/d.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="E"  , url="http://animeflv.net/letra/e.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="F"  , url="http://animeflv.net/letra/f.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="G"  , url="http://animeflv.net/letra/g.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="H"  , url="http://animeflv.net/letra/h.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="I"  , url="http://animeflv.net/letra/i.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="J"  , url="http://animeflv.net/letra/j.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="K"  , url="http://animeflv.net/letra/k.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="L"  , url="http://animeflv.net/letra/l.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="M"  , url="http://animeflv.net/letra/m.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="N"  , url="http://animeflv.net/letra/n.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="O"  , url="http://animeflv.net/letra/o.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="P"  , url="http://animeflv.net/letra/p.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="Q"  , url="http://animeflv.net/letra/q.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="R"  , url="http://animeflv.net/letra/r.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="S"  , url="http://animeflv.net/letra/s.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="T"  , url="http://animeflv.net/letra/t.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="U"  , url="http://animeflv.net/letra/u.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="V"  , url="http://animeflv.net/letra/v.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="W"  , url="http://animeflv.net/letra/w.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="X"  , url="http://animeflv.net/letra/x.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="Y"  , url="http://animeflv.net/letra/y.html"))
    itemlist.append( Item(channel=__channel__, action="series" , title="Z"  , url="http://animeflv.net/letra/z.html"))

    return itemlist


def series(item):
    logger.info("[animeflv.py] series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas 
    patronvideos  = '<div class="anime_box"> <a href="([^"]+)" title="([^"]+)"><img src="([^"]+)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle, viewmode="movie"))

    patron = '<a href="([^"]+)">Siguiente</a><a href="([^"]+)">Ultima</a> </span></div></center><div class="cont_anime">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            scrapedurl = "http://animeflv.net"+match[0]
            scrapedtitle = "!Pagina Siguiente"
            scrapedthumbnail = ""
            scrapedplot = ""

            itemlist.append( Item(channel=__channel__, action="series", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist

def novedades(item):
    logger.info("[animeflv.py] novedades")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  
    patronvideos  = '<div class="abso">.*?<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)".*?>([^<]+)</a></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[3])
        fulltitle = scrapedtitle
        # directory = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2].replace("mini","portada"))
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle=fulltitle, viewmode="movie"))

    return itemlist

def episodios(item):
    logger.info("[animeflv.py] episodios")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Saca el argumento
    try:
        scrapedplot = scrapertools.get_match(data,'<div class="caja_cont">(.*?)</div></div>')
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedplot = scrapertools.htmlclean(scrapedplot)
    except:
        pass
    
    try:
        scrapedthumbnail = scrapertools.get_match(data,'<div class="contenedor_principal".*?<img src="([^"]+)"')
        scrapedthumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
    except:
        pass

    # Saca enlaces a los episodios
    data = scrapertools.get_match(data,'Listado de capitulos(.*?)</ul>')
    patron = '<li class="lcc"><a href="([^"]+)" class="lcc">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape( scrapedtitle )

        try:
            episodio = scrapertools.get_match(scrapedtitle,"Capítulo (\d+)")
            if len(episodio)==1:
                scrapedtitle = "1x0"+episodio
            else:
                scrapedtitle = "1x"+episodio
        except:
            pass
        
        
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        #scrapedthumbnail = item.thumbnail
        #scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show, fulltitle=fulltitle, viewmode="movie_with_plot"))
    
    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def airlist(item):
    logger.info("[animeid.py] airlist")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  
    patronvideos  = 'Animes en Emision(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)" title="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    itemlist = []

    for match in matches:
        scrapedtitle = match[1]
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))

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
    
    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    episodios_items = novedades(mainlist_items[0])
    
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien
