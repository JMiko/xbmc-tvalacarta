# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para ustream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
try:
    import json
except:
    import simplejson as json

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[ustream.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    headers=[ ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:14.0) Gecko/20100101 Firefox/14.0.1"] ]
    location = scrapertools.get_header_from_response(page_url, header_to_get="location")
    logger.info("[ustream.py] location="+location)

    page_url = urlparse.urljoin(page_url,location)
    logger.info("[ustream.py] page_url="+page_url)
    
    data = scrapertools.cache_page("http://piscui.webear.net/ustream.php?url="+page_url,headers=headers)
    logger.info("data="+data)

    video_url = scrapertools.get_match(data,'<textarea rows=3 cols=70>(.*?)</textarea>')

    logger.info("video_url="+video_url)

    if video_url!="":
        video_urls.append( [ "[ustream]" , video_url ] )

    for video_url in video_urls:
        logger.info("[ustream.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.ustream.tv/embed/4700613
    patronvideos  = 'ustream.tv/embed/(\d+)'
    logger.info("[ustream.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[ustream]"
        url = "http://www.ustream.tv/channel-popup/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'ustream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
