# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Movshare
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[bliptv.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Descarga la p�gina
    headers = [ ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],['Referer','http://www.movshare.net/'] ]
    data = scrapertools.cache_page(page_url , headers = headers)
    
    # La vuelve a descargar, como si hubieras hecho click en el bot�n
    data = scrapertools.cache_page(page_url , headers = headers)

    # Extrae el v�deo
    patronvideos  = 'flashvars.file="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        video_urls.append( [ "[movshare]" , match ] )

    for video_url in video_urls:
        logger.info("[movshare.py] %s - %s" % (video_url[0],video_url[1]))

    return matches[0]

# Encuentra v�deos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '"(http://www.movshare.net/video/[^"]+)"'
    logger.info("[movshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "'(http://www.movshare.net/embed/[^']+)'"
    logger.info("[movshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve