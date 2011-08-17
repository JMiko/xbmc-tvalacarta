# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, sys
import urlparse, urllib, urllib2

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[adnstream.py] get_video_url(page_url='%s')" % page_url)

    # TODO: Esto sólo funciona con el ID del vídeo, no con la URL
    code = page_url
    
    mediaurl = "http://www.adnstream.tv/get_playlist.php?lista=video&param="+code+"&c=463"
    data = scrapertools.cachePage(mediaurl)

    # Extrae la URL real
    patronvideos   = '<guid>' +code+ '</guid>.*?'
    patronvideos  += 'video/x-flv" url="(.*?)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        video_urls = [['[adnstream]' , matches[0]]]
    else:
        video_urls = []

    return video_urls

