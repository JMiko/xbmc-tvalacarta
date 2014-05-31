# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para rtpa
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib
import os

from core import config
from core import logger
from core import scrapertools
from core import jsontools
from core.item import Item

DEBUG = config.get_setting("debug")
CHANNELNAME = "rtpa"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.rtpa mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos vídeos añadidos" , url="http://www.rtpa.es/json/vod_parrilla_8.json" , action="novedades" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Programas actuales (con sinopsis)" , url="http://www.rtpa.es/json/programas_actuales_tpa.json" , action="programas_actuales" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , url="http://www.rtpa.es/json/vod_programas.json" , action="programas" , folder=True) )

    return itemlist

def novedades(item):
    logger.info("tvalacarta.channels.rtpa novedades")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    #logger.info("json_object="+repr(json_object))

    for vod in json_object["VOD"]:
        title = vod["nombre_programa"]
        if vod["titulo"]!="":
            title = title + " - " + vod["titulo"]
        
        # http://www.rtpa.es/video:Caballos%20de%20metal_551396652766.html
        url = "http://www.rtpa.es/video:"+urllib.quote(vod["nombre_programa"])+"_"+vod["id_generado"]+".html"

        thumbnail = urllib.quote(vod["url_imagen"]).replace("//","/").replace("http%3A/","http://")
        plot = vod["sinopsis"]
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , plot=plot, server="rtpa", action="play" , show = item.title , folder=False) )

    return itemlist

def programas_actuales(item):
    logger.info("tvalacarta.channels.rtpa programas_actuales")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    #logger.info("json_object="+repr(json_object))
    #logger.info("VOD="+repr(json_object["VOD"]))

    for vodlist in json_object["programas"]:
        
        for vod in vodlist:
            title = vod["nombre"]

            # http://www.rtpa.es/programa:LA%20QUINTANA%20DE%20POLA_1329394981.html
            #url = "http://www.rtpa.es/programa:"+urllib.quote(vod["nombre_programa"])+"_"+vod["id_programa"]+".html"

            # http://www.rtpa.es/api/muestra_json_vod.php?id_programa=1293185502
            url = "http://www.rtpa.es/api/muestra_json_vod.php?id_programa="+vod["id_generado"]
            thumbnail = urllib.quote(vod["imagen"]).replace("//","/").replace("http%3A/","http://")
            plot = scrapertools.htmlclean(vod["sinopsis"])
            itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , plot=plot, fanart=thumbnail, action="episodios" , show = item.title , viewmode="movie_with_plot", folder=True) )

    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.rtpa programas")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    #logger.info("json_object="+repr(json_object))
    #logger.info("VOD="+repr(json_object["VOD"]))

    for vodlist in json_object["VOD"]:
        
        for vod in vodlist:
            title = vod["nombre_programa"]

            # http://www.rtpa.es/programa:LA%20QUINTANA%20DE%20POLA_1329394981.html
            #url = "http://www.rtpa.es/programa:"+urllib.quote(vod["nombre_programa"])+"_"+vod["id_programa"]+".html"

            # http://www.rtpa.es/api/muestra_json_vod.php?id_programa=1293185502
            url = "http://www.rtpa.es/api/muestra_json_vod.php?id_programa="+vod["id_programa"]
            thumbnail = urllib.quote(vod["url_imagen"]).replace("//","/").replace("http%3A/","http://")
            plot = ""
            itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , plot=plot, action="episodios" , show = item.title , viewmode="movie", folder=True) )

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.rtpa episodios")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    #logger.info("json_object="+repr(json_object))
    #logger.info("VOD="+repr(json_object["VOD"]))

    for vod in json_object["VOD"]:
        title = vod["nombre_programa"]
        if vod["titulo"]!="":
            title = title + " - " + vod["titulo"]
        if vod["fecha_emision"]!="":
            title = title + " ("+scrapertools.htmlclean(vod["fecha_emision"])+")"
        url = "http://www.rtpa.es/video:"+urllib.quote(vod["nombre_programa"])+"_"+vod["id_generado"]+".html"
        thumbnail = urllib.quote(vod["url_imagen"]).replace("//","/").replace("http%3A/","http://")
        plot = scrapertools.htmlclean(vod["sinopsis"])
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , plot=plot, fanart=thumbnail, server="rtpa", action="play" , show = item.title , viewmode="movie_with_plot", folder=False) )

    return itemlist

def test():

    # Al entrar sale una lista de categorias
    categorias_items = mainlist(Item())
    if len(categorias_items)==0:
        print "No devuelve categorias"
        return False

    programas_items = programas(categorias_items[-1])
    if len(programas_items)==0:
        print "No devuelve programas en "+categorias_items[0]
        return False

    episodios_items = episodios(programas_items[0])
    if len(episodios_items)==1:
        print "No devuelve videos en "+programas_items[0].title
        return False

    return True