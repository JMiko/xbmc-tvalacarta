# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para sesionvip
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

CHANNELNAME = "sesionvip"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[sesionvip.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[sesionvip.py] mainlist")

	if url=="":
		url = "http://www.sesionvip.com/"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="entry">.*?'
	patronvideos += '<a href="([^"]+)" rel="bookmark">([^<]+)</a>.*?'
	patronvideos += '<img.*?src="([^"]+)".*?'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		if scrapedtitle.startswith("Ver"):
			if scrapedtitle.startswith("Ver Gratis La Pelicula "):
				scrapedtitle = scrapedtitle[23:]
			elif scrapedtitle.startswith("Ver Online La Pelicula "):
				scrapedtitle = scrapedtitle[23:]
			# URL
			scrapedurl = urlparse.urljoin(url,match[0])
			# Thumbnail
			scrapedthumbnail = urlparse.urljoin(url,match[2])
			# Argumento
			scrapedplot = ""

			# Depuracion
			if (DEBUG):
				xbmc.output("scrapedtitle="+scrapedtitle)
				xbmc.output("scrapedurl="+scrapedurl)
				xbmc.output("scrapedthumbnail="+scrapedthumbnail)

			# Añade al listado de XBMC
			xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listmirrors" )

	# Página siguiente
	patronvideos  = '<div class="back"><a href="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = "Página siguiente"
		# URL
		scrapedurl = urlparse.urljoin(url,match)
		# Thumbnail
		scrapedthumbnail = ""
		# Argumento
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "mainlist" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listmirrors(params,url,category):
	xbmc.output("[sesionvip.py] detail")

	title = params.get("title")
	thumbnail = params.get("thumbnail")
	xbmc.output("[sesionvip.py] title="+title)
	xbmc.output("[sesionvip.py] thumbnail="+thumbnail)

	# Descarga la página y extrae el enlace a la siguiente pagina
	data = scrapertools.cachePage(url)
	patronvideos  = '<p style="text-align: center;">.*?<a href\="(http\://www.sesionvip.com/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	#xbmc.output(data)

	if len(matches)==0:
		xbmctools.alertnodisponible()
		return

	# Descarga la siguiente página y extrae el enlace a los mirrors
	url = matches[0]
	data = scrapertools.cachePage(url)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		xbmctools.addvideo( CHANNELNAME , video[0] , video[1] , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[sesionvip.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[sesionvip.py] thumbnail="+thumbnail)
	xbmc.output("[sesionvip.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
