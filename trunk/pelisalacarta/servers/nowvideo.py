# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nowvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[nowvideo.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "The file is being converted" in data:
        return False,"El fichero está en proceso"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[nowvideo.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    data = scrapertools.cache_page( page_url )
    
    # URL a invocar: http://www.nowvideo.eu/api/player.api.php?file=3695bce6e6288&user=undefined&codes=1&pass=undefined&key=83%2E44%2E253%2E73%2D64a25e17853b4b19586841e04b0d9382
    # En la página:
    '''
    flashvars.domain="http://www.nowvideo.eu";
    flashvars.file="3695bce6e6288";
    flashvars.filekey="83.44.253.73-64a25e17853b4b19586841e04b0d9382";
    flashvars.advURL="0";
    flashvars.autoplay="false";
    flashvars.cid="1";
    '''
    file = scrapertools.get_match(data,'flashvars.file="([^"]+)"')
    key = scrapertools.get_match(data,'flashvars.filekey="([^"]+)"')
    codes = scrapertools.get_match(data,'flashvars.cid="([^"]+)"')
    url = "http://www.nowvideo.eu/api/player.api.php?file="+file+"&user=undefined&codes="+codes+"&pass=undefined&key="+key.replace(".","%2E").replace("-","%2D")
    data = scrapertools.cache_page( url )
    logger.info("data="+data)
    # url=http://f23.nowvideo.eu/dl/653d434d3cd95f1f7b9df894366652ba/4fc2af77/nnb7e7f45f276be5a75b10e8d6070f6f4c.flv&title=Title%26asdasdas&site_url=http://www.nowvideo.eu/video/3695bce6e6288&seekparm=&enablelimit=0
    
    location = scrapertools.get_match(data,'url=([^\&]+)&')
    location = location + "?client=FLASH"

    video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [nowvideo]",location ] )

    for video_url in video_urls:
        logger.info("[nowvideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #<a href="http://www.nowvideo.eu/video/3695bce6e6288" target="_blank">1° Tempo</a>
    patronvideos  = '<a href="(http://www.nowvideo.eu/video/[a-z0-9]+)"[^>]+>([^<]+)</a>'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1]+" [nowvideo]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.nowvideo.eu/video/3695bce6e6288
    #http://www.nowvideo.eu/video/4fd0757fd4592
    patronvideos  = '(nowvideo.eu/video/[a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
