# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Extremadura TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

logger.info("[extremaduratv.py] init")

DEBUG = True
CHANNELNAME = "rtvv"
CHANNELCODE = "rtvv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtvv.py] mainlist")

    itemlist=[]
    url = "http://www.rtvv.es/alacarta/princiv.asp"

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las categorias (carpetas)
    patron = '<li><span><a href="(secciones.asp[^"]+)">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(url,match[0].replace("&amp;","&"))
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        scrapedtitle = unicode( scrapedtitle , "iso-8859-1" ).encode("utf-8")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , category=scrapedtitle , folder=True) )

    return itemlist

def videolist(item):
    logger.info("[rtvv.py] videolist")

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae los videos
    patron = '<div class="texto">.*?<a href="([^"]+)">([^<]+)(.*?)</div>.*?<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[1])
        patronfechas = "<p>Emissi&oacute;: ([^<]+)<"
        matchesfechas = re.compile(patronfechas,re.DOTALL).findall(match[2])
        if len(matchesfechas)>0:
            scrapedtitle = scrapedtitle + " (" + matchesfechas[0] + ")"

        scrapedurl = "http://www.rtvv.es/alacarta/secciones.asp"+match[0].replace("&amp;","&")
        scrapedthumbnail = urlparse.urljoin(item.url,match[3]).replace(" ","%20")
        
        scrapedplot = "%s" % match[2]
        scrapedplot = scrapedplot.strip()
        scrapedplot = scrapedplot.replace("</a>","")
        scrapedplot = scrapedplot.replace("</p>","")
        scrapedplot = scrapedplot.replace("<p>","")
        scrapedplot = scrapertools.entityunescape(scrapedplot)

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        scrapedtitle = unicode( scrapedtitle , "iso-8859-1" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot , "iso-8859-1" ).encode("utf-8")
        scrapedplot = scrapedplot.replace("EmissiÃ³","Emissió")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show="" , category=item.category , folder=True) )

    return itemlist

def getvideo(item):
    logger.info("[rtvv.py] play")

    # Descarga pagina detalle
    data = scrapertools.cachePage(item.url)
    patron = '<div id="reproductor">.*?<script.*?>.*?j_url="([^"]+)";.*?flashControl\("([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        url =  matches[0][1]+matches[0][0]
    except:
        url = ""
    logger.info("[rtvv.py] url="+url)
    
    # Amplia el argumento
    patron = '<div id="encuesta">\s*<div class="cab">.*?</div>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        plot = "%s" % matches[0]
        plot = plot.replace("<p>","")
        plot = plot.replace("</p>"," ")
        plot = plot.replace("<strong>","")
        plot = plot.replace("</strong>","")
        plot = plot.replace("<br />"," ")
        plot = plot.strip()
    
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , server="directo" , url=url, thumbnail=item.thumbnail, plot=plot , show=item.show , folder=False) )

    return itemlist