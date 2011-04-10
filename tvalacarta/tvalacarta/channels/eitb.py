# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para EITB
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

try:
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

logger.info("[eitb.py] init")

DEBUG = False
CHANNELNAME = "eitb"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[eitb.py] mainlist")
    itemlist=[]

    url = 'http://www.eitb.com/videos/'

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los programas
    patron = '<li><a href="(/videos/[^"]+)" title="[^"]+"><span>([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def videolist(item):
    logger.info("[eitb.py] videolist")
    itemlist=[]

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los programas
    # --------------------------------------------------------
    patron  = '<li>[^<]*<a href="([^"]+)"[^>]+>[^<]*'
    patron += '<span><img[^>]+></span>[^<]*'
    patron += '<img src="([^"]+)".*?'
    patron += '<div class="info_medio">[^<]*<h3[^<]+'
    patron += '<a[^>]+>\s*([^<]+)</a>'
    patron += '.*?<ul class="lst_info_extra">.*?</ul>'
    patron += '(.*?)<ul class="lst_info_extra">.*?</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG:
        scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[2].strip()
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        
        # procesa el resto
        plot = "%s" % match[3]
        plot = plot.strip()
        plot = plot.replace("</p>","")
        plot = plot.replace("<p>","")
        #plot = common.ConvertHTMLEntities(descripcion)
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    # Página siguiente
    patron  = '<li><a href="(/videos[^"]+)">(Siguiente)[^<]+</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        match = matches[0]
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    # Subcarpetas
    patron  = '<li><a href="(/videos/[^"]+)" title="[^"]+" class="">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def getvideo(item):
    logger.info("[eitb.py] getvideo")

    # Averigua la URL y la descripcion
    data = scrapertools.cachePage(item.url)
    patron = '<a id="descargaMp4" href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        url = urlparse.urljoin(item.url,matches[0])
    except:
        url = ""

    logger.info("[eitb.py] url="+url)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail , plot=item.plot , server = "directo" , folder=False) )

    return itemlist