# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Conector para telefe
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="", page_data="" ):
    logger.info("tvalacarta.servers.telefe get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Descarga la página del vídeo
    data = scrapertools.cache_page(page_url)

    # Esquema normal
    logger.info("tvalacarta.servers.telefe Esquema normal")
    try:
        bloque = scrapertools.get_match(data,'"playlist".*?"sources"(.*?)\]')
        patron = '"file"\:\s*"([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque)
        scrapertools.printMatches(matches)

        for match in matches:
            tipo = match[:4]
            url = match
            if tipo=="rtmp":
                url=url.replace("mp4:TOK","TOK")

            video_urls.append( [ tipo+" [telefe]" , url ] )

            '''
            00:55:30 T:2955980800   ERROR: Valid RTMP options are:
            00:55:30 T:2955980800   ERROR:      socks string   Use the specified SOCKS proxy
            00:55:30 T:2955980800   ERROR:        app string   Name of target app on server
            00:55:30 T:2955980800   ERROR:      tcUrl string   URL to played stream
            00:55:30 T:2955980800   ERROR:    pageUrl string   URL of played media's web page
            00:55:30 T:2955980800   ERROR:     swfUrl string   URL to player SWF file
            00:55:30 T:2955980800   ERROR:   flashver string   Flash version string (default MAC 10,0,32,18)
            00:55:30 T:2955980800   ERROR:       conn AMF      Append arbitrary AMF data to Connect message
            00:55:30 T:2955980800   ERROR:   playpath string   Path to target media on server
            00:55:30 T:2955980800   ERROR:   playlist boolean  Set playlist before play command
            00:55:30 T:2955980800   ERROR:       live boolean  Stream is live, no seeking possible
            00:55:30 T:2955980800   ERROR:  subscribe string   Stream to subscribe to
            00:55:30 T:2955980800   ERROR:        jtv string   Justin.tv authentication token
            00:55:30 T:2955980800   ERROR:       weeb string   Weeb.tv authentication token
            00:55:30 T:2955980800   ERROR:      token string   Key for SecureToken response
            00:55:30 T:2955980800   ERROR:     swfVfy boolean  Perform SWF Verification
            00:55:30 T:2955980800   ERROR:     swfAge integer  Number of days to use cached SWF hash
            00:55:30 T:2955980800   ERROR:    swfsize integer  Size of the decompressed SWF file
            00:55:30 T:2955980800   ERROR:    swfhash string   SHA256 hash of the decompressed SWF file
            00:55:30 T:2955980800   ERROR:      start integer  Stream start position in milliseconds
            00:55:30 T:2955980800   ERROR:       stop integer  Stream stop position in milliseconds
            00:55:30 T:2955980800   ERROR:     buffer integer  Buffer time in milliseconds
            00:55:30 T:2955980800   ERROR:    timeout integer  Session timeout in seconds
            '''

    except:
        pass

    if len(video_urls)>0:
        for video_url in video_urls:
            logger.info("tvalacarta.servers.telefe %s - %s" % (video_url[0],video_url[1]))
        return video_urls

    # Esquema antiguo: telefónica
    logger.info("tvalacarta.servers.telefe Esquema antiguo: telefonica")
    try:
        rtmpUrl = scrapertools.get_match(data,"var rtmpUrl \= \['(rtmp\://[^']+)'")
        streamName = scrapertools.get_match(data,"var streamName \= '(mp4[^']+)'")

        video_url = rtmpUrl+"/"+streamName
        video_urls.append( [ "[telefe]" , video_url ] )

        logger.info("tvalacarta.servers.telefe Encontrado vídeo en formato Telefónica: "+video_url)
    except:
        pass

    if len(video_urls)>0:
        for video_url in video_urls:
            logger.info("tvalacarta.servers.telefe %s - %s" % (video_url[0],video_url[1]))
        return video_urls

    # Esquema antiguo: opcion 2
    logger.info("tvalacarta.servers.telefe Esquema antiguo, opcion 2")

    # Descarga el descriptor del vídeo
    # El vídeo:
    # <script type="text/javascript" src="http://flash.velocix.com/c1197/legacy/UAAA1582_X264_480x360.mp4?format=jscript2&protocol=rtmpe&vxttoken=00004EAA82A8000000000289A60672657573653D32EBF4321F280103EC9B2025F74095B4E74A0E459A" ></script>
    # El anuncio:
    # <script type="text/javascript" src="http://flash.velocix.com/bt/145e8eae1563f092fbdf905113f7c213ebefd8e6/flash?format=jscript2&protocol=rtmpte&vxttoken=00004EAA693D0000000002897CEF72657573653D320830AA52351D57C26FFD6E55F9183C6342438DEB" ></script>
    patron  = '<script type="text/javascript" src="(http://flash.velocix.com/[^"]+)" ></script>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        logger.info("tvalacarta.servers.telefe Encontrado vídeo en formato Velocix")
        page_url2 = matches[0]
        data2 = scrapertools.cache_page(page_url2)
        print("data2="+data2)
        '''
        var streamName = "mp4:bt-145e8eae1563f092fbdf905113f7c213ebefd8e6";
        var rtmpUrl = [];
        rtmpUrl.push("rtmpte://201.251.164.11/flash?vxttoken=00004EAA693D0000000002897CEF72657573653D320830AA52351D57C26FFD6E55F9183C6342438DEB");
        rtmpUrl.push("rtmpte://201.251.118.11/flash?vxttoken=00004EAA693D0000000002897CEF72657573653D320830AA52351D57C26FFD6E55F9183C6342438DEB");
        '''
        patron = 'streamName \= "([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data2)
        streamName = matches[0]

        patron = 'rtmpUrl\.push\("([^"]+)"\)'
        matches = re.compile(patron,re.DOTALL).findall(data2)
        if len(matches)>0:
            videourl = matches[0]+"/"+streamName
        
            logger.info(videourl)
            video_urls.append( [ "[telefe]" , videourl ] )

    for video_url in video_urls:
        for video_url in video_urls:
            logger.info("tvalacarta.servers.telefe %s - %s" % (video_url[0],video_url[1]))
        logger.info("tvalacarta.servers.telefe %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # divxstage http://www.divxstage.net/video/2imiqn8w0w6dx"
    patronvideos  = 'http://www.divxstage.[\w]+/video/([\w]+)'
    logger.info("tvalacarta.servers.telefe find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[telefe]"
        url = "http://www.divxstage.net/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'divxstage' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve
