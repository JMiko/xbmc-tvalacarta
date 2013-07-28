# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal SimpleTV
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
from core import scrapertools
from core import config
from core import logger
from core.item import Item
from core import m3utools

DEBUG = True
LOCAL_FILE = os.path.join( config.get_data_path() , "simpletv.m3u" )
NO_CATEGORY = "Sin categoria"
__channel__ = "simpletv"

def isGeneric():
    return True

def openconfig(item):
    logger.info("simpletv.openconfig")
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def get_online_list():
    logger.info("simpletv.get_online_list")

    # Login
    try:
        request_headers = []
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0"])
        post = urllib.urlencode({'log':config.get_setting("simpletvuser"), 'pwd':config.get_setting("simpletvpassword"), 'rememberme':'forever', 'wp-submit':'Acceder', 'redirect_to':'http://web.iptvonline.com.es/wp-admin/', 'testcookie':'1' })
        data = scrapertools.cache_page("http://web.iptvonline.com.es/wp-login.php", headers=request_headers, post=post)

        # Página con la lista
        request_headers = []
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0"])
        request_headers.append(["Referer","http://web.iptvonline.com.es/playlist-simpletv"])
        data = scrapertools.cache_page("http://temp.iptvonline.com.es", headers=request_headers)
        logger.info("data="+data)

        # Averigua la URL de la lista
        url = scrapertools.get_match(data,'URL PARA ACTUALIZAR\: (http.*?m3u)')

        # Descarga la lista
        data = scrapertools.cache_page(url)
    except:
        data = ""

    return data

def mainlist(item):
    logger.info("simpletv.mainlist")
    itemlist = []

    # Tienes que tener cuenta
    if config.get_setting("simpletvaccount")=="false":
        itemlist.append( Item(channel=__channel__, title="Habilita tu cuenta en la configuración...", action="openconfig", folder=False) )
        return itemlist

    return categorias(item)

def categorias(item,data=""):
    logger.info("simpletv.categorias")

    itemlist = []

    # Obtiene la lista de categorias a partir del m3u
    recursividad_permitida = False
    if data=="":
        recursividad_permitida = True
        data = get_online_list()
        categories = m3utools.parse_categories_from_m3u_list(data)

    # Si ha encontrado canales, graba el fichero actualizado por si en el futuro falla
    if len(categories)>0:
        f = open(LOCAL_FILE,"w")
        f.write(data)
        f.flush()
        f.close()

    # Si no ha encontrado canales, lee el fichero grabado la última vez y carga de nuevo la lista
    elif recursividad_permitida:
        infile = open(LOCAL_FILE,"r")
        data = infile.read()
        infile.close()
        itemlist = categorias(item,data)

    for category in categories:
        itemlist.append( Item(channel=__channel__, title=category.title, action="entradas", folder=True) )

    return itemlist

def entradas(item,data=""):
    logger.info("simpletv.entradas")

    itemlist = []

    # Obtiene la lista de categorias a partir del m3u
    recursividad_permitida = False
    if data=="":
        recursividad_permitida = True
        data = get_online_list()

        # Parsea la lista
        category = item.title
        logger.info("simpletv.entradas category="+category)
        entries = m3utools.parse_items_from_m3u_list(data,category)

    # Si ha encontrado canales, graba el fichero actualizado por si en el futuro falla
    if len(entries)>0:
        f = open(LOCAL_FILE,"w")
        f.write(data)
        f.flush()
        f.close()

    # Si no ha encontrado canales, lee el fichero grabado la última vez y carga de nuevo la lista
    elif recursividad_permitida:
        infile = open(LOCAL_FILE,"r")
        data = infile.read()
        infile.close()
        itemlist = entradas(item,data)

    for entry in entries:
        itemlist.append( Item(channel=__channel__, title=entry.title, url=entry.url, action="play", folder=False) )

    return itemlist
