# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para descargapelis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import logger
from core import config
from core.item import Item
from servers import servertools
#from servers import vk

CHANNELNAME = "descargapelis"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[descargapelis.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=CHANNELNAME , action="newlist"           , title="Nuevas incorporaciones"            , url="http://www.descargapelis.net/"))
    itemlist.append( Item(channel=CHANNELNAME , action="moviecategorylist" , title="Películas - Por categorías"            , url="http://www.descargapelis.net/"))
    itemlist.append( Item(channel=CHANNELNAME , action="moviealphalist"    , title="Películas - Por orden alfabético"            , url="http://www.descargapelis.net/"))
    itemlist.append( Item(channel=CHANNELNAME , action="estrenos"          , title="Películas de estreno"            , url="http://www.descargapelis.net/estreno.php"))
    itemlist.append( Item(channel=CHANNELNAME , action="hayquever"         , title="Películas que hay que ver"            , url="http://www.descargapelis.net/estreno.php"))
    itemlist.append( Item(channel=CHANNELNAME , action="recomendadas"      , title="Recomendadas"            , url="http://www.descargapelis.net/recomendadas.php"))

    return itemlist

# Listado de novedades de la pagina principal
def recomendadas(item):
    logger.info("[descargapelis.py] recomendadas")
    itemlist=[]
    
    data = scrapertools.cachePage(item.url)
    
    if (item.extra == "descargapelis") :
        #xbmctools.addnewfolder( CHANNELNAME , "recomendadas" , "todas" , "Todas" , url , "todas", "" )
        #xbmctools.addnewfolder( CHANNELNAME , "recomendadas" , "todas" , "Todas" , url , "", "" )
        itemlist.append( Item(channel=CHANNELNAME , action="recomendadas" , extra="todas" , title="Todas" , url=item.url))

        patron  = 'PELICULAS DE .+?>(.+?)</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)

        for match in matches:
            #xbmctools.addnewfolder( CHANNELNAME , "recomendadas" , match , match , url , "", "" )
            itemlist.append( Item(channel=CHANNELNAME , action="recomendadas" , extra=match , title=match , url=item.url))
    else:
        url=item.url[0:item.url.index(".net/")+5]
        if item.extra!="todas":
            data=data[data.index(item.extra):data.index("PHP***",data.index(item.extra))]
            logger.info(data)
            
        patron  = '<td align=".+?" colspan="\d+" valign="top" height="\d+" width="\d+"><a href="(.+?)" class="titulo_peli"><img class="foto_prin" width="\d+" height="\d+" src="(.+?)" title="(.+?)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches) > 0 :
            for match in matches:
                #xbmctools.addnewfolder( CHANNELNAME , "findvideos" , category , match[2] ,url + match[0] , match[1], "" )
                itemlist.append( Item(channel=CHANNELNAME , action="findvideos" , extra=item.extra , title=match[2] , url=item.url+match[0], thumbnail=match[1]))

    return itemlist

def estrenos(item):
    logger.info("[descargapelis.py] estrenos")
    itemlist=[]

    # Descarga la página y extrae el bloque bueno
    data = scrapertools.cachePage(item.url)
    data=data[data.index("PELICULAS DE ESTRENO"):data.index("</table>",data.index("PELICULAS DE ESTRENO"))]
    #logger.info(data)

    # Extrae las películas
    url=item.url[0:item.url.index(".net/")+5]
    patron  = 'colspan="3" height="25" class="titulo_peli"><a[^<]+?href="(.+?php)" class="titulo_peli">([^<]+?)<br />.+?src="(.+?)".+?</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = url + match[0]        
        scrapedthumbnail = match[2]
        scrapedplot = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #xbmctools.addnewfolder( CHANNELNAME , "findvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=CHANNELNAME , action="findvideos" , extra=item.extra , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def hayquever(item):
    logger.info("[descargapelis.py] hayquever")
    itemlist=[]

    # Descarga la página y extrae el bloque bueno
    data = scrapertools.cachePage(item.url)
    data=data[data.index("PELICULAS QUE HAY QUE VER"):data.index("</table>",data.index("PELICULAS QUE HAY QUE VER"))]
    #logger.info(data)

    url=url[0:item.url.index(".net/")+5]
    patron  = 'colspan="3".+?height="25" class="titulo_peli"><a[^<]+?href="(.+?php)" class="titulo_peli">([^<]+?)<br />.+?src="(.+?)".+?</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = url + match[0]
        scrapedthumbnail = match[2]
        scrapedplot = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #xbmctools.addnewfolder( CHANNELNAME , "findvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=CHANNELNAME , action="findvideos" , extra=item.extra , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def newlist(item):
    logger.info("[descargapelis.py] newlist")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<td colspan="3" height="25" class="titulo_peli"><a[^<]+?href="(.+?php)" class="titulo_peli">([^<]+?)</a>'
    logger.info(item.url + "es la url")
    url=item.url[0:item.url.index(".net/")+5]
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = url + match[0]
        scrapedthumbnail = ""
        scrapedplot = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #xbmctools.addnewfolder( CHANNELNAME , "findvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=CHANNELNAME , action="findvideos" , extra=item.extra , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de categorias de películas, de la caja derecha de la home
def moviecategorylist(item):
    logger.info("[descargapelis.py] moviecategorylist")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    patron  = '<a class="menu_cat" href="(cat_.+?)">-?(.+?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = item.url + match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #xbmctools.addnewfolder( CHANNELNAME , "newlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=CHANNELNAME , action="newlist" , extra=item.extra , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de letras iniciales de película, de la caja derecha de la home
def moviealphalist(item):
    logger.info("[descargapelis.py] moviealphalist")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    patron  = '<a class="listado_alfabetico" href="(alfa(.)\.php)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = item.url + match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #xbmctools.addnewfolder( CHANNELNAME , "newlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=CHANNELNAME , action="newlist" , extra=item.extra , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Detalle de un vídeo (peli o capitulo de serie), con los enlaces
def findvideos(item):
    logger.info("[descargapelis.py] findvideos")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    patron = '<table width="100%" cellpadding="0" cellspacing="0">[^<]+?'
    patron +='<tr>[^<]+?<td align="center"><img src="(.+?)".+?'
    patron +='<td align="justify" valign="top" class="texto_peli"><b>Sinopsis de (.+?):</b>(.+?)<br />'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    listavideos = servertools.findvideos(data)
    thumbnail=matches[0][0]
    plot=matches[0][2]
    title=matches[0][1]
    for video in listavideos:
        video_title=video[0]
        video_url=video[1]
        video_server=video[2]
        #xbmctools.addnewvideo( CHANNELNAME , "play" , CHANNELNAME ,  ,  , video[1] , thumbnail, plot )
        itemlist.append( Item(channel=CHANNELNAME , action="play" , extra=item.extra , title=title + " [" + video_server + "]" , server=video_server, url=video_url, thumbnail=thumbnail, plot=plot, folder=False))

    return itemlist
