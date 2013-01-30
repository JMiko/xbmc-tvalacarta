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
    data = scrapertools.cachePage("https://googledrive.com/host/0B0MauuTdUSzpOFJsUmlVa1lueTQ/SimpleTV.html")
    #data = data.replace("\n", " ")
    #data = data.replace("\n\r", " ")
    #data = " ".join(data.split())
    logger.info(data)
    #EXTINF:-1 $ExtFilter="España",Canales canal +:Canal + Golf  rtmp://$OPT:rtmp-raw=rtmp://cdn.icricket.tv/secure/?auth=a8cc0c8414a61b02ea371455659383ec50edb5a2d4a9 f playpath=ch8.stream swfUrl=http://www.igoal.tv/player.swf live=1 pageUrl=http://www.igoal.tv/get.php?id=22&reload=1357758436395
    patron = '#EXTINF:-1 \$ExtFilter=(.*?),(.*?)(?:\n|\r|\r\n?)(?:\n|\r|\r\n?)(.*?)(?:\n|\r|\r\n?)'

    # Busca el bloque con los canales
    matches = re.compile(patron,re.DOTALL|re.MULTILINE).findall(data)

    scrapertools.printMatches(matches)
    for match in matches:
        if "Canales +18" in match[1]: continue
        if "Radios" in match[1]: continue
        if not "rtmp" in match[2]: continue
        scrapedfilter = match[0]
        scrapedtitle = match[1]
        scrapedurl = match[2].replace("rtmp://$OPT:rtmp-raw=","").replace("live=1", "live=true")
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
