# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal Descarregadirecta Carles Carmona
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

logger.info("Series.py - Actualización de series")
from platform.xbmc import library
from platform.xbmc import launcher
from pelisalacarta.channels import seriesyonkis
import xbmcgui
  
series = config.get_setting("series","series")

if (isinstance(series,str)):
    serie = series.split(",")
    item = Item(url=serie[1])
    itemlist = seriesyonkis.episodios(item)
    i=0
    for item in itemlist:
        i = i + 1
        item.show=serie[0]
        if i<len(itemlist):
            library.savelibrary( titulo=item.title , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Series" , Serie=item.show , verbose=False, accion="strm_detail", pedirnombre=False, subtitle=item.subtitle )
else:    
    for serie in series:
        serie = serie.split(",")
        logger.info(serie)
        item = Item(url=serie[1])
        itemlist = seriesyonkis.episodios(item)
        i=0
        for item in itemlist:
            i = i + 1
            item.show=serie[0]
            if i<len(itemlist):
                library.savelibrary( titulo=item.title , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Series" , Serie=item.show , verbose=False, accion="strm_detail", pedirnombre=False, subtitle=item.subtitle )
