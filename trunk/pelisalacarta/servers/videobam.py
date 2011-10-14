# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de videobam
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videobam.py] get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    video_urls = []

    patronSD= " low: '([^']+)'" 
    matches = re.compile(patronSD,re.DOTALL).findall(data)
    for match in matches:
        videourl = match
        video_urls.append( [ "SD [videobam]" , videourl ] )
        
    patronHD = " high: '([^']+)'"
    matches = re.compile(patronHD,re.DOTALL).findall(data)
    for match in matches:
        videourl = match
        video_urls.append( [ "HD [videobam]" , videourl ] )

    for video_url in video_urls:
        logger.info("[videobam.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # VideoBam para AnimeID    src="http://videobam.com/widget/USezW"
    patronvideos  = 'http://videobam.com/widget/([^"]+)'
    logger.info("[videobam.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobam]"
        url = "http://videobam.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobam' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
                    
    return devuelve
