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

__channel__ = "cctvspan"
__category__ = "F"
__type__ = "generic"
__title__ = "cctvspan"
__language__ = "ES"
__creationdate__ = "20121130"
__vfanart__ = "http://espanol.cntv.cn/library/column/2010/11/24/C28600/style/img/map2.jpg"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cctvspan.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Arte Culinario Chino", action="videos", url="http://cctv.cntv.cn/lm/ArteCulinarioChino/video/index.shtml", thumbnail="http://p4.img.cctvpic.com/nettv/cctv/lm/ArteCulinarioChino/20121128/images/112511_1354093570266.jpg", fanart = __vfanart__)) 
 
    return itemlist
