# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasid 
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import logger
from core.item import Item
from core import downloadtools
from platform.xbmc import xbmctools
from servers import servertools

CHANNELNAME = "peliculasid"

# Traza el inicio del canal
logger.info("[peliculasid.py] init")

DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasid.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos"      , title="Ultimos capítulos" , url="http://www.peliculasid.net/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos"      , title="Estrenos" , url="http://www.peliculasid.net/categoria/estreno"))
    itemlist.append( Item(channel=CHANNELNAME, action="listbyYears"    , title="Año de estreno", url="http://www.peliculasid.net/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcategorias"    , title="Categorias", url="http://www.peliculasid.net/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listalfanum"    , title="Listado alfabetico", url="http://www.peliculasid.net/"))
    return itemlist

def listcategorias(item):
    logger.info("[peliculas.py] listcategorias")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="generos">(.*?)<div class="corte"></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<a href="(.+?)">(.+?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    
    for match in matches:

        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=CHANNELNAME , action="listvideos" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
        
def listbyYears(item):
    logger.info("[peliculas.py] listbyYears")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="subtitulo">A.+o de estreno</div>(.*?)<div id="ano">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<option value="(/categoria.+?)">(.+?)</option>'
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    
    for match in matches:

        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=CHANNELNAME , action="listvideos" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
    
def listalfanum(item):
    logger.info("[peliculasid.py] listalfanum")
    
    BaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BaseUrl   = "http://peliculasid.net/categoria/letra/%s"
    action    = "listvideos"
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action=action, title="0-9" , url=BaseUrl % "0-9" , thumbnail="" , plot="" , folder=True) )
    for letra in BaseChars:
        scrapedtitle = letra
        scrapedplot = ""
        scrapedurl = BaseUrl % letra
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action=action, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist
    
def listvideos(item):
    logger.info("[peliculasid.py] listvideos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = 'id="filmga[^"]+" class="filmgal">(.*?<strong>Duraci[^<]+</strong>[^<]+</div>)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        # URL
        try:
            scrapedurl = re.compile(r'href="(.+?)"').findall(match)[0]
        except:
            continue
        # Titulo
        try:
            scrapedtitle = re.compile(r'<span class="titulotool">(.+?)</div>').findall(match.replace("\n",""))[0]
            scrapedtitle = re.sub("<[^>]+>","",scrapedtitle)
            try:
                scrapedtitle = scrapertools.unescape(scrapedtitle)
            except:pass
        except:
            scrapedtitle = "sin titulo"
        # Thumbnail
        try:
            scrapedthumbnail = re.compile(r'src="(.+?)"').findall(match)[0]
        except:
            scrapedthumbnail = ""
        # Argumento
        try:
            scrapedplot = re.compile(r'<div class="sinopsis">(.+?)</div>').findall(match)[0]
            scrapedplot = re.sub("<[^>]+>"," ",scrapedplot).strip()
        except:
            scrapedplot = ""

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = scrapedplot , context= 5  ))
        

    # Extrae la marca de siguiente página
    
    patronvideos  = "<span class='current'>[^<]+</span><a href='(.+?)' class='page larger'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot ))
        
    return itemlist
