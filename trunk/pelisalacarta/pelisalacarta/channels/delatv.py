# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para delatv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

CHANNELNAME = "delatv"
DEBUG = True

def isGeneric():
    return True


def mainlist(item):
    logger.info("[delatv.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=CHANNELNAME , action="listvideos"        , title="Ultimas Películas Añadidas"    , url="http://delatv.com/"))
    itemlist.append( Item(channel=CHANNELNAME , action="ListaCat"          , title="Listado por Genero"            , url="http://delatv.com/"))
    itemlist.append( Item(channel=CHANNELNAME , action="ListaAlfa"         , title="Listado Alfanumerico"          , url="http://delatv.com/" ))

    return itemlist

def ListaCat(item):
    logger.info("[delatv.py] ListaCat")

    # Tiene el mismo HTML que cineadicto
    import cineadicto
    return cineadicto.ListaCat(item)

def ListaAlfa(item):
    logger.info("[delatv.py] ListaAlfa")

    # Tiene el mismo HTML que cineadicto
    import cineadicto
    return cineadicto.ListaAlfa(item)

def listvideos(item):
    logger.info("[delatv.py] listvideos")

    # Tiene el mismo HTML que cineadicto
    import cineadicto
    return cineadicto.listvideos(item)

def detail(item):
    logger.info("[delatv.py] listvideos")

    #player(new Array('videozer', '8J18b3'))

    # Tiene el mismo HTML que cineadicto
    import cineadicto
    return cineadicto.detail(item)
