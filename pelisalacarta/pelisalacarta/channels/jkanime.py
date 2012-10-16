# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para jkanime
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "JKanime"
__channel__ = "jkanime"
__language__ = "ES"
__creationdate__ = "20121015"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[jkanime.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="ultimos"  , title="Últimos"           , url="http://jkanime.net/" ))
    itemlist.append( Item(channel=__channel__, action="letras"   , title="Listado Alfabetico", url="http://jkanime.net/" ))
    itemlist.append( Item(channel=__channel__, action="generos"  , title="Listado por Genero", url="http://jkanime.net/" ))
  
    return itemlist

def ultimos(item):
    logger.info("[jkanime.py] ultimos")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="latestul">(.*?)</ul>')
    
    patron = '<a href="([^"]+)">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def generos(item):
    logger.info("[jkanime.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="genres">(.*?)</div>')
    
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def letras(item):
    logger.info("[jkanime.py] letras")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="animelet">(.*?)</ul>')
    
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def series(item):
    logger.info("[jkanime.py] series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    '''
    <table class="search">
    <tr>
    <td rowspan="2">
    <a href="http://jkanime.net/basilisk-kouga-ninpou-chou/"><img src="http://jkanime.net/assets/images/animes/thumbnail/basilisk-kouga-ninpou-chou.jpg" width="50" /></a>
    </td>
    <td><a class="titl" href="http://jkanime.net/basilisk-kouga-ninpou-chou/">Basilisk: Kouga Ninpou Chou</a></td>
    <td rowspan="2" style="width:50px; text-align:center;">Serie</td>
    <td rowspan="2" style="width:50px; text-align:center;" >24 Eps</td>
    </tr>
    <tr>
    <td><p>Basilisk, considerada una de las mejores series del genero ninja, nos narra la historia de dos clanes ninja separados por el odio entre dos familias. Los actuales representantes, Kouga Danjo del clan Kouga y Ogen del clan&#8230; <a class="next" href="http://jkanime.net/basilisk-kouga-ninpou-chou/">seguir leyendo</a></p></td>
    </tr>
    </table>
    '''
    patron  = '<table class="search[^<]+'
    patron += '<tr[^<]+'
    patron += '<td[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '</td>[^<]+'
    patron += '<td><a[^>]+>([^<]+)</a></td>[^<]+'
    patron += '<td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td[^>]+>([^<]+)</td>[^<]+'
    patron += '</tr>[^<]+'
    patron += '<tr>[^<]+'
    patron += '<td>(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl, scrapedthumbnail,scrapedtitle,line1,line2,scrapedplot in matches:
        title = scrapedtitle.strip()+" ("+line1.strip()+") ("+line2.strip()+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot))        

    try:
        siguiente = scrapertools.get_match(data,'<a class="listsiguiente" href="([^"]+)" >Resultados Siguientes')
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="series", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    except:
        pass
    return itemlist

def episodios(item):
    logger.info("[jkanime.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    scrapedplot = scrapertools.get_match(data,'<meta name="description" content="([^"]+)"/>')
    scrapedthumbnail = scrapertools.get_match(data,'<meta property="og.image" content="([^"]+)"/>')
    idserie = scrapertools.get_match(data,"ajax/pagination_episodes/(\d+)/")
    logger.info("idserie="+idserie)
    numero_pagina = item.extra
    if numero_pagina=="":
        numero_pagina="1"
    logger.info("idserie="+idserie)
    
    headers = []
    headers.append( [ "User-Agent" , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:16.0) Gecko/20100101 Firefox/16.0" ] )
    headers.append( [ "Referer" , item.url ] )
    data = scrapertools.cache_page("http://jkanime.net/ajax/pagination_episodes/"+idserie+"/"+numero_pagina+"/")
    logger.info("data="+data)
    
    '''
    [{"id":"14199","title":"GetBackers - 1","number":"1","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14200","title":"GetBackers - 2","number":"2","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14201","title":"GetBackers - 3","number":"3","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14202","title":"GetBackers - 4","number":"4","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14203","title":"GetBackers - 5","number":"5","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14204","title":"GetBackers - 6","number":"6","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14205","title":"GetBackers - 7","number":"7","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14206","title":"GetBackers - 8","number":"8","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14207","title":"GetBackers - 9","number":"9","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14208","title":"GetBackers - 10","number":"10","animes_id":"122","timestamp":"2012-01-04 16:59:30"}]
    '''
    patron = '"id"\:"(\d+)","title"\:"([^"]+)","number"\:"(\d+)","animes_id"\:"(\d+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    #http://jkanime.net/get-backers/1/
    for id,scrapedtitle,numero,animes_id in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,numero)
        thumbnail = scrapedthumbnail
        plot = scrapedplot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot))        

    return itemlist

def findvideos(item):
    logger.info("[jkanime.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    '''
    clip: {
        url: 'http://jkanime.net/stream/jkget/a958097878b2e53826241592d85ecefb/acaa607e676ddf97bc2e856b813b4762/?t=6e',
    '''
    try:
        mediaurl = scrapertools.get_match(data,"clip\: {\s+url\: '([^']+)'")
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver el vídeo - Mirror 1" , url=mediaurl, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server="directo", folder=False))
    except:
        pass
    
    #flashvars="file=http://jkanime.net/stream/jkget/a958097878b2e53826241592d85ecefb/acaa607e676ddf97bc2e856b813b4762/&
    try:
        mediaurl = scrapertools.get_match(data,'flashvars\="file\=([^\&]+)\&')
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver el vídeo - Mirror 2" , url=mediaurl, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server="directo", folder=False))
    except:
        pass
    

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false
    
    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    episodios_items = newlist(mainlist_items[0])
    
    bien = False
    for episodio_item in episodios_items:
        mirrors = findvideos(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien
