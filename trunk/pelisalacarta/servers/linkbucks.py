# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para linkbucks
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, sys
import urlparse, urllib, urllib2

from core import scrapertools
from core import logger
from core import config

# Obtiene la URL que hay detrás de un enlace a linkbucks
def get_long_url(url):
    logger.info("[linkbucks.py] get_long_url(url='%s')" % url)

    # Descarga la página de linkbucks
    data = scrapertools.cache_page(url)

    # Extrae la URL de adf.ly y descarga la página
    location = scrapertools.get_match(data,"Lbjs.TargetUrl \= '([^']+)'")
    logger.info("[linkbucks.py] -> location="+location)

    return location
