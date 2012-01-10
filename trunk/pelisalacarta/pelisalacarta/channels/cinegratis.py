# -*- coding: utf-8 -*-
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
    itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas - Estrenos DVD/BluRay" , url="http://www.cinegratis.net/estrenos-dvd-bluray/", extra="Estrenos+DVD%2FBLURAY"))
    itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas - Estrenos cine"       , url="http://www.cinegratis.net/estrenos-de-cine/", extra="Estrenos+de+Cine"))
    #itemlist.append( Item(channel=__channel__, action="peliscat"   , title="Películas - Géneros"             , url="http://www.cinegratis.net/index.php?module=generos"))
    #itemlist.append( Item(channel=__channel__, action="pelisalfa"  , title="Películas - Idiomas"             , url="http://www.cinegratis.net/index.php?module=peliculas"))
    #itemlist.append( Item(channel=__channel__, action="pelisalfa"  , title="Películas - Calidades"           , url="http://www.cinegratis.net/index.php?module=peliculas"))
    #itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar"                          , url="http://www.cinegratis.net/index.php?module=search&title=%s"))

    return itemlist

def peliculas(item):
    logger.info("[cinegratis.py] peliculas")
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
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra=item.extra))

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

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien