# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mediafire
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mediafire.py] get_video_url(page_url='%s')" % page_url)
    video_urls=[]
    
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    patron = '<a href="([^"]+)" onclick="avh\(this\)[^"]+">Download'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        video_urls.append( ["[mediafire]",matches[0] ] )

    for video_url in video_urls:
        logger.info("[mediafire.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls        

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www.mediafire.com/?4ckgjozbfid
    patronvideos  = '(http://www.mediafire.com/\?[a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Encontrado en animeflv
    #s=mediafire.com%2F%3F7fsmmq2144fx6t4|-|wupload.com%2Ffile%2F2653904582
    patronvideos  = 'mediafire.com\%2F\%3F([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = "http://www.mediafire.com/?"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
