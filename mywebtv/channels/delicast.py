# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Delicast
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

logger.info("[delicast.py] init")

DEBUG = True
CHANNELNAME = "Delicast"
CHANNELCODE = "delicast"

def mainlist(params,url,category):
    logger.info("[delicast.py] mainlist")

    # Añade al listado de XBMC
    xbmctools.addnewfolder( CHANNELCODE , "paises" , CHANNELNAME , "Todos los canales por paises" , "http://es.delicast.com" , "" , "" )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def paises(params,url,category):
    logger.info("[delicast.py] paises")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los paises
    # --------------------------------------------------------
    patron = '<a class=v href=([^>]+)>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "videos" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videos(params,url,category):
    logger.info("[delicast.py] videos")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae las cadenas
    # --------------------------------------------------------
    patron = '<a class=s1 href="([^"]+)">([^<]+)</a></TD><TD width=100%><a class=s href="[^"]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[2]+" ("+match[1]+")"
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = scrapedurl
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # --------------------------------------------------------
    # Página siguiente
    # --------------------------------------------------------
    patron = "<a class=n href='([^']+)'><U>Siguiente .raquo.</U></a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Página siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "videos" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[delicast.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = "Directo"
    
    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae la URL
    # --------------------------------------------------------
    #location.replace("mms://streamingtv01.ib3.es/ib3tv_en_directe")
    patron = 'location.replace\("([^"]+)"\)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    url = matches[0]

    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
