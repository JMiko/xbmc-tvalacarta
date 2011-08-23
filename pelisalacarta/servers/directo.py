# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vídeos directos (urls simples)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import urllib

from core import scrapertools
from core import logger

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[directo.py] get_video_url(page_url='%s')" % page_url)

    video_urls = [["%s [directo]" % page_url[-4:] , page_url]]

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # mysites.com
    patronvideos  = "(http://[a-zA-Z0-9]+\.mysites\.com\/get_file\/.*?\.mp4)"
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        partes = match.split("/")
        filename = partes[len(partes)-1]
        titulo = filename+" [directo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve