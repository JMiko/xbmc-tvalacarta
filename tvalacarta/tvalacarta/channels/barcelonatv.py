# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para barcelonatv
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[barcelonatv.py] init")

DEBUG = False
CHANNELNAME = "barcelonatv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[barcelonatv.py] mainlist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage("http://www.barcelonatv.cat/alacarta/default.php")
    
    # Extrae los programas
    patron = '<option value=\'(\d+)\'\W*>([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = "http://www.barcelonatv.cat/alacarta/cerca.php?cercaProgrames=%s&txt_fInici=01/01/2004&txt_fFin=31/12/2035&Cercar_x=17&Cercar_y=18" % match[0]
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def videolist(item):
    logger.info("[barcelonatv.py] videolist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae los videos
    patron  = '<li>[^<]+'
    patron += '<div class="pro"><strong>[^<]+</strong>[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^>]+>[^<]+'
    patron += '</a>[^<]+'
    patron += '<h4>[^<]+</h4><span>([^<]+)</span></div>[^<]+'
    patron += '<div class="desc"><p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]+" ("+match[3]+")"
        scrapedurl = "http://www.barcelonatv.cat/alacarta/%s" % match[0]
        scrapedthumbnail = match[2]
        scrapedplot = match[4]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    # Extrae el enlace a la siguiente página
    patron  = "<a href='([^']+)'><img src='([^']+)' alt='Mes' title='Mes' id='botomes' /></a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def play(item):
    logger.info("[barcelonatv.py] play")

    # Averigua la URL y la descripcion
    data = scrapertools.cachePage(item.url)
    patron = '<PARAM NAME="url" VALUE="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        url = matches[0]
    except:
        url = ""

    patron = 'so.addVariable\("sinopsis", "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        scrapedplot = matches[0]
    except:
        scrapedplot = ""

    # Descarga el .ASX
    data = scrapertools.cachePage(url)
    patron = 'href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    try:
        url = matches[len(matches)-1]
    except:
        url = ""
    
    logger.info("[barcelonatv.py] scrapedplot="+scrapedplot)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail , plot=scrapedplot , server = "directo" , folder=False) )

    return itemlist