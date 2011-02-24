# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mocosoftx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
from servers import servertools

from core import scrapertools
from core import config
from core import logger
from core.item import Item

CHANNELNAME = "mocosoftx"
USER = config.get_setting("privateuser")
PASSWORD = config.get_setting("privatepassword")
LOGINURL = "http://mocosoftx.com/foro/login2/?user=" + USER + "&passwrd=" + PASSWORD + "&cookieneverexp=on&hash_passwrd="
DEBUG=True

def isGeneric():
    return True

def GetSessionID():
    # Descarga la página
    data = scrapertools.cachePage(LOGINURL)
    #logger.info(data)
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
    #xbmctools.addnewfolder( CHANNELNAME , "Novedades" , category , "Novedades"            ,"http://mocosoftx.com/foro/index.php"+sid,"","")
    itemlist.append( Item( channel=CHANNELNAME , title="Novedades" , action="Novedades" , url="http://mocosoftx.com/foro/index.php"+sid , folder=True ) )
    if sid=='':
        itemlist.append( Item( channel=CHANNELNAME , title="Listado Completo" , action="FullList" , url="http://www.mocosoftx.com/foro/index.php?action=.xml;type=rss2;limit=500;board=14" , folder=True ) )
    else:
        itemlist.append( Item( channel=CHANNELNAME , title="Listado Completo" , action="FullList" , url="http://www.mocosoftx.com/foro/index.php"+sid+";action=.xml;type=rss2;limit=500;board=14" , folder=True ) )
    
    return itemlist

def Novedades(item):
    logger.info("[mocosoftx.py] Novedades")
    itemlist = []
    # Descarga la página
    data = scrapertools.cachePage(item.url)
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
        itemlist.append( Item( channel=CHANNELNAME , title=scrapedtitle , action="detail" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )
    
    # Extrae la marca de siguiente página
    patronvideos = '\[<b>[^<]+</b>\] <a class="navPages" href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item( channel=CHANNELNAME , title=scrapedtitle , action="Novedades" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )

    return itemlist
                                                                                          
def FullList(item):
    logger.info("[mocosoftx.py] FullList")
    itemlist = []
    url = item.url
    
    if url=="":
        url = "http://www.mocosoftx.com/foro/index.php?action=.xml;type=rss2;limit=500;board=14"
    
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patron      = '<item>(.*?)</item>'
    matchesITEM = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matchesITEM[0])
    patronvideos = '<title>(.*?)</title>[^<]+<link>(.*?)</link>.*?'
    #patronvideos += '<\!\[CDATA\[<a href="[^"]+" target="_blank"><img src="([^"]+)".*?'
    for match in matchesITEM:
        matches = re.compile(patronvideos,re.DOTALL).findall(match)
        #print len(matches)
        scrapertools.printMatches(matches)
        
        for match2 in matches:
            scrapedtitle = match2[0]
            scrapedtitle = scrapedtitle.replace("<![CDATA[","")
            scrapedtitle = scrapedtitle.replace("]]>","")
            scrapedurl = match
            scrapedthumbnail = match2[1]
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
            itemlist.append( Item( channel=CHANNELNAME , title=scrapedtitle , action="detail" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )
    
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
        data = scrapertools.cachePage(url+sid)
        patronthumb = '<img src="([^"]+)" alt="" border="0" />[</a>|<br />]+'
        matches = re.compile(patronthumb,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
    #logger.info(data)
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
        itemlist.append( Item( channel=CHANNELNAME , title=title+" - ["+video[2]+"]" , action="play" ,  server= video[2], url=video[1] , plot=item.plot, folder=True ) )
    # ------------------------------------------------------------------------------------
    
    return itemlist

