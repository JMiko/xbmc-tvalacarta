# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal para Disney Junior
#---------------------------------------------------------------------------
import os
import sys

import urlparse,re
import urllib
import datetime

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "disneyjunior"

def isGeneric():
    return True

# Entry point
def mainlist(item):
    logger.info("disneyjunior.main_list")
    itemlist=[]

    itemlist.append( Item(channel=CHANNELNAME, title="Web oficial" , action="disneyweb" , url="http://www.disney.es/disney-junior/contenido/video.jsp", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Canal YouTube (ES)" , action="youtube_playlists" , url="http://gdata.youtube.com/feeds/api/users/DisneyJuniorES/playlists?v=2&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Canal YouTube (LA)" , action="youtube_playlists" , url="http://gdata.youtube.com/feeds/api/users/DisneyJuniorLA/playlists?v=2&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Canal YouTube (UK)" , action="youtube_playlists" , url="http://gdata.youtube.com/feeds/api/users/DisneyJuniorUK/playlists?v=2&start-index=1&max-results=30", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Canal YouTube (FR)" , action="youtube_playlists" , url="http://gdata.youtube.com/feeds/api/users/DisneyJuniorFR/playlists?v=2&start-index=1&max-results=30", folder=True) )

    return itemlist

# Show all videos from the official website
def disneyweb(item):
    logger.info("disneyjunior.disneyweb")
    itemlist=[]

    # Fetch video list page
    data = scrapertools.cache_page( item.url )
    data = scrapertools.find_single_match( data , '<div id="video_main_promos_inner">(.*?)<div id="content_index_navigation">')
    
    # Extract items
    '''
    <div class="promo" style="background-image: url(/cms_res/disney-junior/images/promo_support/promo_holders/video.png);">
        <a href="/disney-junior/contenido/video/canta_con_dj_arcoiris.jsp " class="promoLinkTracking"><img src="/cms_res/disney-junior/images/video/canta_dj_arco_iris_164x104.jpg" class="promo_image" alt=""/></a>
        <div class="promo_title_3row"><p>Canta con DJ: La canción del arco iris</p></div>
        <a class="playlist_button_large"  href="" ref="canta_con_dj_arcoiris"><img src="/cms_res/disney-junior/images/promo_support/playlist_add_icon.png" alt="" /></a>
    </div>
    '''
    pattern  = '<div class="promo"[^<]+'
    pattern += '<a href="([^"]+)"[^<]+'
    pattern += '<img src="([^"]+)"[^<]+'
    pattern += '</a[^<]+'
    pattern += '<div[^<]+'
    pattern += '<p>([^<]+)</p>'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        # Not the better way to parse XML, but clean and easy
        title = scrapedtitle
        thumbnail = urlparse.urljoin( item.url , scrapedthumbnail )
        url = urlparse.urljoin( item.url , scrapedurl.strip() )
        plot = ""

        # Appends a new item to the xbmc item list
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , url=url, thumbnail=thumbnail, plot=plot , folder=False) )

    return itemlist

# Play one video from the official website
def play(item):
    logger.info("disneyjunior.disneyweb_play ")
    itemlist=[]

    if "disney.es" in item.url:

        # Fetch page
        data = scrapertools.cache_page( item.url )

        url_start = scrapertools.find_single_match( data , "config.rtmpeServer \= '([^']+)'")
        logger.info("disneyjunior.disneyweb_play url_start="+url_start)

        url_end = scrapertools.find_single_match( data , "config.firstVideoSource \= '([^']+)'")
        logger.info("disneyjunior.disneyweb_play url_end="+url_end)
        
        url = url_start + url_end
        logger.info("disneyjunior.disneyweb_play url="+url)

        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, folder=False) )
    else:
        itemlist.append(item)
    
    return itemlist

# Show all YouTube playlists for the selected channel
def youtube_playlists(item):
    logger.info("disneyjunior.youtube_playlists ")
    itemlist=[]

    # Fetch video list from YouTube feed
    data = scrapertools.cache_page( item.url )
    logger.info("data="+data)
    
    # Extract items from feed
    pattern = "<entry(.*?)</entry>"
    matches = re.compile(pattern,re.DOTALL).findall(data)
    
    for entry in matches:
        logger.info("entry="+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = scrapertools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = scrapertools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = scrapertools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        url = scrapertools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")

        # Appends a new item to the xbmc item list
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="youtube_videos" , url=url, thumbnail=thumbnail, plot=plot , folder=True) )
    return itemlist

# Show all YouTube videos for the selected playlist
def youtube_videos(item):
    logger.info("disneyjunior.youtube_videos ")
    itemlist=[]

    # Fetch video list from YouTube feed
    data = scrapertools.cache_page( item.url )
    logger.info("data="+data)
    
    # Extract items from feed
    pattern = "<entry(.*?)</entry>"
    matches = re.compile(pattern,re.DOTALL).findall(data)
    
    for entry in matches:
        logger.info("entry="+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = scrapertools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("Disney Junior España | ","")
        plot = scrapertools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = scrapertools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        video_id = scrapertools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = video_id

        # Appends a new item to the xbmc item list
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="youtube", url=url, thumbnail=thumbnail, plot=plot , folder=False) )
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    items_mainlist = mainlist(Item())
    
    items_programas = disneyweb(items_mainlist[0])
    if len(items_programas)==0:
        return False

    items_videos = play(items_programas[0])
    if len(items_videos)==0:
        return False

    for youtube_item in items_mainlist[1:]:
        items_videos = youtube_videos(youtube_item)
        if len(items_videos)==0:
            return False

    return bien