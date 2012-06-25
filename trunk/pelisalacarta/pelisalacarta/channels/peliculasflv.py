# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasflv"
__category__ = "F"
__type__ = "generic"
__title__ = "PeliculasFLV"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"    , action="peliculas", url="http://www.peliculas-flv.com/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Categorías"   , action="categorias", url="http://www.peliculas-flv.com/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Buscar..."    , action="search"))
    
    return itemlist

def search(item,texto):
    logger.info("[peliculasflv.py] search")
    texto = texto.replace(" ","+")
    item.url="http://www.peliculas-flv.com/es/peliculas/search/"+texto
    return peliculas(item)

def peliculas(item):
    logger.info("[peliculasflv.py] listado")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)

    # Extrae las entradas
    '''
    <div class="itemdos" id="numitem26"><a href="http://www.peliculas-flv.com/es/pelicula/0001417/ver-wall-e-online.html" title="romance, adventure, family, animation" class="bslink3"><img src="http://www.peliculas-flv.com/imagenes/portadas/3d3be431e7bfe9eadbb0.jpg" width="140" height="184" class="img imgx" border="0" /></a><div class="bttm">
    <div class="ttl"><a href="http://www.peliculas-flv.com/es/pelicula/0001417/ver-wall-e-online.html" title="WALL·E
    " class="bslink3">WALL·E
    </a></div>
    <div class="idiomes"><select><option selected="selected">Latino</option></select></div>
    <div class="dtlls"><a rel="lyteframe" rev="width: 600px; height: 380px; scrolling: no;" title="By Peliculas-Flv.com" href="http://www.youtube.com/v/D8kwXBZIOUE&amp;hl&amp;autoplay=1" target="_blank"><img src="http://www.peliculas-flv.com/archivos/trailer.png" width="125" height="25" border="0" /></a></div>
    </div><div class="c5 imgx"><a rel="numitem26" href="http://www.peliculas-flv.com/es/pelicula/0001417/ver-wall-e-online.html" title="romance, adventure, family, animation" class="bslink3"></a></div>
    '''
    patron  = '<div class="itemdos" id="numitem[^"]+"><a href="([^"]+)"[^<]+<img src="([^"]+)"[^<]+</a><div class="bttm">[^<]+'
    patron += '<div class="ttl"><a[^>]+>([^<]+)</a></div>[^<]+'
    patron += '<div class="idiomes"><select>(.*?)</select></div>.*?'
    patron += '<div class="(c\d+) imgx">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for url,thumbnail,title,idiomas,calidad in matches:
        if calidad=="c2" or calidad=="c1":
            nombre_calidad="Novedad"
        elif calidad=="c4" or calidad=="c3":
            nombre_calidad="Actualizada"
        elif calidad=="c7" or calidad=="c8":
            nombre_calidad="HD"
        elif calidad=="c5" or calidad=="c6":
            nombre_calidad="DVD"
        else:
            nombre_calidad="Calidad "+calidad
        scrapedtitle = title.strip()+" ["+scrapertools.htmlclean(idiomas)+"]["+nombre_calidad+"]"
        scrapedurl = url
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a href='([^']+)'>\&raquo\;</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def categorias(item):
    logger.info("[peliculasflv.py] categorias")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    data = scrapertools.get_match(data,'<div class="prgnt">(.*?)</li></div>')

    # Extrae las entradas
    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedurl,scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[peliculasflv.py] findvideos")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)

    # Extrae las entradas
    '''
    <tr bgcolor=""><td align="left" class="episode-server" >
    <a href="http://www.peliculas-flv.com/es/reproductor/pelicula/1062/7813/" title="Los vengadores
    " target="_blank"><img src="http://www.peliculas-flv.com/imagenes/servers/veronline.png" height="22" width="22">Reproducir</a>
    </td> <td align="center" class="episode-server-img">
    <a href="http://www.peliculas-flv.com/es/reproductor/pelicula/1062/7813/" title="Los vengadores
    " target="_blank"><span class="server vk"></span></a>
    </td> <td align="center" class="episode-lang">Spanish</td> 
    <td align="center" class="center">no_sub</td> <td align="center"> 
    <span class="episode-quality-icon" title="Calidad DVD SCREENER"> <i class="sprite c4"></i> </span> </td> <td align="center" class="center">
    <span title="DVD SCREENER">DVD SCREENER</span></td> <td align="center" class="episode-uploader">
    <span>adminintrator</span></td> <td align="center" class="center">0</td> </tr>
    '''
    '''
    <tr bgcolor="#EBEBEB">
    <td width="130" align="left" class="episode-server" ><a href="http://peliculas-flv.com/redirect/?url=http%3A%2F%2Fwww.filesline.com%2Fw5ufrob717z9.html" target="_blank"><img src="http://www.peliculas-flv.com/imagenes/servers/descarga.png" height="22" width="22" />Descargar</a></td>
    <td width="160" align="center" class="episode-server-img">
    <a href="http://peliculas-flv.com/redirect/?url=http%3A%2F%2Fwww.filesline.com%2Fw5ufrob717z9.html" title="Los vengadores
    " target="_blank"><span class="server filesline"></span></a>
    </td> <td width="107" align="center" class="episode-lang">English</td> 
    <td width="99" align="center" class="center">Spanish</td> <td width="56" align="center"> 
    <span class="episode-quality-icon" title="Calidad DVD SCREENER"> <i class="sprite c4"></i> </span> </td> <td width="119" align="center" class="center">
    <span title="DVD SCREENER">DVD SCREENER</span></td> <td width="125" align="center" class="episode-uploader">
    <span>adminintrator</span></td> <td width="60" align="center" class="center">0</td> </tr>
    '''
    patron  = '<tr[^<]+<td.*?class="episode-server"[^<]+'
    patron += '<a href="([^"]+)".*?<span class="server([^"]+)">.*?'
    patron += 'class="episode-lang">([^<]+)</td>.*?'
    patron += 'class="center">([^<]+)</td> <td[^<]+'
    patron += '<span class="episode-quality-icon" title="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for url,title,idioma,sub,calidad in matches:
        if calidad.startswith("Calidad "):
            calidad = calidad[8:]
        if sub=="no_sub":
            scrapedtitle = "Ver en "+title.strip()+" ["+idioma+" / "+calidad+"]"
        else:
            scrapedtitle = "Ver en "+title.strip()+" ["+idioma+" / SUB "+sub+" / "+calidad+"]"
        scrapedurl = url
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

    return itemlist

def play(item):
    logger.info("[letmewatchthis.py] play")
    
    itemlist=[]
    
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info("data="+data)
    itemlist = servertools.find_video_items(data=data)
    
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien