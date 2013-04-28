# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal tvonlineapp.com
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tvonlineapp"
__type__ = "generic"
__title__ = "tvonlineapp.com"
__language__ = "ES"

DEBUG = config.get_setting("debug")
MAIN_URL = "http://tvonlineapp.com/app/veotv/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.tvonlineapp.mainlist")
    itemlist = []
    return paises(item)

def paises(item):
    logger.info("mywebtv.channels.tvonlineapp.paises")
    itemlist = []

    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cache_page(url=MAIN_URL,headers=headers)

    data = scrapertools.get_match(data,'<div data-role="page" id="page2"(.*?)<div data-role="page" id="page3">')
    
    patron  = '<li[^<]+'
    patron += '<a class="[^"]+" href="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^>]+>[^<]+'
    patron += '<h3[^>]+>([^<]+)</h3></a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url = scrapedurl
        thumbnail = urlparse.urljoin(MAIN_URL,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item( channel=__channel__ , action="emisoras" , title=title , url=url, thumbnail=thumbnail, plot=plot))

    return itemlist

def emisoras(item):
    logger.info("mywebtv.channels.tvonlineapp.emisoras")
    itemlist = []

    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cache_page(url=item.url,headers=headers)

    '''
    <li class="ui-btn ui-btn-icon-right ui-li ui-li-has-alt ui-li-has-thumb  ui-btn-up-c" data-theme="c" data-iconpos="right" data-icon="arrow-r"  data-wrapperels="div" data-iconshadow="true" data-shadow="false" >
    <a href="http://tvonlineapp.com/app/embedChannel.php?p=18703"  title="CANAL DIOCESANO" target="_self" class="ui-link-inherit">
    <img src="http://www.tvonlineapp.com/test/scripts/thumbnail.php?src=http://t1.gstatic.com/images?q=tbn:ANd9GcQBu0bDGYVEVaVtYG1NxAa_zSP1om6F_qhLb0KYAflCume2AaYeYA&w=80&h=80&zc=0 alt="CANAL DIOCESANO" />
    <h2> CANAL DIOCESANO</h2>
    <p> </p></a>
    </li>
    '''
    
    patron  = '<li[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '<h2[^>]*>([^<]+)</h2>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = scrapedurl
        thumbnail = urlparse.urljoin(url,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item( channel=__channel__ , action="play" , title=title , url=url, folder=False))

    return itemlist

def play(item):
    logger.info("mywebtv.channels.tvonlineapp.play")
    itemlist = []

    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    data = scrapertools.cache_page(url=item.url,headers=headers)
    logger.info("data="+data)

    from servers import justintv
    videos = justintv.find_videos(data)
    server="justintv"

    if len(videos)==0:
        from servers import ustream
        videos = ustream.find_videos(data)
        server="ustream"

    for titulo,url,serverfound in videos:
        title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
        plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

        itemlist.append( Item( channel=__channel__ , action="play" , server="server", title=title , url=url, folder=False))

    return itemlist
