# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filebox
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[filebox.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    '''
    <input type="hidden" name="op" value="download2">
    <input type="hidden" name="id" value="235812b1j9w1">
    <input type="hidden" name="rand" value="na73zeeooqyfkndsv4uxzzpbajwi6mhbmixtogi">
    <input type="hidden" name="referer" value="http://www.seriesyonkis.com/s/ngo/2/5/1/8/773">
    '''
    logger.info("[filebox.py] URL ")
    data = scrapertools.cache_page(page_url)
    # Espera los 5 segundos
    if "xbmc" in config.get_platform():
        from platformcode.xbmc import xbmctools
        xbmctools.handle_wait(5,"filebox",'')
    else:
        import time
        time.sleep(5)


    patron  = '<input type="hidden" name="id" value="([^"]+)">[^<]+'
    patron += '<input type="hidden" name="rand" value="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)

    codigo = ""
    nombre = ""
    if len(matches)>0:
        codigo = matches[0][0]
        rand = matches[0][1]

    post = "op=download2&id="+codigo+"&rand="+rand+"&referer=&method_free=&method_premium=&down_direct=1"

    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    logger.info("data="+data)
    # Busca el video online o archivo de descarga 
    patron = 'href="([^"]+)">>>> Download File <<<<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    if len(matches)>0:
        logger.info("[filebox.py] encuentra archivo de descarga="+matches[0])
    else:
        logger.info("[filebox.py] buscando video para ver online")
        patron = "this\.play\('([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        

    if len(matches)>0:
        video_urls.append( ["."+matches[0].rsplit('.',1)[1]+" [filebox]",matches[0]])

    for video_url in video_urls:
        logger.info("[filebox.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.filebox.com/embed-wa5p8wzh7tlq-700x385.html
    patronvideos  = 'filebox.com/embed-([0-9a-zA-Z]+)'
    logger.info("[filebox.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filebox]"
        url = "http://www.filebox.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filebox' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.filebox.com/729x1eo9zrx1
    patronvideos  = 'filebox.com/([0-9a-zA-Z]+)'
    logger.info("[filebox.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filebox]"
        url = "http://www.filebox.com/"+match
        if url!="http://www.filebox.com/embed" and url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filebox' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
