# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv
# Canales verificados
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "verificados"
__type__ = "generic"
__title__ = "Verificados"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.verificados.mainlist")

    itemlist = []
    itemlist.extend( add_tve() )
    itemlist.extend( add_rtpa() )
    itemlist.extend( add_aragontv() )
    itemlist.extend( add_eltrecetv() )
    
    return itemlist

def add_aragontv():
    logger.info("mywebtv.channels.verificados.add_aragontv")

    itemlist=[]

    try:
        MAIN_URL = "http://www.aragontelevision.es/"
        data = scrapertools.cache_page(MAIN_URL)
        titulo = scrapertools.get_match(data,'<div id="banner-streaming-tv" style="position:relative;">(.*?)</div>')
        titulo = unicode( titulo, "iso-8859-1" , errors="replace" ).encode("utf-8")
        titulo = scrapertools.htmlclean(titulo)
        titulo = re.compile("\s+",re.DOTALL).sub(" ",titulo)
        titulo = titulo.strip()

        data = scrapertools.cache_page("http://alacarta.aragontelevision.es/streaming/streaming.html")
        url = scrapertools.get_match(data,"playlist\:\s*\[\s*\{\s*url\: '([^']+)'")

        itemlist.append( Item(channel=__channel__, title="Aragón TV [web] ("+titulo+")", action="play", url=url, thumbnail="http://mywebtv.mimediacenter.info/squares/aragontv.png", folder=False))
    except:
        import traceback
        logger.info(traceback.format_exc())

    return itemlist

def add_rtpa():
    logger.info("mywebtv.channels.verificados.add_rtpa")

    itemlist=[]

    try:
        MAIN_URL = "http://www.rtpa.es"
        data = scrapertools.cachePage(MAIN_URL)
        #<source type="video/flv" src="http://195.10.10.219/rtpa/tv.flv?GKID=d4c9ed9cae8f11e2973900163e914f68" /> 
        url = scrapertools.get_match(data,'<source type="video/flv" src="([^"]+)"')
        itemlist.append( Item(channel=__channel__, title="RTPA (Asturias) [web]", action="play", url=url, thumbnail="http://mywebtv.mimediacenter.info/squares/rtpa.png", folder=False))

        #<source src="http://iphone.rtpa.stream.flumotion.com/rtpa/tv-iphone-multi/main.m3u8" />
        url = scrapertools.get_match(data,'<source src="([^"]+.m3u8)"')
        itemlist.append( Item(channel=__channel__, title="RTPA (Asturias) [iOS]", action="play", url=url, thumbnail="http://mywebtv.mimediacenter.info/squares/rtpa.png", folder=False))
    except:
        import traceback
        logger.info(traceback.format_exc())

    return itemlist

def add_eltrecetv():
    logger.info("mywebtv.channels.verificados.add_eltrecetv")

    itemlist=[]

    try:
        MAIN_URL = "http://www.eltrecetv.com.ar/vivo"
        data = scrapertools.cachePage(MAIN_URL)
        #"vivo_flash_streamer":"rtmp:\/\/stream.eltrecetv.com.ar\/live13\/13tv",
        #"vivo_android_file":"rtsp:\/\/stream.eltrecetv.com.ar\/live13\/13tv\/13tv3",
        #"vivo_blackberry_file":"rtsp:\/\/stream.eltrecetv.com.ar\/live13\/13tv\/13tv3",
        #"vivo_iphone_file":"http:\/\/stream.eltrecetv.com.ar\/live13\/13tv\/13tv3\/playlist.m3u8",
        #"vivo_ipad_file":"http:\/\/stream.eltrecetv.com.ar\/live13\/13tv\/13tv3\/playlist.m3u8",
        #"eltrecetv_vivo_rtmp":"rtmp:\/\/stream.eltrecetv.com.ar\/live13\/13tv"
        patron  = 'vivo_([^"]+)"\:"([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
        encontrados = set()

        for scrapedtitle,scrapedurl in matches:
            title = "El Trece (Argentina) ["+scrapedtitle+"]"
            url = scrapedurl.replace("\\","")
            thumbnail = "http://mywebtv.mimediacenter.info/squares/eltrece.png"
            plot = ""
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

            # Añade al listado de XBMC
            if url not in encontrados and scrapedtitle!="xml" and not url.startswith("rtmp"):
                itemlist.append( Item(channel=__channel__, title=title, action="play", url=url, thumbnail=thumbnail, plot=plot, folder=False))
                encontrados.add(url)

    except:
        import traceback
        logger.info(traceback.format_exc())


    return itemlist


def add_tve():
    logger.info("mywebtv.channels.verificados.add_tve")

    itemlist=[]

    try:
        MAIN_URL = "http://www.rtve.es/m/alacarta/tve/directos/iphone"

        headers = []
        headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
        data = scrapertools.cachePage2(MAIN_URL,headers)
        
        patron  = '<li class="video"[^<]+'
        patron += '<p class="tag">video en directo</p[^<]+'
        patron += '<h4>([^<]+)</h4.*?'
        patron += '<p class="thumb"><img src="([^"]+)"[^<]+</p[^<]+'
        patron += '<a href="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)

        for scrapedtitle,scrapedthumbnail,scrapedurl in matches:
            title = scrapedtitle+" [iOS]"
            url = scrapedurl
            thumbnail = urlparse.urljoin(MAIN_URL,scrapedthumbnail)
            plot = ""
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, title=title, action="play", url=url, thumbnail=thumbnail, plot=plot, folder=False))

    except:
        import traceback
        logger.info(traceback.format_exc())

    return itemlist
