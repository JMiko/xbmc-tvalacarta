# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yotix
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

CHANNELNAME = "yotix"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[yotix.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[yotix.py] mainlist")

	#53=wall
	#xbmc.executebuiltin("Container.SetViewMode(53)")

	if url=='':
		url = "http://yotix.tv/"

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#patron  = '<div class="item">[^<]+'
	#patron += '<div class="background"></div>[^<]+'
	#patron += '<div class="content">[^<]+'
	#patron += '<a href="([^"]+)"><h1>([^<]+)</h1></a>.*?'
	#patron += '<img src="([^"]+)"/>'
	patron  = '<div class="galleryitem">[^<]+'
	patron += '<a title="[^"]+" rel="[^"]+" href="[^"]+">[^<]+'
	patron += '<img alt="[^"]+" src="([^"]+)" style="[^"]+"/>[^<]+'
	patron += '</a>[^<]+'
	patron += '<h3><a title="[^"]+" rel="[^"]+" href="([^"]+)">([^<]+)</a></h3>[^<]+'
	patron += '</div>'

	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[2]
		scrapedurl = match[1]
		scrapedthumbnail = match[0]
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae la página siguiente
	# ------------------------------------------------------
	patron = '<a href="([^"]+)" >&raquo;</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = match
		scrapedthumbnail = ""
		scrapeddescription = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "mainlist" )


	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listmirrors(params,url,category):
	xbmc.output("[yotix.py] listmirrors")

	#50=full list
	#xbmc.executebuiltin("Container.SetViewMode(50)")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página de detalle
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# Extrae el argumento
	patronvideos  = '<div class="postcontent">.*?<p>(.*?)</p>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = matches[0]

	# Extrae los enlaces a los vídeos (Megavídeo)
	patronvideos  = '<a.*?href="(http://yotix.tv/flash/[^"]+)"[^>]*>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)		

	for match in matches:
		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Megavideo" , match[1] , match[0] , thumbnail , plot )

	# Extrae los enlaces a los vídeos (Directo)
	extraevideos('<a.*?href="(http://yotix.tv/sitio/[^"]+)"[^>]*>([^<]+)</a>',data,category,thumbnail,plot)
	extraevideos('<a.*?href="(http://yotix.tv/media/[^"]+)"[^>]*>([^<]+)</a>',data,category,thumbnail,plot)
	extraevideos('<a.*?href="(http://yotix.tv/video/[^"]+)"[^>]*>([^<]+)</a>',data,category,thumbnail,plot)
	extraevideos('<a.*?href="(http://yotix.tv/ver/[^"]+)"[^>]*>([^<]+)</a>',data,category,thumbnail,plot)
	extraevideos('<a.*?href="(http://yotix.tv/rt/[^"]+)"[^>]*>([^<]+)</a>',data,category,thumbnail,plot)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def extraevideos(patronvideos,data,category,thumbnail,plot):
	xbmc.output("patron="+patronvideos)
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)		

	for match in matches:
		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , match[1] , match[0] , thumbnail , plot )

def play(params,url,category):
	xbmc.output("[yotix.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	server = urllib.unquote_plus( params.get("server") )

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title , plot )

	if server=="Directo":
		# Descarga la página del reproductor
		# http://yotix.com/flash/UPY6KEB4/cleaner.html
		xbmc.output("url="+url)
		data = scrapertools.cachePage(url)

		patron = 'so.addParam\(\'flashvars\',\'\&file\=([^\&]+)\&'
		matches = re.compile(patron,re.DOTALL).findall(data)
		if len(matches)>0:
			url = matches[0]
	else:
		patron = 'http://yotix.tv/flash/([^\/]+)/'
		matches = re.compile(patron,re.DOTALL).findall(url)
		if len(matches)>0:
			url = matches[0]

	xbmc.output("url="+url)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
