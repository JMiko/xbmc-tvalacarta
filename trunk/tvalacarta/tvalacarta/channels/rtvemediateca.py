# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Mediateca RTVE
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse, re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[rtvemediateca.py] init")

DEBUG = True
CHANNELNAME = "rtvemediateca"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtvemediateca.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Noticias"  , action="folderlist", extra="noticias" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Deportes"  , action="folderlist", extra="deportes" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Programas" , action="folderlist", extra="programas" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Archivo"   , action="folderlist", extra="archivo"  , folder=True) )

    return itemlist

def folderlist(item):
    logger.info("[rtvemediateca.py] folderlist")
    itemlist = []

    title = urllib.unquote_plus( params.get("title") )
    url = "http://www.rtve.es/mediateca/video/"+category+"/medialist.inc"

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae las carpetas (nivel 1)
    # --------------------------------------------------------
    #primer nivel
    #<li id="la-2-noticias" class="node-end"><a rel="nofollow" href="javascript://" onclick="loadVideos('noticias/la-2-noticias');" class="sup">La 2 Noticias</a></li>
    #<li id="informativos-territoriales" class="expandable"><span onclick="loadVideos('noticias/informativos-territoriales');" class="closed">Informativos territoriales</span><ul>
    #segundo nivel
    #<li id="informatiu-balear"><a rel="nofollow" href="javascript://" onclick="loadVideos('noticias/informativos-territoriales/informatiu-balear');" class="inf">Informatiu Balear</a></li>
    patron = '<li id="([^"]+)" class="([^"]+)"><.*?onclick="([^"]+)"[^>]*>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        try:
            scrapedtitle = unicode( match[3], "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = match[3]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)

        urlrelativa = match[2][12:-3]

        #scrapedurl = "http://www.rtve.es/mediateca/video/"+urlrelativa+"/pagines_ajax/pagina1.html"
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #addvideo( scrapedtitle , scrapedurl , category )
        if match[1]=="node-end":
            xbmctools.addnewfolder( CHANNELCODE , "videolist" , urlrelativa , scrapedtitle , "" , scrapedthumbnail, scrapedplot )
        elif match[1]=="expandable":
            xbmctools.addnewfolder( CHANNELCODE , "subfolderlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def subfolderlist(item):
    logger.info("[rtvemediateca.py] subfolderlist")
    itemlist = []

    title = urllib.unquote_plus( params.get("title") )

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage("http://www.rtve.es/mediateca/video/"+category+"/medialist.inc")
    #logger.info(data)

    # Localiza la categoria
    patron = '<li id="'+url+'" class="expandable"><span onclick="[^"]+" class="closed">[^<]+</span><ul>(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]

    # --------------------------------------------------------
    # Extrae las categorias (carpetas)
    # --------------------------------------------------------
    #primer nivel
    #<li id="la-2-noticias" class="node-end"><a rel="nofollow" href="javascript://" onclick="loadVideos('noticias/la-2-noticias');" class="sup">La 2 Noticias</a></li>
    #<li id="informativos-territoriales" class="expandable"><span onclick="loadVideos('noticias/informativos-territoriales');" class="closed">Informativos territoriales</span><ul>
    #segundo nivel
    #<li id="informatiu-balear"><a rel="nofollow" href="javascript://" onclick="loadVideos('noticias/informativos-territoriales/informatiu-balear');" class="inf">Informatiu Balear</a></li>
    patron = '<li id="([^"]+)"><.*?onclick="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        try:
            scrapedtitle = unicode( match[2], "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = match[2]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        urlrelativa = match[1][12:-3]

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #addvideo( scrapedtitle , scrapedurl , category )
        xbmctools.addnewfolder( CHANNELCODE , "videolist" , urlrelativa , scrapedtitle , "" , scrapedthumbnail, scrapedplot )

    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(item):
    logger.info("[rtvemediateca.py] videolist")
    itemlist = []

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    if url=="":
        url = "http://www.rtve.es/mediateca/video/"+category+"/pagines_ajax/pagina1.html"
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los videos
    # --------------------------------------------------------
    patron  = '<div class="vthumb">.*?<a.*?href="([^"]+)"><img src="[^>]+><img src="([^"]+)[^>]+>.*?<a.*?href=[^>]+>([^<]+)</a></h2><span class="hour">([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        try:
            scrapedtitle = unicode( match[2] + " (" + match[3] + ")", "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = match[2] + " (" + match[3] + ")"
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)

        scrapedurl = urlparse.urljoin(url,match[0])

        try:
            scrapedplot = unicode( match[2] , "utf-8" ).encode("iso-8859-1")
        except:
            scrapedplot = match[2]
        scrapedplot = scrapertools.entityunescape(scrapedplot)

        scrapedthumbnail = urlparse.urljoin(url,match[1])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewvideo( "rtve" , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # --------------------------------------------------------
    # Extrae los videos
    # --------------------------------------------------------
    patron  = '<a onclick="([^"]+)" href="javascript\:\/\/" rel="nofollow">Siguiente<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        #pagina('content_videos','2', '/mediateca/video/programas/series/aguila-roja')
        #http://www.rtve.es/mediateca/video/programas/series/aguila-roja/pagines_ajax/pagina1.html
        #http://www.rtve.es/mediateca/video/programas/series/aguila-roja/pagines_ajax/pagina2.html
        scrapedtitle = "Página siguiente"
        scrapedurl = "http://www.rtve.es"+matches[0][30:-2]+"/pagines_ajax/pagina"+matches[0][25:26]+".html"
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELCODE , "videolist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
