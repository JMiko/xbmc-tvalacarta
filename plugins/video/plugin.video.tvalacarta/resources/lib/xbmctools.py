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
import favoritos
import descargadoslist

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

#IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )
DEBUG = True
 
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
	#xbmc.output("pluginhandle=%d" % pluginhandle)
	try:
		xbmc.output('[xbmctools.py] addnewfolder( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewfolder(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewfolder2( canal , accion , category , title , url , thumbnail , plot , programId ):
	#xbmc.output("pluginhandle=%d" % pluginhandle)
	try:
		xbmc.output('[xbmctools.py] addnewfolder( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" ,  "'+plot+'" , "'+programId+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewfolder(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&programId=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( programId ) )
	xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)


def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	xbmc.output('[xbmctools.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	#listitem.setProperty('fanart_image',os.path.join(IMAGES_PATH, "cinetube.png"))
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( canal , scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[xbmctools.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
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
	itemurl = '%s?channel=%s&action=play&category=%s&url=%s&server=%s&title=%s' % ( sys.argv[ 0 ] , canal , category , urllib.quote_plus(url) , server , urllib.quote_plus( nombre ) )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def playvideo(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,False,False)

def playvideo2(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,True,False)

def playvideo3(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,False,True)

def playvideoEx(canal,server,url,category,title,thumbnail,plot,desdefavoritos,desdedescargados):
	
	xbmc.output("[xbmctools.py] playvideo")
	xbmc.output("[xbmctools.py] playvideo canal="+canal)
	xbmc.output("[xbmctools.py] playvideo server="+server)
	xbmc.output("[xbmctools.py] playvideo url="+url)
	xbmc.output("[xbmctools.py] playvideo category="+category)

	# Abre el diálogo de selección
	if (server=="Megavideo" or server=="Megaupload") and xbmcplugin.getSetting("megavideopremium")=="true":
		opciones = []
		opciones.append("Ver en calidad alta [Megavideo]")
		opciones.append("Ver en calidad baja [Megavideo]")
		opciones.append("Descargar")
		if desdefavoritos:
			opciones.append("Quitar de favoritos")
		else:
			opciones.append("Añadir a favoritos")
		if desdedescargados:
			opciones.append("Quitar de lista de descargas")
		else:
			opciones.append("Añadir a lista de descargas")

		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una opción", opciones)
		xbmc.output("seleccion=%d" % seleccion)

		if seleccion==-1:
			return
		if seleccion==0:
			if server=="Megaupload":
				mediaurl = servertools.getmegauploadhigh(url)
			else:
				mediaurl = servertools.getmegavideohigh(url)
		elif seleccion==1:
			#advertencia = xbmcgui.Dialog()
			#resultado = advertencia.ok('Megavideo tiene un límite de reproducción de 72 minutos' , 'Aunque tengas una cuenta Premium el límite sigue existiendo' , 'cuando ves los vídeos en calidad baja')
			if server=="Megaupload":
				mediaurl = servertools.getmegauploadlow(url)
			else:
				mediaurl = servertools.getmegavideolow(url)
		elif seleccion==2:
			if xbmcplugin.getSetting("megavideopremium")=="false":
				if server=="Megaupload":
					mediaurl = servertools.getmegauploadlow(url)
				else:
					mediaurl = servertools.getmegavideolow(url)
			else:
				if server=="Megaupload":
					mediaurl = servertools.getmegauploadhigh(url)
				else:
					mediaurl = servertools.getmegavideohigh(url)
			keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
			keyboard.doModal()
			if (keyboard.isConfirmed()):
				title = keyboard.getText()
			downloadtools.downloadtitle(mediaurl,title)
			return
		elif seleccion==3:
			if desdefavoritos:
				# La categoría es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Vídeo quitado de favoritos' , title , 'Se ha quitado de favoritos')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				favoritos.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo vídeo en favoritos' , title , 'se ha añadido a favoritos')
			return
		elif seleccion==4:
			if desdedescargados:
				# La categoría es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Vídeo quitado de lista de descargas' , title , 'Se ha quitado de lista de descargas')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				descargadoslist.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo vídeo en lista de descargas' , title , 'se ha añadido a la lista de descargas')
			return

	else:
		opciones = []
		opciones.append("Ver ["+server+"]")
		opciones.append("Descargar")
		if desdefavoritos:
			opciones.append("Quitar de favoritos")
		else:
			opciones.append("Añadir a favoritos")
		if desdedescargados:
			opciones.append("Quitar de lista de descargas")
		else:
			opciones.append("Añadir a lista de descargas")
	
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
			keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
			keyboard.doModal()
			if (keyboard.isConfirmed()):
				title = keyboard.getText()
			downloadtools.downloadtitle(mediaurl,title)
			return
		elif seleccion==2:
			if desdefavoritos:
				# La categoría es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Vídeo quitado de favoritos' , title , 'Se ha quitado de favoritos')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				favoritos.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo vídeo en favoritos' , title , 'se ha añadido a favoritos')
			return
		elif seleccion==3:
			if desdedescargados:
				# La categoría es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Vídeo quitado de lista de descargas' , title , 'Se ha quitado de lista de descargas')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				descargadoslist.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo vídeo en lista de descargas' , title , 'se ha añadido a la lista de descargas')
			return

	xbmc.output("[xbmctools.py] mediaurl="+mediaurl)
	
	if mediaurl=="":
		alertnodisponibleserver(server)
		return
	
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

def alertnodisponible():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Vídeo no disponible' , 'El vídeo ya no está disponible en la página,' , 'o no se ha podido localizar el enlace')

def alertnodisponibleserver(server):
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Vídeo borrado' , 'El vídeo ya no está en '+server , 'Prueba con otro distinto')

def alerterrorpagina():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Error en la página' , 'No se puede acceder' , 'por un error en la página')

def unseo(cadena):
	if cadena.upper().startswith("VER GRATIS LA PELICULA "):
		cadena = cadena[23:]
	elif cadena.upper().startswith("VER GRATIS PELICULA "):
		cadena = cadena[20:]
	elif cadena.upper().startswith("VER ONLINE LA PELICULA "):
		cadena = cadena[23:]
	elif cadena.upper().startswith("VER GRATIS "):
		cadena = cadena[11:]
	elif cadena.upper().startswith("VER ONLINE "):
		cadena = cadena[11:]
	return cadena

def addSingleChannelOptions(params,url,category):
	addnewfolder( "configuracion" , "mainlist" , "configuracion" , "Configuracion" , "" , "" , "" )
	addnewfolder( "descargados"   , "mainlist" , "descargados"   , "Descargas"     , "" , "" , "" )
	addnewfolder( "favoritos"     , "mainlist" , "favoritos"     , "Favoritos"     , "" , "" , "" )
