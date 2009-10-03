# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinegratis
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

CHANNELNAME = "cinegratis"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[cinegratis.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[cinegratis.py] mainlist")

	url = "http://www.cinegratis.net/index.php?module=peliculas"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = "<table.*?<td.*?>([^<]+)<span class='style1'>\(Visto.*?"
	patronvideos += "<div align='justify'>(.*?)</div>.*?"
	patronvideos += "<a href='(.*?)'.*?"
	patronvideos += "<img src='(.*?)'"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[0]
		# URL
		scrapedurl = urlparse.urljoin(url,match[2])
		# Thumbnail
		scrapedthumbnail = urlparse.urljoin(url,match[3])
		# Argumento
		scrapeddescription = match[1]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[cinegratis.py] detail")

	title = params.get("title")
	thumbnail = params.get("thumbnail")
	xbmc.output("[cinegratis.py] title="+title)
	xbmc.output("[cinegratis.py] thumbnail="+thumbnail)

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		xbmctools.addvideo( CHANNELNAME , "Megavideo - "+video[0] , video[1] , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[cinegratis.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[cinegratis.py] thumbnail="+thumbnail)
	xbmc.output("[cinegratis.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")
