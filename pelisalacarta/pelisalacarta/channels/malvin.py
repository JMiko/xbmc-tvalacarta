# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para malvin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import string

from core import scrapertools
from core import logger
from core import config
from core.item import Item
from platformcode.xbmc import xbmctools
from pelisalacarta import buscador

from servers import servertools

import xbmc
import xbmcgui
import xbmcplugin

CHANNELNAME = "malvin"

# Esto permite su ejecución en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[malvin.py] init")

DEBUG = True

def mainlist(params,url,category):
    logger.info("[malvin.py] mainlist")

    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Estrenos" , "http://www.malvin.tv/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "lista" , CHANNELNAME , "Peliculas" , "http://www.malvin.tv/search/label/Online" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "lista" , CHANNELNAME , "Documentales" , "http://www.malvin.tv/search/label/Documentales" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "generos" , CHANNELNAME , "Generos" , "http://www.malvin.tv/" , "", "" )


    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def movielist(params,url,category):
	logger.info("[malvin.py] mainlist")
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	data = scrapertools.get_match( data , "<div class='widget-content'>(.*?)" + '<div style="text-align: center;">')

	#logger.info(data)
	
	# Extrae las entradas (carpetas)

	patronvideos  = '<div class="contenedor-img"[^<]+'
	patronvideos += '<a href="([^"]+)"[^<]+'
	patronvideos += '<img alt="[^"]+" class="[^"]+" src="([^"]+)"'
	#patronvideos += '="[^=]+'
	#patronvideos += '="([^"])"[^>]+'
	
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapedtitle = ""
	scrapedurl = ""
	scrapedthumbnail = ""
	
	for scrapedurl, scrapedthumbnail in matches:
        # Titulo
		cadenatitulo = scrapedurl.split('/')
		cadenatitulo = cadenatitulo[len(cadenatitulo)-1]
		longitud = len(cadenatitulo)
		scrapedtitle = cadenatitulo[:longitud-5]
		xbmc.log("movielist " + scrapedtitle)
		scrapedtitle = scrapedtitle.replace("-"," ")
        
        # procesa el resto
		scrapeddescription = ""

        # Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )

    # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
def lista(params,url,category):
	logger.info("[malvin.py] mainlist")
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.log("lista " + data)
	data = scrapertools.get_match( data , "<div class='blog-posts hfeed'>(.*?)<div class='blog-pager' id='blog-pager'>")

	#logger.info(data)
	
	# Extrae las entradas (carpetas)

	patronvideos  = "<h3 class='post-title entry-title'>[^<]+"
	patronvideos += "<a href='([^']+)' title='([^']+)'[^<]+</a>[^<]+"
	patronvideos += '</h3>[^<]+'
	patronvideos += '</div>[^<]+'
	patronvideos += "<div class='sentry'>(.*?)<noscript></noscript>"
	
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapedtitle = ""
	scrapedurl = ""
	scrapedthumbnail = ""
	
	for scrapedurl, scrapedtitle, bloque in matches:
        # procesa el resto
		scrapeddescription = ""
		scrapedthumbnail = scrapertools.get_match(bloque,'<img border="[^"]+" height="[^"]+" src="([^"]+)"')

        # Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )

	data = scrapertools.cachePage(url)
	#xbmc.log("lista " + data)
	scrapedurl = scrapertools.get_match( data , "<a class='blog-pager-older-link' href='(.*?)' id='")
	xbmc.log("lista " + scrapedurl)
	xbmctools.addthumbnailfolder( CHANNELNAME , "Pagina Siguiente >>" , scrapedurl , scrapedthumbnail, "lista" )
    # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
def generos(params,url,category):
	logger.info("[malvin.py] mainlist")
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	data = scrapertools.get_match( data , "<h2>Generos</h2>(.*?)" + "<div class='clear'>")

	#logger.info(data)
	#xbmc.log("generos " + data)
	
	# Extrae las entradas (carpetas)

	patronvideos  = "<li>[^<]+"
	patronvideos += "<a dir='ltr' href='([^']+)'>([^<]+)</a>"
	#patronvideos += '="[^=]+'
	#patronvideos += '="([^"])"[^>]+'
	
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapedtitle = ""
	scrapedurl = ""
	scrapedthumbnail = ""
	
	for scrapedurl, scrapedtitle in matches:        
        # procesa el resto
		scrapeddescription = ""

        # Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "lista" )

    # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
def categorias(params,url,category):
	logger.info("[malvin.py] mainlist")
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	data = scrapertools.get_match( data , "<h2>CATEGORIAS</h2>(.*?)" + "<div class='clear'>")

	#logger.info(data)
	#xbmc.log("generos " + data)
	
	# Extrae las entradas (carpetas)

	patronvideos  = "<li>[^<]+"
	patronvideos += "<a dir='ltr' href='([^']+)'>([^<]+)</a>"
	#patronvideos += '="[^=]+'
	#patronvideos += '="([^"])"[^>]+'
	
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapedtitle = "Video"
	scrapedurl = ""
	scrapedthumbnail = ""
	
	for scrapedurl, scrapedtitle in matches:        
        # procesa el resto
		scrapeddescription = ""

        # Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "lista" )

    # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def detail(params,url,category):
    logger.info("[malvin.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        xbmctools.addnewvideo( CHANNELNAME , "play" , category , video[2] , title + " - " + video[0] , video[1] , thumbnail , "" )
    # ------------------------------------------------------------------------------------

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[malvin.py] play")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )
    server = params["server"]

    xbmctools.play_video(CHANNELNAME,server,url,category,title,thumbnail,plot)

#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")
