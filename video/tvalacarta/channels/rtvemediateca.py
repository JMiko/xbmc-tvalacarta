# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Mediateca RTVE
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import binascii
import xbmctools

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[rtvemediateca.py] init")

DEBUG = False
CHANNELNAME = "Mediateca TVE"
CHANNELCODE = "rtvemediateca"

def mainlist(params,url,category):
	xbmc.output("[rtvemediateca.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Noticias" , "http://www.rtve.es/mediateca/video/noticias/medialist.inc"  , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Deportes" , "http://www.rtve.es/mediateca/video/deportes/medialist.inc"  , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Programas", "http://www.rtve.es/mediateca/video/programas/medialist.inc" , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Archivo"  , "http://www.rtve.es/mediateca/video/archivo/medialist.inc"   , "" , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[rtvemediateca.py] videolist")

	title = urllib.unquote_plus( params.get("title") )

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae las categorias (carpetas)
	# --------------------------------------------------------
	patron = '<a rel="nofollow" href="javascript\://" onclick="loadVideos\(\'([^\']+)\'\);" class="inf">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		
		scrapedurl = "http://www.rtve.es/mediateca/video/"+match[0]+"/pagines_ajax/pagina1.html"
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# --------------------------------------------------------
	# Extrae los videos de la página actual
	# --------------------------------------------------------
	patron  = '<div class="vthumb">.*?<a.*?href="([^"]+)"><img src="[^>]+><img src="([^"]+)[^>]+>.*?<a.*?href=[^>]+>([^<]+)</a></h2><span class="hour">([^<]+)</span>'
	matches = re.compile(patron,re.DOTALL).findall(data)

	if DEBUG:
		scrapertools.printMatches(matches)

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

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# --------------------------------------------------------
	# Extrae los videos de la página actual
	# --------------------------------------------------------
	if url.endswith("pagina1.html"):
		xbmc.output("Añade nueva página")
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Página 2" , url.replace("pagina1","pagina2") , "", "" )

	if url.endswith("pagina2.html"):
		xbmc.output("Añade nueva página")
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Página 3" , url.replace("pagina2","pagina3") , "", "" )

	if url.endswith("pagina3.html"):
		xbmc.output("Añade nueva página")
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Página 4" , url.replace("pagina3","pagina4") , "", "" )

	if url.endswith("pagina4.html"):
		xbmc.output("Añade nueva página")
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Página 5" , url.replace("pagina4","pagina5") , "", "" )

	if url.endswith("pagina5.html"):
		xbmc.output("Añade nueva página")
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Página 6" , url.replace("pagina5","pagina6") , "", "" )

	if url.endswith("pagina6.html"):
		xbmc.output("Añade nueva página")
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Página 7" , url.replace("pagina6","pagina7") , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[rtvemediateca.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del vídeo...', title )

	# --------------------------------------------------------
	# Descarga XML con el descriptor del vídeo
	# --------------------------------------------------------
	# Extrae el código
	xbmc.output("[rtvemediateca.py] url=#"+url+"#")
	patron = 'http://.*?/([0-9]+).shtml'
	data = url
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	codigo = matches[0]
	
	# Compone la URL
	url = 'http://www.rtve.es/swf/data/es/videos/video/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
	xbmc.output("[rtvemediateca.py] url=#"+url+"#")
	
	data = scrapertools.cachePage(url)
	patron = '<file>(.*?)</file>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	url = matches[0]
	xbmc.output("[rtvemediateca.py] url=#"+url+"#")

	# Cierra dialogo
	dialogWait.close()
	del dialogWait
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
