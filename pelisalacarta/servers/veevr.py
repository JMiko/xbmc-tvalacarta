# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de veevr
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[veevr.py] get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    video_urls = []
    #Busca video url: 'http://hwcdn.net/q7r3a8u2/cds/03254f3d816f4aef88159cf43ea0a004.mp4%3Fbitrate=1327434002%26token=bf5c0721f08fdc99f1a8485fcbe04faa', //provider: 'rtmp',
    patron  = "url[\W] '([^']+)'[\W][\W]+"
    patron += "provider[\W]"
    matches = re.compile(patron,re.DOTALL).findall(data)
    # si no encuentra lo intentamos con el embed
    if len(matches)==0:
        page_url = page_url.replace("videos","embed") +"?w=607&h=280"
        data = scrapertools.cache_page(page_url)
        matches = re.compile(patron,re.DOTALL).findall(data)

    scrapertools.printMatches(matches)
    encontrados = set()
    for match in matches:
        videourl = match
        logger.info(match)
        videourl = videourl.replace('%5C','')
        videourl = urllib.unquote(videourl)

        if videourl not in encontrados:
            video_urls.append( [ "[veevr]" , videourl ] )
            encontrados.add(videourl)

    for video_url in video_urls:
        logger.info("[veevr.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    
    # veevr http://veevr.com/videos/kgDAMC4Btp"
    patronvideos  = 'http://veevr.[\w]+/videos/([\w]+)'
    logger.info("[veevr.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veevr]"
        url = "http://veevr.com/videos/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veevr' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    # veevr http://veevr.com/embed/kgDAMC4Btp"
    patronvideos  = 'http://veevr.[\w]+/embed/([\w]+)'
    logger.info("[veevr.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veevr]"
        url = "http://veevr.com/videos/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veevr' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve
