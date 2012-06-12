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
    itemlist.append( Item(channel=__channel__, action="newlist" , title="Novedades"                         , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="Lista2"  , title="Ultimas series agregadas o subidas", url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="airlist" , title="Animes en emision"                 , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="ListA"   , title="Listado Alfabetico"                , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="genero"  , title="Listado por Genero"                , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="completo", title="Listado Completo de Animes"        , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="completo", title="Listado Completo de Ovas"          , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="completo", title="Listado Completo de Peliculas"     , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="search"  , title="Buscar"                            , url="http://animeflv.net/buscar/" ))
  
    return itemlist

def search(item,texto):
    logger.info("[animeflv.py] search")
    if item.url=="":
        item.url="http://animeflv.net/buscar/"
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return Lista2(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def genero(item):
    logger.info("[animeflv.py] genero")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    patron  = '<div id="genuno">(.*?)</div>'
        
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[1])
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="Lista2" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))        
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
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))        
    return itemlist

def ListA(item):
    logger.info("[animeflv.py] ListA")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="0-9", url="http://animeflv.net/letra/0-9.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="A"  , url="http://animeflv.net/letra/a.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="B"  , url="http://animeflv.net/letra/b.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="C"  , url="http://animeflv.net/letra/c.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="D"  , url="http://animeflv.net/letra/d.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="E"  , url="http://animeflv.net/letra/e.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="F"  , url="http://animeflv.net/letra/f.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="G"  , url="http://animeflv.net/letra/g.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="H"  , url="http://animeflv.net/letra/h.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="I"  , url="http://animeflv.net/letra/i.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="J"  , url="http://animeflv.net/letra/j.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="K"  , url="http://animeflv.net/letra/k.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="L"  , url="http://animeflv.net/letra/l.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="M"  , url="http://animeflv.net/letra/m.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="N"  , url="http://animeflv.net/letra/n.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="O"  , url="http://animeflv.net/letra/o.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="P"  , url="http://animeflv.net/letra/p.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="Q"  , url="http://animeflv.net/letra/q.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="R"  , url="http://animeflv.net/letra/r.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="S"  , url="http://animeflv.net/letra/s.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="T"  , url="http://animeflv.net/letra/t.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="U"  , url="http://animeflv.net/letra/u.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="V"  , url="http://animeflv.net/letra/v.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="W"  , url="http://animeflv.net/letra/w.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="X"  , url="http://animeflv.net/letra/x.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="Y"  , url="http://animeflv.net/letra/y.html"))
    itemlist.append( Item(channel=__channel__, action="Lista2" , title="Z"  , url="http://animeflv.net/letra/z.html"))

    return itemlist


def Lista2(item):
    logger.info("[animeflv.py] Lista2")

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

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))        
    return itemlist

def newlist(item):
    logger.info("[animeflv.py] newlist")

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

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle=fulltitle))

    return itemlist

def serie(item):
    logger.info("[animeflv.py] serie")
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Saca el argumento
    patronplot  = '<div class="sinop">(.*?)</div>'
    matches = re.compile(patronplot,re.DOTALL).findall(data)
    
    if len(matches)>0:
        scrapedplot = scrapertools.htmlclean( matches[0] )
    
    # Saca enlaces a los episodios
    patron  = 'Listado de capitulos(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li class="lcc"><a href="([^"]+)" class="lcc">([^<]+)</a></li>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape( scrapedtitle )
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        #scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show, fulltitle=fulltitle))
    
    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="serie", show=item.show) )

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

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))

    return itemlist

def findvideos(item):
    logger.info("[animeid.py] findvideos")

    # Busca el argumento
    data = scrapertools.cache_page(item.url)
    patron = '<img src="[^"]+" class="simg" align="left"[^>]+>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedplot = matches[0]
    else:
        scrapedplot = item.plot
    
    # Ahora busca los vídeos
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.plot = scrapedplot
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.title
        videoitem.title = item.title + videoitem.title
    
    #<div style="display:none;" id="videoi">i=yayIeoN8foWQv8p8qY9xgXy4d7W7wYnHhrDPs70=</div>
    codigo_video_plugin = scrapertools.get_match(data,'<div[^>]+>i\=([^<]+)</div>')
    #http://prueba.animeflv.net/mf.php?id=yayIeoN8foWQv8p8qY9xgXy4d7W7wYnHhrDPs70=&paso=obtener
    url="http://prueba.animeflv.net/mf.php?id="+codigo_video_plugin+"&paso=obtener"
    data = scrapertools.cache_page(url)
    #<embed allowfullscreen="true" src="/archivos/player.swf" bgcolor="#000" type="application/x-shockwave-flash" wmode="transparent" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="file=http://205.196.121.103/khff8ehdgfdg/mu0d5033k2ook7r/%5BVagoSubs%5D+Kurokos+Basketball+08+%5B480p%5D.mp4&autostart=true&provider=video" height="100%" width="100%">
    mediaurl = scrapertools.get_match(data,'<embed.*?flashvars\="file\=([^\&]+)&')
    logger.info("data="+data)
    itemlist.append( Item( channel=__channel__, title=item.title+" (acceso plugin) - [directo]", action="play", url=mediaurl, server="directo", thumbnail=item.thumbnail, plot=scrapedplot, fulltitle=item.title, folder=False) )
    
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
    episodios_items = newlist(mainlist_items[0])
    
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien