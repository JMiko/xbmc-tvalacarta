# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para vertelenovelasonline
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools

CHANNELNAME = "vertelenovelasonline"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[vertelenovelasonline.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[vertelenovelasonline.py] mainlist")

	# Menu principal
	xbmctools.addnewfolder( CHANNELNAME , "newlist" , CHANNELNAME , "Novedades" , "http://www.vertelenovelasonline.com/" , "", "" )
	
	# Si es un canal independiente, añade "Configuracion", "Descargas" y "Favoritos"
	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def newlist(params,url,category):
	xbmc.output("[vertelenovelasonline.py] listmirrors")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patron  = '<a onblur="[^"]+" href="([^"]+)"><img style="cursor:pointer; cursor:hand;width: 186px; height: 320px;" src="([^"]+)" border="0" alt=""id="BLOGGER_PHOTO[^>]+></a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1][44:-5]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listmirrors(params,url,category):
	xbmc.output("[vertelenovelasonline.py] listmirrors")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae la sinopsis
	patron  = "<div class='post-body entry-content'>.*?</div>"

	if len(matches)>0:

	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches)>0:
		plot = matches[0].strip()
		xbmc.output(plot)

	patron = '<div id="listanime"><a title="([^"]+)" href="([^"]+)"><strong>[^<]+</strong></a></div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[0]
		scrapedurl = urlparse.urljoin(url,match[1])
		scrapedthumbnail = thumbnail
		scrapedplot = plot
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[vertelenovelasonline.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	patron  = '<div id="listacapdd"><div class="listddserie">[^<]+'
	patron += '<a title="[^"]+" href="([^"]+)"><strong>[^<]+</strong></a>[^<]+'
	patron += '</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		url = matches[0]
		data = scrapertools.cachePage(url)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[vertelenovelasonline.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
