# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cine-adicto.com by Bandavi
# Actualización Carles Carmona 15/08/2011
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from pelisalacarta import buscador
from servers import servertools

CHANNELNAME = "cineadicto"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cineadicto.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME , action="ultimas"        , title="Ultimas Películas Añadidas"    , url="http://www.cine-adicto.com/"))
    itemlist.append( Item(channel=CHANNELNAME , action="ListaCat"          , title="Listado por Genero"            , url="http://www.cine-adicto.com/"))
    #itemlist.append( Item(channel=CHANNELNAME , action="ListaAlfa"         , title="Listado Alfanumerico"          , url="http://www.cine-adicto.com/" ))
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar", action="search") )
    
    return itemlist
    
def search(item,texto):
    logger.info("[cineadicto.py] searchresults")
    itemlist = []
    #convert to HTML
    texto = texto.replace(" ", "+")
    item.url = "http://www.cine-adicto.com/?s="+texto
    itemlist.extend(lista(item))
    return itemlist

def ListaCat(item):
    logger.info("[cineadicto.py] ListaCat")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #print data
    # Extrae las entradas (carpetas)
    #<li class="cat-item cat-item-6"><a href="http://www.cine-adicto.com/category/accion" title="Ver todas las entradas archivadas en Accion">Accion</a></li>
    patronvideos  = '<li class="cat-item cat-item-.*?<a href="(.*?)".*?>(.*?)</a>.*?</li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedurl = match[0]
        scrapedtitle =match[1]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=item.channel , action="lista"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist
    
def ListaAlfa(item):
    itemlist = []
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="0-9",url="http://www.cine-adicto.com/alphabet/9/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="A",url="http://www.cine-adicto.com/alphabet/a/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="B",url="http://www.cine-adicto.com/alphabet/b/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="C",url="http://www.cine-adicto.com/alphabet/c/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="D",url="http://www.cine-adicto.com/alphabet/d/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="E",url="http://www.cine-adicto.com/alphabet/e/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="F",url="http://www.cine-adicto.com/alphabet/f/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="G",url="http://www.cine-adicto.com/alphabet/g/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="H",url="http://www.cine-adicto.com/alphabet/h/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="I",url="http://www.cine-adicto.com/alphabet/i/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="J",url="http://www.cine-adicto.com/alphabet/j/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="K",url="http://www.cine-adicto.com/alphabet/k/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="L",url="http://www.cine-adicto.com/alphabet/l/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="M",url="http://www.cine-adicto.com/alphabet/m/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="N",url="http://www.cine-adicto.com/alphabet/n/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="O",url="http://www.cine-adicto.com/alphabet/o/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="P",url="http://www.cine-adicto.com/alphabet/p/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="Q",url="http://www.cine-adicto.com/alphabet/q/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="R",url="http://www.cine-adicto.com/alphabet/r/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="S",url="http://www.cine-adicto.com/alphabet/s/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="T",url="http://www.cine-adicto.com/alphabet/t/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="U",url="http://www.cine-adicto.com/alphabet/u/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="V",url="http://www.cine-adicto.com/alphabet/v/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="W",url="http://www.cine-adicto.com/alphabet/w/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="X",url="http://www.cine-adicto.com/alphabet/x/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="Y",url="http://www.cine-adicto.com/alphabet/y/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="Z",url="http://www.cine-adicto.com/alphabet/z/"))

    return itemlist

def ultimas(item):
    logger.info("[cineadicto.py] Ultimas")

    url = item.url
    if url=="":
        url = "http://www.cine-adicto.com/"
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    
    #<div class="slidethumb">
    #<a href="http://www.cine-adicto.com/transformers-dark-of-the-moon.html"><img src="http://www.cine-adicto.com/wp-content/uploads/2011/09/Transformers-Dark-of-the-moon-wallpaper.jpg" width="638" alt="Transformers: Dark of the Moon 2011" /></a>
    #</div>

    patron = '<div class="movie-thumbnail">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<a href="(.*?)">.*?'
        patron  += '<img class=".*?" src="(.*?)" width=".*?" height=".*?" alt="(.*?)" />.*?'
        patron  += '<span class="pop_desc">.*?<p>(.*?)</p>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
            scrapedtitle = match2[2]
            scrapedurl = match2[0]
            scrapedthumbnail = match2[1].replace(" ","%20")
            scrapedplot = match2[3]
            
            itemlist.append( Item(channel=item.channel , action="detail"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))

    #Extrae la marca de siguiente página
    #<span class='current'>1</span><a href='http://delatv.com/page/2' class='page'>2</a>
    patronvideos  = '<span class="current">[^<]+</span>[^<]*<a.*?href="([^"]+)"' #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)==0:
        patronvideos  = "<span class='current'>[^<]+</span>[^<]*<a.*?href='([^']+)'" #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'""
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(url,matches[0])#matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=item.channel , action="listvideos"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))

    return itemlist

def lista(item):
    logger.info("[cineadicto.py] Lista")

    url = item.url
    if url=="":
        url = "http://www.cine-adicto.com/"
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    
    #<div class="slidethumb">
    #<a href="http://www.cine-adicto.com/transformers-dark-of-the-moon.html"><img src="http://www.cine-adicto.com/wp-content/uploads/2011/09/Transformers-Dark-of-the-moon-wallpaper.jpg" width="638" alt="Transformers: Dark of the Moon 2011" /></a>
    #</div>

    patron = '<div class="short_post">(.*?)<span class="arch_views">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '.*?<a href="(.*?)">.*?'
        patron  += '<img src="(.*?)" width=".*?" height=".*?" alt="(.*?)" />.*?'
        patron  += '<p>(.*?)</p>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
            scrapedtitle = match2[2]
            scrapedurl = match2[0]
            scrapedthumbnail = match2[1].replace(" ","%20")
            scrapedplot = match2[3]
            
            itemlist.append( Item(channel=item.channel , action="detail"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))

    #Extrae la marca de siguiente página
    #<span class='current'>1</span><a href='http://delatv.com/page/2' class='page'>2</a>
    patronvideos  = '<span class="current">[^<]+</span>[^<]*<a.*?href="([^"]+)"' #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)==0:
        patronvideos  = "<span class='current'>[^<]+</span>[^<]*<a.*?href='([^']+)'" #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'""
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(url,matches[0])#matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=item.channel , action="listvideos"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))

    return itemlist

def detail(item):
    logger.info("[cineadicto.py] detail")

    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot
    scrapedurl = ""
    url = item.url

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(url)
    
    # Usa findvideos    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))



    return itemlist

