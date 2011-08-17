# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,re
import base64

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videobb.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Obtiene el id
    code = Extract_id(page_url)
    
    # Descarga el json con los detalles del vídeo
    controluri = "http://videobb.com/player_control/settings.php?v=%s&fv=v1.1.58"  %code
    datajson = scrapertools.cachePage(controluri)
    #logger.info("response="+datajson);

    # Convierte el json en un diccionario
    datajson = datajson.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")
    
    # Formatos
    formatos = datadict["settings"]["res"]
    
    for formato in formatos:
        uri = base64.decodestring(formato["u"])
        resolucion = formato["l"]
    
        video_urls.append( ["%s [videobb]" % resolucion , uri ])

    for video_url in video_urls:
        logger.info("[videobb.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

def Extract_id(url):
    # Extract video id from URL
    _VALID_URL = r'^((?:http://)?(?:\w+\.)?videobb\.com/(?:(?:(?:e/)|(?:video/))|(?:f/))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
    mobj = re.match(_VALID_URL, url)
    if mobj is None:
        logger.info('[videobb.py] ERROR: URL invalida: %s' % url)
        
        return ""
    id = mobj.group(2)
    return id

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    '''
    patronvideos  = "(http\:\/\/videobb.com\/e\/[a-zA-Z0-9]+)"
    logger.info("[videobb.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobb]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobb' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    '''
    
    patronvideos  = "(http\:\/\/(?:www\.)?videobb.com\/(?:(?:e/)|(?:(?:video/|f/)))?[a-zA-Z0-9]{12})"
    logger.info("[videobb.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobb]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobb' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve