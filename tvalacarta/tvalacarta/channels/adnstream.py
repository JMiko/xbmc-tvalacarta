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
ADNURL = 'http://www.adnstream.tv/canales.php?prf=box'

MAX_SEARCH_RESULTS = "50"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[adnstream.py] mainlist")

    itemlist = []

    # Lee la URL de la página con las entradas
    if item is None or item.url == "":
        url=ADNURL
        primera = True
    else:
        url = item.url
        primera = False

    logger.info("url="+url)

    # Buscador
    if primera:
        itemlist.append( Item(channel=CHANNELNAME, title="Buscar..." , thumbnail=os.path.join(IMAGES_PATH, "busqueda.jpg") , action="search" , folder=True) )

    # Descarga la página
    data = scrapertools.cache_page(url)
    #print data

    # Extrae las entradas (carpetas)
    patronvideos  = '<channel title\="([^"]+)" media\:thumbnail\="([^"]+)" clean_name\="([^"]+)"></channel>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = ADNURL+'&c='+match[2]
        scrapedthumbnail = match[1]
        
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="mainlist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot="" , folder=True) )

    # Extrae las entradas (Vídeos)
    patronvideos  = '<item>[^<]+<guid>([^<]+)</guid>[^<]+<title>([^<]+)</title>[^<]+<description>([^<]+)</description>[^<]+<enclosure type="([^"]+)" url="([^"]+)"/>[^<]+<media\:thumbnail type="[^"]+" url="([^"]+)"/>[^<]+<link>[^<]+</link>([^<]+<minimum_age>18</minimum_age>)?[^<]+(<featured>1</featured>[^<]+)?</item>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = match[2]
        scrapedurl = match[4]
        scrapedthumbnail = match[5]
        
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    if primera:
        itemlist.append( Item(channel=CHANNELNAME, title="Los más valorados" , thumbnail=os.path.join(IMAGES_PATH, "masvalorados.jpg"), url="http://www.adnstream.tv/canal_magico.new.php?i=0&n=30&c=masvalorados" , action="mainlist" , folder=True) )
        itemlist.append( Item(channel=CHANNELNAME, title="Los más vistos" , thumbnail=os.path.join(IMAGES_PATH, "masvistos.jpg") , url="http://www.adnstream.tv/canal_magico.new.php?i=0&n=30&c=masvistos" , action="mainlist" , folder=True) )
        itemlist.append( Item(channel=CHANNELNAME, title="Novedades" , thumbnail=os.path.join(IMAGES_PATH, "New.jpg") , url="http://www.adnstream.tv/canal_magico.new.php?i=0&n=30&c=novedades" , action="mainlist" , folder=True) )
        itemlist.append( Item(channel=CHANNELNAME, title="Destacados" , thumbnail=os.path.join(IMAGES_PATH, "Destacados.jpg") , url="http://www.adnstream.tv/canales.php?c=destacados" , action="mainlist" , folder=True) )


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

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist
