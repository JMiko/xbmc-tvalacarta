# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para capitancinema
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse
import urllib2
import urllib
import re
import os
import sys
import binascii

import xbmc
import xbmcgui
import xbmcplugin

import xbmctools
import scrapertools
import servertools
import linkbucks

CHANNELNAME = "capitancinema"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[capitancinema.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[capitancinema.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "novedades" , category , "Pel�culas - Novedades"            ,"http://www.capitancinema.com/peliculas-online-novedades.htm","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def novedades(params,url,category):
	xbmc.output("[capitancinema.py] novedades")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<td width="23\%"><a href="([^"]+)"[^>]+><img style="[^"]+" src="([^"]+)" border="0" alt="([^"]+)"[^>]+></a></td>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[2]
		scrapedtitle = scrapedtitle.replace("&quot;","")
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedplot = ""

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "mirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def mirrors(params,url,category):
	xbmc.output("[capitancinema.py] mirrors")

	title = urllib.unquote_plus( params.get("title") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<li>([^<]+)<a href="(http://[^\.]+\.linkbucks\.com)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[0].strip()[:-1]
		scrapedurl = match[1]
		scrapedthumbnail = ""
		scrapedplot = ""

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detalle" , title , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detalle(params,url,category):
	xbmc.output("[capitancinema.py] detalle")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	xbmc.output("url=["+url+"]")
	url = linkbucks.geturl(url)
	xbmc.output("url=["+url+"]")
	#xbmc.output(data)

	if url.startswith("http://www.metadivx.com"):
		xbmctools.addnewvideo( CHANNELNAME , "play" , "cine" , "metadivx" , category +" [metadivx]", url , thumbnail , plot )
	if url.startswith("http://www.divxlink.com"):
		xbmctools.addnewvideo( CHANNELNAME , "play" , "cine" , "divxlink" , category +" [divxlink]", url , thumbnail , plot )
	if url.startswith("http://www.divxden.com"):
		xbmctools.addnewvideo( CHANNELNAME , "play" , "cine" , "divxden" , category +" [divxden]", url , thumbnail , plot )
	if url.startswith("http://stagevu.com"):
		xbmctools.addnewvideo( CHANNELNAME , "play" , "cine" , "Stagevu" , category +" [stagevu]", url , thumbnail , plot )
	if url.startswith("http://www.megavideo.com"):
		xbmctools.addnewvideo( CHANNELNAME , "play" , "cine" , "Megavideo" , category +" [megavideo]", url , thumbnail , plot )
	if url.startswith("http://www.megaupload.com"):
		xbmctools.addnewvideo( CHANNELNAME , "play" , "cine" , "Megaupload" , category +" [megaupload]", url , thumbnail , plot )

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	'''
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	'''
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[capitancinema.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
