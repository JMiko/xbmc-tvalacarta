# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streamcloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[streamcloud.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page( url = page_url )
    if "<h1>File Not Found</h1>" in data:
        return False,"El archivo no existe<br/>en streamcloud o ha sido borrado."
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[streamcloud.py] url="+page_url)
    video_urls = []
    
    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    
    patron =  'file\: "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        media_url = scrapertools.get_match( data , 'file\: "([^"]+)"' )+"?start=0"
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [streamcloud]",media_url])
        return video_urls
    
    
    patron  = '<input type="hidden" name="op" value="([^"]+)">[^<]+'
    patron += '<input type="hidden" name="usr_login" value="">[^<]+'
    patron += '<input type="hidden" name="id" value="([^"]+)">[^<]+'
    patron += '<input type="hidden" name="fname" value="([^"]+)">[^<]+'
    patron += '<input type="hidden" name="referer" value="">[^<]+'
    patron += '<input type="hidden" name="hash" value="([^"]+)">[^<]+'
    patron += '<input type="submit" name="imhuman".*?value="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    op = matches[0][0]
    usr_login = ""
    id = matches[0][1]
    fname = matches[0][2]
    referer = ""
    hashstring = matches[0][3]
    imhuman = matches[0][4].replace(" ","+")
    
    import time
    time.sleep(10)
    
    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
    headers.append(["Referer",page_url])
    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    logger.info("data="+data)

    # Extrae la URL
    media_url = scrapertools.get_match( data , 'file\: "([^"]+)"' )+"?start=0"
    
    
    if len(matches)>0:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [streamcloud]",media_url])

    for video_url in video_urls:
        logger.info("[streamcloud.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://streamcloud.eu/cwvhcluep67i
    patronvideos  = '(streamcloud.eu/[a-z0-9]+)'
    logger.info("[streamcloud.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[streamcloud]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streamcloud' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
