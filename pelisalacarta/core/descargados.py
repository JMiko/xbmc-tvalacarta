# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import config
from core import logger
from core.item import Item

CHANNELNAME = "descargados"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[descargados.py] mainlist")
    itemlist=[]

    # Lee la ruta de descargas
    downloadpath = config.get_setting("downloadpath")

    logger.info("[descargados.py] downloadpath=" + downloadpath)
    #logger.info("[descargados.py] pluginhandle=" + pluginhandle)

    itemlist.append( Item( channel="descargadoslist", action="mainlist", title="Descargas pendientes"))
    itemlist.append( Item( channel="descargadoslist", action="errorlist", title="Descargas con error"))

    # Añade al listado de XBMC
    try:
        ficheros = os.listdir(downloadpath)
        for fichero in ficheros:
            logger.info("[descargados.py] fichero=" + fichero)
            if fichero!="lista" and fichero!="error" and fichero!=".DS_Store" and not fichero.endswith(".nfo") and not fichero.endswith(".tbn") and os.path.join(downloadpath,fichero)!=config.get_setting("downloadlistpath"):
                url = os.path.join( downloadpath , fichero )
                itemlist.append( Item( channel="descargados", action="play_video", title=fichero, url=url, server="local", folder=False))

    except:
        logger.info("[descargados.py] exception on mainlist")
        pass

    return itemlist
