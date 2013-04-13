# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para malvin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "malvin"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Malvin.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[malvin.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Estrenos"     , action="movielist", url="http://www.malvin.biz/"))
    itemlist.append( Item(channel=__channel__, title="Películas"    , action="lista",     url="http://www.malvin.biz/search/label/Online"))
    itemlist.append( Item(channel=__channel__, title="Documentales" , action="lista",     url="http://www.malvin.biz/search/label/Documentales"))
    itemlist.append( Item(channel=__channel__, title="Generos"      , action="generos",   url="http://www.malvin.biz/"))

    return itemlist

def movielist(item):
    logger.info("[malvin.py] movielist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match( data , "<div class='widget-content'>(.*?)" + '<div style="text-align: center;">')

    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="contenedor-img"[^<]+'
    patronvideos += '<a href="([^"]+)"[^<]+'
    patronvideos += '<img alt="[^"]+" class="[^"]+" src="([^"]+)"'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapedtitle = ""
    scrapedurl = ""
    scrapedthumbnail = ""
    
    for scrapedurl, scrapedthumbnail in matches:
        # Titulo
        cadenatitulo = scrapedurl.split('/')
        cadenatitulo = cadenatitulo[len(cadenatitulo)-1]
        longitud = len(cadenatitulo)
        scrapedtitle = cadenatitulo[:longitud-5]
        #xbmc.log("movielist " + scrapedtitle)
        scrapedtitle = scrapedtitle.replace("-"," ")
        
        # procesa el resto
        scrapeddescription = ""

        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapeddescription , folder=True) )

    return itemlist

def lista(item):
    logger.info("[malvin.py] lista")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data2 = scrapertools.get_match( data , "<div class='blog-posts hfeed'>(.*?)<div class='blog-pager' id='blog-pager'>")

    # Extrae las entradas (carpetas)
    patronvideos  = "<h3 class='post-title entry-title'>[^<]+"
    patronvideos += "<a href='([^']+)' title='([^']+)'[^<]+</a>[^<]+"
    patronvideos += '</h3>[^<]+'
    patronvideos += '</div>[^<]+'
    patronvideos += "<div class='sentry'>(.*?)<noscript></noscript>"
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data2)
    scrapedtitle = ""
    scrapedurl = ""
    scrapedthumbnail = ""
    
    for scrapedurl, scrapedtitle, bloque in matches:
        # procesa el resto
        scrapeddescription = ""
        scrapedthumbnail = scrapertools.get_match(bloque,'<img border="[^"]+" height="[^"]+" src="([^"]+)"')

        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapeddescription , folder=True) )

    #data = scrapertools.cachePage(item.url)
    scrapedurl = scrapertools.get_match( data , "<a class='blog-pager-older-link' href='(.*?)' id='")
    itemlist.append( Item(channel=__channel__, action="lista", title="Pagina Siguiente >>" , url=scrapedurl , thumbnail=scrapedthumbnail , plot="" , folder=True) )

    return itemlist

def generos(item):
    logger.info("[malvin.py] generos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match( data , "<h2>Generos</h2>(.*?)" + "<div class='clear'>")

    # Extrae las entradas (carpetas)
    patronvideos  = "<li>[^<]+"
    patronvideos += "<a dir='ltr' href='([^']+)'>([^<]+)</a>"
    #patronvideos += '="[^=]+'
    #patronvideos += '="([^"])"[^>]+'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapedtitle = ""
    scrapedurl = ""
    scrapedthumbnail = ""

    for scrapedurl, scrapedtitle in matches:        
        # procesa el resto
        scrapeddescription = ""

        itemlist.append( Item(channel=__channel__, action="lista", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapeddescription , folder=True) )

    return itemlist
