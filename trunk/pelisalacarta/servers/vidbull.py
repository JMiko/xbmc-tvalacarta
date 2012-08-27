# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidbull
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs
import time

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vidbull.py] url="+page_url)
        
    # Lo pide una vez
    data = scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    
    time.sleep(5)
    '''
    <input type="hidden" name="op" value="download2">
    <input type="hidden" name="id" value="8sueg0neje36">
    <input type="hidden" name="rand" value="qzeeevxsks6b57ax2et273j2d7bmdmypzhus3fi">
    <input type="hidden" name="referer" value="">
    
    <input type="hidden" name="method_free" value="">
    <input type="hidden" name="method_premium" value="">
    '''
    op = scrapertools.get_match( data , '<input type="hidden" name="op" value="([^"]+)">')
    id = scrapertools.get_match( data , '<input type="hidden" name="id" value="([^"]+)">')
    randval = scrapertools.get_match( data , '<input type="hidden" name="rand" value="([^"]+)">')

    #op=download2&id=8sueg0neje36&rand=f5ine3x7qo2pa2upku5wbnjktdwvn325mulc4hy&referer=&method_free=&method_premium=&down_direct=1
    post = "op="+op+"&id="+id+"&rand="+randval+"&referer=&method_free=&method_premium=&down_direct=1"
    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    logger.info("data="+data)

    # Extrae el trozo cifrado
    patron = "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d\).*?)</script>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado=""
    for match in matches:
        if "mp4" in match:
            cifrado = match
            break
    
    # Extrae la URL del vídeo
    logger.info("cifrado="+cifrado)
    descifrado = unpackerjs.unpackjs(cifrado)
    descifrado = descifrado.replace("\\","")
    logger.info("descifrado="+descifrado)
    
    # Extrae la URL
    media_url = scrapertools.get_match(descifrado,"s1.addVariable\('file','([^']+)'\)")
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [vidbull]",media_url])

    for video_url in video_urls:
        logger.info("[vidbull.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.vidbull.com/3360qika02mo
    patronvideos  = 'vidbull.com/([A-Z0-9a-z]+)'
    logger.info("[vidbull.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidbull]"
        url = "http://vidbull.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidbull' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
