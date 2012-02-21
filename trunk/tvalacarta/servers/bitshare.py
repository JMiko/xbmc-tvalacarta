# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para bitshare
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[bitshare.py] test_video_exists(page_url='%s')" % page_url)

    # Existe: http://bitshare.com/files/v1ehsvu3/Nikita.S02E15.HDTV.XviD-ASAP.avi.html
    # No existe: 
    data = scrapertools.cache_page(page_url)
    patron  = '<h1>Descargando([^<]+)</h1>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        return True,""
    else:
        patron  = '<h1>(Error - Archivo no disponible)</h1>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            return False,"File not found"
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[bitshare.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://bitshare.com/files/tn74w9tm/Rio.2011.DVDRip.LATiNO.XviD.by.Glad31.avi.html
    patronvideos  = '(http://bitshare.com/files/[^/]+/.*?\.html)'
    logger.info("[bitshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitshare]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve
