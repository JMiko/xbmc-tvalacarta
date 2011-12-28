# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para ver una peli en Megaupload conociendo el codigo
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

from pelisalacarta import buscador

__channel__ = "megauploadsite"
__category__ = "G"
__type__ = "xbmc"
__title__ = "Megaupload"
__language__ = ""

DEBUG = config.get_setting("debug")

# Esto permite su ejecución en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

logger.info("[megaupload.py] init")

def mainlist(params,url,category):
    logger.info("[megaupload.py] mainlist")

    # Añade al listado de XBMC
    xbmctools.addnewfolder( __channel__ , "search" , __channel__ , "Introduce el código del fichero de vídeo" , "" , "", "" )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
    logger.info("[megaupload.py] list")

    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            list(params,tecleado,category)

def list(params,url,category):
    logger.info("[megaupload.py] list")

    xbmctools.addnewvideo( __channel__ , "play" , category , "Megaupload" , "Ver el vídeo [Megaupload]" , url , "" , "" )

    # Asigna el título, desactiva la ordenación, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[megaupload.py] list")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)
