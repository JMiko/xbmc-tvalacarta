# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# XBMC Tools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# 2010/02/13 A�adida funcionalidad de Biblioteca - JUR
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
import library
import descargadoslist

# Esto permite su ejecuci�n en modo emulado
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

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , Serie=""):
	addnewfolderextra( canal , accion , category , title , url , thumbnail , plot , "" ,Serie)

def addnewfolderextra( canal , accion , category , title , url , thumbnail , plot , extradata ,Serie=""):
	#xbmc.output("pluginhandle=%d" % pluginhandle)
	try:
		xbmc.output('[xbmctools.py] addnewfolder( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")" , "'+Serie+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewfolder(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&extradata=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( extradata ) , Serie)
	#xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ,Serie=""):
	try:
		xbmc.output('[xbmctools.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")" , "'+Serie+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewvideo(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	#listitem.setProperty('fanart_image',os.path.join(IMAGES_PATH, "cinetube.png"))
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server , Serie)
	#xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
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

def addvideo( canal , nombre , url , category , server , Serie=""):
	xbmc.output('[xbmctools.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+ '" , "'+Serie+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=%s&action=play&category=%s&url=%s&server=%s&title=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , category , urllib.quote_plus(url) , server , urllib.quote_plus( nombre ) , Serie)
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def playvideo(canal,server,url,category,title,thumbnail,plot,strmfile=False,Serie=""):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,False,False,strmfile,Serie)

def playvideo2(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,True,False)

def playvideo3(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,False,True)

def playvideoEx(canal,server,url,category,title,thumbnail,plot,desdefavoritos,desdedescargados,strmfile=False,Serie=""):
	
	xbmc.output("[xbmctools.py] playvideo")
	xbmc.output("[xbmctools.py] playvideo canal="+canal)
	xbmc.output("[xbmctools.py] playvideo server="+server)
	xbmc.output("[xbmctools.py] playvideo url="+url)
	xbmc.output("[xbmctools.py] playvideo category="+category)
	xbmc.output("[xbmctools.py] playvideo serie="+Serie)
	
	# Abre el di�logo de selecci�n
	opciones = []
	# Los v�deos de Megav�deo s�lo se pueden ver en calidad alta con cuenta premium
	# Los v�deos de Megaupload s�lo se pueden ver con cuenta premium, en otro caso pide captcha
	if (server=="Megavideo" or server=="Megaupload") and xbmcplugin.getSetting("megavideopremium")=="true":
		opciones.append("Ver en calidad alta ["+server+"]")
	# Los v�deos de Megav�deo o Megaupload se pueden ver en calidad baja sin cuenta premium, aunque con el l�mite
	if (server=="Megavideo" or server=="Megaupload"):
		opciones.append("Ver en calidad baja [Megavideo]")
	opciones.append("Descargar")
	if desdefavoritos: 
		opciones.append("Quitar de favoritos")
	else:
		opciones.append("A�adir a favoritos")
	if desdedescargados:
		opciones.append("Quitar de lista de descargas")
	else:
		opciones.append("A�adir a lista de descargas")
	if canal == "seriesyonkis": #De momento s�lo en seriesyonkis
		opciones.append("A�adir a Biblioteca")    
	dia = xbmcgui.Dialog()
	seleccion = dia.select("Elige una opci�n", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	xbmc.output("seleccion=%s" % opciones[seleccion])

	# No ha elegido nada, lo m�s probable porque haya dado al ESC 
	if seleccion==-1:
		if strmfile:  #Para evitar el error "Uno o m�s elementos fallaron" al cancelar la selecci�n desde fichero strm
			listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path="")    # JUR Modified
			xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),False,listitem)    # JUR Added
		return
	# Ver en calidad alta
	if opciones[seleccion].startswith("Ver en calidad alta"):
		if server=="Megaupload":
			mediaurl = servertools.getmegauploadhigh(url)
		else:
			mediaurl = servertools.getmegavideohigh(url)
	# Ver (calidad baja megavideo o resto servidores)
	elif opciones[seleccion].startswith("Ver"):
		if server=="Megaupload":
			mediaurl = servertools.getmegauploadlow(url)
		elif server=="Megavideo":
			if xbmcplugin.getSetting("megavideopremium")=="false":
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Megavideo tiene un l�mite de reproducci�n de 72 minutos' , 'Para evitar que los v�deos se corten pasado ese tiempo' , 'necesitas una cuenta Premium')			mediaurl = servertools.getmegavideolow(url)
		else:
			mediaurl = servertools.findurl(url,server)

	# Descargar
	elif opciones[seleccion]=="Descargar":
		if server=="Megaupload":
			if xbmcplugin.getSetting("megavideopremium")=="false":
				mediaurl = servertools.getmegauploadlow(url)
			else:
				mediaurl = servertools.getmegauploadhigh(url)
		elif server=="Megavideo":
			if xbmcplugin.getSetting("megavideopremium")=="false":
				mediaurl = servertools.getmegavideolow(url)
			else:
				mediaurl = servertools.getmegavideohigh(url)
		else:
			mediaurl = servertools.findurl(url,server)

		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			title = keyboard.getText()
		downloadtools.downloadtitle(mediaurl,title)
		return

	elif opciones[seleccion]=="Quitar de favoritos":
		# La categor�a es el nombre del fichero en favoritos
		os.remove(urllib.unquote_plus( category ))
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('V�deo quitado de favoritos' , title , 'Se ha quitado de favoritos')
		return

	elif opciones[seleccion]=="A�adir a favoritos":
		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			title = keyboard.getText()
		favoritos.savebookmark(title,url,thumbnail,server,plot)
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('Nuevo v�deo en favoritos' , title , 'se ha a�adido a favoritos')
		return

	elif opciones[seleccion]=="Quitar de lista de descargas":
		# La categor�a es el nombre del fichero en la lista de descargas
		os.remove(urllib.unquote_plus( category ))
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('V�deo quitado de lista de descargas' , title , 'Se ha quitado de lista de descargas')
		return

	elif opciones[seleccion]=="A�adir a lista de descargas":
		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			title = keyboard.getText()
		descargadoslist.savebookmark(title,url,thumbnail,server,plot)
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('Nuevo v�deo en lista de descargas' , title , 'se ha a�adido a la lista de descargas')
		return

	elif opciones[seleccion]=="A�adir a Biblioteca":  # Library
		library.savelibrary(title,url,thumbnail,server,plot,canal=canal,category=category,Serie=Serie)
		return

	# Si no hay mediaurl es porque el v�deo no est� :)
	xbmc.output("[xbmctools.py] mediaurl="+mediaurl)
	if mediaurl=="":
		alertnodisponibleserver(server)
		return

	# Crea la playlist para pas�rsela al reproductor
	playlist = createplaylist(canal,title,mediaurl,thumbnail,plot,category)

	# Lanza el reproductor
	launchplayer(strmfile,playlist)

# Crea una playlist para pas�rsela al reproductor
def createplaylist(canal,title,mediaurl,thumbnail,plot,category):
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title )
	dialogWait.update(0) #Jur. Para evitar los porcentajes aleatorios

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	# JUR - Modificaci�n para evitar error "Playback failed" en ficheros strm
	xbmc.output("[xbmctools.py] JUR-Modif 1 added mediaurl to ListItem ,path=")    # JUR Added
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path=mediaurl)    # JUR Modified
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : canal , "Genre" : category } )
	xbmc.output("[xbmctools.py] JUR-Modif 2. Added call to xmbcplugin.setResolvedUrl")    # JUR Added
	xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,listitem)    # JUR Added
	playlist.add( mediaurl, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	return playlist

# Lanza el reproductor
def launchplayer(strmfile,playlist):
	# Reproduce
	playersettings = xbmcplugin.getSetting('player_type')
	xbmc.output("[xbmctools.py] playersettings="+playersettings)

	player_type = xbmc.PLAYER_CORE_AUTO
	if playersettings == "0":
		player_type = xbmc.PLAYER_CORE_AUTO
		xbmc.output("[xbmctools.py] PLAYER_CORE_AUTO")
	elif playersettings == "1":
		player_type = xbmc.PLAYER_CORE_MPLAYER
		xbmc.output("[xbmctools.py] PLAYER_CORE_MPLAYER")
	elif playersettings == "2":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
		xbmc.output("[xbmctools.py] PLAYER_CORE_DVDPLAYER")

	if strmfile: #Si es un fichero strm no hace falta el play
		xbmc.output("[xbmctools.py] strm file. Avoid .play")
	else:
		xbmcPlayer = xbmc.Player( player_type )
		xbmcPlayer.play(playlist)
'''
def playvideoEx(canal,server,url,category,title,thumbnail,plot,desdefavoritos,desdedescargados,strmfile=False,Serie=""):
	
	xbmc.output("[xbmctools.py] playvideo")
	xbmc.output("[xbmctools.py] playvideo canal="+canal)
	xbmc.output("[xbmctools.py] playvideo server="+server)
	xbmc.output("[xbmctools.py] playvideo url="+url)
	xbmc.output("[xbmctools.py] playvideo category="+category)
	xbmc.output("[xbmctools.py] playvideo serie="+Serie)
	
	# Abre el di�logo de selecci�n
	if (server=="Megavideo" or server=="Megaupload") and xbmcplugin.getSetting("megavideopremium")=="true":
		opciones = []
		opciones.append("Ver en calidad alta [Megavideo]")
		opciones.append("Ver en calidad baja [Megavideo]")
		opciones.append("Descargar")
		if desdefavoritos:
			opciones.append("Quitar de favoritos")
		else:
			opciones.append("A�adir a favoritos")
		if desdedescargados:
			opciones.append("Quitar de lista de descargas")
		else:
			opciones.append("A�adir a lista de descargas")
		if canal == "seriesyonkis": #De momento s�lo en seriesyonkis
			opciones.append("A�adir a Biblioteca")    
		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una opci�n", opciones)
		xbmc.output("seleccion=%d" % seleccion)

		if seleccion==-1:
			if strmfile:  #Para evitar el error "Uno o m�s elementos fallaron" al cancelar la selecci�n desde fichero strm
				listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path="")    # JUR Modified
				xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),False,listitem)    # JUR Added
			return
		if seleccion==0:
			if server=="Megaupload":
				mediaurl = servertools.getmegauploadhigh(url)
			else:
				mediaurl = servertools.getmegavideohigh(url)
		elif seleccion==1:
			#advertencia = xbmcgui.Dialog()
			#resultado = advertencia.ok('Megavideo tiene un l�mite de reproducci�n de 72 minutos' , 'Aunque tengas una cuenta Premium el l�mite sigue existiendo' , 'cuando ves los v�deos en calidad baja')
			if server=="Megaupload":
				mediaurl = servertools.getmegauploadlow(url)
			else:
				mediaurl = servertools.getmegavideolow(url)
		elif seleccion==2:  #Descargar
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
		elif seleccion==3:  # Favoritos
			if desdefavoritos:
				# La categor�a es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('V�deo quitado de favoritos' , title , 'Se ha quitado de favoritos')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				favoritos.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo v�deo en favoritos' , title , 'se ha a�adido a favoritos')
			return
		elif seleccion==4:
			if desdedescargados:
				# La categor�a es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('V�deo quitado de lista de descargas' , title , 'Se ha quitado de lista de descargas')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				descargadoslist.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo v�deo en lista de descargas' , title , 'se ha a�adido a la lista de descargas')
			return
		elif seleccion==5:  # Library
			library.savelibrary(title,url,thumbnail,server,plot,canal=canal,category=category,Serie=Serie)
			return

	else:
		opciones = []
		opciones.append("Ver ["+server+"]")
		opciones.append("Descargar")
		if desdefavoritos:
			opciones.append("Quitar de favoritos")
		else:
			opciones.append("A�adir a favoritos")
		if desdedescargados:
			opciones.append("Quitar de lista de descargas")
		else:
			opciones.append("A�adir a lista de descargas")

		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una opci�n", opciones)
		xbmc.output("seleccion=%d" % seleccion)
		
		if seleccion==-1:
			return
		if seleccion==0:
			if server=="Megavideo":
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Megavideo tiene un l�mite de reproducci�n de 72 minutos' , 'Para evitar que los v�deos se corten pasado ese tiempo' , 'necesitas una cuenta Premium')
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
				# La categor�a es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('V�deo quitado de favoritos' , title , 'Se ha quitado de favoritos')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				favoritos.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo v�deo en favoritos' , title , 'se ha a�adido a favoritos')
			return
		elif seleccion==3:
			if desdedescargados:
				# La categor�a es el nombre del fichero en favoritos
				os.remove(urllib.unquote_plus( category ))
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('V�deo quitado de lista de descargas' , title , 'Se ha quitado de lista de descargas')
			else:
				keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
				keyboard.doModal()
				if (keyboard.isConfirmed()):
					title = keyboard.getText()
				descargadoslist.savebookmark(title,url,thumbnail,server,plot)
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Nuevo v�deo en lista de descargas' , title , 'se ha a�adido a la lista de descargas')
			return

	xbmc.output("[xbmctools.py] mediaurl="+mediaurl)
	
	if mediaurl=="":
		alertnodisponibleserver(server)
		return
	
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title )
	dialogWait.update(0) #Jur. Para evitar los porcentajes aleatorios

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	# JUR - Modificaci�n para evitar error "Playback failed" en ficheros strm
	xbmc.output("[xbmctools.py] JUR-Modif 1 added mediaurl to ListItem ,path=")    # JUR Added
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path=mediaurl)    # JUR Modified
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : canal , "Genre" : category } )
	xbmc.output("[xbmctools.py] JUR-Modif 2. Added call to xmbcplugin.setResolvedUrl")    # JUR Added
	xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,listitem)    # JUR Added
	playlist.add( mediaurl, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	playersettings = xbmcplugin.getSetting('player_type')
	xbmc.output("[xbmctools.py] playersettings="+playersettings)

	player_type = xbmc.PLAYER_CORE_AUTO
	if playersettings == "0":
		player_type = xbmc.PLAYER_CORE_AUTO
		xbmc.output("[xbmctools.py] PLAYER_CORE_AUTO")
	elif playersettings == "1":
		player_type = xbmc.PLAYER_CORE_MPLAYER
		xbmc.output("[xbmctools.py] PLAYER_CORE_MPLAYER")
	elif playersettings == "2":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
		xbmc.output("[xbmctools.py] PLAYER_CORE_DVDPLAYER")

	if strmfile: #Si es un fichero strm no hace falta el play
		xbmc.output("[xbmctools.py] strm file. Avoid .play")
	else:
		xbmcPlayer = xbmc.Player( player_type )
		xbmcPlayer.play(playlist)
'''
'''
	# Accion por defecto: Ver
	if xbmcplugin.getSetting("default_action")=="1":
	# Accion por defecto: Ver calidad alta
	elif xbmcplugin.getSetting("default_action")=="2":
	# Accion por defecto: Pregunar
	else:
'''
def logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot):
	if (DEBUG):
		xbmc.output("[xmbctools.py] scrapedtitle="+scrapedtitle)
		xbmc.output("[xmbctools.py] scrapedurl="+scrapedurl)
		xbmc.output("[xmbctools.py] scrapedthumbnail="+scrapedthumbnail)
		xbmc.output("[xmbctools.py] scrapedplot="+scrapedplot)

def alertnodisponible():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('V�deo no disponible' , 'El v�deo ya no est� disponible en la p�gina,' , 'o no se ha podido localizar el enlace')

def alertnodisponibleserver(server):
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('V�deo borrado' , 'El v�deo ya no est� en '+server , 'Prueba con otro distinto')

def alerterrorpagina():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Error en la p�gina' , 'No se puede acceder' , 'por un error en la p�gina')

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

# A�ADIDO POR JUR. SOPORTE DE FICHEROS STRM
def playstrm(params,url,category):
	#Igual que play pero para ficheros strm.
	#Se debe a�adir 2 par�metros a xbmctool.playvideo
	#nostrmfile = 0 porque s� es strm

	xbmc.output("[pelisalacarta.py] strm")
	xbmc.output("[pelisalacarta.py] strm - url="+url)

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	playvideo("STRM Channel",server,url,category,title,thumbnail,plot,1,url)
