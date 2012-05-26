# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para hulkshare
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
    logger.info("[hotfile.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    location = scrapertools.get_header_from_response(page_url, header_to_get="location")
    import urlparse
    parsed_url = urlparse.urlparse(location)
    
    video_urls.append( [ parsed_url.path[-4:] + " [hulkshare]",location ] )
    
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www.hulkshare.com/dl/bp62cf2510h8
    patronvideos  = '(hulkshare.com/dl/[a-z0-9]+)'
    logger.info("[hulkshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[hulkshare]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'hulkshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
