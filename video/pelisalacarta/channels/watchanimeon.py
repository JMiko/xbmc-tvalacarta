# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para watchanimeon
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

CHANNELNAME = "watchanimeon"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[watchanimeon.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[watchanimeon.py] mainlist")

	# Menu principal
	xbmctools.addnewfolder( CHANNELNAME , "newlist"       , category , "Novedades"                   ,"http://www.watchanimeon.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "airinglist"    , category , "Series en curso"             ,"http://www.watchanimeon.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "catlist"       , category , "Series por categoría"        ,"http://www.watchanimeon.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "allserieslist" , category , "Todas las series"            ,"http://www.watchanimeon.com/anime-list/","","")
	xbmctools.addnewfolder( CHANNELNAME , "allmovieslist" , category , "Todas las películas"         ,"http://www.watchanimeon.com/anime/anime-movies/","","")

	# Si es un canal independiente, añade "Configuracion", "Descargas" y "Favoritos"
	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def newlist(params,url,category):
	xbmc.output("[watchanimeon.py] newlist")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las categorias
	patron = '<div class="newpostz"><div class="newposts"><img src="([^"]+)"[^>]+><li><a href="([^"]+)">([^<]+)</a></li><span><em>More Episodes.</em> <a href="([^"]+)">([^<]+)</a></span><span><em>Date Published </em>([^<]+)</span></div><div class="clear"></div></div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Las añade a XBMC
	for match in matches:
		scrapedtitle = match[2]+" ("+match[5]+")"
		scrapedurl = urlparse.urljoin(url,match[1])
		scrapedthumbnail = urlparse.urljoin(url,match[0])
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detallecapitulo" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def catlist(params,url,category):
	xbmc.output("[watchanimeon.py] catlist")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las categorias
	patron = '<a href="(\/\?genre[^"]+)">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Las añade a XBMC
	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detalleserie" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def airinglist(params,url,category):
	xbmc.output("[watchanimeon.py] catlist")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las categorias
	patron = '<div class="btm-sidebar">(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		data = matches[0]

	patron = '<li><span class="[^"]+">([^<]+)</span> <a href="([^"]+)">([^<]+)</a></li>'

	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Las añade a XBMC
	for match in matches:
		scrapedtitle = match[2].strip() + " ("+match[0]+")"
		scrapedurl = urlparse.urljoin(url,match[1])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detallecapitulo" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listsimple(params,url,category):
	xbmc.output("[watchanimeon.py] listsimple")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = "<a href='(index.php\?module\=player[^']+)'[^>]*>(.*?)</a>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
		scrapedtitle = scrapedtitle.replace("</span>","")
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listvideos(params,url,category):
	xbmc.output("[watchanimeon.py] listvideos")

	if url=="":
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
		scrapedplot = match[1]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos  = "<a href='[^']+'><u>[^<]+</u></a> <a href='([^']+)'>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listseries(params,url,category):
	xbmc.output("[watchanimeon.py] listvideos")

	if url=="":
		url = "http://www.cinegratis.net/index.php?module=peliculas"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = "<table width='785'[^>]+><tr><td[^>]+>([^<]+)<.*?"
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
		scrapedplot = match[1]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos  = "<a href='[^']+'><u>[^<]+</u></a> <a href='([^']+)'>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listseries" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[watchanimeon.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

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

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[watchanimeon.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
