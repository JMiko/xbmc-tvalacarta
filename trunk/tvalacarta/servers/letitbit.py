# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para letitbit
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[letitbit.py] test_video_exists(page_url='%s')" % page_url)

    # Existe: http://letitbit.net/download/12300.151ef074afcb8f56a43d97bd64ef/Nikita.S02E15.HDTV.XviD-ASAP.avi.html
    # No existe: 
    data = scrapertools.cache_page(page_url)
    patron  = '<h1 class="file-info[^"]+" title="[^"]+">File: <a href="[^"]+" target="_blank"><span>([^<]+)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        return True,""
    else:
        patron  = '<p style="color:#000">(File not found)</p>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            return False,"File not found"
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[letitbit.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://letitbit.net/download/12300.151ef074afcb8f56a43d97bd64ef/Nikita.S02E15.HDTV.XviD-ASAP.avi.html
    patronvideos  = '(http://letitbit.net/download/.*?\.html)'
    logger.info("[letitbit.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[letitbit]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'letitbit' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
