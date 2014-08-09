# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxatope
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "divxatope"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Mejor Torrent"
__language__ = "ES"

DEBUG = config.get_setting("debug")
LOGIN = "popeye20"
PASSWORD = "popeye20"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.divxatope mainlist")
    itemlist=[]

    item.url="http://www.divxatope.com"
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.get_match(data,'<h2 id="title-categorias">Categorias</h2>[^<]+<ul>(.*?)</ul>')
    patron = "<li><a href='([^']+)'[^>]+>([^<]+)</a></li>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if not title.startswith("Juegos") and not title.startswith("Musica"):
            itemlist.append( Item(channel=__channel__, action="lista", title=title , url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/divxatope.jpg", folder=True) )

    if len(itemlist)>0:
        itemlist.append( Item(channel=__channel__ , action="search"    , title="Buscar" ))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.divxatope search")
    if item.url=="":
        item.url="http://www.divxatope.com/main.php?q="
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return lista(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def lista(item):
    logger.info("pelisalacarta.channels.divxatope lista")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="torrent-container[^<]+'
    patron += '<img class="torrent-image" src="([^"]+)"[^<]+'
    patron += '<div class="torrent-info"[^<]+'
    patron += '<h4><a href ="([^"]+)">([^<]+)</a[^<]+</h4>[^<]+'
    patron += '<p>([^<]+)</p>[^<]+'
    patron += '<p>Subido[^<]+<strong>[^<]+</strong[^<]+<a[^<]+</a><br />[^<]+'
    patron += 'Descargas <strong><a href="." style="[^>]+>([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedurl,scrapedtitle,fecha,descargas in matches:
        title = scrapedtitle.strip()+" ("+descargas+" descargas) ("+fecha+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , viewmode="movie", folder=True) )

    # Extrae el paginador
    if item.extra == "":
        pagina_actual = 1
    else:
        pagina_actual = int(item.extra)

    patronvideos  = '<a class="paginator-items" href="([^"]+)" title="Pagina de torrent[^"]+">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    contador_pagina = 1
    
    for scrapedurl,scrapedtitle in matches:
        if contador_pagina == (pagina_actual + 1):
            title = ">> Ir a pag "+scrapedtitle+" de "+str(len(matches))
            url = urlparse.urljoin(item.url,scrapedurl)
            itemlist.append( Item(channel=__channel__, action="lista", title=title, url=url , extra="%d" % contador_pagina , folder=True) )
            break
        contador_pagina = contador_pagina + 1

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.divxatope findvideos")
    itemlist=[]

    # Averigua el PHPSESSID
    login = LOGIN.replace("@","%40")
    headers = scrapertools.get_headers_from_response("http://www.divxatope.com/index.php",post="login=%s&password=%s&Submit=ENTRAR" % (login,PASSWORD))
    logger.info("headers="+str(headers))
    request_headers=[ ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:14.0) Gecko/20100101 Firefox/14.0.1"] ]
    for header in headers:
        if header[0]=="set-cookie":
            #['set-cookie', 'PHPSESSID=d514b41a42fec11a7cae8bdb07fcef58; path=/']
            #Cookie: PHPSESSID=82336dad3c64c9c4110e793aa54abc4a;
            cookie_value = scrapertools.get_match(header[1],"PHPSESSID\=([a-z0-9]+)\;")
            request_headers.append(["Cookie","PHPSESSID="+cookie_value])

    # Descarga la página
    data = scrapertools.cache_page(item.url,headers=request_headers)

    #logger.info("data="+data)
    #<a id="downloadTorrent" class="btn-download-file_" style="padding:10px 0px 0px 30px;margin:0px 0px 0px 105px;font-size:21px;font-weight:bold;color:#fff;width:355px;height:38px;display:block;background:url('http://www.divxatope.com/images/btn-descarga-torrent.gif');" 
    #href ="http://tumejorserie.com/redirectlink/index.php?domain=www-divx-com&link=uploads/torrents/attachments/7537_elementary_--_temporada_2_[hdtv][cap.223][espanol_castellano].torrent" title="7537_elementary_--_temporada_2_[hdtv][cap.223][espanol_castellano].torrent" target="_blank">Descargar Torrent</a>
    # http://www.divxatope.com/uploads/torrents/attachments/7537_elementary_--_temporada_2_[hdtv][cap.223][espanol_castellano].torrent
    link = scrapertools.find_single_match(data,'redirectlink/index.php\?domain=www-divx-com&link=(.*?\.torrent)')
    if link!="":
        link = "http://www.divxatope.com/"+link
        logger.info("pelisalacarta.channels.divxatope torrent="+link)
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , fulltitle = item.title, url=link , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    # Ahora busca los vídeos
    itemlist.extend(servertools.find_video_items(data=data))

    for videoitem in itemlist:
        videoitem.channel = __channel__

        fichero = scrapertools.get_filename_from_url(videoitem.url)
        partes = fichero.split("/")
        titulo = partes[ len(partes)-1 ]
        videoitem.title = titulo + " - [" + videoitem.server+"]"
        videoitem.fulltitle = item.fulltitle

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    for mainlist_item in mainlist_items:
        if "DVDRip Castellano" in mainlist_item.title:
            peliculas_items = lista(mainlist_item)
            break
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien
