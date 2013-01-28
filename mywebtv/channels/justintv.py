# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Justin.tv
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

logger.info("[justintv.py] init")

DEBUG = True
CHANNELNAME = "Justin.tv"
CHANNELCODE = "justintv"
LANGUAGES_URL = "http://www.justin.tv/directory/dropmenu/language/all?order=hot&amp;lang=es"
CATEGORIES_URL = "http://www.justin.tv/directory/dropmenu/category/featured?lang=%s"
CHANNELS_URL = "http://www.justin.tv/directory/%s?lang=%s"

def mainlist(params,url,category):
    logger.info("[justintv.py] mainlist")
    
    data = scrapertools.cachePage(LANGUAGES_URL)
    patron = '<li class="language_filter"[^<]+<a href="([^"]+)"><span>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(LANGUAGES_URL,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "categories" , CHANNELNAME , title , url , thumbnail, plot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def categories(params,url,category):
    logger.info("[justintv.py] mainlist")

    language = scrapertools.get_match(url,"lang=([a-z]+)")

    data = scrapertools.cachePage(CATEGORIES_URL % language)
    patron = '<li class="category"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    xbmctools.addnewfolder( CHANNELCODE , "channels" , CHANNELNAME , "Featured" , "http://www.justin.tv/directory/featured?lang="+language , "", "" )

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        thumbnail = ""
        plot = ""
        url = urlparse.urljoin(url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "channels" , CHANNELNAME , title , url , thumbnail, plot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def channels(params,url,category):
    logger.info("[justintv.py] mainlist")

    try:
        actualpage = scrapertools.get_match(url,"page\=(\d+)")
        next_page_url = url.replace("page="+actualpage,"page="+str(int(actualpage)+1))
        logger.info("[justintv.py] next_page_url="+next_page_url)
    except:
        actualpage = "1"
        next_page_url = url+"&page=2"
        logger.info("[justintv.py] next_page_url="+next_page_url)

    data = scrapertools.cachePage(url)
    patron  = '<li id="channel[^<]+<div[^<]+'
    patron += '<a class="thumb" href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '<a[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        thumbnail = scrapedthumbnail
        plot = ""
        url = urlparse.urljoin(url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , title , url , thumbnail , "" )

    xbmctools.addnewfolder( CHANNELCODE , "channels" , CHANNELNAME , ">> Página siguiente" , next_page_url , "" , "" )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[justintv.py] play")
    
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = "justintv"
    
    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
