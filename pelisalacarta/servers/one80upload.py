# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para 180upload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[one80upload.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://180upload.com/rtp8y30mlfj0
    #http%3A%2F%2F180upload.com%2F5k344aiotajv
    data = urllib.unquote(data)
    patronvideos  = '(180upload.com/[a-z0-9]+)'
    logger.info("[one80upload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[180upload]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'one80upload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
