# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para chachimovies
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse, urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools
import string
import config
import logger

CHANNELNAME = "chachimovies"

# Esto permite su ejecución en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[chachimovies.py] init")

DEBUG = True

def mainlist(params,url,category):
    logger.info("[chachimovies.py] mainlist")

    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Todas las Películas" , "http://chachimovies.wordpress.com/category/peliculas/feed" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Estrenos Cine" , "http://chachimovies.wordpress.com/category/estrenos-cine/feed" , "", "" )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def movielist(params,url,category):
    logger.info("[chachimovies.py] mainlist")

    # Descarga la página
    data = scrapertools.cachePage(url)
    #print data
    
    start_index = "1"
    start_index_re = "start-index=(.*)&"
    url_params = url.split("?",1)
    url_limpia = url_params[0]
    matches = re.compile(start_index_re,re.DOTALL).findall(url)

    if len(matches)>0:
        start_index = matches[0]
        new_start = int(start_index) + 50

    #Para evitar problemas cuando el XML no esta completo o bien estructurado (que por desgracia pasa)
    entrada_blog_re = '<item>(.*?)</item>'

    # Expresion Regular para extraer la info
    patronvideos  = '<title>(.*?)</title>.*?'
    patronvideos += '<link>(.*?)</link>.*?'
    patronvideos += '<description>(.*?)</description>.*?'
    patronvideos += '<media\:content url\="(http\:\/\/chachimovies.files.wordpress.com[^"]+)"'
    
    matches = re.compile(entrada_blog_re,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    #Procesamos cada coincidencia 
    for match in matches:
        entrada_blog = match
        print match
        matches_entradas = re.compile(patronvideos,re.DOTALL).findall(entrada_blog)
        for match2 in matches_entradas:

            # Titulo
            scrapedtitle = match2[0]

            # URL
            scrapedurl = match2[1]
        
            # Thumbnail
            scrapedthumbnail = match2[3]
            
            # Argumento
            scrapedplot = match2[2]

            # Depuracion
            if (DEBUG):
                logger.info("scrapedtitle="+scrapedtitle)
                logger.info("scrapedurl="+scrapedurl)
                logger.info("scrapedthumbnail="+scrapedthumbnail)

            # Añade al listado de XBMC
            xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        
    if len(matches)>45:
        scrapedurl = url_limpia+"?start-index="+str(new_start)+"&max-results=50" 
        xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Página Siguiente" , scrapedurl , "", "" )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
    logger.info("[chachimovies.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        xbmctools.addnewvideo( CHANNELNAME , "play" , category , video[2] , title + " - " + video[0] , video[1] , thumbnail , "" )
    # ------------------------------------------------------------------------------------

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[chachimovies.py] play")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )
    server = params["server"]

    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

