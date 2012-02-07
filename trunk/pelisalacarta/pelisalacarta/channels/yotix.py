# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yotix
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "yotix"
__category__ = "A"
__type__ = "generic"
__title__ = "Yotix.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[yotix.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="series"         , title="Novedades", url="http://yotixanime.com/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias" , title="Listado por categorías", url="http://yotix.tv/"))
    itemlist.append( Item(channel=__channel__, action="search"         , title="Buscador", url="http://yotix.tv/?s=%s"))

    return itemlist

def search(item,texto):
    logger.info("[yotix.py] search")

    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://yotix.tv/?s=%s"

        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto

        # Devuelve los resultados
        return videolist(item)
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def listcategorias(item):
    logger.info("[yotix.py] listcategorias")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    patron  = '<a href="(/categoria/[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="videolist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def series(item):
    logger.info("[yotix.py] videolist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    '''
    <a title="Ver Serie Pokemon Fuerza Máxima (sexta temporada)" href="http://yotixanime.com/pokemon-fuerza-maxima-sexta-temporada/"><img class="imagen" src="http://yotixanime.com/caratula/Pokemon-06.jpg" border="0" /></a><p>Su desarrollo comienza en la región Hoenn desde Pueblo Littleroot a Ciudad Mauville. Ash conoce a May y su hermano Max y con la compañía de Brock inician su viaje, durante el cual Ash colecta medallas para participar en la Liga Hoenn mientras que May participa en los concursos de coordinadores para llegar al Gran Festival.</p>
    '''
    patron  = '<a title="([^"]+)" href="([^"]+)"><img class="imagen" src="([^"]+)"[^>]+></a>(.*?)<div'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []

    for scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot in matches:
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la página siguiente
    patron = '<a href="([^"]+)" class="nextpostslink">»'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Pagina siguiente >>"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapeddescription = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def episodios(item):
    logger.info("[yotix.py] episodios")
    itemlist=[]
    
    data = scrapertools.cachePage(item.url)
    patronvideos  = '<a class="azul" href="([^"]+)" target="_blank">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot))

    return itemlist