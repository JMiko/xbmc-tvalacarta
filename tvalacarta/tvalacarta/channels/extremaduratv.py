# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Extremadura TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "extremaduratv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[extremaduratv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Informativos"   , action="programas"    , url="http://alacarta.canalextremadura.es/tv/informativos/alfabetico") )
    itemlist.append( Item(channel=CHANNELNAME, title="Programas"      , action="programas"    , url="http://alacarta.canalextremadura.es/tv/programas/alfabetico") )
    itemlist.append( Item(channel=CHANNELNAME, title="Deportes"       , action="programas"    , url="http://alacarta.canalextremadura.es/tv/deportes/alfabetico") )
    itemlist.append( Item(channel=CHANNELNAME, title="Archivo"        , action="programas"    , url="http://alacarta.canalextremadura.es/tv/archivo/alfabetico") )

    return itemlist

def programas(item):
    logger.info("[extremaduratv.py] categorias")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = '<span class="field-content"><a href="([^"]+)" title="Ver ficha del programa">([^<]+)</a></span>'
    matches = re.findall(patron,data,re.DOTALL)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, show=scrapedtitle) )

    return itemlist

def episodios(item):
    logger.info("[extremaduratv.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <li class="views-row views-row-5 views-row-odd">  
    <div class="views-field-field-video-imagen-fid">
    <span class="field-content"><a href="/tv/videos/extremadura-desde-el-aire-1" class="imagecache imagecache-imagen_carrusel_pie imagecache-linked imagecache-imagen_carrusel_pie_linked"><img src="http://alacarta.canalextremadura.es/sites/default/files/imagecache/imagen_carrusel_pie/S-B4885-005_0.jpg" alt="Ver video o escuchar audio" title="Ver video o escuchar audio"  class="imagecache imagecache-imagen_carrusel_pie" width="416" height="234" /></a></span>
    </div>    
    <div class="views-field-title">
    <span class="field-content"><a href="/tv/videos/extremadura-desde-el-aire-1" title="Ver video o escuchar audio">Extremadura desde el aire</a></span>
    </div>
    <div class="views-field-field-video-descripcion-corta-value">
    <div class="field-content"><p>UN CANTO DE CERCANIAS</p></div>
    </div>
    </li>
    '''
    '''
    <div class="views-field-field-video-imagen-fid">
    <span class="field-content"><a href="/tv/videos/esfera-180312" class="imagecache imagecache-imagen_carrusel_pie imagecache-linked imagecache-imagen_carrusel_pie_linked"><img src="http://alacarta.canalextremadura.es/sites/default/files/imagecache/imagen_carrusel_pie/PROG00054173_2.jpg" alt="" title=""  class="imagecache imagecache-imagen_carrusel_pie" width="416" height="234" /></a></span>
    </div>
    <div class="views-field-title">
    <span class="field-content"><a href="/tv/videos/esfera-180312" title="Ver video o escuchar audio">Esfera (18/03/12)</a></span>
    </div>    
    <div class="views-field-field-video-descripcion-corta-value">
    <div class="field-content"></div>
    </div>
    '''
    patron  = '<img src="([^"]+)".*?'
    patron += '<div class="views-field-title">[^<]+'
    patron += '<span class="field-content"><a href="([^"]+)" title="Ver video o escuchar audio">([^<]+)</a></span>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="views-field-field-video-descripcion-corta-value">[^<]+'
    patron += '<div class="field-content">(.*?)</div>[^<]+'
    patron += '</div>'
    matches = re.findall(patron,data,re.DOTALL)

    for thumbnail,url,titulo,subtitulo in matches:
        scrapedtitle = titulo + " - " + scrapertools.htmlclean(subtitulo).strip()
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail = scrapedthumbnail, show=item.show, folder=False) )

    patron = '<li class="pager-next"><a href="([^"]+)" title="Ir a la p'
    matches = re.findall(patron,data,re.DOTALL)

    for url in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="episodios" , url=scrapedurl, show=item.show) )


    return itemlist

def play(item):
    logger.info("[extremaduratv.py] play")
    itemlist = []

    # Descarga la página
    '''
    data = scrapertools.cachePage(item.url)
    patron  = '<div id="mediaplayer" rel="([^"]+)"></div>'
    matches = re.findall(patron,data,re.DOTALL)

    for url in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail = item.thumbnail, show=item.show, folder=False) )
    '''
    headers = []
    headers.append( ["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"] )
    data = scrapertools.cachePage(item.url,headers=headers)
    patron = "<video.*?src ='([^']+)'"
    matches = re.findall(patron,data,re.DOTALL)

    for url in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail = item.thumbnail, show=item.show, folder=False) )

    return itemlist
