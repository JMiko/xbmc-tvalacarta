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
from platform.xbmc import library
from platform.xbmc import launcher
from pelisalacarta.channels import seriesyonkis
#from pelisalacarta.channels import cuevana
import xbmcgui

try:
    
    #Eliminar carpeta antes de actualizar
    
    import shutil
    directorio = config.get_library_path()+"\SERIES"
    logger.info (directorio)
    shutil.rmtree(directorio)
    os.mkdir(directorio)
    
    
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , "series.xml" )
    config_canal = open( nombre_fichero_config_canal , "r" )

    for serie in config_canal.readlines():
        serie = serie.split(",")
        logger.info("[library_service.py] Actualizando "+serie[2])
        item = Item(url=serie[1])
        if serie[2]=='seriesyonkis\n': itemlist = seriesyonkis.episodios(item)
        #if serie[2]=='cuevana\n': itemlist = cuevana.episodios(item)
        i=0
        for item in itemlist:
            i = i + 1
            item.show=serie[0]
            if i<len(itemlist):
                library.savelibrary( titulo=item.title , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Series" , Serie=item.show , verbose=False, accion="strm_detail", pedirnombre=False, subtitle=item.subtitle )

    import xbmc
    xbmc.executebuiltin('UpdateLibrary(video)')

except:
    logger.info("[library_service.py] Error al actualizar la biblioteca")
    import sys
    for line in sys.exc_info():
        logger.error( "%s" % line )
