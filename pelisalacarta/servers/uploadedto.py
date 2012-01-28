# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para uploaded.to
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[uploadedto.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://uploaded.to/file/1haty8nt
    patronvideos  = '(http://uploaded.to/file/[a-zA-Z0-9]+)'
    logger.info("[uploadedto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[uploaded.to]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'uploadedto' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://ul.to/mjphp9hl
    patronvideos  = '(http://ul.to/[a-zA-Z0-9]+)'
    logger.info("[uploadedto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[uploaded.to]"
        url = match.replace("http://ul.to/","http://uploaded.to/file/")
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'uploadedto' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
