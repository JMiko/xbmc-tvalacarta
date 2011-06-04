# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC addon
# Server connector para Antena 3
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG=True

def get_movie_links(url,data=""):
    logger.info("[antena3.py] get_movie_links( url="+url+",data=")

    itemlist = []
    # Descarga la página de detalle y extrae el nombre del XML
    data = scrapertools.cache_page(url,modo_cache=scrapertools.CACHE_NUNCA)
    patron = "player_capitulo.xml='([^']+)';"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    scrapedurl = urlparse.urljoin(url,matches[0])
    logger.info("url="+scrapedurl)
    
    # Descarga el XML y extrae el vídeo y el thumbnail
    data = scrapertools.cache_page(scrapedurl,modo_cache=scrapertools.CACHE_NUNCA)
    
    # Extrae la URL base del vídeo
    patron = '<urlVideoMp4><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    baseurlvideo = matches[0]
    logger.info("baseurlvideo="+baseurlvideo)
    
    # Extrae la URL base el thumbnail
    patron = '<urlImg><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    baseurlthumb = matches[0]
    logger.info("baseurlthumb="+baseurlthumb)
    
    # Extrae el título
    patron = '<descripcion><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    programa = matches[0]
    logger.info("programa="+programa)
    
    patron = '<nombre><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    episodio = matches[0]
    logger.info("episodio="+episodio)
    
    # Extrae el thumbnail
    patron  = '<archivoMultimediaMaxi>[^<]+'
    patron += '<archivo><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapedthumbnail = urlparse.urljoin(baseurlthumb,matches[0])
    logger.info("scrapedthumbnail="+scrapedthumbnail)
    
    # Extrae los fragmentos del vídeo
    patron  = '<archivoMultimedia>[^<]+'
    patron += '<archivo><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    i = 1
    for match in matches:
        scrapedurl = baseurlvideo+match
        logger.info("scrapedurl="+scrapedurl)
        itemlist.append( Item( title=programa + " - " + episodio , url=scrapedurl , thumbnail=scrapedthumbnail ) )
        i=i+1

    return itemlist
