# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rutube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config


def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rutube.py] url="+page_url)

    patron = 'http://video.rutube.ru/([a-z0-9]+)'
    matches = re.compile(patron,re.DOTALL).findall(page_url)
    if len(matches)==0:return []
    code = matches[0]
    logger.info("code="+code)

    url = "http://bl.rutube.ru/"+code+".xml?referer="
    data = scrapertools.cache_page( url )
    logger.info("data="+data)

    '''
    <?xml version="1.0"?>
    <response status="302"><finalAddress>
    <![CDATA[rtmp://video-13-7.rutube.ru/rutube_vod_2/mp4:n2vol1/movies/91/20/91203fc46405f06c2cadb98c9052dd68.mp4?e=1327761052&s=fc2477835e2ee7cf6e9fb437d6eb8341]]>
    </finalAddress></response>
    '''
    '''
    <response status="302"><finalAddress>
    <![CDATA[rtmp://video-12-9.rutube.ru/rutube_vod_1/mp4:n1vol1/movies/4c/b0/4cb0b5b76105084987be355f5c0cf5cc.mp4?e=1328574823&s=7ce76180534e1f8d5a88f81095d3e133]]>
    </finalAddress></response>
    '''
    patron = "<finalAddress>[^<]+<\!\[CDATA\[([^\]]+)\]\]>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    video_urls = []
    
    if len(matches)>0:
        
        # Code adapted from http://code.google.com/p/xbmc-xstream-plugin/
        sRtmpFile = matches[0]
        
        if "rutube_vod_1" in sRtmpFile:
            aSplitt = sRtmpFile.split('rutube_vod_1/')
        else:
            aSplitt = sRtmpFile.split('rutube_vod_2/')
        sPlaypath = aSplitt[1]
            
        aSplitt = sRtmpFile.split('.ru/')
        sRtmp = aSplitt[0] + '.ru:1935/'
        
        aSplitt = aSplitt[1].split('mp4')
        sApp = aSplitt[0]

        sSwfUrl = 'http://rutube.ru/player.swf'

        sStreamUrl = sRtmp + ' app=' + sApp + ' swfurl=' + sSwfUrl + ' playpath=' + sPlaypath
        #rtmp://video-1-1.rutube.ru:1935/ app=rutube_vod_2/_definst_/ swfurl=http://rutube.ru/player.swf playpath=mp4:vol32/movies/14/bd/14bd98f3733ef080507ff5f517f28830.mp4?e=1295385656&s=adb28dba086b7394013c37550cb48dd8&blid=957c0d2befa18c8d286b2076cecf01bd
        
        logger.info("stream="+sStreamUrl)

        video_urls.append( ["[rutube]",sStreamUrl])

    for video_url in video_urls:
        logger.info("[rutube.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://video.rutube.ru/91203fc46405f06c2cadb98c9052dd68
    patronvideos  = '(http://video.rutube.ru/[a-z0-9]+)'
    logger.info("[rutube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rutube]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rutube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
