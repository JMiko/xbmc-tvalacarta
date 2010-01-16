# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mcanime
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
import time
import xbmctools

CHANNELNAME = "mcanime"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[mcanime.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[mcanime.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "home"       , category , "Novedades"                             ,"http://www.mcanime.net/","","")
	xbmctools.addnewfolder( CHANNELNAME , "onlineforum", category , "Foro anime en línea"                   ,"http://www.mcanime.net/foro/viewforum.php?f=113","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddnovedades", category , "Descarga directa - Novedades"          ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddalpha"    , category , "Descarga directa - Listado alfabético" ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddcat"      , category , "Descarga directa - Categorías"         ,"http://www.mcanime.net/descarga_directa/anime","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def home(params,url,category):
	xbmc.output("[cine15.py] listvideos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="release" style="background-image.url\(\'([^\']+)\'\)\;">[^<]+'
	patronvideos += '<h4>([^<]+)<a href="([^"]+)">([^<]+)</a> <span class="date">([^<]+)</span></h4>[^<]+'
	patronvideos += '<div class="rimg"><img src="([^"]+)"[^>]+></div>[^<]+'
	patronvideos += '<div class="rtext">(.*?)</div>[^<]+'
	patronvideos += '<div class="rfinfo">(.*?)</div>[^<]+'
	patronvideos += '<div class="rflinks">(.*?)</div>[^<]+'
	patronvideos += '<div class="rinfo">(.*?)</div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		if match[0].endswith("anime.gif"):
			scrapedtitle = match[3].strip() + " " + match[1].strip() + " (" + match[4] + ")"
			scrapedurl = urlparse.urljoin(url,match[2])
			scrapedthumbnail = urlparse.urljoin(url,match[5])
			scrapedplot = scrapertools.htmlclean(match[6])
			if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

			# Añade al listado de XBMC
			xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos = '<span class="next"><a href="([^"]+)">Anteriores</a>...</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "home" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddalpha(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="(/descarga_directa/anime/lista/[^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddnovedades(params,url,category):
	xbmc.output("[mcanime.py] ddnovedades")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="(/descarga_directa/anime/lista/[^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddcat(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="(/descarga_directa/anime/genero/[^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def onlineforum(params,url,category):
	xbmc.output("[mcanime.py] novedades")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------------------
	# Extrae las entradas del foro (series / pelis)
	# --------------------------------------------------------------------
	patronvideos  = '<ul class="topic_row">[^<]+<li class="topic_type"><img.*?'
	patronvideos += '<li class="topic_title"><h5><a href="([^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Extrae
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0].replace("&amp;","&"))
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		xbmctools.logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# --------------------------------------------------------------------
	# Extrae la siguiente página
	# --------------------------------------------------------------------
	patronvideos  = '<a href="([^"]+)" class="next">(Siguiente &raquo;)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,match[0].replace("&amp;","&"))
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		xbmctools.logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot)
		
		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "mainlist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


def detail(params,url,category):
	xbmc.output("[mcanime.py] detail")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, paginas, o capítulos de las series...
	# ------------------------------------------------------------------------------------
	patronvideos  = '([^"]+)" class="next">Siguiente'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	for match in matches:
		xbmc.output("Encontrada pagina siguiente")
		addfolder("Pagina siguiente",urlparse.urljoin(url,match).replace("&amp;","&"),"list")

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	# Saca el cuerpo del post
	#logFile.info("data="+data)
	#patronvideos  = '<div class="content">.*?<div class="poster">.*?</div>(.*?)</div>'
	patronvideos  = '<div class="content">(.*?)<div class="content">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	datapost=""
	if len(matches)>0:
		datapost=matches[0]
	else:
		datapost = ""
	#logFile.info("dataPost="+dataPost)

	# Saca el thumbnail
	patronvideos  = '<img src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(datapost)
	thumbnailurl=""
	xbmc.output("thumbnails")
	for match in matches:
		xbmc.output(match)
	if len(matches)>0:
		thumbnailurl=matches[0]

	patronvideos  = '<img.*?>(.*?)<a'
	matches = re.compile(patronvideos,re.DOTALL).findall(datapost)
	descripcion = ""
	if len(matches)>0:
		descripcion = matches[0]
		descripcion = descripcion.replace("<br />","")
		descripcion = descripcion.replace("<br/>","")
		descripcion = descripcion.replace("\r","")
		descripcion = descripcion.replace("\n"," ")
		descripcion = re.sub("<[^>]+>"," ",descripcion)
	xbmc.output("descripcion="+descripcion)
	
	listavideos = servertools.findvideos(datapost)
	
	for video in listavideos:
		titulo = descripcion = re.sub("<[^>]+>","",video[0])
		addthumbnailvideo( titulo , video[1] , thumbnailurl , descripcion , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[mcanime.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[mcanime.py] thumbnail="+thumbnail)
	xbmc.output("[mcanime.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def addfolder(nombre,url,accion):
	xbmc.output('[mcanime.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	listitem.setInfo( "video", { "Title" : nombre, "Date" : str(int(time.clock()*100000000)) } )
	itemurl = '%s?channel=mcanime&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[mcanime.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	listitem.setInfo( "video", { "Title" : nombre, "Date" : str(int(time.clock()*100000000)) } )
	itemurl = '%s?channel=mcanime&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category,server):
	xbmc.output('[mcanime.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=mcanime&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , url , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailvideo(nombre,url,thumbnail,descripcion,category,server):
	xbmc.output('[mcanime.py] addvideo( "'+nombre+'" , "' + url + '" , "'+thumbnail+'" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : descripcion } )
	itemurl = '%s?channel=mcanime&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , url , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)
