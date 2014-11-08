# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mail.ru
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mail.ru.py] get_video_url(page_url='%s')" % (page_url))

    video_urls = []

    # Descarga
    data = scrapertools.cache_page( page_url )
    logger.info("data=%s" % (data))

    video_key = scrapertools.get_match( data , 'video_key=([^&]+)&')
    try:
        media_url_hd = scrapertools.get_match( data , '"videos":{[^,]+,"hd":"([^"]+)"' )
        media_url_hd += "|Cookie=video_key="+video_key
        video_urls.append( [ scrapertools.get_filename_from_url(media_url_hd)[-4:] + " [mail.ru] HD",media_url_hd ] )
    except: pass
    try:
        media_url_sd = scrapertools.get_match( data , '"videos":{"sd":"([^"]+)"' )
        media_url_sd += "|Cookie=video_key="+video_key
        video_urls.append( [ scrapertools.get_filename_from_url(media_url_sd)[-4:] + " [mail.ru] SD",media_url_sd ] )
    except: pass

    for video_url in video_urls:
        logger.info("[mail.ru] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    logger.info("[mail.ru.py] find_videos(data='%s')" % (data))

    encontrados = set()

    devuelve = []

    titulo = "[mail.ru]"
    if "http://api.video.mail.ru/videos/embed/" in data:
        url = data.replace("embed/","").replace(".html",".json")
    else:
        id_page_url = scrapertools.get_match(data,'/_myvideo/(\d+).html')
        author_name = scrapertools.get_match(data,'/video/mail([^/]+)/')
        url = "http://api.video.mail.ru/videos/mail/%s/_myvideo/%s.json" % (author_name,id_page_url)

    if url not in encontrados:
        logger.info("  url=%s" % (url))
        devuelve.append( [ titulo , url , 'mailru' ] )
        encontrados.add(url)
    else:
        logger.info("  url duplicada=%s" % (url))

    return devuelve
