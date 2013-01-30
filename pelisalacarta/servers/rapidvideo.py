# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rapidvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rapidvideo.py] url="+page_url)

    data = scrapertools.cache_page(page_url)

    patron  = '<form[^<]+'
    patron += '<input type="hidden" value="([^"]+)" name="block"[^<]+'
    patron += '<input name="confirm" type="submit" value="([^"]+)" class="confirm_button"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0: return []

    post = "block="+matches[0][0]+"&confirm="+(matches[0][1].replace(" ","+"))
    headers = []
    headers.append( ['User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'] )
    headers.append( [ "Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ])
    headers.append( ['Referer',page_url] )

    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    #logger.info("data="+data)
    # extrae 
    patron = 'file\: "([^"]+)"\,\s+height\: (\d+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    video_urls = []
    if len(matches)>0:
        for location,altura in matches:
            video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:]+" ["+str(altura)+"p][rapidvideo]",location] )

    for video_url in video_urls:
        logger.info("[rapidvideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []
            
    # http://www.rapidvideo.com/embed/sy6wen17
    patronvideos  = 'http://www.rapidvideo.com/embed/([a-z0-9]+)'
    logger.info("[rapidvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "http://www.rapidvideo.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rapidvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://www.rapidvideo.com/embed/sy6wen17")

    return len(video_urls)>0