# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# XBMC Tools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urllib
import xbmc
import xbmcgui
import xbmcplugin
import sys
import servertools
import downloadtools
import os

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

#IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )
import xbmc

fullfanart = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'kideos-fanart.jpg' ) )

def get_system_platform():
	""" fonction: pour recuperer la platform que xbmc tourne """
	platform = "unknown"
	if xbmc.getCondVisibility( "system.platform.linux" ):
		platform = "linux"
	elif xbmc.getCondVisibility( "system.platform.xbox" ):
		platform = "xbox"
	elif xbmc.getCondVisibility( "system.platform.windows" ):
		platform = "windows"
	elif xbmc.getCondVisibility( "system.platform.osx" ):
		platform = "osx"
	return platform

def addnewfolder( canal , accion , category , title , url , thumbnail , plot ):
	xbmc.output("pluginhandle=%d" % pluginhandle)
	try:
		xbmc.output('[xbmctools.py] addnewfolder( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewfolder(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setProperty( "fanart_image", fullfanart )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	try:
		xbmc.output('[xbmctools.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewvideo(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setProperty( "fanart_image", fullfanart )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	#listitem.setProperty('fanart_image',os.path.join(IMAGES_PATH, "cinetube.png"))
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( canal , scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	try:
		xbmc.output('[xbmctools.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	except:
		xbmc.output('[xbmctools.py] addthumbnailfolder(<unicode>)')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	listitem.setProperty( "fanart_image", fullfanart )
	itemurl = '%s?channel=%s&action=%s&category=%s&url=%s&title=%s&thumbnail=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedthumbnail ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addfolder( canal , nombre , url , accion ):
	xbmc.output('[xbmctools.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=%s&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addvideo( canal , nombre , url , category , server ):
	xbmc.output('[xbmctools.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=%s&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , canal , category , urllib.quote_plus(url) , server )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def playvideo(canal,server,url,category,title,thumbnail,plot):
	
	xbmc.output("[xbmctools.py] playvideo")

	# Abre el diálogo de selección
	if server=="Megavideo" and xbmcplugin.getSetting("megavideopremium")=="true":
		opciones = []
		opciones.append("Ver en calidad alta (Megavideo)")
		opciones.append("Ver en calidad baja (Megavideo)")
		opciones.append("Descargar")

		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una opción", opciones)
		xbmc.output("seleccion=%d" % seleccion)

		if seleccion==-1:
			return
		if seleccion==0:
			mediaurl = servertools.getmegavideohigh(url)
		elif seleccion==1:
			advertencia = xbmcgui.Dialog()
			resultado = advertencia.ok('Megavideo tiene un límite de reproducción de 72 minutos' , 'Aunque tengas una cuenta Premium el límite sigue existiendo' , 'cuando ves los vídeos en calidad baja')
			mediaurl = servertools.getmegavideolow(url)
		elif seleccion==2:
			if xbmcplugin.getSetting("megavideopremium")=="false":
				mediaurl = servertools.getmegavideolow(url)
			else:
				mediaurl = servertools.getmegavideohigh(url)
			downloadtools.downloadtitle(mediaurl,title)
			return
	else:
		opciones = []
		opciones.append("Ver")
		opciones.append("Descargar")
	
		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una opción", opciones)
		xbmc.output("seleccion=%d" % seleccion)
		
		if seleccion==-1:
			return
		if seleccion==0:
			if server=="Megavideo":
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Megavideo tiene un límite de reproducción de 72 minutos' , 'Para evitar que los vídeos se corten pasado ese tiempo' , 'necesitas una cuenta Premium')
			mediaurl = servertools.findurl(url,server)
		elif seleccion==1:
			mediaurl = servertools.findurl(url,server)
			downloadtools.downloadtitle(mediaurl,title)
			return
		
	xbmc.output("[xbmctools.py] mediaurl="+mediaurl)
	
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title )

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : canal , "Genre" : category } )
	playlist.add( mediaurl, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER )
	xbmcPlayer.play(playlist)   

def logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot):
	if (DEBUG):
		xbmc.output("[xmbctools.py] scrapedtitle="+scrapedtitle)
		xbmc.output("[xmbctools.py] scrapedurl="+scrapedurl)
		xbmc.output("[xmbctools.py] scrapedthumbnail="+scrapedthumbnail)
		xbmc.output("[xmbctools.py] scrapedplot="+scrapedplot)
