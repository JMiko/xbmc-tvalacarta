# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Clan TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item
from core import jsontools

DEBUG = True
CHANNELNAME = "clantve"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.clantv mainlist")

    itemlist = []
    #itemlist.append( Item(channel=CHANNELNAME, title="Últimos vídeos añadidos" , url="http://www.rtve.es/infantil/components/TE_INFDEF/videos/videos-1.inc" , action="ultimos_videos" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , url="http://www.rtve.es/api/agr-programas/490/programas.json?size=60&page=1" , action="programas" , folder=True) )
    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.clantv programas")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    #logger.info("json_object="+json_object)
    json_items = json_object["page"]["items"]

    for json_item in json_items:
        title = json_item["name"]
        url = json_item["uri"]
        thumbnail = json_item["imgPoster"]
        if json_item["description"] is not None:
            plot = json_item["description"]
        else:
            plot = ""
        fanart = json_item["imgPortada"]
        page = url
        if (DEBUG): logger.info(" title=["+repr(title)+"], url=["+repr(url)+"], thumbnail=["+repr(thumbnail)+"] plot=["+repr(plot)+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="episodios" , url=url, thumbnail=thumbnail, plot=plot , page=page, show=title , fanart=fanart, viewmode="movie_with_plot", folder=True) )

    # Añade el resto de páginas
    current_page = scrapertools.find_single_match(item.url,'page=(\d+)')
    next_page = str( int(current_page)+1 )
    itemlist.append(Item(channel=CHANNELNAME,action="programas",title=">> Página siguiente",url=item.url.replace("page="+current_page,"page="+next_page), folder=True))

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.clantv episodios")

    itemlist = []

    # Descarga la página
    url = item.url+"/videos.json"
    data = scrapertools.cache_page(url)
    json_object = jsontools.load_json(data)
    #logger.info("json_object="+json_object)
    json_items = json_object["page"]["items"]

    for json_item in json_items:
        title = json_item["longTitle"]
        url = json_item["uri"]
        thumbnail = item.thumbnail
        if json_item["description"] is not None:
            plot = json_item["description"]
        else:
            plot = ""
        fanart = item.fanart
        page = url
        if (DEBUG): logger.info(" title=["+repr(title)+"], url=["+repr(url)+"], thumbnail=["+repr(thumbnail)+"] plot=["+repr(plot)+"]")
        itemlist.append( Item(channel="rtve", title=title , action="play" , server="rtve", page=page, url=url, thumbnail=thumbnail, fanart=thumbnail, show=item.show , plot=plot , viewmode="movie_with_plot", folder=False) )

    from core import config
    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=item.channel, title=">> Opciones para esta serie", url=item.url, action="serie_options##episodios", thumbnail=item.thumbnail, show=item.show, folder=False))

    return itemlist
