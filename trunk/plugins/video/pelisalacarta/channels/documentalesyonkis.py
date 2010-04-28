# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documentalesyonkis
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
import DecryptYonkis as Yonkis

CHANNELNAME = "documentalesyonkis"

#xbmc.executebuiltin("Container.SetViewMode(57)")  #57=DVD Thumbs
#xbmc.executebuiltin("Container.SetViewMode(50)")  #50=full list
#xbmc.executebuiltin("Container.SetViewMode(51)")  #51=list
#xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons
#xbmc.executebuiltin("Container.SetViewMode(54)")  #54=wide icons

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[documentalesyonkis.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[documentalesyonkis.py] mainlist")

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(50)") #full list

	xbmctools.addnewfolder( CHANNELNAME , "lastvideolist" , category , "Últimos documentales","http://documentales.videosyonkis.com/ultimos-videos.php","","")
	xbmctools.addnewfolder( CHANNELNAME , "allvideolist"  , category , "Listado completo","http://documentales.videosyonkis.com/lista-videos.php","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def lastvideolist(params,url,category):
	xbmc.output("[documentalesyonkis.py] lastvideolist")
	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<td><a href="([^"]+)" title="([^"]+)"><img.*?src=\'([^\']+)\'[^>]+>.*?</td>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def allvideolist(params,url,category):
	xbmc.output("[documentalesyonkis.py] allvideolist")
	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<li> <a href="([^"]+)" title="([^"]+)"><img.*?src=\"([^\"]+)\"[^>]+\/>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
	xbmc.output("[documentalesyonkis.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	data = scrapertools.cachePage(url)
	patroniframe = '<iframe src="(http:\/\/documentales\.videosyonkis\.com.*?id=(.*?))" onLoad.*'
	matches = re.compile(patroniframe,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)
	
	if(len(matches)>0):
		id = matches[0][1]
		xbmc.output("[documentalesyonkis.py] detail id="+id)
		if "&" in id:
			ids = id.split("&")
			id = ids[0]
		dec = Yonkis.DecryptYonkis()
		id = dec.decryptALT(dec.unescape(id))
		xbmc.output("[documentalesyonkis.py] detail id="+id)
		url=id
	else:
		xbmctools.alertnodisponible()
		return
	
	xbmctools.playvideo(CHANNELNAME,"Megavideo",url,category,title,thumbnail,plot)
	# ------------------------------------------------------------------------------------
