# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para dailymotion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Basado en el resolver hecho por Shailesh Ghimire para su plugin "canadanepal"
# http://code.google.com/p/canadanepal-xbmc-plugin/source/browse/script.module.urlresolver/lib/urlresolver/plugins/dailymotion.py?name=Version_0.0.1
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[dailymotion.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    data = scrapertools.cache_page(page_url)
    sequence = re.compile('"sequence":"(.+?)"').findall(data)
    newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')

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

    # <a href="http://www.dailymotion.com/video/xssekp_natgeo-huesos-con-historia-08-los-esqueletos-de-windy-pits_tech" target="_blank">[Natgeo] Huesos con Historia 08 - Los Esqueletos de Windy Pits</a><br />
    patronvideos  = '<a href=".*?dailymotion.com/video/([a-z0-9]+)[^>]+([^<]+)</a>'
    logger.info("[dailymotion.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for url,title in matches:
        titulo = title[1:]+" [dailymotion]"
        url = "http://www.dailymotion.com/video/"+url
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
