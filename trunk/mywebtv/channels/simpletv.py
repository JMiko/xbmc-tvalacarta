# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal SimpleTV
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import binascii
import xbmctools
from core import config
from core import logger
from core.item import Item

import simpletv_multiplataforma

try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

logger.info("[simpletv.py] init")

DEBUG = True
CHANNELNAME = "SimpleTV"
CHANNELCODE = "simpletv"

def mainlist(params,url,category):
    logger.info("[simpletv.py] mainlist")

    itemlist = simpletv_multiplataforma.mainlist(Item())
    for item in itemlist:
        xbmctools.addnewfolder( CHANNELCODE , "play" , CHANNELNAME , item.title , item.url , "", "" )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[simpletv.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = "Directo"

    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
