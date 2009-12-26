# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Plus TV
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

xbmc.output("[plus.py] init")

DEBUG = True
CHANNELNAME = "Plus TV"
CHANNELCODE = "plus"

def mainlist(params,url,category):
	xbmc.output("[plus.py] mainlist")

	url = "http://www.plus.es/tv/canales.html"

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los programas
	# --------------------------------------------------------
	patron = '<li class="canales estirar[^"]*">[^<]+<h2><a href="([^"]+)">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		try:
			scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
		except:
			pass
		scrapedurl = "http://www.plus.es/tv/" + match[0].replace("index.html?idList","emisiones.html?id")
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		#addfolder( scrapedtitle , scrapedurl , "videolist" )
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[plus.py] videolist")

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los programas
	# --------------------------------------------------------
	patron  = '<li class="video estirar">[^<]+<div class="imagen">[^<]+<a title="[^"]+" href="([^"]+)">[^<]+<img alt="" src="([^"]+)">[^<]+<span>[^<]+</span>[^<]+</a>[^<]+</div>[^<]+<div class="tooltip" title="([^"]+)">[^<]+<div class="textos">[^<]+<p class="titulo"><a href="[^"]+">([^<]+)</a></p>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Datos
		scrapedtitle = match[3]
		scrapedurl = "http://www.plus.es/tv/" + match[0]
		scrapedthumbnail = match[1]
		scrapedplot = match[2]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[plus.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[plus.py] thumbnail="+thumbnail)

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del v�deo...', title )

	# --------------------------------------------------------
	# Descarga pagina detalle
	# --------------------------------------------------------
	# Averigua la URL
	# URL Detalle: http://www.plus.es/tv/index.html?idList=PLTVDO&amp;idVid=725903&amp;pos=0
	# URL XML v�deo: http://www.plus.es/tv/bloques.html?id=0&idList=PLTVDO&idVid=725903
	#<?xml version="1.0" encoding="iso-8859-1"?>
	#<bloque modo="U">
	#<video tipo="P" url="http://canalplus.ondemand.flumotion.com/canalplus/ondemand/plustv/GF755806.flv" title=""></video>
	#<video tipo="T" url="http://canalplus.ondemand.flumotion.com/canalplus/ondemand/plustv/NF754356.flv" title="Encuentros en el fin del mundo"></video>
	#</bloque>
	idCategoria = re.compile("idList=([^&]+)&",re.DOTALL).findall(url)
	xbmc.output('idCategoria='+idCategoria[0])
	idVideo = re.compile("idVid=(\d+)",re.DOTALL).findall(url)
	xbmc.output('idVideo='+idVideo[0])
	urldetalle = "http://www.plus.es/tv/bloques.html?id=0&idList=" + idCategoria[0] + "&idVid=" + idVideo[0]
	bodydetalle = scrapertools.cachePage(urldetalle)
	xbmc.output(bodydetalle)
	enlacevideo = re.compile('<video tipo="T" url="([^"]+)"',re.DOTALL).findall(bodydetalle)
	xbmc.output("enlacevideo="+enlacevideo[0])
	#enlacevideo = 
	url = enlacevideo[0]
	
	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	#url = "rtmp://od.flash.plus.es/ondemand/14314/plus/plustv/PO778395.flv"
	
	cabecera = url[:32]
	xbmc.output("cabecera="+cabecera)
	finplaypath = url.rfind(".")
	playpath = url[33:finplaypath]
	xbmc.output("playpath="+playpath)
	
	#url = "rtmp://od.flash.plus.es/ondemand"
	url = cabecera
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setProperty("SWFPlayer", "http://www.plus.es/tv/carcasa.swf")
	#listitem.setProperty("Playpath","14314/plus/plustv/PO778395")
	listitem.setProperty("Playpath",playpath)
	listitem.setProperty("Hostname","od.flash.plus.es")
	listitem.setProperty("Port","1935")
	#listitem.setProperty("tcUrl","rtmp://od.flash.plus.es/ondemand")
	listitem.setProperty("tcUrl",cabecera)
	listitem.setProperty("app","ondemand")
	listitem.setProperty("flashVer","LNX 9,0,124,0")
	listitem.setProperty("pageUrl","LNX 9,0,124,0")

	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	#url= rtmp://od.flash.plus.es/ondemand/14314/plus/plustv/PO778395.flv
	#DEBUG: Protocol : RTMP
	#DEBUG: Playpath : 14314/plus/plustv/PO778395
	#DEBUG: Hostname : od.flash.plus.es
	#DEBUG: Port     : 1935
	#DEBUG: tcUrl    : rtmp://od.flash.plus.es:1935/ondemand
	#DEBUG: app      : ondemand
	#DEBUG: flashVer : LNX 9,0,124,0
	#DEBUG: live     : no
	#DEBUG: timeout  : 300 sec

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   
