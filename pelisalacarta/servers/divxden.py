# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para divxden
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

import os
COOKIEFILE = os.path.join(config.get_data_path() , "cookies.lwp")

# http://www.vidxden.com/3360qika02mo/whale.wars.s04e10.hdtv.xvid-momentum.avi.html
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[divxden.py] url="+page_url)
    
    # Lo pide una vez
    scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    
    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    patron = 'http\:\/\/www\.vidxden\.com/([^\/]+)/(.*?)\.html'
    matches = re.compile(patron,re.DOTALL).findall(url)
    logger.info("[divxden.py] fragmentos de la URL")
    scrapertools.printMatches(matches)
    
    codigo = ""
    nombre = ""
    if len(matches)>0:
        codigo = matches[0][0]
        nombre = matches[0][1]

    post = "op=download1&usr_login=&id="+codigo+"&fname="+nombre+"&referer=&method_free=Free+Stream"
    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    
    # Extrae el trozo cifrado
    patron = '<div align="center" id="divxshowboxt">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        data = matches[0]
        logger.info("[divxden.py] bloque packed="+data)
    else:
        return ""
    
    # Lo descifra
    descifrado = unpackerjs.unpackjs(data)
    
    # Extrae la URL del vídeo
    logger.info("descifrado="+descifrado)
    # Extrae la URL
    patron = '<param name="src"value="([^"]+)"/>'
    matches = re.compile(patron,re.DOTALL).findall(descifrado)
    scrapertools.printMatches(matches)
    
    url = ""
    
    if len(matches)>0:
        url = matches[0]

    logger.info("[divxden.py] url="+url)
    return url
