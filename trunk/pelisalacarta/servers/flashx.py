# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para flashx
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
    logger.info("[flashx.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    #http://flashx.tv/video/4KB84GO238XX/themakingofalady720phdtvx264-bia
    hash = scrapertools.get_match(page_url,"flashx.tv/video/([A-Z0-9]+)")
    url = "http://play.flashx.tv/nuevo/player/cst.php?hash="+hash
    data = scrapertools.cache_page(url)
    media_url = scrapertools.get_match(data,"<file>([^<]+)</file>")
    
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [flashx]",media_url])

    for video_url in video_urls:
        logger.info("[flashx.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://flashx.tv/video/4KB84GO238XX/themakingofalady720phdtvx264-bia
    data = urllib.unquote(data)
    patronvideos  = '(flashx.tv/video/[A-Z0-9]+/[a-z0-9\-]+)'
    logger.info("[flashx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[flashx]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'flashx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
