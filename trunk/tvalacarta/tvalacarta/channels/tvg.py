# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para TVG
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

logger.info("[tvg.py] init")

DEBUG = False
CHANNELNAME = "tvg"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tvg.py] mainlist")
    itemlist=[]

    url = "http://www.crtvg.es/TVGacarta/"

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las categorias (carpetas)
    patron = '<option>(.*?)\\n'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match.rstrip()
        if scrapedtitle.startswith("<I>"):
            scrapedtitle = scrapedtitle[3:-4]
        scrapedurl = "http://www.crtvg.es/tvgacarta/index.asp?tipo=" + scrapedtitle.replace(" ","+") + "&procura="
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" ).encode("utf-8")
        scrapedurl = unicode( scrapedurl, "iso-8859-1" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" ).encode("utf-8")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="programlist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show="" , category = scrapedtitle , folder=True) )

    return itemlist

def programlist(item):
    logger.info("[tvg.py] categorylist")
    itemlist=[]
    
    # Descarga la página
    posturl = item.url[:39]
    postdata = item.url[40:]
    logger.info("posturl="+posturl)
    logger.info("postdata="+postdata)
    data = scrapertools.cache_page(posturl,post=postdata)
    #logger.info(data)

    # Extrae las carpetas
    patron = '<table align="center" id="prog_front">[^<]+<tr>[^<]+<th class="cab">[^<]+<strong>([^<]+)</strong>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match.rstrip()
        scrapedurl = "http://www.crtvg.es/tvgacarta/index.asp?tipo=" + item.category.replace(" ","+") + "&procura=" + match.replace(" ","+")
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" ).encode("utf-8")
        scrapedurl = unicode( scrapedurl, "iso-8859-1" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" ).encode("utf-8")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, page=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=True) )

    return itemlist

def videolist(item):
    import urllib
    logger.info("[tvg.py] videolist")
    itemlist = []

    # Descarga la página
    posturl = item.url[:39]
    postdata = item.url[40:]
    logger.info("posturl="+posturl)
    logger.info("postdata="+postdata)
    data = scrapertools.cache_page(posturl,post=postdata)
    #logger.info(data)

    # Extrae los videos
    patron = '[^<]+<table class="video" onmouseover="[^"]+" onmouseout="[^"]+" onclick="javascript:AbreReproductor\(\'([^\']+)\'[^"]+" >[^<]+<tr>[^<]+<td rowspan="2" class="foto"><img src="([^"]+)"></td>[^<]+<td class="texto">(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        patron2 = "programa=([^&]+)&"
        matches2 = re.compile(patron2,re.DOTALL).findall(match[0])
        scrapedtitle = urllib.unquote_plus(matches2[0])

        patron2 = "fecha=([^&]+)&"
        matches2 = re.compile(patron2,re.DOTALL).findall(match[0])
        scrapedtitle = scrapedtitle + " (" + matches2[0] + ")"

        scrapedurl = "http://www.crtvg.es" + match[0].replace("&amp;","&").replace(" ","%20")
        scrapedthumbnail = "http://www.crtvg.es"+match[1]
        scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" ).encode("utf-8")
        scrapedurl = unicode( scrapedurl, "iso-8859-1" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" ).encode("utf-8")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=True) )

    return itemlist

def getvideo(item):
    logger.info("[tvg.py] play")
    itemlist = []

    # Descarga pagina detalle
    logger.info("[tvg.py] descarga "+item.url)
    data = scrapertools.cachePage(item.url)

    # Primer frame
    #<frame src="laterali.asp?canal=tele&amp;arquivo=1&amp;Programa=ALALÁ&amp;hora=09/02/2009 21:35:16&amp;fecha=03/02/2009&amp;id_Programa=7" name="pantalla" frameborder="0" scrolling="NO" noresize>
    patron = '<frame src="(laterali.asp[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    url = matches[0].replace("&amp;","&")
    url = url.replace(" ","%20")
    url = "http://www.crtvg.es/reproductor/"+url

    # Segundo frame
    #<frame src="ipantalla.asp?canal=tele&amp;arquivo=1&amp;Programa=ALALÁ&amp;hora=09/02/2009 21:35:16&amp;fecha=03/02/2009&amp;opcion=pantalla&amp;id_Programa=7" name="pantalla" frameborder="0" scrolling="NO" noresize>
    logger.info("[tvg.py] descarga "+url)
    data = scrapertools.cachePage(url)
    patron = '<frame src="(ipantalla.asp[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    url = matches[0].replace("&amp;","&")
    url = url.replace(" ","%20")
    url = "http://www.crtvg.es/reproductor/"+url

    # Video
    #<param name='url' value='http://www.crtvg.es/asfroot/acarta_tvg/ALALA_20090203.asx' />
    #<PARAM NAME="URL" value="http://www.crtvg.es/asfroot/acarta_tvg/ALALA_20090203.asx" />
    logger.info("[tvg.py] descarga "+url)
    data = scrapertools.cachePage(url)
    patron = '<PARAM NAME="URL" value="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches) == 0:
        logger.info("probando e.r. alternativa")
        patron = "<param name='url' value='([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
    
    url = matches[0]
    
    #<ASX VERSION="3.0"><TITLE>Televisi¾n de Galicia - ALAL-</TITLE><ENTRY><REF HREF="mms://media2.crtvg.es/videos_f/0007/0007_20090203.wmv"/><STARTTIME VALUE="0:00:00" />
    logger.info("[tvg.py] descarga "+url)
    data = scrapertools.cachePage(url)
    patron = 'HREF="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    url = matches[0]
    logger.info("url="+url)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail , plot=item.plot , server = "directo" , show = item.show , category = item.category , folder=False) )

    return itemlist