# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para InternautasTV
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

xbmc.output("[internautastv.py] init")

DEBUG = True
CHANNELNAME = "internautastv"
CHANNELCODE = "internautastv"

def mainlist(params,url,category):
	xbmc.output("[internautastv.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELCODE , "ultimosvideos"   , CHANNELNAME , "Últimos vídeos"     , "http://www.internautas.tv/backend/m4v.xml" , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "archivo"         , CHANNELNAME , "Archivo"            , "http://www.internautas.tv/" , "" , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def ultimosvideos(params,url,category):
	xbmc.output("[internautastv.py] ultimosvideos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Vídeos del RSS
	'''
	<item>
	<title>Polémicas declaraciones de Enrique Urbizu</title>
	<link>http://www.internautas.tv/programa/706.html</link>
	<description>No ha dejado a nadie indiferente las declaraciones del presidente de DAMA en la que le parece incluso que la polemica ley de los 3 avisos es insuficiente  </description>
	<enclosure url="http://serv2.internautas.tv/videos/m4v/20091229_1.m4v" type="video/m4v" />
	<pubDate>Tue, 29 Dec 2009 07:00:00 GMT</pubDate>
	<guid isPermaLink="true">http://www.internautas.tv/programa/706.html</guid>
	</item>
	'''
	patron  = '<item>[^<]+'
	patron += '<title>([^<]+)</title>[^<]+'
	patron += '<link>[^<]+</link>[^<]+'
	patron += '<description>([^<]+)</description>[^<]+'
	patron += '<enclosure url="([^"]+)" type="video/m4v" />[^<]+'
	patron += '<pubDate>([^<]+)</pubDate>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos del vídeo
		scrapedtitle = match[0].strip()+" ("+match[3].strip()+")"
		scrapedurl = urlparse.urljoin(url,match[2])
		scrapedthumbnail = ""
		scrapedplot = match[1].strip()
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , category , "Directo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def archivo(params,url,category):
	xbmc.output("[internautastv.py] archivo")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Busca la URL del archivo
	patron  = '<div class="barraopcion"><a href="([^"]+)">Archivo</a></div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches)>0:
		xbmctools.alerterrorpagina()
		return

	videosmes(params,matches[0],category)

def videosmes(params,url,category):
	xbmc.output("[internautastv.py] videosmes")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Busca la URL del archivo
	patron  = '<div class="ie"><a href="/programa/690.html" title="El Gobierno propondrá que la banda ancha sea servicio universal en toda Europa. El Partido Pirata quiere impulsar la Declaración de Derechos de Internet" alt=""><img src="http://www.internautas.tv/imagenes/20091201_1.jpg" alt="" width="80" /></a></div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos del vídeo
		scrapedtitle = match[0].strip()+" ("+match[3].strip()+")"
		scrapedurl = urlparse.urljoin(url,match[2])
		scrapedthumbnail = ""
		scrapedplot = match[1].strip()
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , category , "Directo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[internautastv.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	xbmctools.playvideo(CHANNELCODE,server,url,category,title,thumbnail,plot)
