﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "rtspan"
__category__ = "F"
__type__ = "generic"
__title__ = "rtspan"
__language__ = "ES"
__creationdate__ = "20121212"
__vfanart__ = "http://actualidad.rt.com/static/actualidad/design1/i/d/bg.png"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtspan.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Detrás de la noticia", action="videos", url="http://actualidad.rt.com/programas/detras_de_la_noticia",  fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="RT reporta", action="videos", url="http://actualidad.rt.com/programas/rt_reporta",  fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Keiser report", action="videos", url="http://actualidad.rt.com/programas/keiser_report",  fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="Desde la sombra", action="videos", url="http://actualidad.rt.com/programas/desde_la_sombra",  fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Entrevista", action="videos", url="http://actualidad.rt.com/programas/entrevista",  fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Deportes en reportes", action="videos", url="http://actualidad.rt.com/programas/deportes_reportes",  fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="La lista de Erick", action="videos", url="http://actualidad.rt.com/programas/la_lista_de_erick",  fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Especial", action="videos", url="http://actualidad.rt.com/programas/especial",  fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Tecnología de punta", action="videos", url="http://actualidad.rt.com/programas/tecnologia",  fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="Más allá de Moscú", action="videos", url="http://actualidad.rt.com/programas/mas_alla_de_moscu",  fanart = __vfanart__))     #itemlist.append( Item(channel=__channel__, title="Diálogos con Julian Assange", action="videos", url="http://assange.rt.com/es/",  fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="Archivo - A fondo", action="videos", url="http://actualidad.rt.com/programas/a_fondo",  fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="Archivo - A solas", action="videos", url="http://actualidad.rt.com/programas/a_solas",  fanart = __vfanart__)) 
 
    return itemlistdef videos(item):    logger.info("[rtspan.py] videos")        data = scrapertools.cachePage(item.url)    data = data.replace("\n", " ")    data = data.replace("\r", " ")    data = " ".join(data.split())	    #logger.info(data)        patron = '<a href="([^"]+)" title="(.*?)"> <img src="([^"]+)"> <span>(.*?)</span> </a>'    matches = re.compile(patron,re.DOTALL).findall(data)    if DEBUG: scrapertools.printMatches(matches)	    itemlist = []    for match in matches:        scrapedtitle = match[3]        scrapedthumbnail = 'http://actualidad.rt.com'+match[2]        scrapedurl   = 'http://actualidad.rt.com'+match[0]        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,  folder=False) )    patron = '<div class="right"><a href="([^"]+)" onclick='    matches = re.compile(patron,re.DOTALL).findall(data)    if DEBUG: scrapertools.printMatches(matches)	    for match in matches:        scrapedurl = 'http://actualidad.rt.com'+match		        scrapedtitle = "!Página siguiente"        itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle , url=scrapedurl ,  folder=True) )        return itemlist
def play(item):    logger.info("[rtspan.py] play")        data = scrapertools.cachePage(item.url)	    logger.info(data)        patron = '<meta property="og:video" content="([^"]+)" />'		    matches = re.compile(patron,re.DOTALL).findall(data)		    if DEBUG: scrapertools.printMatches(matches)		    if matches:         scrapedurl = matches[0]		    itemlist = []    itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=scrapedurl ,  folder=False) )    return itemlist