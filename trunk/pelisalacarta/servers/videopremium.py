# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videopremium
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
    logger.info("[videopremium.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    data = scrapertools.cache_page( page_url )
    location = scrapertools.get_match(data,"url\: '([^']+)'")
    
    import urlparse
    parsed_url = urlparse.urlparse(location)
    
    video_urls.append( [ parsed_url.path[-4:] + " [videopremium]",location ] )

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #<a href="http://videopremium.net/0yo7kkdsfdh6/21.Jump.Street.2012.Subbed.ITA.DVDRIP.XviD-ZDC.CD1.avi.flv.html" target="_blank">1° Tempo</a>
    patronvideos  = '<a href="(http://videopremium.net[^"]+)"[^>]+>([^<]+)</a>'
    logger.info("[videopremium.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1]+" [videopremium]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videopremium' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

    #http://videopremium.net/0yo7kkdsfdh6/21.Jump.Street.2012.Subbed.ITA.DVDRIP.XviD-ZDC.CD1.avi.flv.html
    patronvideos  = '(videopremium.net/[a-z0-9]+)'
    logger.info("[videopremium.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videopremium]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videopremium' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
