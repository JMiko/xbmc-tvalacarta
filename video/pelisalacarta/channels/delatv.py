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

CHANNELNAME = "delatv"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[delatv.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[cinegratis.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "novedades" , category , "Novedades" ,"http://delatv.com/","","")

	if config.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

	
def novedades(params,url,category):
	xbmc.output("[delatv.py] novedades")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

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
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

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
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "novedades" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listmirrors(params,url,category):
	xbmc.output("[delatv.py] listmirrors")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# Descarga la página de detalle
	# http://delatv.com/sorority-row/
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# Extrae el argumento
	patron = '<div class="sinopsis">.*?<li>(.*?)</li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = matches[0]

	# Extrae los enlaces a los vídeos (Megavídeo)
	'''
	<div class="div-servidores">
	<div class="servidores-titulo">Lista de servidores</div>
	<div class="servidores-fondo">
	<div class="boton-ver-pelicula">         <a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMjU4LzI3Ny8xMDU1NTcwMzk0OTYwNjdfMjA5NzY=" target="_blank" class="boton-azul">Audio Latino - Parte 1</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMjM2LzY4NS8xMDU1NTcxNDYxNjI3MjNfMzQ5ODk=" target="_blank" class="boton-azul">Audio Latino - Parte 2</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMTU2LzcwLzEwNTU1NzE5NjE2MjcxOF8yOTA3MQ==" target="_blank" class="boton-azul">Audio Latino - Parte 3</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMTE4LzcxNi8xMDU1NTcyMzI4MjkzODFfMjI0OTM=" target="_blank" class="boton-azul">Audio Latino - Parte 4</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMzA4Lzk2Ni8xMDU1NTcyOTYxNjI3MDhfMzU3ODg=" target="_blank" class="boton-azul">Audio Latino - Parte 5</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMjE2LzE3NS8xMDU1Njg0NTk0OTQ5MjVfNDE5NDE=" target="_blank" class="boton-azul">Audio Latino - Parte 6</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMzA2LzgwNi8xMDU1NTc0OTYxNjI2ODhfNDcxNjc=" target="_blank" class="boton-azul">Audio Latino - Parte 7</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMzI4Lzc2MS8xNTE5MzAzMTAyNjkzXzk2NDA=" target="_blank" class="boton-rojo">Subtitulado - Parte 1</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMzI4LzY0MS8xNTE5MzAzMjIyNjk2XzQ4NzQw" target="_blank" class="boton-rojo">Subtitulado - Parte 2</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMzI4LzgyNC8xNTE5MzAzNDIyNzAxXzI1MjQ0" target="_blank" class="boton-rojo">Subtitulado - Parte 3</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1zbmM0LzMzMzI4Lzk4Ni8xNTE5MzAzNTAyNzAzXzUyMjQx" target="_blank" class="boton-rojo">Subtitulado - Parte 4</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMzI4LzEwLzE1MTkzMDM3NDI3MDlfNjI5MjU=" target="_blank" class="boton-rojo">Subtitulado - Parte 5</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMzI4LzQ3Ni8xNTE5MzA1MzQyNzQ5XzM2OQ==" target="_blank" class="boton-rojo">Subtitulado - Parte 6</a>
	<a href="http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMzI4LzUyLzE1MTkzMDU1MDI3NTNfNTAzNDk=" target="_blank" class="boton-rojo">Subtitulado - Parte 7</a>
	</div>
	'''

	patron = '<div class="servidores-titulo">Lista de servidores</div>(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	if len(matches)>0:
		data = matches[0]
		patron  = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
		matches = re.compile(patron,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		
		for match in matches:
			scrapedtitle = title + " - " + match[1]
			scrapedurl = match[0]
			scrapedthumbnail = thumbnail
			scrapedplot = plot
			xbmctools.addnewfolder( CHANNELNAME , "play" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[delatv.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title , plot )

	# Descarga la página del reproductor
	# http://delatv.com/modulos/player.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMjM2LzY4NS8xMDU1NTcxNDYxNjI3MjNfMzQ5ODk=
	# http://delatv.com/modulos/embed/playerembed.php?url=dmlkZW8uYWsuZmFjZWJvb2suY29tL2Nmcy1hay1hc2gyLzMzMjM2LzY4NS8xMDU1NTcxNDYxNjI3MjNfMzQ5ODk=
	url = url.split("?")[1]
	url = "http://delatv.com/modulos/embed/playerembed.php?"+url
	xbmc.output("[delatv.py] url="+url)
	data = scrapertools.cachePage(url)
	patron = 'player.swf\?file=([^\&]+)&'
	matches = re.compile(patron,re.DOTALL).findall(data)
	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	if len(matches)>0:
		url = matches[0]
		xbmc.output("url="+url)
		xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
	else:
		xbmctools.alertnodisponible()
