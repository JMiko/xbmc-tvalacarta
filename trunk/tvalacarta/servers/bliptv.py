# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para blip.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import urllib
from core import scrapertools
from core import logger

# Resuelve los videos de blip.tv que se usan en el embed
# 
def geturl(bliptv_url,recurse=True):
    logger.info("[bliptv.py] bliptv_url="+bliptv_url)

    devuelve = ""

    if bliptv_url.startswith("http://blip.tv/play"):    
        redirect = scrapertools.getLocationHeaderFromResponse(bliptv_url)
        logger.info("[bliptv.py] redirect="+redirect)
        
        patron='http\://a.blip.tv/scripts/flash/stratos.swf\?file\=([^\&]+)\&'
        matches = re.compile(patron).findall(redirect)
        
        if len(matches)>0:
            url = matches[0]
            logger.info("[bliptv.py] url="+url)
            url = urllib.unquote(url)
            logger.info("[bliptv.py] url="+url)

            data = scrapertools.cache_page(url)
            patron = '<media\:content url\="([^"]+)" blip\:role="([^"]+)".*?type="([^"]+)"[^>]+>'
            matches = re.compile(patron).findall(data)

            for match in matches:
                print match
                devuelve = match[0]

    return devuelve