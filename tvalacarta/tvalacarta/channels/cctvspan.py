# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cctvspan"
__category__ = "F"
__type__ = "generic"
__title__ = "cctvspan"
__language__ = "ES"
__creationdate__ = "20121130"
__vfanart__ = "http://espanol.cntv.cn/library/column/2010/11/24/C28600/style/img/map2.jpg"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cctvspan.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Arte Culinario Chino", action="videos", url="http://cctv.cntv.cn/lm/ArteCulinarioChino/video/index.shtml", thumbnail="http://p4.img.cctvpic.com/nettv/cctv/lm/ArteCulinarioChino/20121128/images/112511_1354093570266.jpg", fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="Mundo Insólito", action="videos", url="http://cctv.cntv.cn/lm/MundoInsolito/video/index.shtml", thumbnail="http://p3.img.cctvpic.com/nettv/cctv/lm/MundoInsolito/20121128/images/111805_1354091216387.jpg", fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Puntos de Vista", action="videos", url="http://cctv.cntv.cn/lm/PuntosdeVista/video/index.shtml", thumbnail="http://p4.img.cctvpic.com/nettv/xiyu/program/lanmeishidian/20110711/images/106127_1310370853022.jpg", fanart = __vfanart__))     itemlist.append( Item(channel=__channel__, title="Aprendiendo Chino", action="videos", url="http://cctv.cntv.cn/lm/ViajandoyAprendiendoChino/video/index.shtml", thumbnail="http://p4.img.cctvpic.com/nettv/cctv/lm/ViajandoyAprendiendoChino/20120302/images/101146_1330653020151.jpg", fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Así es China", action="videos", url="http://cctv.cntv.cn/lm/AsiesChina/video/index.shtml", thumbnail="http://p4.img.cctvpic.com/nettv/cctv/lm/AsiesChina/20121128/images/112181_1354091418296.jpg", fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Documental", action="videos", url="http://cctv.cntv.cn/lm/Documental/video/index.shtml", thumbnail="http://p2.img.cctvpic.com/nettv/cctv/lm/Documental/20121128/images/112456_1354093093102.jpg", fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Recorriendo China", action="videos", url="http://cctv.cntv.cn/lm/RecorriendoChina/video/index.shtml", thumbnail="http://p4.img.cctvpic.com/nettv/cctv/lm/RecorriendoChina/20121128/images/112475_1354093309250.jpg", fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Ronda Artística", action="videos", url="http://cctv.cntv.cn/lm/RondaArtistica/video/index.shtml", thumbnail="http://p3.img.cctvpic.com/nettv/cctv/lm/RondaArtistica/20121128/images/112527_1354093750845.jpg", fanart = __vfanart__))    itemlist.append( Item(channel=__channel__, title="Telenovela", action="videos", url="http://cctv.cntv.cn/lm/Telenovela/video/index.shtml", thumbnail="http://p3.img.cctvpic.com/nettv/cctv/lm/Telenovela/20121128/images/111776_1354091088259.jpg", fanart = __vfanart__)) 
 
    return itemlistdef videos(item):    logger.info("[cctvspan.py] videos")        # Descarga la pȧina    data = scrapertools.cachePage(item.url)	    #logger.info(data)    #=new title_array_01('Mundo Insólito 11/29/2012 Leyenda de los Naxi parte 1','http://espanol.cntv.cn/program/MundoInsolito/20121129/104390.shtml');    patron = '=new title_array_01\(\'(.*?)\',\'(.*?)\'\);'    matches = re.compile(patron,re.DOTALL).findall(data)    if DEBUG: scrapertools.printMatches(matches)	    itemlist = []    for match in matches:        scrapedtitle = scrapertools.htmlclean(match[0])        scrapedurl   = match[1]        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl ,  folder=False) )        return itemlist
def play(item):    logger.info("[cctvspan.py] play")        data = scrapertools.cachePage(item.url)	    #logger.info(data)        #fo.addVariable("videoCenterId","ee29f6db733d406092bf81fe22c85092");    # ver http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=ee29f6db733d406092bf81fe22c85092    patron = '"videoCenterId","(.*?)"'		    matches = re.compile(patron,re.DOTALL).findall(data)		    if DEBUG: scrapertools.printMatches(matches)		    if matches:         scrapedurl = "http://asp.v.cntv.cn/hls/"+matches[0]+"/main.m3u8"		    itemlist = []    itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=scrapedurl ,  folder=False) )    return itemlist