# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasaudiolatino
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasaudiolatino"
__category__ = "F"
__type__ = "generic"
__title__ = "Peliculasaudiolatino"
__language__ = "ES"
__creationdate__ = "20111014"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasaudiolatino.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas Recien Agregadas", action="listarpeliculas", url="http://www.peliculasaudiolatino.com/newest-movies/page/0.html" , extra="http://www.peliculasaudiolatino.com/newest-movies/page/"))
    itemlist.append( Item(channel=__channel__, title="Estrenos" , action="listarpeliculas", url="http://www.peliculasaudiolatino.com/latest-movies/page/0.html" , extra="http://www.peliculasaudiolatino.com/latest-movies/page/"))
    itemlist.append( Item(channel=__channel__, title="Peliculas Actualizadas", action="listarpeliculas", url="http://www.peliculasaudiolatino.com/updated-movies/page/0.html" , extra="http://www.peliculasaudiolatino.com/updated-movies/page/"))
    itemlist.append( Item(channel=__channel__, title="Peliculas Mas Vistas", action="listarpeliculas", url="http://www.peliculasaudiolatino.com/most-viewed-movies/page/0.html" , extra="http://www.peliculasaudiolatino.com/most-viewed-movies/page/"))
    itemlist.append( Item(channel=__channel__, title="Peliculas Mejor Valoradas", action="listarpeliculas", url="http://www.peliculasaudiolatino.com/top-rated-movies/page/0.html" , extra="http://www.peliculasaudiolatino.com/top-rated-movies/page/"))
    itemlist.append( Item(channel=__channel__, title="Listado Alfabetico" , action="alfabetico", url="http://www.peliculasaudiolatino.com/letter/"))
    itemlist.append( Item(channel=__channel__, title="Listado por Generos" , action="generos", url="http://www.peliculasaudiolatino.com"))
    itemlist.append( Item(channel=__channel__, title="Buscar" , action="search") )
    return itemlist

def listarpeliculas(item):
    logger.info("[peliculasaudiolatino.py] listarpeliculas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    extra = item.extra

    # Extrae las entradas de la pagina seleccionada
    '''<td class="DarkText" align="center" valign="top" width="100px" height="160px" style="background-color:#1e1e1e;" onmouseover="this.style.backgroundColor='#000000'" onmouseout="this.style.backgroundColor='#1e1e1e'"><p style="margin-bottom: 3px;border-bottom:#ABABAB 1px solid"> 
                    	<a href="http://www.peliculasaudiolatino.com/movies/Larry_Crowne.html"><img src="http://www.peliculasaudiolatino.com/poster/85x115/peliculas/movieimg/movie1317696842.jpg" alt="Larry Crowne" border="0" height="115" width="85"></a>'''
    patron = '<td class=.*?<a '
    patron += 'href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedurl = match[0]
        scrapedtitle = match[2]
        scrapedthumbnail = match[1]
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=extra , folder=True) )
           
    # Extrae la marca de siguiente página
    patron = 'Anterior.*?  :: <a href="/../../.*?/page/([^"]+)">Siguiente '
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        if len(matches)>0:
            scrapedurl = extra+match
            scrapedtitle = "!Pagina Siguiente"
            scrapedthumbnail = ""
            scrapedplot = ""
    
            itemlist.append( Item(channel=__channel__, action="listarpeliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=extra , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[peliculasaudiolatino.py] videos")
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    title = item.title
    scrapedthumbnail = item.thumbnail
    itemlist = []
    patron = "tr>.*?window.open[\D]'([^']+)'.*?Servidor: ([^<]+)<.*?Audio: ([^<]+)<.*?Calidad: ([^<]+)<.*?Formato: ([^<]+)</font>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
    for match in matches:
        url = match[0]
        title = "SERVIDOR: "+match[1]+" IDIOMA: "+match[2]+" CALIDAD: "+match[3]+" "
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , thumbnail=scrapedthumbnail , folder=False) )

    return itemlist

def play(item):
    logger.info("[peliculasaudiolatino.py] play")
    itemlist=[]

    data2 = scrapertools.cache_page(item.url)
    data2 = data2.replace("http://www.peliculasaudiolatino.com/show/mv.php?url=","http://www.megavideo.com/?v=")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/show/videobb.php?url=","http://www.videobb.com/watch_video.php?v=")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/show/vidbux.php?url=","http://www.vidbux.com/")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/show/vidxden.php?url=","http://www.vidxden.com/")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/show/videozer.php?url=","http://www.videozer.com/video/")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/v/pl/play.php?url=","http://www.putlocker.com/embed/")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/v/mv/play.php?url=","http://www.modovideo.com/frame.php?v=")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/v/ss/play.php?url=","http://www.sockshare.com/embed/")
    data2 = data2.replace("http://www.peliculasaudiolatino.com/v/vb/play.php?url=","http://vidbull.com/")

    listavideos = servertools.findvideos(data2)
    for video in listavideos:
        invalid = video[1]
        invalid = invalid[0:8]
        if invalid!= "FN3WE43K" and invalid!="9CC3F8&e":
            scrapedtitle = item.title+video[0]
            videourl = video[1]
            server = video[2]
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+videourl+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=videourl , server=server , folder=False) )
    
    return itemlist

def generos(item):
    logger.info("[peliculasaudiolatino.py] categorias")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patron = '<img src="/templates/images/mgeneros.jpg"(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
    data = matches[0]
                                          
    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
                                          
    for match in matches:
        scrapedurl = urlparse.urljoin("http://www.peliculasaudiolatino.com",match[0])
        scrapedurl = scrapedurl.replace(".html","/page/0.html")
        extra = scrapedurl.replace ("/page/0.html","/page/")
        scrapedtitle = match[1].replace("&nbsp;&nbsp;&nbsp;*","").strip()
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        if scrapedtitle=="Adultos +18":
            if config.get_setting("enableadultmode") == "true":
                itemlist.append( Item(channel=__channel__, action="listado2", title=scrapedtitle , url="http://www.myhotamateurvideos.com" , thumbnail=scrapedthumbnail , plot=scrapedplot , extra="" , folder=True) )
        else:
            itemlist.append( Item(channel=__channel__, action="listado2", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=extra, folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title)    
    return itemlist
    
def alfabetico(item):
    logger.info("[cinetube.py] listalfabetico")

    extra = item.url
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="listado2" , title="0-9", url="http://www.peliculasaudiolatino.com/search/0-9/page/0.html", extra="http://www.peliculasaudiolatino.com/search/0-9/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="A"  , url="http://www.peliculasaudiolatino.com/letter/a/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/a/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="B"  , url="http://www.peliculasaudiolatino.com/letter/b/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/b/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="C"  , url="http://www.peliculasaudiolatino.com/letter/c/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/c/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="D"  , url="http://www.peliculasaudiolatino.com/letter/d/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/d/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="E"  , url="http://www.peliculasaudiolatino.com/letter/e/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/e/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="F"  , url="http://www.peliculasaudiolatino.com/letter/f/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/f/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="G"  , url="http://www.peliculasaudiolatino.com/letter/g/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/g/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="H"  , url="http://www.peliculasaudiolatino.com/letter/h/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/h/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="I"  , url="http://www.peliculasaudiolatino.com/letter/i/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/i/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="J"  , url="http://www.peliculasaudiolatino.com/letter/j/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/j/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="K"  , url="http://www.peliculasaudiolatino.com/letter/k/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/k/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="L"  , url="http://www.peliculasaudiolatino.com/letter/l/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/l/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="M"  , url="http://www.peliculasaudiolatino.com/letter/m/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/m/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="N"  , url="http://www.peliculasaudiolatino.com/letter/n/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/n/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="O"  , url="http://www.peliculasaudiolatino.com/letter/o/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/o/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="P"  , url="http://www.peliculasaudiolatino.com/letter/p/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/p/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="Q"  , url="http://www.peliculasaudiolatino.com/letter/q/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/q/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="R"  , url="http://www.peliculasaudiolatino.com/letter/r/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/r/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="S"  , url="http://www.peliculasaudiolatino.com/letter/s/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/s/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="T"  , url="http://www.peliculasaudiolatino.com/letter/t/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/t/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="U"  , url="http://www.peliculasaudiolatino.com/letter/u/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/u/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="V"  , url="http://www.peliculasaudiolatino.com/letter/v/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/v/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="W"  , url="http://www.peliculasaudiolatino.com/letter/w/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/w/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="X"  , url="http://www.peliculasaudiolatino.com/letter/x/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/x/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="Y"  , url="http://www.peliculasaudiolatino.com/letter/y/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/y/page/"))
    itemlist.append( Item(channel=__channel__, action="listado2" , title="Z"  , url="http://www.peliculasaudiolatino.com/letter/z/page/0.html", extra="http://www.peliculasaudiolatino.com/letter/z/page/"))

    return itemlist

def listado2(item):
    logger.info("[cinetube.py] listado2")
    extra = item.extra
    itemlist = []
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = '<td height=90 valign=top width=60>.*?<a href="([^"]+)"><img src="([^"]+)" .*?<b>([^<]+)</b>.*?<td><b>([^<]+)</b></td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = urlparse.urljoin("http://www.peliculasaudiolatino.com",match[0])
        scrapedtitle = match[2]
        scrapedthumbnail = match[1]
        scrapedplot = match[3]
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if extra<>"":
        # Extrae la marca de siguiente página
        patron = "Anterior.*?  :: <a href='/../../.*?/.*?/page/([^']+)'>Siguiente "
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
        for match in matches:
            if len(matches)>0:
                scrapedurl = extra+match
                scrapedtitle = "!Pagina Siguiente"
                scrapedthumbnail = ""
                scrapedplot = ""
    
                itemlist.append( Item(channel=__channel__, action="listado2", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=extra , folder=True) )

    return itemlist

def search(item,texto):
    logger.info("[peliculasaudiolatino.py] search")
    itemlist = []

    texto = texto.replace(" ","+")
    try:
        # Series
        item.url="http://www.peliculasaudiolatino.com/result.php?q=%s&type=search&x=0&y=0"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(listado2(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 
        
        return itemlist
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
    '''url = "http://www.peliculasaudiolatino.com/series-anime"
    data = scrapertools.cachePage(url)

    # Extrae las entradas de todas series
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a.+?href="([\D]+)([\d]+)">[^<]+'
    patronvideos += '.*?/>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2].strip()

        # Realiza la busqueda
        if scrapedtitle.lower()==texto.lower() or texto.lower() in scrapedtitle.lower():
            logger.info(scrapedtitle)
            scrapedurl = urlparse.urljoin(url,(match[0]+match[1]))
            scrapedthumbnail = urlparse.urljoin("http://www.peliculasaudiolatino.com/images/series/",(match[1]+".png"))
            scrapedplot = ""

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist'''


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = listarpeliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = findvideos( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien