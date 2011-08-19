# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videoweed
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, urlparse, urllib, urllib2
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videoweed.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Descarga la p�gina de linkbucks
    data = scrapertools.cachePage(page_url)

    # Extrae la URL real
    patronvideos  = 'flashvars.file="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    for match in matches:
        video_urls.append(["[videoweed]",match])

    for video_url in video_urls:
        logger.info("[videoweed.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra v�deos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '(http://www.videoweed.[a-z]+/file/[a-zA-Z0-9]+)'
    logger.info("[videoweed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Videoweed]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videoweed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #logger.info("1) Videoweed formato islapeliculas") #http://embed.videoweed.com/embed.php?v=h56ts9bh1vat8
    patronvideos  = "(http://embed.videoweed.*?)&"
    logger.info("[videoweed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Videoweed]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videoweed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve