# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal para la sexta
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[sexta.py] init")

DEBUG = True
CHANNELNAME = "lasexta"
MAIN_URL = "http://www.lasexta.com/programas"
def isGeneric():
    return True

def mainlist(item):
    logger.info("[sexta.py] mainlist")
    itemlist=[]
    
    itemlist.append( Item(channel="antena3", title="Series"         , action="series"       , url="http://www.lasexta.com/videos/series.html", folder=True) )
    itemlist.append( Item(channel="antena3", title="Noticias"       , action="series"     , url="http://www.lasexta.com/videos/noticias.html", folder=True) )
    itemlist.append( Item(channel="antena3", title="Programas"      , action="series"    , url="http://www.lasexta.com/videos/programas.html", folder=True) )
    itemlist.append( Item(channel="antena3", title="Xplora"         , action="series"       , url="http://www.lasexta.com/videos/videos-xplora.html", folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # Todas las opciones tienen que tener algo
    items = mainlist(Item())
    import antena3
    for item in items:
        exec "itemlist=antena3."+item.action+"(item)"
    
        if len(itemlist)==0:
            return False

    # La sección de programas devuelve enlaces
    series = antena3.series(items[2])
    episodios = antena3.episodios(series[0])
    videos = antena3.detalle(episodios[0])
    if len(videos)==0:
        return False

    return bien
