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

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[dailymotion.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    data = scrapertools.cache_page(page_url)
    sequence = re.compile('"sequence",  "(.+?)"').findall(data)
    newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')
    imgSrc = re.compile('og:image" content="(.+?)"').findall(data)
    if(len(imgSrc) == 0):
            imgSrc = re.compile('/jpeg" href="(.+?)"').findall(data)
    dm_low = re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
    dm_high = re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
    videoUrl = ''
    if(len(dm_high) == 0):
        videoUrl = dm_low[0]
    else:
        videoUrl = dm_high[0]
            
    video_urls.append( [ "[dailymotion]",videoUrl ] )

    for video_url in video_urls:
        logger.info("[dailymotion.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.dailymotion.com/embed/video/xrva9o
    patronvideos  = 'dailymotion.com/embed/video/([a-z0-9]+)'
    logger.info("[dailymotion.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[dailymotion]"
        url = "http://www.dailymotion.com/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'dailymotion' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.dailymotion.com/video/xrva9o
    patronvideos  = 'dailymotion.com/video/([a-z0-9]+)'
    logger.info("[dailymotion.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[dailymotion]"
        url = "http://www.dailymotion.com/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'dailymotion' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve