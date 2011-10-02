# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para ver una peli en Megavideo conociendo el codigo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

from pelisalacarta import buscador

CHANNELNAME = "megavideosite"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[megavideosite.py] mainlist")
    itemlist=[]
    itemlist.append( Item(channel=CHANNELNAME, action="search" , title="Introduce el código del vídeo") )
    return itemlist

def search(item,texto):
    logger.info("[megavideosite.py] search")
    itemlist=[]
    itemlist.append( Item(channel=CHANNELNAME, action="play" , title="Ver el vídeo" , url="http://www.megavideo.com/?v="+texto,server="megavideo",folder=False) )
    return itemlist
