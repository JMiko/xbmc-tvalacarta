# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinetux
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinetux"
__category__ = "F"
__type__ = "generic"
__title__ = "Cinetux"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinetux.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas"         , title="Novedades"    , url="http://www.cinetux.org/" ))

    return itemlist

def peliculas(item):
    logger.info("[cinetux.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <!--PELICULA--><div class="peli_item textcenter">
    <div class="pelicula_img">
    <a href="http://www.cinetux.org/2012/02/ver-pelicula-ano-de-gracia-online.html"><img width="134" height="193" src="http://4.bp.blogspot.com/-uGdvLa7IHok/Tw2T6R_D9bI/AAAAAAAAEzw/Z6WgUHdnCPA/s270/ano_de_gracia.jpg" /></a></div>
    <a href="http://www.cinetux.org/2012/02/ver-pelicula-ano-de-gracia-online.html"><div class="dvdrip">
    </div>
    </a><a href="http://www.cinetux.org/2012/02/ver-pelicula-ano-de-gracia-online.html"><div style="color: white; font-size:13px;">Año de Gracia</div></a>
    <span class="rosa">DVD-RIP</span>
    <div class="icos_lg">
    <img style="border: 0pt none;" src="http://3.bp.blogspot.com/-d-kbbyjdxYI/TeA7nHuZ8mI/AAAAAAAADM8/Ii149s3ed2c/espanol.png"/><img style="border: 0pt none;" src="http://3.bp.blogspot.com/-t8w6a8_Hk-w/TeA7nd5Ad9I/AAAAAAAADNI/UYV40sR_sfc/online.png"/><img style="border: 0pt none;" src="https://lh5.googleusercontent.com/-35yef7ubBv8/TeA7nNfUXJI/AAAAAAAADM0/RCQqAiWLX9o/descarga.png"/>
    <div class="calidad5"></div>
    </div>
    </div>
    <!--FIN PELICULA-->
    '''
    '''
    <!--PELICULA--><div class="peli_item textcenter">
    <div class="pelicula_img">
    <a href="http://www.cinetux.org/2012/03/ver-pelicula-blancanieves-mirror-mirror.html"><img width="134" height="193" src="http://4.bp.blogspot.com/-0ymaaBAcy0M/TvnNJf7m0dI/AAAAAAAAAgA/7h8hI3napgI/s270/blancanieves-mirror-mirror-poster.jpg" /></a></div>
    <a href="http://www.cinetux.org/2012/03/ver-pelicula-blancanieves-mirror-mirror.html"><div class="HD-Real-720">
    </div>
    </a><a href="http://www.cinetux.org/2012/03/ver-pelicula-blancanieves-mirror-mirror.html"><div style="color: white; font-size:13px;">Blancanieves<br />(Mirror Mirror)</div></a>
    <span class="rosa">HD-REAL-720</span><br />
    <span class="rosa">DVD-RIP</span>
    <div class="icos_lg">
    <img style="border: 0pt none;" src="http://3.bp.blogspot.com/-d-kbbyjdxYI/TeA7nHuZ8mI/AAAAAAAADM8/Ii149s3ed2c/espanol.png"/><img style="border: 0pt none;" src="http://3.bp.blogspot.com/--2xClYCIiwY/TeA7nUAYXXI/AAAAAAAADNE/Mr530W5fFFk/sub.png"/><img style="border: 0pt none;" src="http://3.bp.blogspot.com/-sBVn6JyvTeA/TeA7nERPF4I/AAAAAAAADM4/2iRloiVHCG8/lat.png"/><img style="border: 0pt none;" src="http://3.bp.blogspot.com/-t8w6a8_Hk-w/TeA7nd5Ad9I/AAAAAAAADNI/UYV40sR_sfc/online.png"/><img style="border: 0pt none;" src="https://lh5.googleusercontent.com/-35yef7ubBv8/TeA7nNfUXJI/AAAAAAAADM0/RCQqAiWLX9o/descarga.png"/>
    <div class="calidadhd"></div>
    </div>
    </div>
    <!--FIN PELICULA-->
    '''
    patron  = '<!--PELICULA--><div class="peli_item textcenter">[^<]+'
    patron += '<div class="pelicula_img">[^<]+'
    patron += '<a href="([^"]+)[^<]+<img width="\d+" height="\d+" src="([^"]+)".*?'
    patron += '<div style="color[^>]+>(.*?)</div></a>[^<]+'
    patron += '<span class="rosa">([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,title,calidad in matches:
        scrapedplot = ""
        scrapedtitle = title + " ["+calidad+"]"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    '''
    <div id="post-10787">
    <div class="index_item index_item_ie"><a href="http://www.cinetux.org/2012/07/ver-pelicula-una-guerra-de-pelicula-online-gratis-2008.html" rel="bookmark" title="Ver Película Una Guerra de Pelicula Online Gratis (2008)"><img style="border: 1px solid #E2E2E2; padding: 2px;" width="139" height="205" src=http://2.bp.blogspot.com/-eTm8fqaOKJc/TtJYW_y6gzI/AAAAAAAABFg/zuOHhHwuNO8/s320/Una_Guerra_De_Pelicula_%2528Latino%2529.jpg />
    <center><b>Ver Película Una Guerra de Pelicula </b></center></a></div>
    '''
    patron  = '<div id="post-\d+">[^<]+'
    patron += '<div class="index_item index_item_ie"><a href="([^"]+)" rel="[^"]+" title="[^"]+"><img style="[^"]+" width="\d+" height="\d+" src=([^>]+)>[^<]+'
    patron += '<center><b>([^<]+)</b></center></a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,thumbnail,title in matches:
        scrapedplot = ""
        scrapedthumbnail = thumbnail[:-2]
        scrapedtitle = title[14:]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)"\s*><strong>\&raquo\;</strong></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien