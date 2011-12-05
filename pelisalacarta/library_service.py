# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc,time

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

logger.info("[library_service.py] Actualizando series...")
from platformcode.xbmc import library
from platformcode.xbmc import launcher
from pelisalacarta.channels import seriesyonkis
from pelisalacarta.channels import cuevana
import xbmcgui

#Eliminar carpeta antes de actualizar

directorio = os.path.join(config.get_library_path(),"SERIES")
logger.info ("directorio="+directorio)
import shutil

#if os.path.exists(directorio):
#    shutil.rmtree(directorio)

if not os.path.exists(directorio):
    os.mkdir(directorio)

nombre_fichero_config_canal = os.path.join( config.get_data_path() , "series.xml" )

try:
    config_canal = open( nombre_fichero_config_canal , "r" )
    
    for serie in config_canal.readlines():
        logger.info("[library_service.py] serie="+serie)
        serie = serie.split(",")
    
        ruta = os.path.join( config.get_library_path() , "SERIES" , serie[0] )
        logger.info("[library_service.py] ruta =#"+ruta+"#")
        if os.path.exists( ruta ):
            logger.info("[library_service.py] Actualizando "+serie[0])
            item = Item(url=serie[1], show=serie[0])
            try:
                if serie[2].strip()=='seriesyonkis': itemlist = seriesyonkis.episodios(item)
                if serie[2].strip()=='cuevana': itemlist = cuevana.episodios(item)
            except:
                itemlist = []
        else:
            logger.info("[library_service.py] No actualiza "+serie[0]+" (no existe el directorio)")
            itemlist=[]
            
        i=0
        for item in itemlist:
            i = i + 1
            item.show=serie[0].strip()
            if i<len(itemlist):
                library.savelibrary( titulo=item.title , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Series" , Serie=item.show , verbose=False, accion="play_from_library", pedirnombre=False, subtitle=item.subtitle )
    
    import xbmc
    xbmc.executebuiltin('UpdateLibrary(video)')

except:
    logger.info("[library_service.py] No hay series para actualizar")
