# -*- coding: utf-8 -*-
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

__channel__ = "hispantv"
__category__ = "F"
__type__ = "generic"
__title__ = "hispantv"
__language__ = "ES"
__creationdate__ = "20121130"
__vfanart__ = "http://www.dw.de/cssi/dwlogo-print.gif"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[hispantv.py] mainlist")    
    itemlist = []

    item.url="http://www.hispantv.es/programs.aspx"
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="ProgDiv">
    <div class="ImageDiv">
    <img class="Image" alt="iran" src="/images/prog_logos/351010515.jpg"/>
    </div>
    <div class="HSpacer"></div>
    <div class="TextDiv">
    <div class="TextTitle"><a href="/section.aspx?id=351010515">El Color del Dinero</a></div>
    <div class="TextBody">
    Programa que analiza temas económicos, y en especial la crisis económica europea y sus consecuencias en la Unión Europea.
    </div>
    </div>
    '''
    patron  = '<div class="ProgDiv"[^<]+'
    patron += '<div class="ImageDiv"[^<]+'
    patron += '<img class="Image" alt="[^"]+" src="([^"]+)"/[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="HSpacer"></div[^<]+'
    patron += '<div class="TextDiv"[^<]+'
    patron += '<div class="TextTitle"><a href="([^"]+)">([^<]+)</a></div[^<]+'
    patron += '<div class="TextBody">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedthumbnail,scrapedurl,scrapedtitle,scrapedplot in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = scrapedplot.strip()
        itemlist.append( Item(channel=__channel__, action="videos", title=title, url=url, thumbnail=thumbnail,  plot=plot, folder=True))

    return itemlist

def videos(item):
    logger.info("[hispantv.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
    logger.info(data)
    '''
    <div style="width:100%;float:left;height:20px;"></div></div><div style="width:100%;float:left;border-bottom:solid 1px #dddddd;height:120px;"><div style="width:100%;float:left;height:20px;"></div>
    <div style="width:100%;float:left;height:80px;"><div style="width:140px;overflow:hidden;float:left;height:80px;">
    <img alt="CategoryDetail" src="sp_photo/20121202/mrg pregunta.jpg" style="height:80px;width:140px;"/></div><div style="width:20px;overflow:hidden;float:left;height:80px;"></div>
    <div style="width:470px;text-align:left;overflow:hidden;float:left;height:80px;">
    <div class="CatPageDetailTitle"><a class="CatPageDetailTitleLink" href="/detail/2012/12/02/203768/una-pregunta-sencilla-actos-patrioticos">Una pregunta sencilla - Actos patrióticos</a></div>
    <div class="CatPageDetailDetail">Petróleo, preguntas sencillas, muchas respuestas.
    
    En este episodio escucharemos las respuestas de las siguientes preguntas:
    ¿Qué provoca la drásti ...</div><div class="CatPageDetailDate">02/12/2012 05:00 GMT</div></div></div><
    '''
    patron  = '<img alt="CategoryDetail" src="([^"]+)".*?'
    patron += '<a class="CatPageDetailTitleLink" href="([^"]+)">([^<]+)</a></div[^<]+'
    patron += '<div class="CatPageDetailDetail">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedthumbnail,scrapedurl,scrapedtitle,scrapedplot in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail).replace(" ","%20")
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = scrapedplot.strip()
        itemlist.append( Item(channel=__channel__, action="play", title=title, url=url, thumbnail=thumbnail, plot=plot, folder=False))
        
    return itemlist

def play(item):
    logger.info("[hispantv.py] play")    
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    itemlist = []
    
    #videoFile='/video/20121205/Una_pregunta_sencilla_20121205_P12.flv'
    patron = "videoFile\='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        # "rtmp://64.150.186.181/vod playpath=mp4:hispantv/20130627/Recorridos_urbanos_P74_(Asentamientos_ilegales_en_Uruguay)_new.mp4"
        playpath = match.replace("/video/","mp4:hispantv/")
        url = "rtmp://64.150.186.181/vod playpath="+playpath
        itemlist.append( Item(channel=__channel__, action="play",  server="directo",  title=item.title, url=url, folder=False))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Mainlist es la lista de programas
    programas_items = mainlist(Item())
    if len(programas_items)==0:
        print "No encuentra los programas"
        return False

    episodios_items = videos(programas_items[0])
    if len(episodios_items)==0:
        print "El programa '"+programas_items[0].title+"' no tiene episodios"
        return False

    return True
