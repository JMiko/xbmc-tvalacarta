# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para vertelenovelasonline
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import config
from core import logger
from platformcode.xbmc import xbmctools
from core.item import Item
from servers import servertools
from servers import vk

from pelisalacarta import buscador

__channel__ = "vertelenovelasonline"
__category__ = "S"
__type__ = "xbmc"
__title__ = "Ver Telenovelas Online"
__language__ = "ES"

DEBUG = config.get_setting("debug")

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[vertelenovelasonline.py] init")

def mainlist(params,url,category):
    logger.info("[vertelenovelasonline.py] mainlist")

    # Menu principal
    xbmctools.addnewfolder( __channel__ , "newlist" , __channel__ , "Novedades" , "http://www.vertelenovelasonline.com/" , "", "" )
    
    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def newlist(params,url,category):
    logger.info("[vertelenovelasonline.py] listmirrors")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<a onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}" href="http://www.vertelenovelasonline.com/2009/11/amor-palos.html">
    #<img style="cursor:pointer; cursor:hand;width: 186px; height: 320px;" src="http://1.bp.blogspot.com/__kdloiikFIQ/SwSWTExa3NI/AAAAAAAAl9Q/JmBSh1D40kE/s320/amor+a+palos.jpg" border="0" alt=""id="BLOGGER_PHOTO_ID_5405610707194141906" /></a><a onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}" href="http://www.vertelenovelasonline.com/2009/11/alcanzar-una-estrella-ii.
    #<a onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}" href="http://www.vertelenovelasonline.com/2009/10/catalina-y-sebastian.html">
    #<img style="cursor: pointer; width: 186px; height: 320px;" src="http://4.bp.blogspot.com/__kdloiikFIQ/SuH75qhmrfI/AAAAAAAAk8A/aLUZX2HAmUY/s320/catalina+y+sebastian.jpg" alt="" id="BLOGGER_PHOTO_ID_5395870796652916210" border="0" /></a><a onblur="
    patron  = '<a onblur="[^"]+" href="([^"]+)">'
    patron += '<img style="[^"]+" src="([^"]+)"[^>]+></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # http://www.vertelenovelasonline.com/2009/10/dona-barbara.html
        scrapedtitle = match[0][44:-5]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listmirrors(params,url,category):
    logger.info("[vertelenovelasonline.py] listmirrors")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae la sinopsis
    patron  = '<span style="font-weight: bold;">(.*?)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        plot = matches[0].strip()
        logger.info(plot)

    #<a style="color: rgb(51, 51, 255);" href="http://www.vertelenovelasonline.com/2009/10/dona-barbara-1-50.html" target="_blank"> capitulo 1-50.</a><br /><br /><a style="color: rgb(51, 51, 255);" href="http://www.vertelenovelasonline.com/
    #<a style="color: rgb(51, 51, 255);" href="http://www.vertelenovelasonline.com/2009/10/amor-real-1.html"> capitulo 1.</a>
    patron = '<a style="color. rgb\([^\,]+, [^\,]+, [^\)]+\)." href="(http://www.vertelenovelasonline.com/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = thumbnail
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
    logger.info("[vertelenovelasonline.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        videotitle = video[0]
        url = video[1]
        server = video[2]
        xbmctools.addnewvideo( __channel__ , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
    # ------------------------------------------------------------------------------------

    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[vertelenovelasonline.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)
