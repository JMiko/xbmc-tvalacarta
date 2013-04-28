# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para justintv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
try:
    import json
except:
    import simplejson as json

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[justintv.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    channelname = scrapertools.get_match(page_url,"justin.tv/([_a-z0-9]+)")
    logger.info("channelname="+channelname)

    video_url = ""
    
    if page_url.startswith('rtmp'):
        video_url = page_url
    else:
        headers=[ ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:14.0) Gecko/20100101 Firefox/14.0.1"] ]
        data = scrapertools.cache_page(page_url,headers=headers)
        logger.info("data="+data)
        '''
        //<![CDATA[
        swfobject.embedSWF(
            'http://www-cdn.justin.tv/widgets/live_site_player.swf', 
            'live_site_player_flash',
            '630px',
            '381px',
            '9',
            'http://www-cdn.justin.tv/widgets/expressinstall.swf', 
            {
                'publisherGuard': null,
                'hide_chat': 'true',
                'searchquery': null,
                'backgroundImageUrl': 'http://static-cdn.jtvnw.net/jtv_user_pictures/extremotv_univision-profile_image-MnSIeiFgWqs0lTI-70x70.jpg',
                'channel': 'extremotv_univision',
                'hostname': 'www.justin.tv',
                'auto_play': 'true',
                'publisherTimezoneOffset': 420
            }, 
            {
                'allowNetworking': 'all',
                'allowScriptAccess': 'always',
                'allowFullScreen': 'true',
                'wmode': 'opaque'
            },
            ''
        );
        //]]>
        </script>
        '''
        data = scrapertools.get_match(data,'swfobject.embedSWF\((.+?)\)')
        logger.info("[justintv.py] data="+data)
        swf = ' swfUrl='+scrapertools.get_match(data,"'([^']+)'")
        logger.info("[justintv.py] swf="+swf)
        
        headers.append( ["Referer","http://justin.tv"] )
        data = scrapertools.cache_page('http://usher.justin.tv/find/'+channelname+'.json?type=live')
        logger.info("data="+data)
        datadict = json.loads(data)
        for entry in datadict:
            logger.info("entry="+str(entry))

        try:
            token = ' jtv='+datadict[0]["token"].replace('\\','\\5c').replace('"','\\22').replace(' ','\\20')
            logger.info("token="+str(token))
            connect = datadict[0]["connect"]+'/'+datadict[0]["play"]
            logger.info("connect="+str(connect))
            Pageurl = ' Pageurl=http://www.justin.tv/'+channelname
            logger.info("Pageurl="+str(Pageurl))
            video_url = connect+token+swf+Pageurl
            logger.info("video_url="+str(video_url))
        except:
            video_url=""

    logger.info("video_url="+video_url)

    if video_url!="":
        video_urls.append( [ "[justintv]" , video_url ] )

    for video_url in video_urls:
        logger.info("[justintv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.justin.tv/cineplanet82
    patronvideos  = 'justin.tv/([_0-9a-z]+)'
    logger.info("[justintv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        if match!="widgets":
            titulo = "[justintv]"
            url = "http://www.justin.tv/justin.tv/"+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'justintv' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    #http://www.justin.tv/widgets/live_embed_player.swf?channel=matrix_tv25
    patronvideos  = 'justin.tv/widgets/live_embed_player.swf\?channel=([_0-9a-z]+)'
    logger.info("[justintv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[justintv]"
        url = "http://www.justin.tv/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'justintv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #hostname=www.justin.tv&channel=matrix_tv25
    patronvideos  = 'hostname=www.justin.tv\&channel=([_0-9a-z]+)'
    logger.info("[justintv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[justintv]"
        url = "http://www.justin.tv/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'justintv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
