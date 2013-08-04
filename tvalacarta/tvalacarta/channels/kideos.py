# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para kideos
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

DEBUG = False
CHANNELNAME = "kideos"
MAIN_URL = "http://www.kideos.com/channels"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[kideos.py] mainlist")
    return programas(item)

def programas(item):
    logger.info("[kideos.py] programas")
    itemlist = []
    
    # Descarga la lista de canales
    item.url = MAIN_URL
    data = scrapertools.cache_page(item.url)
    '''
    <div id="VideoClip">
    <table width="100" border="0" cellpadding="0" cellspacing="0">
    <tr>
    <td valign="bottom" height="70">
    <a href="/cookie-monster"><span class="VideoTitles"><h1>Cookie Monster</h1></span></a>
    </td>
    </tr>
    <tr valign="top">
    <td height="100" valign="top">
    <div id="SearchThumbnail">
    <a href="/cookie-monster">
    <h1>
    <img src="http://img.youtube.com/vi/shbgRyColvE/0.jpg" width="100" alt="Cookie Monster" height="69" hspace="4" vspace="4" />				              </h1>
    </a>
    </div>
    '''
    patron  = '<div id="VideoClip">[^<]+'
    patron += '<table width="100" border="0" cellpadding="0" cellspacing="0">[^<]+'
    patron += '<tr>[^<]+'
    patron += '<td[^<]+'
    patron += '<a href="([^"]+)"><span class="VideoTitles"><h1>([^>]+)</h1></span></a>[^<]+'
    patron += '</td>[^<]+'
    patron += '</tr>[^<]+'
    patron += '<tr valign="top">[^<]+'
    patron += '<td height="100" valign="top">[^<]+'
    patron += '<div id="SearchThumbnail">[^<]+'
    patron += '<a href="[^"]+">[^<]+'
    patron += '<h1>[^<]+'
    patron += '<img src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show = scrapedtitle , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[kideos.py] episodios")
    itemlist = []
    
    # Descarga la lista de canales
    data = scrapertools.cache_page(item.url)
    '''
    <div id="VideoClip" style="width: 150px;">
    <br/>
    <table width="150" border="0" cellpadding="0" cellspacing="0">
    <tr>
    <td valign="bottom" height="70">
    <a href="/video/oh-there-you-are-perry-phineas-and-ferb">
    <span class="VideoTitles">
    <h1>Oh, There You Are, Perry - Phineas and Ferb</h1>
    </span>
    </a>
    </td>
    </tr>
    <tr valign="top">
    <td valign="top">
    <div id="SearchThumbnail" style="background-position:-200px -224px;height:110px;width:140px;">
    <a href="/video/oh-there-you-are-perry-phineas-and-ferb">
    <h1>
    <img src="http://img.youtube.com/vi/sD8hqHSyYxw/0.jpg" width="132" height="99" hspace="4" vspace="4" />				    </h1>
    </a>
    </div>
    '''
    patron  = '<div id="VideoClip"[^<]+'
    patron += '<br/>[^<]+'
    patron += '<table width="150" border="0" cellpadding="0" cellspacing="0">[^<]+'
    patron += '<tr>[^<]+'
    patron += '<td valign="bottom" height="70">[^<]+'
    patron += '<a href="([^"]+)">[^<]+'
    patron += '<span class="VideoTitles">[^<]+'
    patron += '<h1>([^<]+)</h1>[^<]+'
    patron += '</span>[^<]+'
    patron += '</a>[^<]+'
    patron += '</td>[^<]+'
    patron += '</tr>[^<]+'
    patron += '<tr valign="top">[^<]+'
    patron += '<td valign="top">[^<]+'
    patron += '<div id="SearchThumbnail"[^<]+'
    patron += '<a[^<]+'
    patron += '<h1>[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show = scrapedtitle , folder=False) )

    return itemlist

def play(item):
    logger.info("[kideos.py] episodios")
    itemlist = []
    
    # Descarga la lista de canales
    data = scrapertools.cache_page(item.url)
    youtube_id = scrapertools.get_match(data,"'flashVars', 'youtube\=1\&videoId\=([^']+)'")
    url = "http://www.youtube.com/watch?v="+youtube_id
    item = Item(channel=item.channel, title=item.title, url=url, thumbnail=item.thumbnail, server="youtube")
    itemlist.append(item)
    
    return itemlist

def test():

    # Al entrar sale una lista de programas
    programas_items = mainlist(Item())
    if len(programas_items)==0:
        print "No devuelve programas"
        return False

    videos_items = episodios(programas_items[0])
    if len(videos_items)==1:
        print "No devuelve videos en "+programas_items[0].title
        return False

    return True