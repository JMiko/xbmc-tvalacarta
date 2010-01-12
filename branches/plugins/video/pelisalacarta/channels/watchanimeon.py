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
	xbmctools.addnewfolder( CHANNELNAME , "newlist"         , category , "Novedades"                   ,"http://www.watchanimeon.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "airinglist"      , category , "Series en curso"             ,"http://www.watchanimeon.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "catlist"         , category , "Series por categoría"        ,"http://www.watchanimeon.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "alphaserieslist" , category , "Series por orden alfabético" ,"http://www.watchanimeon.com/anime-list/","","")
	xbmctools.addnewfolder( CHANNELNAME , "allmovieslist"   , category , "Todas las películas"         ,"http://www.watchanimeon.com/anime/anime-movies/","","")

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
	xbmc.output("[watchanimeon.py] airinglist")

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

def alphaserieslist(params,url,category):
	xbmc.output("[watchanimeon.py] alphaserieslist")

	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , ".",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "A",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "B",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "C",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "D",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "E",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "F",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "G",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "H",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "I",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "J",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "K",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "L",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "M",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "N",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "O",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "P",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "Q",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "R",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "S",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "T",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "U",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "V",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "W",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "X",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "Y",url,"","")
	xbmctools.addnewfolder( CHANNELNAME ,"singleletterserieslist", category , "Z",url,"","")

	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def singleletterserieslist(params,url,category):
	xbmc.output("[watchanimeon.py] singleletterserieslist")

	# El título es la letra elegida
	letra = urllib.unquote_plus( params.get("title") )

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae el bloque con las entradas correspondientes a esa letra
	patron = '<h3 class="postlist-title"><a name="'+letra+'"></a><p class="sep">'+letra+'</p></h3><ul class="postlist">(.*?)</ul>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		data = matches[0]

	# Ahora extrae las series
	patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
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

def allmovieslist(params,url,category):
	xbmc.output("[watchanimeon.py] allmovieslist")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae el bloque con las entradas correspondientes a esa letra
	patron = '<ul class="sip-list">(.*?)</ul>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		data = matches[0]

	# Ahora extrae las series
	patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Las añade a XBMC
	for match in matches:
		scrapedtitle = match[1].replace("&#8211;","-")
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detallecapitulo" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detalleserie(params,url,category):
	xbmc.output("[watchanimeon.py] detalleserie")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Argumento
	patron = '<div class="gen-info">(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		plot = matches[0].strip()
		plot = plot.replace("<p>","")
		plot = plot.replace("</p>","")
		plot = plot.replace("</span>","")
		plot = plot.replace("</a>","")
		plot = plot.replace("<br/>","")
		plot = plot.replace("<strong>","")
		plot = plot.replace("</strong>","")
		plot = plot.replace("</ul>","")
		plot = plot.replace("<li>","")
		plot = plot.replace("</li>","")

		plot = re.compile("<span[^>]*>",re.DOTALL).sub("",plot)
		plot = re.compile("<a[^>]*>",re.DOTALL).sub("",plot)
		plot = re.compile("<ul[^>]*>",re.DOTALL).sub("",plot)
		plot = plot.replace("\t","")

	# Thumbnail
	patron  = '<div class="sip-thumb">[^<]+'
	patron += '<img src="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		thumbnail = matches[0]

	# Episodios
                                            
    # Extrae el bloque con las entradas correspondientes a esa letra
	patron = '<ul class="sip-list">(.*?)</ul>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		data = matches[0]

	# Ahora extrae los episodios
	patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Las añade a XBMC
	for match in matches:
		scrapedtitle = match[1].replace("&#8211;","-")
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = thumbnail
		scrapedplot = plot
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detallecapitulo" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detallecapitulo(params,url,category):
	xbmc.output("[watchanimeon.py] detallecapitulo")

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

	# Extrae el enlace a la serie completa
	patron = '<a href="([^"]+)" title="View all posts in'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Las añade a XBMC
	for match in matches:
		scrapedtitle = "Ver serie completa"
		scrapedurl = urlparse.urljoin(url,match)
		scrapedthumbnail = thumbnail
		scrapedplot = plot
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detalleserie" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[watchanimeon.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
