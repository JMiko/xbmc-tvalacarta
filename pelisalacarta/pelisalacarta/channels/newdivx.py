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
    return itemlist

def peliculas(item):
    logger.info("[newdivx.py] peliculas")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <td align="center" valign="middle" width="20%" class="short"> 
    <a href="http://www.newdivx.net/peliculas-online/comedia/4716-la-oportunidad-de-mi-vida-2010-lat.html"><img src="http://www.newhd.org/uploads/thumbs/1327685908_La_oportunidad_de_mi_vida-184333983-large.jpg"  alt='La oportunidad de mi vida (2010) [LAT]' title='La oportunidad de mi vida (2010) [LAT]'  style="max-width: 190px; "></a>
    <div><a href="http://www.newdivx.net/peliculas-online/comedia/4716-la-oportunidad-de-mi-vida-2010-lat.html">La oportunidad de mi vida (2010) [LAT]</a></div>
    '''

    # Patron de las entradas
    patronvideos  = '<td align="center" valign="middle" width="20%" class="short">[^<]+'
    patronvideos += '<a href="([^"]+)"><img src="([^"]+)"[^<]+</a>[^<]+'
    patronvideos += '<div><a [^>]+>([^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        # Atributos
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

