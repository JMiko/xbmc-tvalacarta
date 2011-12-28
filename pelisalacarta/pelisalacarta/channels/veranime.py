# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://www.veranime.net/
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

__channel__ = "veranime"
__category__ = "A"
__type__ = "generic"
__title__ = "Ver-anime"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[veranime.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Ultimos Capitulos Agregados", action="novedades"     , url="http://www.ver-anime.net/"))
    itemlist.append( Item(channel=__channel__, title="Ultimos Animes Agregados"   , action="ultimos"        , url="http://www.ver-anime.net/"))
    itemlist.append( Item(channel=__channel__, title="Listado Alfabetico"         , action="listaalfabetica", url="http://www.ver-anime.net/letra/"))
    itemlist.append( Item(channel=__channel__, title="Listado Completo"           , action="listacompleta"  , url="http://www.ver-anime.net/letra/"))
    itemlist.append( Item(channel=__channel__, title="Animes Populares"           , action="populares"      , url="http://www.ver-anime.net/"))
    itemlist.append( Item(channel=__channel__, title="Animes en Emision"          , action="emision"  , url="http://www.ver-anime.net/"))
    itemlist.append( Item(channel=__channel__, title="Buscar" , action="search") )

    return itemlist

def novedades(item):
    logger.info("[veranime.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron  = 'Ultimos Capitulos.*?<div id="elmenu">(.*?)<div class'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    patron = '<a href="([^"]+)" title="([^"]+)"'
    matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
    for match in matches2:
        scrapedurl = match[0]
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def ultimos(item):
    logger.info("[veranime.py] ultimos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron  = 'Ultimos Animes Agregados.*?<div id="elmenu">(.*?)<div class'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    patron = '<a href="([^"]+)" title="([^"]+)"'
    matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
    for match in matches2:
        scrapedurl = match[0]
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def listaalfabetica(item):
    logger.info("[veranime.py] listaalfabetica")

    url = item.url
    itemlist = []
    
    itemlist.append( Item(channel=__channel__, action="listar", title="0-9" , url=url+"09.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="A"   , url=url+"a.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="B"   , url=url+"b.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="C"   , url=url+"c.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="D"   , url=url+"d.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="E"   , url=url+"e.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="F"   , url=url+"F.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="G"   , url=url+"g.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="H"   , url=url+"h.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="I"   , url=url+"i.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="J"   , url=url+"j.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="K"   , url=url+"k.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="L"   , url=url+"l.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="M"   , url=url+"m.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="N"   , url=url+"n.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="O"   , url=url+"o.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="P"   , url=url+"p.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="Q"   , url=url+"q.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="R"   , url=url+"r.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="S"   , url=url+"s.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="T"   , url=url+"t.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="U"   , url=url+"u.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="V"   , url=url+"v.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="W"   , url=url+"w.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="X"   , url=url+"x.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="Y"   , url=url+"y.html" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="listar", title="Z"   , url=url+"z.html" , folder=True) )

    return itemlist

def listacompleta(item):
    logger.info("[veranime.py] listacompleta")
    url = item.url
    itemlist = []
    # Descarga las páginas
    data = scrapertools.cachePage(url+"09.html")
    data = data + scrapertools.cachePage(url+"a.html")
    data = data + scrapertools.cachePage(url+"b.html")
    data = data + scrapertools.cachePage(url+"c.html")
    data = data + scrapertools.cachePage(url+"d.html")
    data = data + scrapertools.cachePage(url+"e.html")
    data = data + scrapertools.cachePage(url+"f.html")
    data = data + scrapertools.cachePage(url+"g.html")
    data = data + scrapertools.cachePage(url+"h.html")
    data = data + scrapertools.cachePage(url+"i.html")
    data = data + scrapertools.cachePage(url+"j.html")
    data = data + scrapertools.cachePage(url+"k.html")
    data = data + scrapertools.cachePage(url+"l.html")
    data = data + scrapertools.cachePage(url+"m.html")
    data = data + scrapertools.cachePage(url+"n.html")
    data = data + scrapertools.cachePage(url+"o.html")
    data = data + scrapertools.cachePage(url+"p.html")
    data = data + scrapertools.cachePage(url+"q.html")
    data = data + scrapertools.cachePage(url+"r.html")
    data = data + scrapertools.cachePage(url+"s.html")
    data = data + scrapertools.cachePage(url+"t.html")
    data = data + scrapertools.cachePage(url+"u.html")
    data = data + scrapertools.cachePage(url+"v.html")
    data = data + scrapertools.cachePage(url+"w.html")
    data = data + scrapertools.cachePage(url+"x.html")
    data = data + scrapertools.cachePage(url+"y.html")
    data = data + scrapertools.cachePage(url+"z.html")
    
    # Busca las series
    patron = '<div class="bl">[^<]+<a href="([^"]+)" title="([^"]+)">[^<]+<img src="([^"]+)"[^<]+</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist    

def populares(item):
    logger.info("[veranime.py] populares")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron  = 'Animes Populares.*?<div id="elmenu">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    patron = '<a href="([^"]+)" title="([^"]+)"'
    matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
    for match in matches2:
        scrapedurl = match[0]
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def emision(item):
    logger.info("[veranime.py] emision")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron  = 'Animes en Emision.*?<div id="elmenu">(.*?)<div class'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    patron = '<a href="([^"]+)" title="([^"]+)"'
    matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
    for match in matches2:
        scrapedurl = match[0]
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def listar(item):
    logger.info("[veranime.py] listar")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    itemlist = []
    
    # Busca las series
    patron = '<div class="bl">[^<]+<a href="([^"]+)" title="([^"]+)">[^<]+<img src="([^"]+)"[^<]+</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def capitulos(item):
    logger.info("[veranime.py] capitulos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    itemlist = []
    
    # Busca la caratula y el argumento
    patronplot = '<div class="caratula">.*?<img src="([^"]+)".*?<p>(.*?)</p>.*?</tr>'
    matches = re.compile(patronplot,re.DOTALL).findall(data)
    for match in matches:
        scrapedthumbnail = match[0]
        scrapedplot = match[1]

    # Busca donde estan todos los capitulos
    patron = 'Lista de capitulos de.*?<ul class="truindexlist">(.*?)</ul>'
    matches2 = re.compile(patron,re.DOTALL).findall(data)
    data2 = matches2[0]

    # Busca cada capitulo
    patroncapitulos = '<a title="([^"]+)" href="([^"]+)"'
    matches3 = re.compile(patroncapitulos,re.DOTALL).findall(data2)
    for match3 in matches3:
        scrapedtitle = match3[0]
        scrapedurl = match3[1]
        itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def videos(item):
    logger.info("[veranime.py] videos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    itemlist = []
    patron = '<div id="mirror" class="alternateMirrors contentModuleSmall">(.*?)showmedia_about'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data2 = matches[0]
    patronvideos = '<a href="([^"]+)".*?">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data2)
    for match in matches:
        listavideos = servertools.findvideos(scrapertools.cachePage(match[0]))
        for video in listavideos:
            itemlist.append( Item(channel=__channel__, action="play", title=match[1] , url=video[1] , thumbnail="" , server=video[2] , folder=False) )

    return itemlist

def search(item,texto):
    logger.info("[veranime.py] search")
    itemlist = []
    
    # Descarga la página con la busqueda
    data = scrapertools.cache_page( "http://www.ver-anime.net/search.php" , post="tuti="+texto )

    # Extrae las entradas de todas series
    patron  = '<ul class="truindexlist">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    patron = '<a href="([^"]+)" title="([^"]+)">'
    matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
    for match in matches2:
        scrapedtitle = match[1].strip()
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title) 
    return itemlist
