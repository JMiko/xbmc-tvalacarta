# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[allmyvideos.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    if ".html" not in page_url:
        logger.info("[allmyvideos.py] URL incompleta")
        data = scrapertools.cache_page(page_url)
        patron = '<input type="hidden" name="fname" value="([^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        page_url = page_url+"/"+matches[0]+".html"

    # Lo pide una vez
    scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    
    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    patron = 'http\:\/\/allmyvideos\.net/([^\/]+)/(.*?)\.html'
    matches = re.compile(patron,re.DOTALL).findall(page_url)
    logger.info("[allmyvideos.py] fragmentos de la URL")
    scrapertools.printMatches(matches)
    
    codigo = ""
    nombre = ""
    if len(matches)>0:
        codigo = matches[0][0]
        nombre = matches[0][1]

    #op=download1&usr_login=&id=yqa1zlnum819&fname=harrys.law.219.hdtv-lol.mp4&referer=&method_free=Watch+Now%21
    post = "op=download1&usr_login=&id="+codigo+"&fname="+nombre+"&referer=&method_free=Watch+Now%21"
    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    
    # Extrae el trozo cifrado
    patron = "<div id='flvplayer'></div>[^<]+"
    patron += "<script type='text/javascript'>(.*?)</script>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        data = matches[0]
        logger.info("[allmyvideos.py] bloque packed="+data)
    else:
        logger.info("[allmyvideos.py] no encuentra bloque packed="+data)

        return ""
    
    # Lo descifra
    descifrado = unpackerjs.unpackjs(data)
    descifrado = descifrado.replace("\\","")
    # Extrae la URL del vídeo
    logger.info("descifrado="+descifrado)
    # Extrae la URL
    #'file':'http://sd481.allmyvideos.net:182/d/2gmhj7h7yq5dh6lnhtgyd4g5pmks5h3dog2xp6ege3teeecdbp6zhy7f/video.mp4'
    patron = "'file'\:'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(descifrado)
    scrapertools.printMatches(matches)
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( ["."+matches[0].rsplit('.',1)[1]+" [allmyvideos]",matches[0]])

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allmyvideos.net/fg85ovidfwxx
    patronvideos  = '(allmyvideos.net/[a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://allmyvideos.net/ugk8qqbywuk8/alc103.mp4.html
    patronvideos  = '(allmyvideos.net/[A-Z0-9a-z]+/.*?html)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    return devuelve
