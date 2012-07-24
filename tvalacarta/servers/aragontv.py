# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para aragontv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="", page_data="" ):
    logger.info("[aragontv.py] get_video_url(page_url='%s')" % page_url)

    # ANTES
    #url:'mp4%3A%2F_archivos%2Fvideos%2Fweb%2F2910%2F2910.mp4',
    #netConnectionUrl: 'rtmp%3A%2F%2Falacarta.aragontelevision.es%2Fvod'
    #rtmp://iasoftvodfs.fplive.net/iasoftvod/web/980/980.mp4

    # AHORA
    #{ url:'mp4%3A%2Fweb%2F5573%2F5573.mp4', provider: 'rtmp' }
    #netConnectionUrl: 'rtmp%3A%2F%2Faragontvvodfs.fplive.net%2Faragontvvod'
    #rtmp://iasoftvodfs.fplive.net/iasoftvod/web/980/980.mp4
    
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(page_url)
    final = scrapertools.get_match(data,"url\:'(mp4\%3A[^']+)'")
    principio = scrapertools.get_match(data,"netConnectionUrl\: '([^']+)'")

    if urllib.unquote(principio).startswith("rtmp://aragon") or urllib.unquote(principio).startswith("rtmp://iasoft"):
        url = principio+"/"+final[9:]
    else:
        url = principio+"/"+final
    url = urllib.unquote(url)
    logger.info("url="+url)

    video_urls = []
    video_urls.append( [ "RTMP [aragontv]" , url ] )

    for video_url in video_urls:
        logger.info("[aragontv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    return devuelve

