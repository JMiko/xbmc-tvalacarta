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

    # Lee el script
    data = scrapertools.cachePage("http://chitawar.blogspot.com.es/p/blog-page_20.html")
    patron = '<li><span style="color: magenta;">SIMPLETV:</span> <span style="color: red;">(.*?)</span></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if matches:
        data = scrapertools.cachePage(matches[0])
        patron = '#EXTINF:-1 \$ExtFilter="(.*?)",(.*?)(?:\n|\r|\r\n?)(?:\n|\r|\r\n?)(.*?)(?:\n|\r|\r\n?)'

        # Busca el bloque con los canales
        matches = re.compile(patron,re.DOTALL|re.MULTILINE).findall(data)

        scrapertools.printMatches(matches)
        for match in matches:
            if "Canales +18".upper() in match[1].upper(): continue
            if "Radios".upper() in match[1].upper(): continue
            if "Radios".upper() in match[0].upper(): continue
            if "Estrenos".upper() in match[0].upper(): continue
            scrapedtitle = match[0].upper() + ' - ' + match[1].upper()
            if "rtmp" in match[2]:
                scrapedurl = match[2].replace("rtmp://$OPT:rtmp-raw=","").replace("live=1", "live=true") + " timeout=120"
            else:
                scrapedurl = match[2]               
            xbmctools.addnewfolder( CHANNELCODE , "play" , CHANNELNAME , scrapedtitle , scrapedurl , "", "" )

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
