# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para ADNStream
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib
import os

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "adnstream"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[adnstream.py] mainlist")

    itemlist = []
    data = scrapertools.cache_page("http://www.adnstream.com")
    data = scrapertools.get_match(data,'<div class="botones" id="canales">(.*?)</div>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" title="[^"]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        #/canal/Documentales/
        url = urlparse.urljoin("http://www.adnstream.com",scrapedurl)
        thumbnail = "http://www.adnstream.com/img/"+scrapedurl.replace("/canal/","canales/")[:-1]+"_w320.jpg"
        
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , action="subcanales" , folder=True) )

    return itemlist

def subcanales(item):
    logger.info("[adnstream.py] subcanales")

    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron  = '<a class="captura" href="([^"]+)">[^>]+'
    patron += '<img width="\d+" height="\d+" src="([^"]+)"[^<]+'
    patron += '</a>[^<]+'
    patron += '<h3>[^<]+'
    patron += '<a[^>]+>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , action="subcanales" , folder=True) )

    if len(itemlist)==0:
        itemlist = videos(item)

    return itemlist

def videos(item):
    logger.info("[adnstream.py] videos")

    itemlist = []
    data = scrapertools.cache_page(item.url)
    '''
    <a class="captura" href="/video/zmeXyuLsiC/Pasion-de-Gavilanes-Ep006">
    <span>&nbsp;</span>
    <img width="160" height="120" src="http://46.4.33.243/static/thbs/z/zmeXyuLsiC_w160.jpg" alt="Pasión de Gavilanes - Ep006" title="Pasión de Gavilanes - Ep006" />
    </a>
    </span>
    <h3>
    <a href="/video/zmeXyuLsiC/Pasion-de-Gavilanes-Ep006" title="Pasión de Gavilanes - Ep006">Pasión de Gavilanes - Ep006</a>
    '''
    patron  = '<a class="captura" href="([^"]+)">[^>]+'
    patron += '<span>[^<]+</span>[^>]+'
    patron += '<img width="\d+" height="\d+" src="([^"]+)"[^<]+'
    patron += '</a>[^<]+'
    patron += '</span>[^<]+'
    patron += '<h3>[^<]+'
    patron += '<a[^>]+>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , action="play" , folder=False) )

    # Página siguiente
    # <a href="/canal/Pasion-de-Gavilanes/2" class="flecha">Next &gt;</a>
    patron = '<a href="([^"]+)" class="flecha">Next .gt.</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , url=urlparse.urljoin(item.url,matches[0]), action="videos" , folder=True) )

    return itemlist

def play(item):
    logger.info("[adnstream.py] play")

    itemlist = []
    id_video = scrapertools.get_match(item.url,".*?video/([^/]+)/")
    data = scrapertools.cache_page("http://www.adnstream.com/get_playlist.php?lista=video&param="+id_video)
    mediaurl = scrapertools.get_match(data,'<media.content type="[^"]+" url="([^"]+)"')

    itemlist.append( Item(channel=CHANNELNAME, title=item.title , server = "directo" , action="play" , url=mediaurl, thumbnail=item.thumbnail, folder=False) )

    return itemlist
