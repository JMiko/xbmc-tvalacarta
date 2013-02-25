﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "rtspan"
__category__ = "F"
__type__ = "generic"
__title__ = "rtspan"
__language__ = "ES"
__creationdate__ = "20121212"
__vfanart__ = "http://actualidad.rt.com/static/actualidad/design1/i/d/bg.png"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtspan.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Detrás de la noticia", action="videos", url="http://actualidad.rt.com/programas/detras_de_la_noticia",  fanart = __vfanart__)) 
 
    return itemlist
