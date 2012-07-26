# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para ADNStream
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib
import os

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[adnstream.py] init")

DEBUG = False
CHANNELNAME = "adnstream"

IMAGES_PATH = os.path.join( os.getcwd(), 'resources' , 'images' , 'adnstream' )
ADNURL = 'http://api.adnstream.com/canales.php'

MAX_SEARCH_RESULTS = "50"

def isGeneric():
    return True

def mainlist(item, numero_por_pagina=None, pagina=None):
    logger.info("[adnstream.py] mainlist")

    itemlist = []

    # Lee la URL de la página con las entradas
    if item is None or item.url == "":
        url=ADNURL
        primera = True
        if numero_por_pagina is not None and pagina is not None:
            url = url + "?n=%d&p=%d" % (numero_por_pagina,pagina)

    else:
        url = item.url
        primera = False
        if numero_por_pagina is not None and pagina is not None:
            url = url + "&n=%d&p=%d" % (numero_por_pagina,pagina)

    logger.info("url="+url)

    # Descarga la página
    data = scrapertools.cache_page(url)
    #print data

    # Extrae las entradas (carpetas)
    patronvideos  = '<canal>[^<]+'
    patronvideos += '<idcanal>[^<]*</idcanal>[^<]+'
    patronvideos += '<nombre>([^<]+)</nombre>[^<]+'
    patronvideos += '<nombrelimpio>([^<]+)</nombrelimpio>[^<]+'
    patronvideos += '<thumbnails>.*?'
    patronvideos += '<thumb[^>]+>([^<]+)</thumb>[^<]+'
    patronvideos += '</thumbnails>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for nombre,nombrelimpio,thumbnail in matches:
        scrapedtitle = nombre
        scrapedurl = 'http://api.adnstream.com/canales.php?canal='+nombrelimpio
        scrapedthumbnail = thumbnail
        
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = scrapedtitle , action="mainlist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot="", show=scrapedtitle, folder=True) )

    # Extrae las entradas (Vídeos)
    patronvideos  = '<video>[^<]+'
    patronvideos += '<idvideo>([^<]+)</idvideo>[^<]+'
    patronvideos += '<nombre>([^<]+)</nombre>[^<]+'
    patronvideos += '<descripcion>(.*?)</descripcion>[^<]+'
    patronvideos += '<duracion>([^<]+)</duracion>[^<]+'
    patronvideos += '<link>([^<]+)</link>[^<]+'
    patronvideos += '<thumbnails>.*?'
    patronvideos += '<thumb[^>]+>([^<]+)</thumb>[^<]+'
    patronvideos += '</thumbnails>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for idvideo,nombre,descripcion,duracion,link,thumbnail in matches:
        scrapedtitle = nombre+" ("+duracion+")"
        scrapedplot = descripcion
        scrapedurl = "http://api.adnstream.com/video.php?video="+idvideo
        scrapedthumbnail = thumbnail
        
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = item.fulltitle + " " + scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , duration=duracion, page=link, show=item.title, folder=False) )

    # Extrae las entradas (Vídeos)
    patronvideos  = '<video>[^<]+'
    patronvideos += '<idvideo>([^<]+)</idvideo>[^<]+'
    patronvideos += '<nombre>([^<]+)</nombre>[^<]+'
    patronvideos += '<descripcion>(.*?)</descripcion>[^<]+'
    patronvideos += '<duracion>([^<]+)</duracion>[^<]+'
    patronvideos += '<link>([^<]+)</link>[^<]+'
    patronvideos += '<ppv>([^<]+)</ppv>[^<]+'
    patronvideos += '<thumbnails>.*?'
    patronvideos += '<thumb[^>]+>([^<]+)</thumb>[^<]+'
    patronvideos += '</thumbnails>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for idvideo,nombre,descripcion,duracion,link,ppv,thumbnail in matches:
        scrapedtitle = nombre+" ("+duracion+")"
        scrapedplot = descripcion
        scrapedurl = "http://api.adnstream.com/video.php?video="+idvideo
        scrapedthumbnail = thumbnail
        
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = item.fulltitle + " " + scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , duration=duracion, page=link, show=item.title, folder=False) )

    return itemlist

def play(item):
    logger.info("[adnstream.py] mainlist")

    itemlist = []
    data = scrapertools.cache_page(item.url)
    patronvideos  = '<video>[^<]+'
    patronvideos += '<idvideo>([^<]+)</idvideo>[^<]+'
    patronvideos += '<nombre>([^<]+)</nombre>[^<]+'
    patronvideos += '<descripcion>(.*?)</descripcion>[^<]+'
    patronvideos += '<duracion>([^<]+)</duracion>[^<]+'
    patronvideos += '<thumbnails>.*?'
    patronvideos += '<thumb[^>]+>([^<]+)</thumb>[^<]+'
    patronvideos += '</thumbnails>[^<]+'
    patronvideos += '<urls>.*?'
    patronvideos += '<url[^>]+>([^<]+)</url>[^<]+'
    patronvideos += '</urls>'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for idvideo,nombre,descripcion,duracion,thumbnail,mediaurl in matches:
        scrapedtitle = nombre+" ("+duracion+")"
        scrapedplot = descripcion
        scrapedurl = mediaurl
        scrapedthumbnail = thumbnail
        
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = item.fulltitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    return itemlist

def search(item):
    logger.info("[adnstream.py] search")

    itemlist = []
    
    import xbmc
    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            itemlist = searchresults(tecleado)

    return itemlist

def searchresults(term):
    logger.info("[adnstream.py] searchresults")

    itemlist = []

    term = term.replace(" ", "+")
    url = "http://www.adnstream.tv/adn/buscador.php?q="+term+"&n="+MAX_SEARCH_RESULTS+"&i=0&cachebuster=1243592712726"
    logger.info("url="+url)

    # Descarga la página
    data = scrapertools.cache_page(url)

    # Extrae las entradas (Vídeos)
    patronvideos  = '<item>([^<]+)<guid>([^<]+)</guid>[^<]+<title>([^<]+)</title>[^<]+<description>([^<]+)</description>[^<]+<enclosure type="([^"]+)" url="([^"]+)"/>[^<]+<media\:thumbnail type="[^"]+" url="([^"]+)"/>[^<]+<link>[^<]+</link>([^<]+<minimum_age>18</minimum_age>)?[^<]+</item>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2]
        scrapedplot = match[3]
        scrapedurl = match[5]
        scrapedthumbnail = match[6]

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = title, action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist
