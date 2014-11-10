﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import xbmc, xbmcgui

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelisadicto"
__category__ = "F"
__type__ = "generic"
__title__ = "Pelisadicto"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cuevana.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Últimas agregadas"  , action="agregadas", url="http://pelisadicto.com"))
    itemlist.append( Item(channel=__channel__, title="Listado por género" , action="porGenero", url="http://pelisadicto.com"))
    itemlist.append( Item(channel=__channel__, title="Buscar" , action="buscar", url="http://pelisadicto.com") )
    
    return itemlist

def porGenero(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Acción",url="http://pelisadicto.com/genero/Acción/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Adulto",url="http://pelisadicto.com/genero/Adulto/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Animación",url="http://pelisadicto.com/genero/Animación/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Aventura",url="http://pelisadicto.com/genero/Aventura/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Biográfico",url="http://pelisadicto.com/genero/Biográfico/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Ciencia Ficción",url="http://pelisadicto.com/genero/Ciencia Ficción/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Cine Negro",url="http://pelisadicto.com/genero/Cine Negro/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Comedia",url="http://pelisadicto.com/genero/Comedia/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Corto",url="http://pelisadicto.com/genero/Corto/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Crimen",url="http://pelisadicto.com/genero/Crimen/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Deporte",url="http://pelisadicto.com/genero/Deporte/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Documental",url="http://pelisadicto.com/genero/Documental/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Drama",url="http://pelisadicto.com/genero/Drama/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Familiar",url="http://pelisadicto.com/genero/Familiar/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Fantasía",url="http://pelisadicto.com/genero/Fantasía/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Guerra",url="http://pelisadicto.com/genero/Guerra/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Historia",url="http://pelisadicto.com/genero/Historia/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Misterio",url="http://pelisadicto.com/genero/Misterio/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Música",url="http://pelisadicto.com/genero/Música/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Musical",url="http://pelisadicto.com/genero/Musical/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Romance",url="http://pelisadicto.com/genero/Romance/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Terror",url="http://pelisadicto.com/genero/Terror/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Thriller",url="http://pelisadicto.com/genero/Thriller/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Western",url="http://pelisadicto.com/genero/Western/1"))

    return itemlist	

def agregadas(item):
    logger.info("[cuevana.py] novedades")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)
    # Extrae las entradas
    patron  = '<li class="col-xs-6 col-sm-2 CALBR">.*?'
    patron += '<a href="(.*?)".*?src="(.*?)".*?alt="(.*?)".*?calidad">(.*?)<.*?</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,tit,calidad in matches:
        url="http://pelisadicto.com"+url
        data = scrapertools.cache_page(url)
        patron = "<!-- SINOPSIS -->.*?"
        patron += "<h2>.*?</h2>.*?"
        patron += "<p>(.*?)</p>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        plot = matches[0]
        thumbnail = "http://pelisadicto.com"+thumbnail
        itemlist.append( Item(channel=__channel__, action="findvideos3", title=tit, fulltitle=tit , url=url , thumbnail=thumbnail , plot=plot , show=tit, viewmode="movie_with_plot") )
    patron  = '<li class="active">.*?</li><li><span><a href="(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        parametro = matches[0]
        patron = '<ul class="listitems">.*?<li><a href="(.*?)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        genero = matches[0]
        genero = genero.replace("mejores-peliculas", "genero")
        url = genero + "/" + parametro
        itemlist.append( Item(channel=__channel__, action="agregadas", title="Página siguiente >>" , url=url) )

    return itemlist

def findvideos3(item):
    itemlist = []
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    patron = '<tr>.*?'
    patron += '<td><img src="(.*?)".*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<a href="(.*?)".*?</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedidioma, scrapedcalidad, scrapedserver, scrapedurl in matches:
        idioma =""
        if "/img/1.png" in scrapedidioma: idioma="Castellano"
        if "/img/2.png" in scrapedidioma: idioma="Latino"
        if "/img/3.png" in scrapedidioma: idioma="Subtitulado"
        title = item.title + " ["+scrapedcalidad+"][" + idioma + "][" + scrapedserver + "]"
        itemlist.append( Item(channel=__channel__, action="play", title=title, fulltitle=title , url=scrapedurl , thumbnail="" , plot="" , show = item.show) )
    return itemlist	
	
def play(item):

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    

def buscar(item):
    itemlist = []
    keyboard = xbmc.Keyboard()
    keyboard.doModal()
    busqueda=keyboard.getText()
    # Descarga la pagina
    data = scrapertools.cache_page("http://pelisadicto.com/buscar/" + busqueda)
    #logger.info("data="+data)
    # Extrae las entradas
    patron  = '<li class="col-xs-6 col-sm-2 CALBR">.*?'
    patron += '<a href="(.*?)".*?src="(.*?)".*?alt="(.*?)".*?calidad">(.*?)<.*?</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,tit,calidad in matches:
        url="http://pelisadicto.com"+url
        data = scrapertools.cache_page(url)
        patron = "<!-- SINOPSIS -->.*?"
        patron += "<h2>.*?</h2>.*?"
        patron += "<p>(.*?)</p>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        plot = matches[0]
        thumbnail = "http://pelisadicto.com"+thumbnail
        itemlist.append( Item(channel=__channel__, action="findvideos3", title=tit, fulltitle=tit , url=url , thumbnail=thumbnail , plot=plot , show=tit, viewmode="movie_with_plot") )
    patron  = '<li class="active">.*?</li><li><span><a href="(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        parametro = matches[0]
        patron = '<ul class="listitems">.*?<li><a href="(.*?)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        genero = matches[0]
        genero = genero.replace("mejores-peliculas", "genero")
        url = genero + "/" + parametro
        itemlist.append( Item(channel=__channel__, action="agregadas", title="Página siguiente >>" , url=url) )
    return itemlist