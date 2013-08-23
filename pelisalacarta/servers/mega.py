# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mega.co.nz
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mega.py] get_video_url(page_url='%s')" % page_url)
    #data = scrapertools.cache_page(page_url)
    video_urls = []
    url_service2 = ""
    url_service1 = ""
    #patronurl = 'https://mega.co.nz/(.*?)[<"\']'
    #matches = re.compile(patronurl,re.DOTALL).findall(data)

    #for scrapedurl in matches:
    url_service1 = scrapedurl
    url_service1 = "https://mega.co.nz/" + url_service1
    url_service1 = url_service1.replace("https://mega.co.nz/#!","http://megastreamer.net/mega_stream.php?url=https%3A%2F%2Fmega.co.nz%2F%23%21")
    url_service1 = url_service1.replace("!","%21")
    url_service1 = url_service1 + "&mime=vnd.divx"
    logger.info("[mega.py] video urlappend'%s')" % url_service1)
    video_urls.append(["Megastreamer.net",url_service1])

    url_service2 = scrapedurl.replace("#!","")
    url_service2 = url_service2.replace("!","&key=")
    url_service2 = "http://mega-stream.me/stream.php?ph="+url_service2
    logger.info("[mega.py] video urlappend'%s')" % url_service2)
    video_urls.append(["Mega-stream.me",url_service2])
    
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    #https://mega.co.nz/#!TNBl0CbR!S0GFTCVr-tM_cPsgkw8Y-0HxIAR-TI_clqys
    patronvideos  = '(mega.co.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Mega]"
        url = "https://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mega' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)    
            

    return devuelve
