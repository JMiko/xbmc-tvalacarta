# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal community-links
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

logger.info("[community_links.py] init")

DEBUG = True
CHANNELNAME = "Community-links"
CHANNELCODE = "community_links"

def mainlist(params,url,category):
    logger.info("[community_links.py] mainlist")
    
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "theStreamDB","https://community-links.googlecode.com/svn/trunk/theStreamDB.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "theStreamDB.for.Apple.TV","https://community-links.googlecode.com/svn/trunk/theStreamDB.for.Apple.TV.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "hamradio","https://community-links.googlecode.com/svn/trunk/hamradio.TV.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "divingmulesStreams","https://community-links.googlecode.com/svn/trunk/divingmulesStreams.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "arabic","https://community-links.googlecode.com/svn/trunk/arabic.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "SidhuTV","https://community-links.googlecode.com/svn/trunk/SidhuTV.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "Radio","https://community-links.googlecode.com/svn/trunk/Radio.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "Live-CAMs","https://community-links.googlecode.com/svn/trunk/Live-CAMs.xml","","")
    xbmctools.addnewfolder( CHANNELCODE , "lista" , CHANNELNAME , "AxisCCTV","https://community-links.googlecode.com/svn/trunk/AxisCCTV.xml","","")

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def lista(params,url,category):
    logger.info("[community_links.py] lista")

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
    logger.info("[community_links.py] videos")

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
