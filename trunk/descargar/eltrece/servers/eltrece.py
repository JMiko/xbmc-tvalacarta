# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para eltrece
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="", page_data="" ):
    logger.info("[eltrece.py] get_video_url(page_url='%s')" % page_url)

    #http://www.eltrecetv.com.ar/los-%C3%BAnicos/los-%C3%BAnicos-2012/00052062/cap%C3%ADtulo-28-los-%C3%BAnicos
    data = scrapertools.cache_page(page_url)

    # Gracias a susi por la pista http://blog.tvalacarta.info/2011/02/11/como-descargar-videos-de-el-trece-tv-argentina/comment-page-3/#comment-46245
    final_url = scrapertools.get_match(data,"data-video='13tv([^']+)'")
    url = "http://ctv.eltrecetv.com.ar"+final_url
    extension = scrapertools.get_filename_from_url(url)[-4:]
    
    video_urls = []
    video_urls.append( [ extension+" [eltrece]" , url ] )

    for video_url in video_urls:
        logger.info("[eltrece.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    return devuelve

