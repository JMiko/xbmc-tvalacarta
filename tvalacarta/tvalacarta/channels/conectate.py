﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "conectate"
__category__ = "F"
__type__ = "generic"
__title__ = "conectate"
__language__ = "ES"
__creationdate__ = "20121130"
__vfanart__ = "http://conectate.gov.ar/educar-portal-video-web/module/decorator/img/bgBody.gif"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[conectate.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Encuentro", action="encuentro", url="http://conectate.gov.ar/educar-portal-video-web/module/busqueda/busquedaAvanzada.do?modulo=menu&temaCanalId=1&canalId=1&tipoEmisionId=3", thumbnail="http://conectate.gov.ar/educar-portal-video-web/module/decorator/img/footer_encuentro.png", fanart = __vfanart__)) 
    itemlist.append( Item(channel=__channel__, title="Pakapaka", action="pakapaka", url="http://conectate.gov.ar/educar-portal-video-web/module/busqueda/busquedaAvanzada.do?modulo=menu&temaCanalId=2&canalId=2&tipoEmisionId=3", thumbnail="http://conectate.gov.ar/educar-portal-video-web/module/decorator/img/footer_pakapaka.png", fanart = __vfanart__)) 
    itemlist.append( Item(channel=__channel__, title="Ronda", action="ronda", url="http://conectate.gov.ar/educar-portal-video-web/module/busqueda/busquedaAvanzada.do?modulo=menu&temaCanalId=3&canalId=3&tipoEmisionId=3", thumbnail="http://conectate.gov.ar/educar-portal-video-web/module/decorator/img/footer_pakapaka.png", fanart = __vfanart__))
    itemlist.append( Item(channel=__channel__, title="Educ.ar", action="educar", url="http://conectate.gov.ar/educar-portal-video-web/module/busqueda/busquedaAvanzada.do?modulo=menu&temaCanalId=125&canalId=125&tipoEmisionId=2", thumbnail="http://conectate.gov.ar/educar-portal-video-web/module/decorator/img/footer_educar.png", fanart = __vfanart__))
    itemlist.append( Item(channel=__channel__, title="Conectar igualdad", action="conectar", url="http://conectate.gov.ar/educar-portal-video-web/module/busqueda/busquedaAvanzada.do?modulo=menu&temaCanalId=126&canalId=126&tipoEmisionId=2", thumbnail="http://conectate.gov.ar/educar-portal-video-web/module/decorator/img/footer_conectarigualdad.png", fanart = __vfanart__))

    return itemlist
