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
    
    data = scrapertools.cache_page( short_url )
    
    # Busca la url de "Saltar el anuncio"
    #var url = '/go/a59f91b58940e169d612a806f03bffbc/aHR0cDovL2dvby5nbC9nT3c4OA';	
    skip_ad_url = urlparse.urljoin( short_url , scrapertools.get_match(data,"var url \= '(/go/[^']+)'") )
    logger.info( "skip_ad_url=" + skip_ad_url )
    
    # Espera los 5 segundos
    try:
        from platformcode.xbmc import xbmctools
        xbmctools.handle_wait(5,"adf.ly",'')
    except:
        import time
        time.sleep(5)

    # Obtiene la url larga
    location = scrapertools.get_header_from_response(skip_ad_url,header_to_get="location")
    logger.info("location="+location)

    return location
