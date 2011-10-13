# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para discoverymx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools
#from pelisalacarta import buscador

CHANNELNAME = "discoverymx"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[discoverymx.py] mainlist")
    itemlist=[]
    
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Novedades"  , action="listvideos" , url="http://discoverymx.blogspot.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Series Disponibles"  , action="DocuSeries" , url="http://discoverymx.blogspot.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Tag"  , action="DocuTag" , url="http://discoverymx.blogspot.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Archivo por meses"  , action="DocuARCHIVO" , url="http://discoverymx.blogspot.com/"))

    return itemlist

def search(item):
    logger.info("[discoverymx.py] search")

    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            searchUrl = "http://discoverymx.blogspot.com/index.php?s="+tecleado
            SearchResult(params,searchUrl,category)
            
def SearchResult(item):
    logger.info("[discoverymx.py] SearchResult")
    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<p class="entry-title"><[^>]+>[^<]+</span><a href="([^"]+)"[^>]+>([^<]+)</a></p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedurl = match[0]
        
        scrapedtitle =match[1]
        scrapedtitle = scrapedtitle.replace("&#8211;","-")
        scrapedtitle = scrapedtitle.replace("&nbsp;"," ")
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Propiedades
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
        

def performsearch(texto):
    logger.info("[discoverymx.py] performsearch")
    url = "http://discoverymx.blogspot.com/index.php?s="+texto

    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<p class="entry-title"><[^>]+>[^<]+</span><a href="([^"]+)"[^>]+>([^<]+)</a></p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    resultados = []

    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = scrapedtitle.replace("&#8211;","-")
        scrapedtitle = scrapedtitle.replace("&nbsp;"," ")
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        resultados.append( [CHANNELNAME , "detail" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
        
    return resultados

def DocuSeries(item):
    logger.info("[discoverymx.py] DocuSeries")
    itemlist=[]
    
    # Descarga la p�gina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<li><b><a href="([^"]+)" target="_blank">([^<]+)</a></b></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedurl = match[0]
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def DocuTag(item):
    logger.info("[discoverymx.py] DocuSeries")
    itemlist=[]

    # Descarga la p�gina
    data = scrapertools.cache_page(item.url)
    patronvideos  =    "<a dir='ltr' href='([^']+)'>([^<]+)</a>[^<]+<span class='label-count' dir='ltr'>(.+?)</span>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedurl = match[0]
        scrapedtitle = match[1] + " " + match[2]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def DocuARCHIVO(item):
    logger.info("[discoverymx.py] DocuSeries")
    itemlist=[]

    # Descarga la p�gina
    data = scrapertools.cache_page(item.url)
    patronvideos = "<a class='post-count-link' href='([^']+)'>([^<]+)</a>[^<]+"
    patronvideos +=    "<span class='post-count' dir='ltr'>(.+?)</span>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedurl = match[0]
        scrapedtitle = match[1] + " " + match[2]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist
    
def DocuCat(item):
    logger.info("[discoverymx.py] peliscat")
    itemlist=[]

    # Descarga la p�gina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<li class="cat-item cat-item[^"]+"><a href="([^"]+)" title="[^"]+">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Propiedades
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listvideos(item):
    logger.info("[discoverymx.py] listvideos")
    itemlist=[]

    scrapedthumbnail = ""
    scrapedplot = ""

    # Descarga la p�gina
    data = scrapertools.cache_page(item.url)
    patronvideos  = "<h3 class='post-title entry-title'>[^<]+"
    patronvideos += "<a href='([^']+)'>([^<]+)</a>.*?"
    patronvideos += "<div class='post-body entry-content'>(.*?)<div class='post-footer'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = re.sub("<[^>]+>"," ",scrapedtitle)
        scrapedtitle = scrapertools.unescape(scrapedtitle)
        scrapedurl = match[0]
        regexp = re.compile(r'src="(http[^"]+)"')
        
        matchthumb = regexp.search(match[2])
        if matchthumb is not None:
            scrapedthumbnail = matchthumb.group(1)
        matchplot = re.compile('<div align="center">(<img.*?)</span></div>',re.DOTALL).findall(match[2])

        if len(matchplot)>0:
            scrapedplot = matchplot[0]
            #print matchplot
        else:
            scrapedplot = ""

        scrapedplot = re.sub("<[^>]+>"," ",scrapedplot)
        scrapedplot = scrapertools.unescape(scrapedplot)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        #xbmctools.addnewfolder( CHANNELNAME , "findevi" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae la marca de siguiente p�gina
    patronvideos = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P�gina siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[discoverymx.py] findvideos")
    itemlist=[]
    
    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Busca los enlaces a videos no megavideo (youtube)
    patronyoutube = '<a href="http\:\/\/www.youtube.com/watch\?v=[^=]+=PlayList\&amp\;p=(.+?)&[^"]+"'
    matchyoutube  = re.compile(patronyoutube,re.DOTALL).findall(data)
    if len(matchyoutube)>0:
        for match in matchyoutube:
            listyoutubeurl = 'http://www.youtube.com/view_play_list?p='+match
            data1 = scrapertools.cachePage(listyoutubeurl)
            newpatronyoutube = '<a href="(.*?)".*?<img src="(.*?)".*?alt="([^"]+)"'
            matchnewyoutube  = re.compile(newpatronyoutube,re.DOTALL).findall(data1)
            if len(matchnewyoutube)>0:
                for match2 in matchnewyoutube:
                    scrapedthumbnail = match2[1]
                    scrapedtitle     = match2[2]
                    scrapedurl       = match2[0]
                    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                    #xbmctools.addnewvideo( CHANNELNAME , "play" , category , "youtube" , scrapedtitle +" - "+"(youtube) ", scrapedurl , scrapedthumbnail , plot )
                    itemlist.append( Item(channel=CHANNELNAME, action="play", server="youtube", title=scrapedtitle+" [youtube]" , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

                logger.info(" lista de links encontrados U "+str(len(matchnewyoutube)))
    
    # Busca los enlaces a los videos
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        videotitle = scrapertools.unescape(video[0])
        url = video[1]
        server = video[2]
        #xbmctools.addnewvideo( CHANNELNAME , "play" , category , server ,  , url , thumbnail , plot )
        itemlist.append( Item(channel=CHANNELNAME, action="play", server=server, title=item.title.strip() + " - " + videotitle , url=url , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    return itemlist