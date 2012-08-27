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
    logger.info("[divxatope.py] mainlist")
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

    return itemlist

def lista(item):
    logger.info("[divxatope.py] lista")
    itemlist = []

    # Descarga la p�gina
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
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=False) )

    # Extrae el paginador
    patronvideos  = '<a class="paginator-items" href="([^"]+)" title="Pagina de torrent[^"]+">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        title = ">> P�gina "+scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="lista", title=title, url=url , folder=True) )

    return itemlist

def play(item):
    logger.info("[divxatope.py] play")
    itemlist = []

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

    # Descarga la p�gina
    data = scrapertools.cache_page(item.url,headers=request_headers)
    #logger.info("data="+data)
    #href ="redirect.php?file=31351&url=http://www.divxatope.com/uploads/torrents/attachments/5730_iceberg-
    link = scrapertools.get_match(data,'redirect.php\?file=\d+\&url=(.*?\.torrent)')
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , url=link , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    return itemlist