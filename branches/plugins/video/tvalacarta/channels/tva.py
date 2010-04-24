# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para tva
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

xbmc.output("[tva.py] init")

DEBUG = True
CHANNELNAME = "TV Azteca"
CHANNELCODE = "tva"

def mainlist(params,url,category):
	xbmc.output("[tva.py] mainlist")

	url = "http://www.tvazteca.com/barraprogramacion/index"

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae las categorias (carpetas)
	# --------------------------------------------------------
	#patron = '<li><span><a href="(secciones.asp[^"]+)">([^<]+)<'   url=\'([^\']+)\'/>'
	
	#http://www.tvazteca.com/capitulos
	
	patron = '<a class="aproghover" href="/([^"]+)"></a>' 
	
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		xbmc.output(match)
		scrapedtitle = match
		scrapedurl = "http://www.tvazteca.com/capitulos/" + match + "/index"
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		#addnewfolder( canal , accion , category , title , url , thumbnail , plot ):
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[tva.py] videolist")

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los videos
	# --------------------------------------------------------
	#patron = '<div class="texto">.*?<a href="([^"]+)">([^<]+)(.*?)</div>.*?<img src="([^"]+)"'
	titulo = params.get("title")
	xbmc.output(titulo)
	patron='<a href="/capitulos/' + titulo + '/([^"]+)"'
	#patron='<a href="/capitulos/a-cada-quien-su-santo([^"]+)"' 
	xbmc.output(patron)
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		xbmc.output(match)
		scrapedtitle = match
		# TODO: Sacar la fecha de la descripcion
		#patronfechas = "<p>Emissi&oacute;: ([^<]+)<"
		#matchesfechas = re.compile(patronfechas,re.DOTALL).findall(match[2])
		#if len(matchesfechas)>0:
		#	scrapedtitle = scrapedtitle + " (" + matchesfechas[0] + ")"

		scrapedurl = 'http://www.tvazteca.com/capitulos/' + titulo + "/" + match
		scrapedthumbnail =""
		#scrapedthumbnail = urlparse.urljoin(url,match[3]).replace(" ","%20")
		
		scrapedplot = ""
		#scrapedplot = "%s" % match[2]
		#scrapedplot = scrapedplot.strip()
		#scrapedplot = scrapedplot.replace("</a>","")
		#scrapedplot = scrapedplot.replace("</p>","")
		#scrapedplot = scrapedplot.replace("<p>","")
		#scrapedplot = scrapertools.entityunescape(scrapedplot)

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		#addnewfolder( canal , accion , category , title , url , thumbnail , plot ):
		xbmctools.addnewfolder( CHANNELCODE , "videolist2" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
def videolist2(params,url,category):
	xbmc.output("[tva.py] videolist2")

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los videos
	# --------------------------------------------------------
	#patron = '<div class="texto">.*?<a href="([^"]+)">([^<]+)(.*?)</div>.*?<img src="([^"]+)"'
	titulo = params.get("title")
	patron='urlToPlay=([^"]+)\'>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		xbmc.output(match)
		scrapedtitle = scrapertools.entityunescape(match)
		# TODO: Sacar la fecha de la descripcion
		#patronfechas = "<p>Emissi&oacute;: ([^<]+)<"
		#matchesfechas = re.compile(patronfechas,re.DOTALL).findall(match[2])
		#if len(matchesfechas)>0:
		#	scrapedtitle = scrapedtitle + " (" + matchesfechas[0] + ")"

		scrapedurl = match
		scrapedthumbnail = ""
		scrapedplot = ""
		
		#scrapedplot = "%s" % match[2]
		#scrapedplot = scrapedplot.strip()
		#scrapedplot = scrapedplot.replace("</a>","")
		#scrapedplot = scrapedplot.replace("</p>","")
		#scrapedplot = scrapedplot.replace("<p>","")
		#scrapedplot = scrapertools.entityunescape(scrapedplot)

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )	

def play2(params,url,category):
	xbmc.output("[tva.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[tva.py] thumbnail="+thumbnail)

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del v�deo...', title )

	# --------------------------------------------------------
	# Descarga pagina detalle
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	patron = '<div id="reproductor">.*?<script.*?>.*?j_url="([^"]+)";.*?flashControl\("([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	try:
		url =  matches[0][1]+matches[0][0]
	except:
		url = ""
	xbmc.output("[tva.py] url="+url)
	
	# --------------------------------------------------------
	# Amplia el argumento
	# --------------------------------------------------------
	patron = '<div id="encuesta">\s*<div class="cab">.*?</div>(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches)>0:
		plot = "%s" % matches[0]
		plot = plot.replace("<p>","")
		plot = plot.replace("</p>"," ")
		plot = plot.replace("<strong>","")
		plot = plot.replace("</strong>","")
		plot = plot.replace("<br />"," ")
		plot = plot.strip()
	
	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   

def play(params,url,category):
	xbmc.output("[a3.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
