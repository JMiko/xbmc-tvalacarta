# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para putlocker
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config


def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[putlocker.py] url="+page_url)
    data = scrapertools.cache_page(page_url)

    patron = 'value="([0-9a-f]+?)" name="hash"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:return []


    post = "hash="+matches[0]+"&confirm=Continue as Free User"
    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    # extrae 
    patron = "playlist: '(.+?)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    if len(matches)>0:
        xmlurl = urlparse.urljoin(page_url,matches[0])
        logger.info("[putlocker.py] Playlis="+xmlurl)
    else:
        logger.info("[putlocker.py] No encuentra Playlist="+xmlurl)

        return []
    

    logger.info("xmlurl="+xmlurl)
    data = scrapertools.downloadpageWithoutCookies(xmlurl)
    # Extrae la URL
    patron = '</link><media\:content url="(.+?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( ["."+matches[0].rsplit('.',1)[1][0:3]+" [putlocker]",matches[0]])

    for video_url in video_urls:
        logger.info("[putlocker.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.peliculasaudiolatino.com/show/putlocker.php?url=CEE0B3A7DDFED758
    patronvideos  = 'putlocker.php\?url=([A-Z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www.putlocker.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://www.putlocker.com/embed/CEE0B3A7DDFED758 | http://www.putlocker.com/file/CEE0B3A7DDFED758
    patronvideos  = 'http://www.putlocker.com/(?:file|embed)/([A-Z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www.putlocker.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
