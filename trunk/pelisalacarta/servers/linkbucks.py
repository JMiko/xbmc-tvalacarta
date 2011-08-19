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
def geturl(url):

    # Descarga la página de linkbucks
    data = scrapertools.cachePage(url)

    # Extrae la URL real
    patronvideos  = "linkDestUrl \= '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    devuelve = "";
    if len(matches)>0:
        devuelve = matches[0]

    return devuelve
