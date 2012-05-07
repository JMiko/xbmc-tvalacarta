# -*- coding: utf-8 -*-
#------------------------------------------------------------
# sipeliculas.com - XBMC Plugin
# Canal para sipeliculas.com by juso
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys
import base64

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "sipeliculas"
__category__ = "F"
__type__ = "generic"
__title__ = "Si peliculas"
__language__ = "ES"
__creationdate__ = "20120301"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("[sipeliculas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas recientes" , action="lista2", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Listado por Generos" , action="generos", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Listado Alfabetico" , action="alfa", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Buscar pelicula" , action="search", url=""))
 
    return itemlist

def search(item,texto):
    logger.info("[sipeliculas.py] search")
    itemlist = []

    texto = texto.replace(" ","+")
    item.url="http://www.sipeliculas.com/Buscar.php?q="+texto    
    item.extra = ""
    itemlist.extend(lista1(item))
    
    return itemlist

def alfa(item):
    logger.info("[sipeliculas.py] alfabetico")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    patron='<div id="abc">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data=matches[0]
    patron='<a .*? href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="lista2", url=scrapedurl)) 
    return itemlist

def generos(item):
    logger.info("[sipeliculas.com] generos")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    patron='<div id="fondo">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data=matches[0]
    patron='<a  href="([^"]+)".*?>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="lista2", url=scrapedurl)) 
    return itemlist

def lista1(item):
    logger.info("[sipeliculas.py] lista1")
    itemlist=[]
    data = scrapertools.cachePage(item.url)   
    patron = '<div id="CEN">\n<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        scrapedthumbnail=match[2]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="mirrors", url=scrapedurl, thumbnail=scrapedthumbnail))

    patron='class="PaginaActual".*?href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)    
    scrapedurl='http://www.sipeliculas.com'+matches[0];
    scrapedurl=scrapedurl.replace('./','/')
    itemlist.append( Item(channel=__channel__, title="! Pagina Siguiente" , action="lista1", url=scrapedurl))
    #itemlist.append( Item(channel=__channel__, title=matchx , action="lista2", url=matchx)) 
    return itemlist

def lista2(item):
    logger.info("[sipeliculas.py] lista2")
    itemlist=[]
    data = scrapertools.cachePage(item.url)   
    patron = '<div id="pelicula"><a.*? href="([^"]+)" title="([^"]+)".*?<img src="([^"]+)"'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        scrapedthumbnail=match[2]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="mirrors", url=scrapedurl, thumbnail=scrapedthumbnail))

    patron='class="PaginaActual".*?href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)    
    scrapedurl=matches[0];
    itemlist.append( Item(channel=__channel__, title="! Pagina Siguiente" , action="lista2", url=scrapedurl))
    #itemlist.append( Item(channel=__channel__, title=matchx , action="lista2", url=matchx)) 
    return itemlist

def mirrors(item):
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    patron = '<li><a href="([^"]+)"[^>]*>(Opcion[^>]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,title in matches:
        itemlist.append( Item(channel=__channel__, title=title , action="findvideos", url=url, folder=True))

    if len(itemlist)==0:
        itemlist = findvideos(item)
    
    return itemlist

def findvideos(item):
    data = scrapertools.cachePage(item.url)
    patron='decode64.*?"(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("matches[0]="+matches[0])
    decripted=base64.decodestring(matches[0])
    logger.info("decripted="+decripted)
    listavideos = servertools.findvideos(decripted)
    itemlist = []
    plot=""
    for video in listavideos:
        videotitle = scrapertools.unescape(video[0])
        #print videotitle
        url = video[1]
        server = video[2]
        videotitle = item.title+ " - " +videotitle
        itemlist.append( Item(channel=__channel__, action="play", server=server, title=videotitle , url=url , thumbnail=item.thumbnail , plot=plot ,subtitle="", folder=False) )
    #itemlist.append( Item(channel=__channel__, title=titu , action="generos", url="http://yahoo.com"))
    return itemlist