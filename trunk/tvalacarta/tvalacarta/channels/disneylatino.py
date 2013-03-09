# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# creado por rsantaella
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "disneylatino"
__category__ = "F"
__type__ = "generic"
__title__ = "disneylatino"
__language__ = "ES"
__creationdate__ = "20121216"
__vfanart__ = ""

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[disneylatino.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Disney Channel" , extra="channel=all" , action="characters" , url="http://www.disneylatino.com/es/videos/dc/index.jsp", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Disney XD" , extra="channel=xd" , action="characters" , url="http://www.disneylatino.com/es/videos/xd/index.jsp", folder=True) )
    itemlist.append( Item(channel=__channel__, title="Disney Junior" , extra="channel=jr" , action="characters" , url="http://www.disneylatino.com/es/videos/jr/index.jsp", folder=True) )
    return itemlist

def characters(item):

    logger.info("[disneylatino.py] characters")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    if (data == ""):
        return itemlist
    
    logger.info(data)

    scrapedurl = item.url
    extra_info = item.extra + "&character=all"
    itemlist.append( Item(channel=__channel__, action="categories", extra= extra_info,  title="Todo", url=scrapedurl,  folder=True) )

    #<a href="#" data-name="jake_y_los_piratas" title="Jake y los Piratas del país de nunca jamas"><img src="/res/disneylatino/content/latam/dlOnlineGameCatalog/junior/jake.jpg" alt="Jake y los Piratas del país de nunca jamas" /></a>
    patron = '<a href="#" data-name="(.*?)" title="(.*?)"><img src="([^"]+)" alt="(.*?)" /></a>'

    matches = re.compile(patron,re.DOTALL).findall(data)

    if DEBUG: scrapertools.printMatches(matches)
    

    for match in matches:
        scrapedthumbnail = 	"http://www.disneylatino.com" + match[2]
        scrapedtitle = scrapertools.htmlclean(match[1])
        extra_info = item.extra + "&character=" + match[0]
        itemlist.append( Item(channel=__channel__, action="categories", extra= extra_info,  title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,  folder=True) )
    return itemlist

def categories(item):

    logger.info("[disneylatino.py] categories")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    if (data == ""):
        return itemlist
    
    logger.info(data)

    #<a href="#" data-filter="all">Todos</a></li>
    patron = '<a href="#" data-filter="(.*?)">(.*?)</a></li>'

    matches = re.compile(patron,re.DOTALL).findall(data)

    if DEBUG: scrapertools.printMatches(matches)
    

    for match in matches:
        scrapedurl = "http://befsn.disneylatino.com/index.php/catalog/videos.json?" + item.extra + "&category=" + match[0] + "&page=%d&itemsPerPage=25"
        scrapedthumbnail = 	""
        scrapedtitle = scrapertools.htmlclean(match[1])
        itemlist.append( Item(channel=__channel__, action="videos", extra="1", title=scrapedtitle, url=scrapedurl,  folder=True) )

    return itemlist
    
def videos(item):

    logger.info("[disneylatino.py] videos")
    itemlist = []
    page = int(item.extra)
    data = scrapertools.cachePage(item.url % page)
    if (data == ""):
        return itemlist
    
    logger.info(data)

    import json
    videos_json = json.loads(data)
    if videos_json == None : videos_json = []
    

    for video in videos_json['videos']:
        scrapedurl = video['id']
        scrapedthumbnail = video['thumbnail'].encode("utf8","ignore").replace('\\', '')
        scrapedtitle = scrapertools.htmlclean(video['title'].encode("utf8","ignore"))
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,  folder=False) )

    if (page < int(videos_json['pages'])):
        itemlist.append( Item(channel=__channel__, action="videos", extra= str(page + 1), title="!Pagina siguiente.", url=item.url,  folder=True) )        
    return itemlist
    
def play(item):

    logger.info("[disneylatino.py] play")
    itemlist = []

    data = scrapertools.cachePage("http://befsn.disneylatino.com/index.php/catalog/video.json?country=venezuela&id=" + item.url)
    if (data == ""):
        return itemlist
    
    logger.info(data)

    import json
    video = json.loads(data)
    if video == None :
        return itemlist

    scrapedurl = video['video_url'].encode("utf8","ignore").replace('\\','').replace('mp4:', '') + " swfURL=http://www.disneylatino.com/res/swf/dlVideoPlayer/VideoPlayer.swf swfvfy=true"
    scrapedthumbnail = 	video['thumbnail'].encode("utf8","ignore").replace('\\','')
    scrapedtitle = scrapertools.htmlclean(video['title'])
    itemlist.append( Item(channel=__channel__, action="play", server="directo", title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,  folder=False) )

    return itemlist
