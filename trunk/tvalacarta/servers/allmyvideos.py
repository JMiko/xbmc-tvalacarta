# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[allmyvideos.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allmyvideos.net/fg85ovidfwxx
    patronvideos  = '(http://allmyvideos.net/[a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
