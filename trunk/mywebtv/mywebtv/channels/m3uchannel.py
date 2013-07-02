# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# m3u Channel
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
__channel__ = "m3uchannel"

def isGeneric():
    return True

def mainlist(item):
    logger.info("m3uchannel.mainlist")
    return categorias(item)

def categorias(item):
    logger.info("m3uchannel.categorias")

    itemlist = []

    # Si es una URL la descarga
    if item.url.startswith("http://") or item.url.startswith("https://"):
        data = scrapertools.cache_page(item.url)

    # Si es un fichero local, lo abre
    else:
        infile = open( item.url )
        data = infile.read()
        infile.close()

    # Parsea la lista
    categories = m3utools.parse_categories_from_m3u_list(data)

    for category in categories:
        itemlist.append( Item(channel=__channel__, title=category.title, action="entradas", url=item.url , folder=True) )

    return itemlist

def entradas(item):
    logger.info("m3uchannel.entradas")

    itemlist = []

    # Si es una URL la descarga
    if item.url.startswith("http://") or item.url.startswith("https://"):
        data = scrapertools.cache_page(item.url)

    # Si es un fichero local, lo abre
    else:
        infile = open( item.url )
        data = infile.read()
        infile.close()

    # Parsea la lista
    category = item.title
    logger.info("m3uchannel.entradas category="+category)
    entries = m3utools.parse_items_from_m3u_list(data,category)

    for entry in entries:
        itemlist.append( Item(channel=__channel__, title=entry.title, url=entry.url, action="play", folder=False) )

    return itemlist
