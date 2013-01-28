# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal TVE
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

logger.info("[tve.py] init")

DEBUG = True
CHANNELNAME = "TVE"
CHANNELCODE = "tve"
MAIN_URL = "http://www.rtve.es/m/alacarta/tve/directos/iphone"
def mainlist(params,url,category):
    logger.info("[tve.py] mainlist")
    
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cachePage2(MAIN_URL,headers)
    
    patron  = '<li class="video"[^<]+'
    patron += '<p class="tag">video en directo</p[^<]+'
    patron += '<h4>([^<]+)</h4.*?'
    patron += '<p class="thumb"><img src="([^"]+)"[^<]+</p[^<]+'
    patron += '<a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedtitle,scrapedthumbnail,scrapedurl in matches:
        title = scrapedtitle
        url = scrapedurl
        thumbnail = urlparse.urljoin(MAIN_URL,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , title , url , thumbnail, plot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def lista(params,url,category):
    logger.info("[tve.py] lista")

    data = scrapertools.cachePage(url)

    # Extrae los paises
    patron  = '<channel>[^<]+'
    patron += '<name>([^<]+)</name>[^<]+'
    patron += '<thumbnail>([^<]+)</thumbnail>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = match[0]+"|#|"+url
        scrapedthumbnail = match[1]
        if scrapedthumbnail=="none":
            scrapedthumbnail=""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "videos" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videos(params,url,category):
    logger.info("[tve.py] videos")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    channel_id = url.split("|#|")[0]
    url = url.split("|#|")[1]
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae las cadenas
    # --------------------------------------------------------
    patron  = '<channel>[^<]+'
    patron += '<name>'+channel_id.replace("\\","\\\\")+'</name>(.*?)</channel'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        data = matches[0]

        patron  = '<title>([^<]+)</title>.*?'
        patron += '<link>([^<]+)</link>.*?'
        patron += '<thumbnail>([^<]+)</thumbnail>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        for match in matches:
            scrapedtitle = match[0]
            scrapedurl = match[1]
            scrapedthumbnail = match[2]
            scrapedplot = scrapedurl
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado de XBMC
            xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[tivion.py] play")
    
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = "Directo"
    
    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
