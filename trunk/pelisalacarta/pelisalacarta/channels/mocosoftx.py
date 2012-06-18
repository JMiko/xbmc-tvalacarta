# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mocosoftx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "mocosoftx"
__category__ = "F"
__type__ = "generic"
__title__ = "MocosoftX"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

USER = config.get_setting("privateuser")
PASSWORD = config.get_setting("privatepassword")
LOGINURL = "http://mocosoftx.com/foro/login2/?user=" + USER + "&passwrd=" + PASSWORD + "&cookieneverexp=on&hash_passwrd="

MAIN_HEADERS = []
MAIN_HEADERS.append( ["Host","mocosoftx.com"] )
MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0) Gecko/20100101 Firefox/8.0"] )
MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )
MAIN_HEADERS.append( ["Accept-Language","es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"] )
MAIN_HEADERS.append( ["Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7"] )
MAIN_HEADERS.append( ["Connection","keep-alive"] )


def isGeneric():
    return True

def GetSessionID():
    # Descarga la página
    data = scrapertools.cache_page(LOGINURL,headers=MAIN_HEADERS)
    logger.info("data="+data)
    plogin = '<a href="([^"]+)">ingresa</a>'
    plogout = '<a href="http://mocosoftx.com/foro/logout/?([^"]+)"><span>'
    matches = re.compile(plogout,re.DOTALL).findall(data)
    
    if len(matches)>0:
        return str(matches[0])
    else:
        return ''

def mainlist(item):
    logger.info("[mocosoftx.py] mainlist")
    itemlist = []
    sid = GetSessionID()
    # Añade al listado de XBMC
    #xbmctools.addnewfolder( __channel__ , "Novedades" , category , "Novedades"            ,"http://mocosoftx.com/foro/index.php"+sid,"","")
    itemlist.append( Item( channel=__channel__ , title="Novedades" , action="Novedades" , url="http://mocosoftx.com/foro/index.php"+sid , folder=True ) )
    if sid=='':
        itemlist.append( Item( channel=__channel__ , title="Listado Completo" , action="FullList" , url="http://www.mocosoftx.com/foro/index.php?action=.xml;type=rss2;limit=500;board=14;sa=news" , folder=True ) )
    else:
        itemlist.append( Item( channel=__channel__ , title="Listado Completo" , action="FullList" , url="http://www.mocosoftx.com/foro/index.php"+sid+";action=.xml;type=rss2;limit=500;board=14;sa=news" , folder=True ) )
    
    return itemlist

def Novedades(item):
    logger.info("[mocosoftx.py] Novedades")
    itemlist = []
    # Descarga la página
    data = scrapertools.cache_page(item.url,headers=MAIN_HEADERS)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patron  = '<td class="sp_middle sp_regular_padding sp_fullwidth">'
    patron += '<a href="(http://mocosoftx.com/foro/peliculas-xxx-online-\(completas\)[^"]+)"'
    patron += '>([^<]+)</a>'
    patron += '.*?<img src="([^"]+)" alt=""'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        # if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        # Añade al listado de XBMC
        itemlist.append( Item( channel=__channel__ , title=scrapedtitle , action="detail" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )
    
    # Extrae la marca de siguiente página
    patronvideos = '\[<b>[^<]+</b>\] <a class="navPages" href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item( channel=__channel__ , title=scrapedtitle , action="Novedades" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )

    return itemlist
                                                                                          
def FullList(item):
    logger.info("[mocosoftx.py] FullList")
    itemlist = []
    url = item.url
    
    if url=="":
        url = "http://www.mocosoftx.com/foro/index.php?action=.xml;type=rss2;limit=500;board=14"
    
    # Descarga la página
    data = scrapertools.cache_page(url , headers=MAIN_HEADERS , timeout=30)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patron      = '<item>(.*?)</item>'
    matchesITEM = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matchesITEM[0])
    patronvideos = '<title>(.*?)</title>[^<]+<link>(.*?)</link>'
    #patronvideos += '<\!\[CDATA\[<a href="[^"]+" target="_blank"><img src="([^"]+)".*?'
    for match in matchesITEM:
        matches = re.compile(patronvideos,re.DOTALL).findall(match)
        scrapertools.printMatches(matches)
        
        for match2 in matches:
            scrapedtitle = match2[0]
            scrapedtitle = scrapedtitle.replace("<![CDATA[","")
            scrapedtitle = scrapedtitle.replace("]]>","")
            scrapedurl = match2[1]
            try:
                scrapedthumbnail = re.compile('<img src="(.+?)"').findall(match)[0]
            except:
                scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
            itemlist.append( Item( channel=__channel__ , title=scrapedtitle , action="detail" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )
    
    return itemlist

def detail(item):
    logger.info("[mocosoftx.py] detail")
    itemlist = []
    url = item.url
    title = urllib.unquote_plus( item.title )
    thumbnail = urllib.unquote_plus( item.thumbnail )
    #plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    if "CDATA" in url:
        data = url
        patronthumb = '<img src="([^"]+)"'
        matches = re.compile(patronthumb,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
    else:
        #Descarga la página
        sid = GetSessionID()
        data = scrapertools.cache_page(url+sid,headers=MAIN_HEADERS)
        patronthumb = '<img src="([^"]+)" alt="" border="0" />[</a>|<br />]+'
        matches = re.compile(patronthumb,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
    logger.info(data)
    #addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)
    c=0
    for video in listavideos:
        c=c+1
        try:
            imagen = matches[c]
        except:
            imagen = thumbnail
        itemlist.append( Item( channel=__channel__ , title=title+" - ["+video[2]+"]" , action="play" ,  server= video[2], url=video[1] ,thumbnail=imagen, plot=item.plot, folder=False ) )
    # ------------------------------------------------------------------------------------
    
    return itemlist

