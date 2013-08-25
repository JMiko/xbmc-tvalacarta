# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para adfly (acortador de url)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_long_url( short_url ):
    logger.info("[adfly.py] get_long_url(short_url='%s')" % short_url)
    
    '''
    data = scrapertools.cache_page( short_url )
    #var zzz = 'http://freakshare.com/files/ivkf5hm4/The.Following.S01E01.UNSOLOCLIC.INFO.avi.html'
    location = scrapertools.get_match(data,"var zzz \= '([^']+)'")
    logger.info("location="+location)

    # Espera los 5 segundos
    try:
        from platformcode.xbmc import xbmctools
        xbmctools.handle_wait(5,"adf.ly",'')
    except:
        import time
        time.sleep(5)

    if "adf.ly" in location:
        # Obtiene la url larga
        data = scrapertools.cache_page(location)
        logger.info("data="+data)

        location = scrapertools.get_match(data,'<META HTTP-EQUIV\="Refresh".*?URL=([^"]+)"')
    '''
    # Accede para conseguir las cookies
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0"])
    data = scrapertools.cache_page( "http://dead.altervista.org/" )

    # Ahora envía el formulario
    headers.append(["Referer","http://dead.altervista.org/"])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    post = urllib.urlencode({'url':short_url})
    data = scrapertools.cache_page( "http://dead.altervista.org/bypasser/process.php" , post=post , headers=headers )
    logger.info("data="+data)
    location = scrapertools.get_match(data,'<a href="([^"]+)"')

    logger.info("location="+location)

    return location

def test():
    
    location = get_long_url("http://adf.ly/HnJnC")
    ok = ("freakshare.com" in location)

    if ok:
        location = get_long_url("http://adf.ly/Fp6BF")
        ok = "http://vk.com/" in location

    return ok