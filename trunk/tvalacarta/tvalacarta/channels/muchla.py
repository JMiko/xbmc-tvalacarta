# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# MuchMusic Lationamérica
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#
# Autor: Juan Pablo Candioti (@JPCandioti)
# Desarrollo basado sobre otros canales de tvalacarta
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "muchla"
MAIN_URL = "http://www.muchla.com"


def isGeneric():
    return True


def mainlist(item):
    logger.info("[cda.py] mainlist")

    itemlist = []
    #itemlist.append( Item(channel=CHANNELNAME, title="Todos"            , action="videos"    , url=MAIN_URL+"/videos?p_p_id=videoselectorportlet_WAR_videoselectorportlet&p_p_lifecycle=2&_videoselectorportlet_WAR_videoselectorportlet_jspPage=/html/portlet/video-selector/video-selector-display.jsp"                                                                                                     , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos videos"   , action="videos"    , url=MAIN_URL+"/videos?p_p_id=videoselectorportlet_WAR_videoselectorportlet&p_p_lifecycle=2&_videoselectorportlet_WAR_videoselectorportlet_jspPage=/html/portlet/video-selector/video-selector-display.jsp&_videoselectorportlet_WAR_videoselectorportlet_VIDEO_FILTER_STRATEGY_NAME=LAST_VIDEOS_STRATEGY"      , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Videos más vistos", action="videos"    , url=MAIN_URL+"/videos?p_p_id=videoselectorportlet_WAR_videoselectorportlet&p_p_lifecycle=2&_videoselectorportlet_WAR_videoselectorportlet_jspPage=/html/portlet/video-selector/video-selector-display.jsp&_videoselectorportlet_WAR_videoselectorportlet_VIDEO_FILTER_STRATEGY_NAME=TOP_VIEWED_VIDEOS_STRATEGY", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Categorias"       , action="categorias", url=MAIN_URL+"/videos", folder=True) )

    return itemlist


def categorias(item):
    logger.info("[" + CHANNELNAME + "] categorias")
    
    # Descargo la página principal de videos.
    data = scrapertools.cachePage(item.url)
    if (DEBUG): logger.info(data)

    # Extraigo la URL y el nombre de las categorias.
    patron  = '<div class="category_list_item">\s*<a href="javascript:search_videos\(\'(.*?)\'\)".*?>(.*?)</a>\s*</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for categoria_url, categoria_name in matches:
        # Añado el item de la categoria al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=categoria_name , action="videos", url=categoria_url, folder=True) )

    return itemlist


def videos(item):
    logger.info("[" + CHANNELNAME + "] videos")

    # Descargo la página de la sección.
    data = scrapertools.cachePage(item.url)
    if (DEBUG): logger.info(data)

    # Extraigo URL, imagen, título y nombre de categoría.
    patron  = '<div class="video_preview">\s*?<a href="(.*?)">\s*?<img src="(.*?)"/>\s*?</a>\s*?<div class="artist">(.*?)</div>\s*?<div class="song">(.*?)</div>\s*?</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for iurl, ithumbnail, name, categoria_name in matches:
        ititle = name
        # Si los videos son de la categoría seleccionada no debería mostrarse.
        if item.title != categoria_name:
            ititle += ' (' + categoria_name + ')'

        # Añado el item de la calidad al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=ititle, action="reproducir", url=MAIN_URL+iurl, thumbnail=ithumbnail, folder=True) )

    return itemlist


def reproducir(item):
    logger.info("[" + CHANNELNAME + "] reproducir")

    # Descargo la página del video.
    data = scrapertools.cachePage(item.url)
    if (DEBUG): logger.info(data)

    iurl = scrapertools.get_match(data, 'file:"(.*?)"')

    itemlist = [Item(channel=CHANNELNAME, title=item.title, action="play", url=iurl, thumbnail=item.thumbnail, folder=False)]

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():

    # Todas las opciones tienen que tener algo
    items = mainlist(Item())
    for item in items:
        if item.title!="Videos más vistos":
            exec "itemlist="+item.action+"(item)"
        
            if len(itemlist)==0:
                print "La sección '"+item.title+"' no devuelve videos"
                return False

    return True