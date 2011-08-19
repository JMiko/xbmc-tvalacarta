# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para 4shared
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,httplib

from core import scrapertools
from core import logger
from core import config

import os

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[fourshared.py] get_video_url(page_url='%s')" % page_url)

    # http://www.4shared.com/embed/392975628/ff297d3f
    page_url = scrapertools.getLocationHeaderFromResponse(page_url)

    # http://www.4shared.com/flash/player.swf?file=http://dc237.4shared.com/img/392975628/ff297d3f/dlink__2Fdownload_2Flj9Qu-tF_3Ftsid_3D20101030-200423-87e3ba9b/preview.flv&d
    logger.info("[fourshared.py] redirect a '%s'" % page_url)
    patron = "file\=([^\&]+)\&"
    matches = re.compile(patron,re.DOTALL).findall(page_url)

    video_urls = [ ]
    
    try:
        video_urls.append([ "[fourshared]" , matches[0] ])
    except:
        pass

    for video_url in video_urls:
        logger.info("[fourshared.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra v�deos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = "(http://www.4shared.com/embed/[A-Z0-9a-z]+/[A-Z0-9a-z]+)"
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '"(http://www.4shared.com.*?)"'
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "'(http://www.4shared.com.*?)'"
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
