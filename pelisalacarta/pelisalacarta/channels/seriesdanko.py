# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesdanko.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

from xml.dom import minidom
from xml.dom import EMPTY_NAMESPACE

PLUGIN_NAME = "pelisalacarta"
CHANNELNAME = "seriesdanko"
ATOM_NS = 'http://www.w3.org/2005/Atom'
DEBUG = config.get_setting("debug")

if config.get_system_platform() == "xbox":
    MaxResult = "55"
else:
    MaxResult = "500"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesdanko.py] mainlist")

    
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Listado A-Z"     , action="alfabetico", url="http://www.seriesdanko-rs.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Listado completo", action="series", url="http://www.seriesdanko-rs.com/"))
    return itemlist

def alfabetico(item):
    logger.info("[seriesdanko.py] alfabetico")
    
    BaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BaseUrl   = "http://www.seriesdanko-rs.com/series.php?id=%s"
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="episodios", title="0-9" , url=BaseUrl % "0" , thumbnail="" , plot="" , folder=True) )
    for letra in BaseChars:
        scrapedtitle = letra
        scrapedplot = ""
        scrapedurl = BaseUrl % letra
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="series", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def series(item):
    logger.info("[seriesdanko.py] allserieslist")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    # Extrae el bloque de las series
    patronvideos = 'Listado de series disponibles</h2>(.*?)<div class=.clear.></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = matches[0]
    scrapertools.printMatches(matches)

    # Extrae las entradas (carpetas)
    #<a href='/serie.php?serie=1' title='10 razones para odiarte'>10 razones para odiarte</a>
    patronvideos  = "<a href='([^']+)' title='[^']+'>([^<]+)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for url,title in matches:
        scrapedtitle = title.strip().replace("\n","").replace("\r","")
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show = scrapedtitle , totalItems = len(matches)))

    return itemlist

def episodios(item):
    logger.info("[seriesdanko.py] episodios")
    
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    #<a href='/serie.php?serie=1' title='10 razones para odiarte'>10 razones para odiarte</a>
    patronvideos  = "<a href='(capitulo.php[^']+)'>([^<]+)</a>(.*?)<Br>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for url,title,flags in matches:
        scrapedtitle = title.strip().replace("\n","").replace("\r","")
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info("title="+scrapedtitle+", flags="+flags)

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show = scrapedtitle , totalItems = len(matches)))

    #print datalist
    return itemlist

