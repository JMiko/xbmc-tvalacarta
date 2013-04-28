# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Tivion
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
from streams import tivionchannels
from streams import tivionconstants
from streams import tivioncountries

__channel__ = "tivion"
__type__ = "generic"
__title__ = "Tivion"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.tivion.mainlist")

    itemlist = []
    itemlist.append( Item( channel=__channel__ , action="paises" , title="Todos los canales por paises"))
    return itemlist

def paises(item):
    logger.info("[tivion.py] paises")
    itemlist = []

    dictionarypaises = {}
    channels = tivionchannels.CHANNEL
    
    for channel in channels:
        if not dictionarypaises.has_key(channel[1]):
            itemlist.append( Item( channel=__channel__ , action="videos" , title=channel[1], url=channel[1]))
            dictionarypaises[channel[1]] = True

    return itemlist

def videos(item):
    logger.info("[tivion.py] videos")
    itemlist = []

    channels = tivionchannels.CHANNEL
    
    for channel in channels:
        if item.url == channel[1]:
            itemlist.append( Item( channel=__channel__ , action="play" , title=channel[3]+" "+channel[1], url=channel[4], plot=channel[4], folder=False))

    return itemlist