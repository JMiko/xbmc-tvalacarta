# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de v�deos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import downloadtools
from core import logger

CHANNELNAME = "descargados"

# Traza el inicio del canal
logger.info("[descargados.py] init")

DEBUG = True

def mainlist(params,url,category):
    import xbmc
    import xbmcgui
    import xbmcplugin
    from core import xbmctools

    logger.info("[descargados.py] mainlist")

    # Verifica ruta de descargas
    downloadpath = downloadtools.getDownloadPath()
    logger.info("[descargados.py] downloadpath=" + downloadpath)
    #logger.info("[descargados.py] pluginhandle=" + pluginhandle)

    xbmctools.addnewfolder( "descargadoslist" , "mainlist"  , category , "Descargas pendientes","","","")
    xbmctools.addnewfolder( "descargadoslist" , "errorlist"  , category , "Descargas con error","","","")

    # A�ade al listado de XBMC
    try:
        ficheros = os.listdir(downloadpath)
        for fichero in ficheros:
            logger.info("[descargados.py] fichero=" + fichero)
            if fichero!="lista" and fichero!="error" and fichero!=".DS_Store" and not fichero.endswith(".nfo") and not fichero.endswith(".tbn") and os.path.join(downloadpath,fichero)!=downloadtools.getDownloadListPath():
                url = os.path.join( downloadpath , fichero )
                listitem = xbmcgui.ListItem( fichero, iconImage="DefaultVideo.png" )
                xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url = url, listitem=listitem, isFolder=False)
    except:
        logger.info("[descargados.py] exception on mainlist")
        pass
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
