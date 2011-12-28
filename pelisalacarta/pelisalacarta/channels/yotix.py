# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yotix
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "yotix"
__category__ = "A"
__type__ = "generic"
__title__ = "Yotix.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[yotix.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videolist"      , title="Novedades", url="http://yotixanime.com/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias" , title="Listado por categorías", url="http://yotix.tv/"))
    itemlist.append( Item(channel=__channel__, action="search"         , title="Buscador", url="http://yotix.tv/?s=%s"))

    return itemlist

def search(item,texto):
    logger.info("[yotix.py] search")

    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://yotix.tv/?s=%s"

        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto

        # Devuelve los resultados
        return videolist(item)
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def listcategorias(item):
    logger.info("[yotix.py] listcategorias")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    patron  = '<a href="(/categoria/[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="videolist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def videolist(item):
    logger.info("[yotix.py] videolist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    patron  = '<div class="galleryitem">[^<]+'
    patron += '<h1><a title="([^"]+)"[^<]+</a></h1>[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []

    for match in matches:
        scrapedtitle = match[0].replace("&#8211;","-")
        scrapedurl = match[1]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="listmirrors" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la página siguiente
    patron = '<a href="([^"]+)" >&raquo;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Pagina siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapeddescription = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="videolist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listmirrors(item):
    logger.info("[yotix.py] listmirrors")

    title = item.title
    url = item.url
    thumbnail = item.thumbnail
    plot = item.plot
    itemlist = []

    # Descarga la página de detalle
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    # Extrae el argumento
    patronvideos  = '<div class="texto-sinopsis">(.*?)<div'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        plot = scrapertools.htmlclean(matches[0].strip())

    # Extrae los enlaces si el video está en la misma página
    patron = 'so.addParam\(\'flashvars\',\'.*?file\=([^\&]+)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        url = matches[0]
        newurl = findnewlocation(url)
        if newurl!="":
            url = newurl
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, server="Directo", folder=False))

    # Extrae los enlaces a los vídeos (Megavídeo)
    patronvideos  = '<a.*?href="(http://yotix.tv/flash/[^"]+)"[^>]*>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)        

    for match in matches:
        # Añade al listado de XBMC
        scrapedtitle = scrapertools.htmlclean(match[1].replace("&#8211;","-")).strip()
        scrapedurl = match[0]
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, server="Megavideo", folder=False))

    # Extrae los enlaces a los vídeos (Directo)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/sitio/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/media/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/video/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/ver/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/rt/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/anime/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/gb/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/online/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)
    buscamirrors(itemlist,'<a.*?href="(http://yotix.tv/4s/[^"]+)"[^>]*>(.*?)</a>',data,thumbnail,plot)

    return itemlist

def buscamirrors(itemlist,patronvideos,data,thumbnail,plot):
    logger.info("patron="+patronvideos)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)        

    for match in matches:
        scrapedtitle = scrapertools.htmlclean(match[1].replace("&#8211;","-")).strip()
        scrapedurl = match[0]
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=thumbnail, plot=plot))

def findvideos(item):
    logger.info("[yotix.py] play")

    title = urllib.unquote_plus( params.get("title") )
    url = item.url
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )
    server = urllib.unquote_plus( params.get("server") )

    data = scrapertools.cachePage(url)
    #logger.info(data)

    itemlist = []

    # Busca videos directos
    patron = 'so.addParam\(\'flashvars\',\'\&file\=([^\&]+)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedurl = matches[0]
        
        newurl = findnewlocation(scrapedurl)
        if newurl!="":
            url = newurl
    
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, server="Directo", folder=False))

    # Busca el resto de videos
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title + " (" + video[2] + ")"
        scrapedurl = video[1]
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        server = video[2]
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, server=server, folder=False))

    return itemlist

def findnewlocation(url):
    #http://www.yotix.tv/onlineflv/hrsg03.flv
    logger.info("url="+url)

    import httplib
    parsedurl = urlparse.urlparse(url)
    print "parsedurl=",parsedurl

    try:
        host = parsedurl.netloc
    except:
        host = parsedurl[1]
    print "host=",host

    try:
        print "1"
        query = parsedurl.path
    except:
        print "2"
        query = parsedurl[2]
    print "query=",query
    query = urllib.unquote( query )
    print "query = " + query

    import httplib
    conn = httplib.HTTPConnection(host)
    
    headers = {"Range": "bytes=0-10"}
    conn.request("GET", query,headers=headers)
    response = conn.getresponse()
    if response.status==302:
        location = response.getheader("location")
    else:
        location = ""
    conn.close()
    
    print "location=",location

    #location: http://z4.przeklej.pl/przv164/1cfe677d00270c2d4cc09c32/hyakka_ryouran_samurai_girls_03_by_sombra_blanca.mp4
    print "videourl=",location

    return location
