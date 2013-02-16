# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para adnstream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, sys
import urlparse, urllib, urllib2

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[adnstream.py] get_video_url(page_url='%s')" % page_url)

    if page_url.startswith("http:"):
        id_video = scrapertools.get_match(item.url,".*?video/([^/]+)/")
    else:
        id_video = page_url

    data = scrapertools.cache_page("http://www.adnstream.com/get_playlist.php?lista=video&param="+id_video)
    media_url = scrapertools.get_match(data,'<media.content type="[^"]+" url="([^"]+)"')
    video_urls = [[ scrapertools.get_filename_from_url(media_url)[-4:]+' [adnstream]' , media_url]]

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    logger.info("[adnstream.py] find_videos")
    return []
