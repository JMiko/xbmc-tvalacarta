# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para delatv
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
import config
import logger

CHANNELNAME = "delatv"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[delatv.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[cinegratis.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "novedades" , category , "Novedades" ,"http://delatv.com/","","")

	if config.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

	
def novedades(params,url,category):
	logger.info("[delatv.py] novedades")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#patron  = '<div class="thumb">[^<]+<a href="([^"]+)"><img src="([^"]+)".*?alt="([^"]+)"/></a>'
	patron  = '<div class="galleryitem">[^<]+'
	patron += '<h1>([^<]+)</h1>[^<]+'
	patron += '<a href="([^"]+)"><img src="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[0]
		scrapedurl = match[1]
		scrapedthumbnail = match[2].replace(" ","%20")
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "servidores" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae la página siguiente
	# ------------------------------------------------------
	#patron = '<a href="([^"]+)" >\&raquo\;</a>'
	patron  = 'class="current">[^<]+</span><a href="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "!Pagina siguiente"
		scrapedurl = match
		scrapedthumbnail = ""
		scrapeddescription = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "novedades" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def servidores(params,url,category):
	logger.info("[delatv.py] servidores")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# Descarga la página de detalle
	# http://delatv.com/sorority-row/
	data = scrapertools.cachePage(url)
	#logger.info(data)
	
	# Extrae el argumento
	patron = '<div class="sinopsis">.*?<li>(.*?)</li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = matches[0]

	# Extrae los enlaces a los vídeos (Megavídeo)
	patron = '<div class="servidores-titulo">Lista de servidores</div>(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	if len(matches)>0:
		data = matches[0]
		patron  = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
		matches = re.compile(patron,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		
		for match in matches:
			scrapedtitle = "[SERVIDOR] " + title + " - " + match[1]
			scrapedurl = match[0]
			scrapedthumbnail = thumbnail
			scrapedplot = plot
			xbmctools.addnewfolder( CHANNELNAME , "videos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videos(params,url,category):
	logger.info("[delatv.py] videos")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	data = scrapertools.cachePage(url)
	patron = '<div class="reproductor-contenido">(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	if len(matches)>0:
		data = matches[0]
		patron  = '<iframe src="([^"]+)"'
		matches = re.compile(patron,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)

		for match in matches:
			scrapedtitle = "[VIDEO] "+title
			scrapedurl = match
			scrapedthumbnail = thumbnail
			scrapedplot = plot
			if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "", scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	logger.info("[delatv.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = ""

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title , plot )

	# Busca los enlaces a los videos
	data = scrapertools.cachePage(url)
	listavideos = servertools.findvideos(data)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	if len(listavideos)>0:
		url = listavideos[0][1]
		server = listavideos[0][2]
		logger.info("url="+url)
		xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
	else:
		xbmctools.alertnodisponible()

