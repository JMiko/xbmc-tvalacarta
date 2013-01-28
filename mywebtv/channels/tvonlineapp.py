# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal tvonlineapp.com
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

logger.info("[tvonlineapp.py] init")

DEBUG = True
CHANNELNAME = "tvonlineapp.com"
CHANNELCODE = "tvonlineapp"
MAIN_URL = "http://tvonlineapp.com/app/veotv/"

def mainlist(params,url,category):
    logger.info("[tvonlineapp.py] mainlist")
    paises(params,url,category)

def paises(params,url,category):
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cachePage2(MAIN_URL,headers)

    data = scrapertools.get_match(data,'<div data-role="page" id="page2"(.*?)<div data-role="page" id="page3">')
    
    patron  = '<li[^<]+'
    patron += '<a class="[^"]+" href="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^>]+>[^<]+'
    patron += '<h3[^>]+>([^<]+)</h3></a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url = scrapedurl
        thumbnail = urlparse.urljoin(MAIN_URL,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "emisoras" , CHANNELNAME , title , url , thumbnail , plot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def emisoras(params,url,category):
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cachePage2(url,headers)
    
    patron  = '<li[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '<h3[^>]+>([^<]+)</h3>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url = scrapedurl
        thumbnail = urlparse.urljoin(url,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "justintv" , title , url , thumbnail, plot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[tvonlineapp.py] play")

    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cachePage2(url,headers)
    logger.info("data="+data)

    from servers import justintv
    videos = justintv.find_videos(data)
    server="justintv"

    if len(videos)==0:
        from servers import ustream
        videos = ustream.find_videos(data)
        server="ustream"

    for titulo,url,serverfound in videos:
        title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
        plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    
        xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
