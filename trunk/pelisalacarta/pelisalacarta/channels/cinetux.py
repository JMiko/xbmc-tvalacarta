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
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Novedades" , url="http://www.cinetux.org/", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades subtitulado" , url="http://www.cinetux.org/", extra="Nuevo Sub", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades DVD" , url="http://www.cinetux.org/", extra="ltimo DVDRIP", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades latino" , url="http://www.cinetux.org/", extra="Nuevo Latino", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades castellano" , url="http://www.cinetux.org/", extra="Nuevo Castellano", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Nueva calidad disponible" , url="http://www.cinetux.org/", extra="Nueva Calidad", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="generos", title="Por géneros" , url="http://www.cinetux.org/", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))

    return itemlist

def peliculas(item):
    logger.info("[cinetux.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
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
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg",  folder=True) )

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
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg", folder=True) )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)"\s*><strong>\&raquo\;</strong></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg", folder=True) )

    return itemlist

def bloque(item):
    logger.info("[cinetux.py] bloque")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,item.extra+'</h6>(.*?)</div>')
    
    patron = '<a href="([^"]+)"><img style="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail in matches:
        scrapedplot = ""
        
        parsed_url = urlparse.urlparse(scrapedurl)
        fichero = parsed_url.path
        partes = fichero.split("/")
        scrapedtitle = partes[ len(partes)-1 ]
        scrapedtitle = scrapedtitle.replace("ver-pelicula-","")
        scrapedtitle = scrapedtitle.replace("-online-gratis","")
        scrapedtitle = scrapedtitle.replace(".html","")
        scrapedtitle = scrapedtitle.replace("-"," ")
        scrapedtitle = scrapedtitle.capitalize()

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=True) )

    return itemlist

def generos(item):
    logger.info("[cinetux.py] generos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'neros</h6>(.*?)</div>')
    
    patron = '<a href="([^"]+)">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=True) )

    return itemlist

def tags(item):
    logger.info("[cinetux.py] tags")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'Tags</h6>(.*?)</div>')
    patron = "<a href='([^']+)'[^>]+>([^<]+)<"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[cinetux.py] findvideos")
    itemlist=[]

    # Busca el argumento
    data = scrapertools.cache_page(item.url)
    '''
    <tr class="tabletr">
    <td class="episode-server" align="left"><img src="http://www.cinetux.org/imagenes/veronline.png" alt="" width="22" height="22" />Opción 01</td>
    <td class="episode-server-img" align="center">PutLocker</td>
    <td class="episode-lang" align="center">Español</td>
    <td align="center">DVD-SCR</td>
    <td class="center" align="center"><a rel="nofollow" target="_blank" class="myButtonLink" href="http://www.putlocker.com/file/BADCD9ACA395E318"></a></td>
    <td align="center">Anónimo</td>
    </tr>
    '''
    patron  = '<tr class="tabletr">[^<]+'
    patron += '<td class="opcion-td"><img[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="server-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="idioma-td[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="calidad-td[^<]+</td>[^<]+'
    patron += '<td class="fuente-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="link-td">(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle,scrapedserver,scrapedlanguage,scrapedquality,scrapedlink in matches:
        title = "Ver "+scrapedtitle+" en "+scrapedserver+" ("+scrapedlanguage+") ("+scrapedquality+")"
        url = scrapedlink
        thumbnail = item.thumbnail
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle+" ["+scrapedlanguage+"]["+scrapedquality+"]", url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=False) )

    patron  = '<tr class="tabletr">[^<]+'
    patron += '<td class="opcion-td"><img[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="server-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="idioma-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="fuente-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="link-td">(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle,scrapedserver,scrapedlanguage,scrapedquality,scrapedlink in matches:
        title = "Ver "+scrapedtitle+" en "+scrapedserver+" ("+scrapedlanguage+") ("+scrapedquality+")"
        url = scrapedlink
        thumbnail = item.thumbnail
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle+" ["+scrapedlanguage+"]["+scrapedquality+"]", url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=False) )

    patron  = '<tr class="tabletr">[^<]+'
    patron += '<td class="episode-server[^>]+><img[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="episode-server-img[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="episode-lang[^>]+>([^>]+)</td>[^<]+'
    patron += '<td align="center">([^<]+)</td>[^<]+'
    patron += '<td(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle,scrapedserver,scrapedlanguage,scrapedquality,scrapedlink in matches:
        title = "Ver "+scrapedtitle+" en "+scrapedserver+" ("+scrapedlanguage+") ("+scrapedquality+")"
        url = scrapedlink
        thumbnail = item.thumbnail
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle+" ["+scrapedlanguage+"]["+scrapedquality+"]", url=url , thumbnail=thumbnail , plot=plot , folder=False) )

    if len(itemlist)==0:
        itemlist = servertools.find_video_items(data=data)
        i=1
        for videoitem in itemlist:
            videoitem.title = "Ver Opción %d en %s" % (i,videoitem.server)
            videoitem.fulltitle = item.fulltitle
            videoitem.channel=channel=__channel__

    return itemlist

def play(item):
    logger.info("[cinetux.py] play")
    itemlist=[]
    itemlist = servertools.find_video_items(data=item.url)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

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