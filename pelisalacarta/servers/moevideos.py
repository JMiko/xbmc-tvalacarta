# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para moevideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[moevideos.py] test_video_exists(page_url='%s')" % page_url)

    # Si es el código embed directamente, no se puede comprobar
    if "video.php" in page_url:
        return True,""
    
    # No existe / borrado: http://www.moevideos.net/online/27991
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<span class='tabular'>No existe</span>" in data:
        return False,"No existe o ha sido borrado de moevideos"
    else:
        # Existe: http://www.moevideos.net/online/18998
        patron  = "<span class='tabular'>([^>]+)</span>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[moevideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    headers = []
    headers.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
    data = scrapertools.cache_page( page_url , headers=headers )
        
    # Descarga el script (no sirve para nada, excepto las cookies)
    headers.append(['Referer',page_url])
    post = "id=1&enviar2=ver+video"
    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    code = scrapertools.get_match(data,"video.php\?file\=([^\&]+)\&")
        
    # API de letitbit
    headers2 = []
    headers2.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
    url = "http://api.letitbit.net"
    #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2272871%2E71f6541e64b0eda8da727a79424d%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2272871%2E71f6541e64b0eda8da727a79424d%22%7D%5D%5D"
    post = 'r=["tVL0gjqo5",["preview/flv_image",{"uid":"'+code+'"}],["preview/flv_link",{"uid":"'+code+'"}]]'
    data = scrapertools.cache_page(url,headers=headers2,post=post)
    logger.info("data="+data)
    data = data.replace("\\","")
    patron = '"link"\:"([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    video_url = matches[0]
    logger.info("[moevideos.py] video_url="+video_url)

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(video_url)[-4:] + " [moevideos]",video_url ] )

    for video_url in video_urls:
        logger.info("[moevideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.moevideos.net/online/18998
    patronvideos  = '(moevideos.net/online/\d+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.moevideos.net/view/30086
    patronvideos  = '(moevideos.net/view/\d+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://moevideo.net/video.php?file=71845.7a9a6d72d6133bb7860375b63f0e&width=600&height=450
    patronvideos  = '"(http://moevideo.net/video.php[^"]+)"'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
