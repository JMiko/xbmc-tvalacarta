# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para kochikame
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
import megaupload
import binascii
import xbmctools

CHANNELNAME = "kochikame"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[kochikame.py] init")

DEBUG = True

Generate = False # poner a true para generar listas de peliculas

LoadThumbnails = False # indica si cargar los carteles

def mainlist(params,url,category):
	xbmc.output("[kochikame.py] mainlist")

	url = "http://www.astroteamrg.org/foro/index.php?showtopic=15845"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae los enlaces a los vídeos - Megaupload - Vídeos con título
	patronvideos  = '<a href\="http\:\/\/www.megaupload.com/\?d\=([^"]+)".*?>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		titulo = match[1]
		if titulo[0:3] == "Cap":
			     titulo = titulo[9:]
		url = match[0]
		if url == "3P78ET7H":
		     titulo = "012 - "+titulo
		if url == "99D5HEEY":
		     url = ""
		if titulo[0:3] == "000":
	             url = ""
                titulo = titulo.replace('&#33;' , '!')
		titulo = "Kochikame - "+titulo+" - [Megaupload] - by friki100"
		plot = "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=15845 por friki100. Colaboradores: elisa_chan, friki100, kouta-kun & sunnyghiba"
		
		# Añade al listado de XBMC 
		if url <> "":
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Megaupload" , titulo , url , "" , plot )
			
	# Extrae la fecha de la próxima actualización
	patronvideos  = '<span style="font-size:12pt;line-height:(100)%"><!--/sizeo-->(.*?)<!--sizec-->'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		titulo = match[1]
		url = "UPFO7JTH"
		# Añade al listado de XBMC 
		xbmctools.addvideo( CHANNELNAME , titulo , url , category , "Megaupload" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
			

def play(params,url,category):
	xbmc.output("[kochikame.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]	
	xbmc.output("[kochikame.py] thumbnail="+thumbnail)
	xbmc.output("[kochikame.py] server="+server)

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)