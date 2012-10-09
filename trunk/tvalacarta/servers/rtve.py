# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para boing
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
    #http://www.rtve.es/mediateca/videos/20100410/telediario-edicion/741525.shtml
    #http://www.rtve.es/alacarta/videos/espana-entre-el-cielo-y-la-tierra/espana-entre-el-cielo-y-la-tierra-la-mancha-por-los-siglos-de-los-siglos/232969/
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
        data = scrapertools.cache_page("http://www.piraminet.com/lab/calcular.php",post=urllib.urlencode({"url_original":page_url}))
        url = scrapertools.get_match(data,"<a href='([^']+)' class='enlace'><strong>Enlace del video</strong></a>")

    '''
    if url=="":
        logger.info("[rtve.py] Probando nuevo sistema")

        # Ponemos el id en el siguiente enlace
        url = "http://www.rtve.es/ztnr/?idasset="+codigo
        logger.info("url="+url)
        data = scrapertools.cache_page(url)
        logger.info("data="+data)

        # Cuando la página carga nos muestra el nuevo id
        category = scrapertools.get_match(data,"<td>Category</td>[^<]+<th>([^<]+)</th>")
        
        patron  = '<td\s+class="s\d+">(\d+)</td>[^<]+'
        patron += '<td\s+class="s\d+">([^<]+)</td>[^<]+'
        patron += '<td\s+class="s\d+">([^<]+)</td>[^<]+'
        patron += '<td\s+class="s\d+">([^<]+)</td>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        for idpreset,videoaudio,tipo,lenguaje in matches:
            
            # Ponemos el nuevo id en el siguiente enlace:
            #http://www.rtve.es/ztnr/preset.jsp?idpreset=910988&lenguaje=es&tipo=video
            url = "http://www.rtve.es/ztnr/preset.jsp?idpreset="+idpreset+"&lenguaje="+lenguaje+"&tipo="+videoaudio
            logger.info("url="+url)
            data = scrapertools.cache_page(url)
            logger.info("data="+data)

            # De ahí sacamos el video
            # <li><em>File Name</em>&nbsp;<span class="titulo">mp4/4/1/1340907208714.mp4</span></li>
            finalurl = scrapertools.get_match(data,'<li><em>File Name</em>&nbsp;<span class="titulo">([^<]+)</span></li>')
            
            # Ahora solo nos falta el principio del enlace y quedaría así:
            url = "http://www.rtve.es/resources/"+category+"/"+finalurl
            logger.info("url="+url)
    '''
    
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
