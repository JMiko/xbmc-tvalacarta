
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Wupload (solo filenium)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config


def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[novamov.py] get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    patron = 'flashvars.file="(.*?)";'
    matches = re.compile(patron).findall(data)
    for match in matches:
    	logger.info("File = "+match)
	flashvarsfile = match
    patron = 'flashvars.filekey="(.*?)";'
    matches = re.compile(patron).findall(data)
    for match in matches:
    	logger.info("Key = "+match)
	flashvarsfilekey = match
    post="key="+flashvarsfilekey+"&user=undefined&codes=1&pass=undefined&file="+flashvarsfile
    url = "http://www.novamov.com/api/player.api.php?"+post
    data = scrapertools.cache_page(url, post=post)
    logger.info(data)
    patron = 'url=(.*?)&title='
    matches = re.compile(patron).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    logger.info(matches[0])
    video_urls.append( ["FLV [novamov]",matches[0]])
	
    return video_urls

def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = '(http://www.novamov.com/video/[a-z0-9]{13})'
    logger.info("[novamov.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[novamov]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'novamov' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://embed.novamov.com/embed.php?width=568&height=340&v=zadsdfoc0pirx&px=1
    # http://embed.novamov.com/embed.php?width=620&amp;height=348&amp;v=4f21e91a1f2f7&amp;px=1&amp;px=1
    patronvideos = 'http://embed.novamov.com/embed.php.*?v=([a-z0-9]{13})'
    logger.info("[novamov.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[novamov]"
        url = "http://www.novamov.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'novamov' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
