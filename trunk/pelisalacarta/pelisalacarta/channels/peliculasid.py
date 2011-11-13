# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal Descarregadirecta Carles Carmona
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

CHANNELNAME = "peliculasid"
DEBUG = True


def isGeneric():
    return True


def mainlist(item):
    logger.info("[peliculasid.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=CHANNELNAME , action="generico"        , title="Películas"                      , url="http://peliculasid.net/"))
    itemlist.append( Item(channel=CHANNELNAME , action="categorias"         , title="Categorias"            , url="http://peliculasid.net/"))
    itemlist.append( Item(channel=CHANNELNAME , action="abc"         , title="Lista Alfabética"            , url="http://peliculasid.net/"))
     
    return itemlist


def generico(item):
    logger.info("[peliculasid.py] Anime")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '<div id="listpeliculas">(.*?)<div class=\'wp-pagenavi\'>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    
    if len(matches) == 0: 
        patron = '<div id="listpeliculas">(.*?)<div align="center" class="pagination corte">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<a target="_blank" href="(.*?)">.*?<img width="145" height="199" border="0" src="(.*?)" alt="(.*?)"/>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = match2[0]
            scrapedtitle = match2[2].replace("Ver pelicula","").replace("&#038;","&").strip()
            scrapedthumbnail = match2[1]
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="detail"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    # Extrae el paginador
    #<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
    patronvideos  = '<a href="([^"]+)" class="nextpostslink">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="generico", title="Página siguiente" , url=scrapedurl) )

    return itemlist

def categorias(item):
    logger.info("[descarregadirecta.py] BuscaVideos")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    

    patron = '<div id="genero">(.*?)<div class="corte">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<a href="(.*?)">(.*?)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
            scrapedtitle = match2[1]
            scrapedurl = "http://www.peliculasid.net"+match2[0]
            scrapedthumbnail = ""
            scrapedplot = ""
            
            itemlist.append( Item(channel=item.channel , action="generico"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))
    
    
    return itemlist

def abc(item):
    logger.info("[descarregadirecta.py] Abc")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    

    patron = '<div id="abecedario">(.*?)<div class="corte">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<a href="(.*?)">(.*?)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
            scrapedtitle = match2[1]
            scrapedurl = "http://www.peliculasid.net"+match2[0]
            scrapedthumbnail = ""
            scrapedplot = ""
            
            itemlist.append( Item(channel=item.channel , action="generico"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))
    
    
    return itemlist


def detail(item):
    logger.info("[Descarregadirecta.py] detail")

    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot
    scrapedurl = ""
    url = item.url

    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    
    # Usa findvideos    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))



    return itemlist

    