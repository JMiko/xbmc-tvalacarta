# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasonlineflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasonlineflv"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Peliculas Online FLV"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasonlineflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="peliculas", url="http://www.peliculasonlineflv.net", extra="1"))
    return itemlist

def peliculas(item):
    logger.info("[peliculasonlineflv.py] peliculas")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div id='summary6460896240038050290'><div class="separator" style="clear: both; text-align: center;"><a class="vtip" href="http://www.peliculasonlineflv.net/2012/01/el-gato-con-botas-los-tres-diablos-2012.html" title="Ver El gato con botas: Los tres diablos (2012)  Audio Latino"> <img src="http://4.bp.blogspot.com/-5n5pyABPx_o/Txzz987AiiI/AAAAAAAAAkI/QwLhNBWM4yo/s1600/El_gato_con_botas_Los_tres_diablos-379546995-large.jpg" alt="Ver El gato con botas: Los tres diablos (2012)  Audio Latino" height="0" width="0"></a></div></div>
    <script type='text/javascript'>createSummaryAndThumb("summary6460896240038050290");</script>
    </div>
    <div class='content'>
    <a name='6460896240038050290'></a>
    <h3>
    <a href='http://www.peliculasonlineflv.net/2012/01/el-gato-con-botas-los-tres-diablos-2012.html'>El gato con botas: Los tres diablos (2012) - Castellano Online</a>
    '''

    # Patron de las entradas
    patronvideos  = '<div id=\'summary[^<]+<div class="separator"[^<]+<a class="vtip" href="([^"]+)" title="([^"]+)"> <img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        # Atributos
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    #<a class='blog-pager-older-link' href='http://www.peliculasonlineflv.net/search?updated-max=2012-01-21T08:47:00-08:00&max-results=24'
    patron = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        siguiente_pagina = int( item.extra ) + 1
        siguiente_url = matches[0]+"#PageNo="+str(siguiente_pagina)
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=siguiente_url , extra=str(siguiente_pagina) , folder=True) )

    return itemlist
