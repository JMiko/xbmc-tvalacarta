# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para backin.net
# by be4t5
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[backin.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    #if '<meta property="og:title" content=""/>' in data:
        #return False,"The video has been cancelled from Backin.net"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[backin.py] url="+page_url)
    video_urls = []
    headers = []
    headers.append( [ "User-Agent"     , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"] )
    
 
    # First access
    data = scrapertools.cache_page(page_url,headers=headers)
    logger.info("data="+data)

    
    # URL 
    url = scrapertools.find_single_match(data,'type="video/mp4" src="([^"]+)"')
    logger.info("url="+url)

    # URL del vídeo
    video_urls.append( [ ".mp4" + " [backin]",url ] )

    for video_url in video_urls:
       logger.info("[backin.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    
	
	#http://backin.net/iwbe6genso37
    patronvideos  = '(?:backin).net/([A-Z0-9]+)'
    logger.info("[backin.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[backin]"
        url = "http://backin.net/s/generating.php?code="+match
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'backin' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)        
					
	
	#http://cineblog01.pw/HR/go.php?id=6475
    temp  = text.split('<strong>Streaming')
    tem = temp[1].split('Download')
    patronvideos  = '(?:HR)/go.php\?id\=([A-Z0-9]+)'
    logger.info("[backin.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(tem[0])

    for match in matches:
        titulo = "[backin]"
        data = "http://cineblog01.pw/HR/go.php?id="+match
        data = scrapertools.cache_page(data)
        id = scrapertools.find_single_match(data,'content="0; url=http://backin.net/([^"]+)"')
        url = "http://backin.net/s/generating.php?code="+id
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'backin' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)        
    
    return devuelve

def test():

    video_urls = get_video_url("http://www.firedrive.com/embed/E89565C3A0C6183E")

    return len(video_urls)>0