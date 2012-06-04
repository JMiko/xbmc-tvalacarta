﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allbox4
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allbox4.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Descarga
    data = scrapertools.cache_page( page_url )
    #<param name="flashvars" value="skin=http://www.allbox4.com/player/greenskin1_2.swf&file=http://95.211.80.24:8080/d/ni66a6y5j2ldrqo22ey2jkmiof7gq42i5ewhyw6y24d7f4ejawj6snjn/video.mp4&start=0&type=http&image=http://95.211.80.24/i/00002/6szcvf0tv0s3.jpg&controlbar=over&file_code=6szcvf0tv0s3&token=9a6b9c3d3e5f0429&duration=2613&bufferlength=1" />
    try:
        paramstext = scrapertools.get_match( data , '<param name="flashvars" value="([^"]+)"')
        #skin=http://www.allbox4.com/player/greenskin1_2.swf&file=http://95.211.80.24:8080/d/ni66a6y5j2ldrqo22ey2jkmiof7gq42i5ewhyw6y24d7f4ejawj6snjn/video.mp4&start=0&type=http&image=http://95.211.80.24/i/00002/6szcvf0tv0s3.jpg&controlbar=over&file_code=6szcvf0tv0s3&token=9a6b9c3d3e5f0429&duration=2613&bufferlength=1
        params = paramstext.split("&")
        #skin=http://www.allbox4.com/player/greenskin1_2.swf
        #file=http://95.211.80.24:8080/d/ni66a6y5j2ldrqo22ey2jkmiof7gq42i5ewhyw6y24d7f4ejawj6snjn/video.mp4
        #start=0
        #type=http
        #image=http://95.211.80.24/i/00002/6szcvf0tv0s3.jpg
        #controlbar=over
        #file_code=6szcvf0tv0s3
        #token=9a6b9c3d3e5f0429
        #duration=2613
        #bufferlength=1
        
        #http://95.211.80.24:8080/d/ni66a6y5j2ldrqo22ey2jkmiof7gq42i5ewhyw6y24d7f4ejawj6snjn/video.mp4?start=0&token=9a6b9c3d3e5f0429
        file=""
        token=""
        start=""
        for param in params:
            if param.startswith("file="):
               file=param[5:] 
            if param.startswith("token="):
               token=param[6:] 
            if param.startswith("start="):
               start=param[6:] 
        
        media_url = file+"?"+start+"&"+token
    except:
        packed = scrapertools.get_match(data,"<div id=\"player_coded\">(<script type='text/javascript'>eval\(function\(p,a,c,k,e,d.*?</script>)</div>")
        from core import unpackerjs
        unpacked = unpackerjs.unpackjs(packed)
        logger.info("unpacked="+unpacked)
        media_url = scrapertools.get_match(unpacked,'<embed id="np_vid"type="video/divx"src="([^"]+)"')

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:] + " [allbox4]",media_url ] )

    for video_url in video_urls:
        logger.info("[allbox4.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.allbox4.com/embed-6szcvf0tv0s3.html
    patronvideos  = '(allbox4.com/[a-z0-9\-\.]+)'
    logger.info("[allbox4.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allbox4]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allbox4' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
