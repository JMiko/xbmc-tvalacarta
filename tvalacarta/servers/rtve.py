# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rtve
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rtve.py] get_video_url(page_url='%s')" % page_url)

    # Extrae el código
    logger.info("url="+page_url)
    patron = 'http://.*?/([0-9]+)/'
    data = page_url
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    codigo = matches[0]
    url=""
    itemlist = []
    logger.info("assetid="+codigo)

    if url=="":
        url = "http://www.rtve.es/ztnr/consumer/xl/video/alta/" + codigo + "_es_292525252525111"
        logger.info("url="+url)

        location = scrapertools.get_header_from_response(url,header_to_get="location")

        if location != "":
            url = location.replace("www.rtve.es", "media5.rtve.es")

    if url=="":
        data = scrapertools.cache_page("http://web.pydowntv.com/api?url="+page_url)
        url = scrapertools.get_match(data,'"url_video"\: \["([^"]+)"\]')

    if url=="":
        try:
            # Compone la URL
            #http://www.rtve.es/swf/data/es/videos/alacarta/5/2/5/1/741525.xml
            url = 'http://www.rtve.es/swf/data/es/videos/alacarta/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)
    
            # Descarga el XML y busca el vídeo
            #<file>rtmp://stream.rtve.es/stream/resources/alacarta/flv/6/9/1270911975696.flv</file>
            data = scrapertools.cachePage(url)
            #print url
            #print data
            patron = '<file>([^<]+)</file>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            if len(matches)>0:
                #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
                url = matches[0]
            else:
                url = ""
            
            patron = '<image>([^<]+)</image>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            #print len(matches)
            #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
            thumbnail = matches[0]
        except:
            url = ""
    
    # Hace un segundo intento
    if url=="":
        try:
            # Compone la URL
            #http://www.rtve.es/swf/data/es/videos/video/0/5/8/0/500850.xml
            url = 'http://www.rtve.es/swf/data/es/videos/video/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)

            # Descarga el XML y busca el vídeo
            #<file>rtmp://stream.rtve.es/stream/resources/alacarta/flv/6/9/1270911975696.flv</file>
            data = scrapertools.cachePage(url)
            patron = '<file>([^<]+)</file>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
            url = matches[0]
        except:
            url = ""
    
    if url=="":

        try:
            # Compone la URL
            #http://www.rtve.es/swf/data/es/videos/video/0/5/8/0/500850.xml
            url = 'http://www.rtve.es/swf/data/es/videos/video/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)

            # Descarga el XML y busca el assetDataId
            #<plugin ... assetDataId::576596"/>
            data = scrapertools.cachePage(url)
            #logger.info("[rtve.py] data="+data)
            patron = 'assetDataId\:\:([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
            codigo = matches[0]
            logger.info("assetDataId="+codigo)
            
            #url = http://www.rtve.es/scd/CONTENTS/ASSET_DATA_VIDEO/6/9/5/6/ASSET_DATA_VIDEO-576596.xml
            url = 'http://www.rtve.es/scd/CONTENTS/ASSET_DATA_VIDEO/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/ASSET_DATA_VIDEO-'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)
            
            data = scrapertools.cachePage(url)
            #logger.info("[rtve.py] data="+data)
            patron  = '<field>[^<]+'
            patron += '<key>ASD_FILE</key>[^<]+'
            patron += '<value>([^<]+)</value>[^<]+'
            patron += '</field>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            codigo = matches[0]
            logger.info("[rtve.py] url="+url)
            
            #/deliverty/demo/resources/mp4/4/3/1290960871834.mp4
            #http://media4.rtve.es/deliverty/demo/resources/mp4/4/3/1290960871834.mp4
            #http://www.rtve.es/resources/TE_NGVA/mp4/4/3/1290960871834.mp4
            url = "http://www.rtve.es/resources/TE_NGVA"+codigo[-26:]

        except:
            url = ""

    logger.info("[rtve.py] url="+url)

    '''
    if url=="":
        logger.info("[rtve.py] Extrayendo URL tipo iPad")
        headers = []
        headers.append( ["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"] )
        location = scrapertools.get_header_from_response(page_url,headers=headers,header_to_get="location")
        logger.info("[rtve.py] location="+location)
        
        data = scrapertools.cache_page(location,headers=headers)
        logger.info("[rtve.py] data="+data)
        #<a href="/usuarios/sharesend.shtml?urlContent=/resources/TE_SREP63/mp4/4/8/1334334549284.mp4" target
        url = scrapertools.get_match(data,'<a href="/usuarios/sharesend.shtml\?urlContent\=([^"]+)" target')
        logger.info("[rtve.py] url="+url)
        #http://www.rtve.es/resources/TE_NGVA/mp4/4/8/1334334549284.mp4
        url = urlparse.urljoin("http://www.rtve.es",url)
        logger.info("[rtve.py] url="+url)
    '''
    
    video_urls = []
    video_urls.append( [ "[rtve]" , url ] )

    for video_url in video_urls:
        logger.info("[rtve.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    return devuelve
