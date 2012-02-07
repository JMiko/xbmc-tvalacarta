# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para modovideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, urlparse, urllib, urllib2
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[modovideo.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []
    page_url = 'http://www.modovideo.com/frame.php?v='+page_url
    data = scrapertools.cachePage(page_url)
    logger.info("data")

    # Extrae la URL real
    patronvideos  = 'player5plugin.video=([^&]+)&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    for match in matches:
        video_urls.append(["[modovideo]",match])

    for video_url in video_urls:
        logger.info("[modovideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    #http://www.modovideo.com/frame.php?v=qzyrxqsxacbq3q43ssyghxzqkp35t8rh
    patronvideos  = 'http://www.modovideo.com/(?:frame|video)\.php\?v=([a-zA-Z0-9]+)' 
    logger.info("[modovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Modovideo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'modovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #logger.info("1) Modovideo formato Peliculasaudiolatino") #http://www.peliculasaudiolatino.com/show/modovideo.php?url=qzyrxqsxacbq3q43ssyghxzqkp35t8rh
    patronvideos  = "modovideo.php\?url=([a-zA-Z0-9]+)"
    logger.info("[modovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Modovideo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'modovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve