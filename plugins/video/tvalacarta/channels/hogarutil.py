# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para hogarutil.com
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
#
# TODO patronvideos  = '"paramVideoPubli", "([^"]+)"'
#

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import binascii

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[hogarutil.py] init")

DEBUG = True
CHANNELNAME = "hogarutil.com"
CHANNELCODE = "hogarutil"

def mainlist(params,url,category):
	xbmc.output("[hogarutil.py] mainlist")

	# Añade al listado de XBMC
	addfolder("Cocina","http://www.hogarutil.com/Cocina/Recetas+en+v%C3%ADdeo","videolist")
	addfolder("Decogarden","http://www.hogarutil.com/Decogarden/Trabajos+en+v%C3%ADdeo","videolist")
	addfolder("Jardineria","http://www.hogarutil.com/Jardineria/Trabajos+en+v%C3%ADdeo","videolist")
	addfolder("Bricomania","http://www.hogarutil.com/Bricomania/Trabajos+en+v%C3%ADdeo","videolist")
	#addvideodirecto("¡En directo!","rtmp://aialanetlivefs.fplive.net/aialanetlive-live/hogarutil","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[hogarutil.py] videolist")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae el enlace a la página siguiente
	patronvideos  = '<a.*?href="([^"]+)"[^>]+> siguiente'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Siguiente"
		scrapedurl = urlparse.urljoin("http://www.hogarutil.com",urllib.quote(match[0]))
		scrapedthumbnail = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		addfolder( scrapedtitle , scrapedurl , "videolist" )

	# Extrae las entradas (carpetas)
	#patronvideos  = '<li(?: class="par")?><a href="(/[^/]+/Trabajos\+en\+v[^"]+)">([^<]+)<'
	#patronvideos = '<li><span style="text-align:left; width:165px; margin-right:1px;" class="floatright"><img style="float:right;" src="/staticFiles/logo-hogarutil-video.gif"/>Karlos Arguiñano</span><a title="Bacalao fresco con puerros y vinagreta de sepia" href="/Cocina/Recetas+en+v%C3%ADdeo/Bacalao+fresco+con+puerros+y+vinagreta+de+sepia">Bacalao fresco con puerros y vinagreta de...</a></li>'
	patronvideos = '<li><span[^>]+><img.*?src="/staticFiles/logo-hogarutil-video.gif"[^>]+>([^<]+)</span><a title="([^"]+)" href="([^"]+)">[^<]+</a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]+" ("+match[0]+")"
		try:
			scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
		except:
			pass

		# URL
		scrapedurl = urlparse.urljoin("http://www.hogarutil.com",urllib.quote(match[2]))
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		addvideo( scrapedtitle , scrapedurl , category )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[hogarutil.py] play")

	infotitle = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	#xbmc.output("[hogarutil.py] infotitle="+infotitle)
	
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del vídeo...', infotitle )

	# Averigua la descripcion (plot)
	data = scrapertools.cachePage(url)
	patronvideos = '<meta name="BNT_RECETA_DESC" content="([^"]+)" />'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	try:
		infoplot = matches[0]
	except:
		infoplot = ""
	xbmc.output("[hogarutil.py] infoplot="+infoplot)

	# Averigua el thumbnail
	patronvideos = '<img class="fotoreceta" alt="[^"]*" src="([^"]+)"/>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	try:
		infothumbnail = scrapedurl = urlparse.urljoin("http://www.hogarutil.com",urllib.quote(matches[0]))
	except:
		infothumbnail = ""
	xbmc.output("[hogarutil.py] infothumbnail="+infothumbnail)

	# Averigua la URL del video
	patronvideos = 'addVariable\("paramVideoContent", "([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	try:
		mediaurl = matches[0]
	except:
		mediaurl = ""
	xbmc.output("[hogarutil.py] mediaurl="+mediaurl)

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( infotitle, iconImage="DefaultVideo.png", thumbnailImage=infothumbnail )
	listitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
	listitem.setInfo( "video", { "Title": infotitle, "Plot" : infoplot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( mediaurl, listitem )
	#xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://aialanetfs.fplive.net/aialanet?slist=Jardineria/palmera-roebelen.flv", nuevoitem)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   

def directplay(params,url,category):

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( "Emision en directo", iconImage="DefaultVideo.png" )
	listitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
	listitem.setInfo( "video", { "Title": "Emision en directo", "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   

def addfolder(nombre,url,accion):
	xbmc.output('[hogarutil.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=hogarutil&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category):
	xbmc.output('[hogarutil.py] addvideo( "'+nombre+'" , "' + url + '" , "'+category+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=hogarutil&action=play&category=%s&url=%s' % ( sys.argv[ 0 ] , category , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addvideodirecto(nombre,url,category):
	xbmc.output('[hogarutil.py] addvideodirecto( "'+nombre+'" , "' + url + '" , "'+category+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : "Emision en directo" } )
	itemurl = '%s?channel=hogarutil&action=directplay&category=%s&url=%s' % ( sys.argv[ 0 ] , category , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[hogarutil.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	itemurl = '%s?channel=hogarutil&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

#mainlist(None,"","mainlist")
#videolist(None,"http://www.hogarutil.com/Cocina/Recetas+en+vídeo","Cocina")
#play(None,"http://www.hogarutil.com/Cocina/Recetas+en+v%C3%ADdeo/Sepia+con+arroz+negro","")
