# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidxden
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vidxden.py] url="+page_url)
    if ".html" not in page_url:
        logger.info("[vidxden.py] URL incompleta")
        data = scrapertools.cache_page(page_url)
        patron = '<input name="fname" type="hidden" value="([^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        page_url = page_url+"/"+matches[0]+".html"

        
    # Lo pide una vez
    scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    
    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    patron = 'http\:\/\/www\.vidxden\.com/([^\/]+)/(.*?)\.html'
    matches = re.compile(patron,re.DOTALL).findall(page_url)
    logger.info("[vidxden.py] fragmentos de la URL")
    scrapertools.printMatches(matches)
    
    codigo = ""
    nombre = ""
    if len(matches)>0:
        codigo = matches[0][0]
        nombre = matches[0][1]

    post = "op=download1&usr_login=&id="+codigo+"&fname="+nombre+"&referer=&method_free=Free+Stream"
    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    
    # Extrae el trozo cifrado
    patron = '<div id="embedcontmvshre"[^>]+>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        data = matches[0]
        logger.info("[vidxden.py] bloque packed="+data)
    else:
        logger.info("[vidxden.py] no encuentra bloque packed="+data)

        return ""
    
    # Lo descifra
    descifrado = unpackerjs.unpackjs(data)
    
    # Extrae la URL del vídeo
    logger.info("descifrado="+descifrado)
    # Extrae la URL
    patron = '<param name="src"value="([^"]+)"/>'
    matches = re.compile(patron,re.DOTALL).findall(descifrado)
    scrapertools.printMatches(matches)
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( ["."+matches[0].rsplit('.',1)[1]+" [vidxden]",matches[0]])

    for video_url in video_urls:
        logger.info("[vidxden.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.vidxden.com/3360qika02mo/whale.wars.s04e10.hdtv.xvid-momentum.avi.html
    patronvideos  = '(http://www.vidxden.com/[A-Z0-9a-z]+/.*?html)'
    logger.info("[vidxden.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidxden]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidxden' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://www.vidxden.com/qya0qmf3k502
    patronvideos  = 'http://www.vidxden.com/([\w]+)'
    logger.info("[vidxden.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidxden]"
        url = "http://www.vidxden.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidxden' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
