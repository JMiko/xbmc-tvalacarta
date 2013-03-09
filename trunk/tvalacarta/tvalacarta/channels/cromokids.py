# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para cromokids
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "cromokids"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cromokids.py] mainlist")

    itemlist=[]
    itemlist.append( Item(channel=CHANNELNAME, title="Catalá"  , action="series", url="http://www.cromokids.tv/mobile/?idioma=1", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Español" , action="series", url="http://www.cromokids.tv/mobile/?idioma=2", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="English" , action="series", url="http://www.cromokids.tv/mobile/?idioma=3", folder=True) )

    return itemlist

def series(item):
    logger.info("[cromokids.py] series")
    
    # Descarga la página
    headers = []
    headers.append( ["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version"])
    headers.append( ["Accept-Language","es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info(data)

    # Extrae las entradas (series)
    '''
    <li class="menuchannels"><a href="capitolsSerie.php?idioma=2&canal=1&usr=guest&p=Z3Vlc3Q="><img src="/assets/thumbnails/iphone-images/logo-canal/miniman-logo.gif" alt="Miniman" /></a>
    <li class="menuchannels"><a href="capitolsSerie.php?idioma=1&canal=1&usr=guest&p=Z3Vlc3Q="><img src="/assets/thumbnails/iphone-images/logo-canal/miniman-logo.gif" alt="Miniman" /></a></li>
    <li class="menuchannels"><a href="capitolsSerie.php?idioma=1&canal=2&usr=guest&p=Z3Vlc3Q="><img src="/assets/thumbnails/iphone-images/logo-canal/pipsplanet-logo.gif" alt="PipsqueakPlanet" />
    
    '''
    patron = '<li\s+class="menuchannels"><a\s+href="(capitolsSerie.php[^"]+)"><img\s+src="([^"]+)"\s+alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,title in matches:
        scrapedtitle = title
        scrapedtitle = unicode( scrapedtitle , "iso-8859-1" , errors="ignore").encode("utf-8")
        
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[cromokids.py] episodios")
    
    # Descarga la página
    headers = []
    headers.append( ["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version"])
    data = scrapertools.cache_page(item.url,headers=headers)
    #logger.info(data)

    # episodios
    '''
    <a class="noeffect" href="http://212.31.41.50:1935/vod/mp4:PipsqueakPlanet-S01E04-CA004-512k.mp4/playlist.m3u8" >
    <img alt="PipsqueakPlanet" src="/assets/thumbnails/iphone-images/THUMBS/PipsqueakPlanet-S01E04-thumb.gif"/>
    <span class="name">En Pipsqueak va a la ciutat</span><span class="comment">Ep. 4 - Temp. 01</span>
    '''
    patron  = '<a class="noeffect" href="([^"]+)"[^<]+'
    patron += '<img alt="[^"]+" src="([^"]+)"[^<]+'
    patron += '<span class="name">([^"]+)</span><span class="comment">([^"]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,title,subtitle in matches:
        scrapedtitle = title+" "+subtitle
        scrapedtitle = unicode( scrapedtitle , "iso-8859-1" , errors="ignore").encode("utf-8")
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=False) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    items = mainlist(Item())
    items_programas = series(items[0])
    if len(items_programas)==0:
        return False

    items_episodios = episodios(items_programas[0])
    if len(items_episodios)==0:
        return False

    return bien
