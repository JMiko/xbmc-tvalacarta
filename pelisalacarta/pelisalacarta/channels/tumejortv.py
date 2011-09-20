# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tumejortv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "tumejortv"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tumejortv.py] mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=CHANNELNAME, action="newlist"           , title="Novedades" , url="http://www.tumejortv.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="moviecategorylist" , title="Películas - Por categorías" , url="http://www.tumejortv.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="moviealphalist"    , title="Películas - Por orden alfabético" , url="http://www.tumejortv.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="serienewlist"      , title="Series - Novedades" , url="http://www.tumejortv.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="seriealllist"      , title="Series - Todas" , url="http://www.tumejortv.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="seriealphalist"    , title="Series - Por orden alfabético" , url="http://www.tumejortv.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="search"            , title="Buscar", url="http://www.tumejortv.com/buscar/%s"))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):

    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url = "http://www.tumejortv.com/buscar/%s"
        
        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto
    
        # Devuelve los resultados
        return shortlist(item)
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

# Listado de novedades de la pagina principal
def newlist(item):
    logger.info("[tumejortv.py] movielist")

    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = '<div class="item " style="clear:both;">[^<]+'
    patron += '<div class="covershot[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="post-title">[^<]+'
    patron += '<h3><a[^<]+>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]
        scrapedtitle = scrapedtitle.replace("<span class=\'smallTitle'>","(")
        scrapedtitle = scrapedtitle.replace("</span>",")")
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la página siguiente
    patron = '<a href="([^"]+)" >&raquo;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG:
        scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "!Pagina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapeddescription = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="newlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de películas de una categoria / letra
def shortlist(item):
    logger.info("[tumejortv.py] shortlist")

    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = '<li><div class="movieTitle">[^<]+</div><div class="covershot">'
    patron += '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"[^>]+></a></div></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # http://www.tumejortv.com/series-tv-online/battlestar-galactica
        if "series-tv-online" in scrapedurl:
            action="detailserie"
        else:
            action="findvideos"
        itemlist.append( Item(channel=CHANNELNAME, action=action , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la página siguiente
    patron = '<a href="([^"]+)" >&raquo;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "!Pagina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="shortlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de series de una letra
def shortlistserie(item):
    logger.info("[tumejortv.py] shortlistserie")
    itemlist = []
    url = item.url
    salir = False

    while not salir:
        # Descarga la página
        data = scrapertools.cachePage(url)

        # Extrae las entradas
        partial_list = get_pagina(data)
        itemlist.extend( partial_list )

        # Extrae la página siguiente
        patron = '<a href="([^"]+)" >&raquo;</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        if len(matches)>0:
            url = matches[0]
        else:
            url = ""

        # Condicion de salida
        salir = ( len(partial_list) == 0 or url=="")

    return itemlist

def get_pagina(data):
    patron  = '<li><div class="covershot"><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"[^>]+></a></div></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="detailserie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))
    
    return itemlist

# Listado de categorias de películas, de la caja derecha de la home
def moviecategorylist(item):
    logger.info("[tumejortv.py] moviecategorylist")

    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = '<li class="cat-item[^<]+<a href="(http\:\/\/www\.tumejortv\.com\/peliculas\-online\-es\/[^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="shortlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de letras iniciales de película, de la caja derecha de la home
def moviealphalist(item):
    logger.info("[tumejortv.py] moviealphalist")

    # Descarga la página
    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = '<a href="(http\:\/\/www\.tumejortv\.com\/peliculas-es-con-letra-[^"]+)".*?class="listados_letras">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="shortlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de letras iniciales de series, de la caja derecha de la home
def seriealphalist(item):
    logger.info("[tumejortv.py] seriealphalist")

    # Descarga la página
    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = '<a href="(http\:\/\/www\.tumejortv\.com\/series-con-letra-[^"]+)".*?class="listados_letras">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="shortlistserie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de series actualizadas, de la caja derecha de la home
def serienewlist(item):
    logger.info("[tumejortv.py] serienewlist")

    # Descarga la página
    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = '<span><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)".*?</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="detailserie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Listado de todas las series, de la caja derecha de la home
def seriealllist(item):
    logger.info("[tumejortv.py] seriealllist")

    # Descarga la página
    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    patron  = "<li class='cat-item[^<]+<a href='(http\:\/\/www\.tumejortv\.com\/series\-tv\-online\/[^']+)'[^>]+>([^<]+)</a></li>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="detailserie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Detalle de un vídeo (peli o capitulo de serie), con los enlaces
def findvideos(item):
    logger.info("[tumejortv.py] findvideos")

    # Descarga la página
    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    patron = '<div id="blogitem">[^<]+<p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        plot = matches[0]

    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title + " (" + video[2] + ")"
        scrapedurl = video[1]
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        server = video[2]
        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, server=server, folder=False))

    return itemlist

# Detalle de una serie, con sus capítulos
def detailserie(item):
    logger.info("[tumejortv.py] detailserie")

    # Descarga la página
    url = item.url
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # ------------------------------------------------------
    #<ul class="linksListados">
    #<li><a href="http://www.tumejortv.com/series-tv-online/babylon-5/babylon-5-temporada-1/capitulo-122-15-15-04-2009.html">Babylon 5, Babylon 5 Temporada 1, Capitulo 122</a></li>
    patron  = '<ul class="linksListados">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        patron2 = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
        matches2 = re.compile(patron2,re.DOTALL).findall(match)
        #if DEBUG: scrapertools.printMatches(matches2)

        for match2 in matches2:
            scrapedtitle = match2[1]
            #print "#"+scrapedtitle+"# == #"+item.show+"#"
            scrapedtitle = scrapertools.remove_show_from_title(scrapedtitle,item.show)
            if scrapedtitle.startswith(", "):
                scrapedtitle = scrapedtitle[2:]
            scrapedtitle = scrapertools.remove_show_from_title(scrapedtitle,item.show)

            scrapedtitle = scrapedtitle.replace(", Capítulo ","x")
            scrapedtitle = scrapedtitle.replace(", Capitulo ","x")
            scrapedtitle = scrapedtitle.replace("&#215;","x")
            scrapedtitle = scrapedtitle.replace(", Series Online ","x")
            scrapedtitle = scrapedtitle.replace(", Series online capitulo ","x")
            scrapedtitle = scrapedtitle.replace(", Series Online Capítulo ","x")
            scrapedtitle = scrapedtitle.replace(", Series online capítulo ","x")
            scrapedtitle = scrapedtitle.strip()
            #scrapedtitle = scrapedtitle.replace("Temporada ","")
            
            #print scrapedtitle

            # Reemplaza "1, 1x33" por "1x33"
            patron = "\d+\, (\d+x\d+)"
            matches3 = re.compile(patron,re.DOTALL).findall(scrapedtitle)
            if len(matches3)>0 and len(matches3[0])>0:
                scrapedtitle = matches3[0]

            #print scrapedtitle

            # Reemplaza "Temporada 1, Capítulo 33" por "1x33"
            patron = "Temporada (\d+). Cap.*?lo (\d+.*?)"
            matches3 = re.compile(patron,re.DOTALL).findall(scrapedtitle)
            #print matches3
            if len(matches3)>0:
                scrapedtitle = matches3[0][0]+"x"+matches3[0][1]

            #print scrapedtitle

            # Reemplaza "Temporada 1, Capítulo 33" por "1x33"
            patron = "Temporada (\d+). Series online\s+(\d+x\d+.*?)"
            matches3 = re.compile(patron,re.DOTALL).findall(scrapedtitle)
            #print matches3
            if len(matches3)>0:
                scrapedtitle = matches3[0][1]

            #print scrapedtitle

            if scrapedtitle.startswith(item.title+", "):
                scrapedtitle = scrapedtitle[ len(item.title)+2 : ]

            #scrapedtitle = scrapedtitle + "#"+match2[1]+"#"
            
            scrapedurl = match2[0]
            scrapedthumbnail = item.thumbnail
            scrapedplot = ""

            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show))

    return itemlist