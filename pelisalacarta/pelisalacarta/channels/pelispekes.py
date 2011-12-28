# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelispekes
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelispekes"
__category__ = "F,A"
__type__ = "xbmc"
__title__ = "Pelis Pekes"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelispekes.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__ , action="Generico"        , title="Novedades"                      , url="http://pelispekes.com/"))
    itemlist.append( Item(channel=__channel__ , action="Categorias"        , title="Categorias"                      , url="http://pelispekes.com/"))
    itemlist.append( Item(channel=__channel__ , action="Abecedario"        , title="Abecedario"                      , url="http://pelispekes.com/"))
    

    return itemlist


def Generico(item):
    logger.info("[filmixt.py] Generico")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = 'class="filmgal">(.*?)<strong>Duración: </strong>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        patron  = '<a target="_blank" href="(.*?)">.*?'
        patron += '<img width="145" height="199" border="0" src="(.*?)" alt="(.*?)"/>.*?'
        patron += '<strong>Sinopsis:</strong>(.*?)</div>'
        matches2 = re.compile(patron,re.DOTALL).findall(match)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = match2[0]
            scrapedtitle =match2[2].replace("Ver pelicula","").replace("&#8211;","")
            scrapedthumbnail = match2[1]
            scrapedplot = match2[3]
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="buscavideos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    # ------------------------------------------------------
    # Extrae la p?gina siguiente
    # ------------------------------------------------------
    #patron = '<a href="([^"]+)" >\&raquo\;</a>'
    patron  = "class='current'>[^<]+</span><a href='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG:
        scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "!Pagina siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapeddescription = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=item.channel , action="Generico"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    
    return itemlist

def buscavideos(item):
    logger.info("[pelispekes.py] BuscaVideos")

    url = item.url
                
    data = scrapertools.cachePage(url)
    
    logger.info(data)
    # Usa findvideos    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist

def Categorias(item):
    logger.info("[filmixt.py] Categorias")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '<div id="genero">(.*?)<div class="corte"></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    
    itemlist = []
    for match in matches:
        patron  = '<a href="(.*?)">(.*?)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(match)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://pelispekes.com"+match2[0]
            scrapedtitle =match2[1]
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="Generico"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
        
    return itemlist

def Abecedario(item):
    logger.info("[filmixt.py] Abecedario")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '<div id="abecedario">(.*?)<div class="corte"></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    
    itemlist = []
    for match in matches:
        patron  = '<a href="(.*?)">(.*?)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(match)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://pelispekes.com"+match2[0]
            scrapedtitle =match2[1]
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="Generico"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
        
    return itemlist

