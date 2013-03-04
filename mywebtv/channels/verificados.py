# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canales verificados
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

logger.info("[verificados.py] init")

DEBUG = True
CHANNELNAME = "Verificados"
CHANNELCODE = "verificados"

def mainlist(params,url,category):
    logger.info("[verificados.py] mainlist")

    add_tve()
    add_rtpa()
    add_aragontv()

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def add_aragontv():
    logger.info("[verificados.py] add_aragontv")

    try:
        MAIN_URL = "http://www.aragontelevision.es/"
        data = scrapertools.cachePage(MAIN_URL)
        titulo = scrapertools.get_match(data,'<div id="banner-streaming-tv" style="position:relative;">(.*?)</div>')
        titulo = unicode( titulo, "iso-8859-1" , errors="replace" ).encode("utf-8")
        titulo = scrapertools.htmlclean(titulo)
        titulo = re.compile("\s+",re.DOTALL).sub(" ",titulo)
        titulo = titulo.strip()

        data = scrapertools.cachePage("http://alacarta.aragontelevision.es/streaming/streaming.html")
        url = scrapertools.get_match(data,"playlist\:\s*\[\s*\{\s*url\: '([^']+)'")
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , "Aragón TV [web] ("+titulo+")" , url , "http://mywebtv.mimediacenter.info/squares/aragontv.png", "" )
    except:
        import traceback
        logger.info(traceback.format_exc())

def add_rtpa():
    logger.info("[verificados.py] add_rtpa")

    try:
        MAIN_URL = "http://www.rtpa.es"
        data = scrapertools.cachePage(MAIN_URL)
        url = scrapertools.get_match(data,'file\: "([^"]+)"')
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , "RTPA (Asturias) [web]" , url , "http://mywebtv.mimediacenter.info/squares/rtpa.png", "" )
        url = scrapertools.get_match(data,'\s+var liveurl \= "([^"]+)"')
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , "RTPA (Asturias) [iOS]" , url , "http://mywebtv.mimediacenter.info/squares/rtpa.png", "" )
    except:
        import traceback
        logger.info(traceback.format_exc())

def add_tve():
    logger.info("[verificados.py] add_tve")

    try:
        MAIN_URL = "http://www.rtve.es/m/alacarta/tve/directos/iphone"

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
            title = scrapedtitle+" [iOS]"
            url = scrapedurl
            thumbnail = urlparse.urljoin(MAIN_URL,scrapedthumbnail)
            plot = ""
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

            # Añade al listado de XBMC
            xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , title , url , thumbnail, plot )

    except:
        pass

def play(params,url,category):
    logger.info("[verificados.py] play")
    
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = "Directo"
    
    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
