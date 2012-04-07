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

    #http://www.eltrecetv.com.ar/los-unicos-2012/video/54380/capitulo-28-los-unicos
    video_id = scrapertools.get_match(page_url,"http://www.eltrecetv.com.ar/[a-z0-9\-]+/video/(\d+)/[a-z0-9\-]+")
    
    # Truco genial, gracias a Gastón (http://blog.tvalacarta.info/2011/02/11/como-descargar-videos-de-el-trece-tv-argentina/comment-page-2/#comment-32325)
    url = "http://www.eltrecetv.com.ar/feed/videowowza/"+video_id
    data = scrapertools.cache_page(url)
    videourl = scrapertools.get_match(data,'<media:content url="([^"]+)"')
    
    video_urls = []
    video_urls.append( [ "[eltrece]" , videourl ] )

    for video_url in video_urls:
        logger.info("[eltrece.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # divxstage http://www.divxstage.net/video/2imiqn8w0w6dx"
    patronvideos  = 'http://www.divxstage.[\w]+/video/([\w]+)'
    logger.info("[telefe.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[telefe]"
        url = "http://www.divxstage.net/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'divxstage' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve

