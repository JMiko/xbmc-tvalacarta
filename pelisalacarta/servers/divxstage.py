# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de divxstage
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[divxstage.py] get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    video_urls = []
    # Descarga la página
    headers = [ ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],['Referer','http://www.movshare.net/'] ]
    data = scrapertools.cache_page(page_url , headers = headers)
    
    # La vuelve a descargar, como si hubieras hecho click en el botón
    data = scrapertools.cache_page(page_url , headers = headers)

    # Extrae el vídeo
    #flashvars.file="an6u81bpsbenn";
    #flashvars.filekey="88.12.109.83-e2d263cbff66b2a510d6f7417a57e498";
    file = scrapertools.get_match(data,'flashvars.file="([^"]+)"')
    filekey = scrapertools.get_match(data,'flashvars.filekey="([^"]+)"')
    
    #http://www.divxstage.eu/api/player.api.php?file=pn7tthffreyoo&user=undefined&pass=undefined&codes=1&key=88%2E12%2E109%2E83%2Df1d041537679b37f5b25404ac66b341b
    filekey = filekey.replace(".","%2E")
    filekey = filekey.replace("-","%2D")
    url = "http://www.divxstage.eu/api/player.api.php?file="+file+"&user=undefined&pass=undefined&codes=1&key="+filekey
    data = scrapertools.cache_page(url , headers = headers)
    logger.info("data="+data)
    location = scrapertools.get_match(data,"url=([^\&]+)\&")

    try:
        import urlparse
        parsed_url = urlparse.urlparse(location)
        logger.info("parsed_url="+str(parsed_url))
        extension = parsed_url.path[-4:]
    except:
        if len(parsed_url)>=4:
            extension = parsed_url[2][-4:]
        else:
            extension = ""

    video_urls.append( [ extension+" [divxstage]" , location ] )

    for video_url in video_urls:
        logger.info("[divxstage.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # divxstage http://www.divxstage.net/video/2imiqn8w0w6dx"
    patronvideos  = 'http://www.divxstage.[\w]+/video/([\w]+)'
    logger.info("[divxstage.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Divxstage]"
        url = "http://www.divxstage.net/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'divxstage' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve
