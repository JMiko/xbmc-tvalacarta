﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinegratis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinegratis"
__category__ = "F,S,A,D"
__type__ = "generic"
__title__ = "Cinegratis"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinegratis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="estrenos"   , title="Películas - Estrenos DVD/BluRay" , url="http://www.cinegratis.net/estrenos-dvd-bluray/", extra="Estrenos+DVD%2FBLURAY"))
    itemlist.append( Item(channel=__channel__, action="estrenos"   , title="Películas - Estrenos cine"       , url="http://www.cinegratis.net/estrenos-de-cine/", extra="Estrenos+de+Cine"))
    #itemlist.append( Item(channel=__channel__, action="peliscat"   , title="Películas - Géneros"             , url="http://www.cinegratis.net/index.php?module=generos"))
    #itemlist.append( Item(channel=__channel__, action="pelisalfa"  , title="Películas - Idiomas"             , url="http://www.cinegratis.net/index.php?module=peliculas"))
    #itemlist.append( Item(channel=__channel__, action="pelisalfa"  , title="Películas - Calidades"           , url="http://www.cinegratis.net/index.php?module=peliculas"))
    #itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar"                          , url="http://www.cinegratis.net/index.php?module=search&title=%s"))

    return itemlist

def estrenos(item):
    logger.info("[cinegratis.py] estrenos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae los items
    patron  = "<td class='asd2'.*?"
    patron += "<table.*?<a.*?href='([^']+)'>([^<]+)</a>.*?"
    patron += "<img src='([^']+)'"#.*?"
    #patron += "<table>(.*?)</table>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for url,titulo,thumbnail in matches:
        plot=""
        if not url.startswith("/"):
            url = "/"+url
        scrapedtitle = unicode(titulo,"iso-8859-1").encode("utf-8")
        scrapedurl = urlparse.urljoin(item.url,url.replace("\n",""))
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = scrapertools.htmlclean(plot)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, context="4|5"))

    # Extrae la marca de siguiente página
    patron = "<input class='boton' type='button' value='[^']+' style='[^']+'><input class='boton' style='[^']+' type='button' value='[^']+' onclick='document.homesearch.pag.value\=(\d+)\;"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente >>"
        scrapedurl = "http://www.cinegratis.net/index.php?hstype=t%EDtulo&hstitle=Todos...&hscat=Todos&hslanguage=Todos&hsquality=Todas&hsestreno="+item.extra+"&hsyear1=Desde...&hsyear2=...Hasta&pag="+matches[0]+"&hsletter=&tesths=1"
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="estrenos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra=item.extra))

    return itemlist

def listsimple(item):
    logger.info("[cinegratis.py] listsimple")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los items
    patronvideos  = "<a href='(index.php\?module\=player[^']+)'[^>]*>(.*?)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
        scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto, categoria="*"):
    logger.info("[cinegratis.py] search")

    texto = texto.replace(" ", "+")
    itemlist = []
    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            if categoria in ("*","F"):
                item.url = "http://www.cinegratis.net/index.php?module=search&title="+texto
                itemlist.extend(listsimple(item)) 
            if categoria in ("*","D"):
                item.url = "http://www.cinegratis.net/index.php?hstitle="+texto+"&hscat=Documentales&hsyear"
                itemlist.extend(listsimple_documentales(item))
        else:
            item.url = item.url % texto
            itemlist.extend(listsimple(item))
              
        return itemlist
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def peliscat(item):
    logger.info("[cinegratis.py] peliscat")

    url = item.url

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="listsimple" , title="Versión original" , url="http://www.cinegratis.net/index.php?module=search&title=subtitulado"))
    itemlist.append( Item(channel=__channel__, action="listsimple" , title="Versión latina"   , url="http://www.cinegratis.net/index.php?module=search&title=latino"))

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los items
    patronvideos  = "<td align='left'><a href='([^']+)'><img src='([^']+)' border='0'></a></td>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        patron2 = "genero/([A-Za-z\-]+)/"
        matches2 = re.compile(patron2,re.DOTALL).findall(match[0])
        scrapertools.printMatches(matches2)
        
        scrapedtitle = matches2[0]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="listvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listseries(item):
    logger.info("[cinegratis.py] listvideos")

    url = item.url
    
    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los items
    patronvideos  = "<table width='785'[^>]+><tr><td[^>]+>([^<]+)<.*?"
    patronvideos += "<div align='justify'>(.*?)</div>.*?"
    patronvideos += "<a href='(.*?)'.*?"
    patronvideos += "<img src='(.*?)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = urlparse.urljoin(url,match[2])
        scrapedthumbnail = urlparse.urljoin(url,match[3])
        scrapedplot = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la marca de siguiente página
    patronvideos  = "<a href='[^']+'><u>[^<]+</u></a> <a href='([^']+)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="listseries" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist
    

def listsimple_documentales(item):
    logger.info("[cinegratis.py] listsimple_documentales")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    '''
<table cellspacing='1' cellpadding='0' class='style3'>
<tr class='style4'><td>T?tulo</td><td width='10'></td><td>G?nero</td></tr>
<tr><td height='5'></td></tr>
<tr><td><a href='/pelicula/Abusos sexuales y el Vaticano/455'>Abusos sexuales y el Vaticano</td><td width='10'></td><td>Documentales</td></tr>
<tr><td><a href='/pelicula/Abusos sexuales y el Vaticano (Documental)/7320'>Abusos sexuales y el Vaticano (Documental)</td><td width='10'></td><td>Documentales</td></tr>
</table></td></tr></table></td></tr></table>
    '''
    # Extrae los items
    patronvideos  = "<tr><td><a href='([^']+)'>([^<]+)</td>"   
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin("http://www.cinegratis.net",match[0]).replace(" ","+")
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def findvideos(item):
    logger.info("[cinegratis.py] findvideos")

    from core import scrapertools
    data = scrapertools.cache_page(item.url)    
    patronvideos = "<td width='100\%' align='justify' valign='top' class='style3'>(.+?)<br>\s*?<center>\s*?<br><br>\s*?\s*?<style>.+?(http://www\.stage54\.net/cgimages/caratulas/.+?jpg)" # plot
    matches = re.compile(patronvideos,re.S).findall(data)
    if len(matches)>0: 
        item.plot = matches[0][0]
        item.thumbnail = matches[0][1]

    from servers import servertools
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = video[0]
        scrapedurl = video[1]
        server = video[2]
        itemlist.append( Item(channel=channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, fulltitle=item.fulltitle, folder=False))

    return itemlist

    

