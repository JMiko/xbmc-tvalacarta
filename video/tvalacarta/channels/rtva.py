# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVA
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

xbmc.output("[rtva.py] init")

DEBUG = True
CHANNELNAME = "Andalucia TV"
CHANNELCODE = "rtva"

def mainlist(params,url,category):
	xbmc.output("[rtva.py] mainlist")

	url = "http://www.radiotelevisionandalucia.es/tvcarta/impe/web/portada"

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los programas
	# --------------------------------------------------------
	patron = '<div class="infoPrograma"><h3 class="h3TituloProgramaCarta"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h3><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div><div class="enlacePrograma"><a href="[^"]+" title="[^"]+"><img class="imgLista" src="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	dictionaryurl = {}

	for match in matches:
		titulo = match[1].replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace('&Aacute;','�')
		titulo = titulo.replace('&Eacute;','�')
		titulo = titulo.replace('&Iacute;','�')
		titulo = titulo.replace('&Oacute;','�')
		titulo = titulo.replace('&Uacute;','�')
		titulo = titulo.replace('&ntilde;','�')
		titulo = titulo.replace('&Ntilde;','�')
		scrapedtitle = titulo
		scrapedurl = 'http://www.radiotelevisionandalucia.es/tvcarta/impe/web/portada'
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		#addfolder( scrapedtitle , scrapedurl , "videolist" )
		if dictionaryurl.has_key(scrapedtitle):
			xbmc.output("%s ya existe" % scrapedtitle)
		else:
			xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
			dictionaryurl[scrapedtitle] = True

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_TITLE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[rtva.py] videolist")

	title = urllib.unquote_plus( params.get("title") )

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los programas
	# --------------------------------------------------------
	patron  = '<div class="infoPrograma"><h3 class="h3TituloProgramaCarta"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h3><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div><div class="enlacePrograma"><a href="[^"]+" title="[^"]+"><img class="imgLista" src="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Datos
		titulo = match[1].replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace("�","�")
		titulo = titulo.replace('&Aacute;','�')
		titulo = titulo.replace('&Eacute;','�')
		titulo = titulo.replace('&Iacute;','�')
		titulo = titulo.replace('&Oacute;','�')
		titulo = titulo.replace('&Uacute;','�')
		titulo = titulo.replace('&ntilde;','�')
		titulo = titulo.replace('&Ntilde;','�')
		scrapedtitle = titulo
		scrapedurl = urlparse.urljoin(url, match[0])
		scrapedthumbnail = match[6].replace(' ','%20')
		titulocapitulo =  ( "%s %s %s %s" % (match[2],match[3],match[4],match[5]))
		titulocapitulo = titulocapitulo.replace('&Aacute;','�')
		titulocapitulo = titulocapitulo.replace('&Eacute;','�')
		titulocapitulo = titulocapitulo.replace('&Iacute;','�')
		titulocapitulo = titulocapitulo.replace('&Oacute;','�')
		titulocapitulo = titulocapitulo.replace('&Uacute;','�')
		titulocapitulo = titulocapitulo.replace('&ntilde;','�')
		titulocapitulo = titulocapitulo.replace('&Ntilde;','�')
		titulocapitulo = titulocapitulo.replace('&aacute;','�')
		titulocapitulo = titulocapitulo.replace('&eacute;','�')
		titulocapitulo = titulocapitulo.replace('&iacute;','�')
		titulocapitulo = titulocapitulo.replace('&oacute;','�')
		titulocapitulo = titulocapitulo.replace('&uacute;','�')
		scrapedplot = titulocapitulo

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		if scrapedtitle == title:
			xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle + " " + scrapedplot , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[rtva.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[rtva.py] thumbnail="+thumbnail)

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del v�deo...', title )

	# --------------------------------------------------------
	# Descarga pagina detalle
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	patron = '<param name="flashvars" value="&amp;video=(http://[^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	try:
		url = matches[0].replace(' ','%20')
	except:
		url = ""
	xbmc.output("[rtva.py] url="+url)

	# --------------------------------------------------------
	# Argumento detallado
	# --------------------------------------------------------
	patron = '<div class="zonaContenido"><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div>'
	argumento = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(argumento)
	argumentofull = ""
	if len(argumento) > 0:
		if len(argumento[0]) >= 4:
			argumentofull = ("%s\n%s\n%s\n%s\n%s" % (title , argumento[0][0] , argumento[0][1] , argumento[0][2] , argumento[0][3] ))
		elif len(argumento[0]) >= 3:
			argumentofull = ("%s\n%s\n%s\n%s" % (title , argumento[0][0] , argumento[0][1] , argumento[0][2] ))
		elif len(argumento[0]) >= 2:
			argumentofull = ("%s\n%s\n%s" % (title , argumento[0][0] , argumento[0][1] ))
		elif len(argumento[0]) >= 1:
			argumentofull = ("%s\n%s" % (title , argumento[0][0] ))
	#argumentofull = ("%s\n%s" % (item.description , argumento[0][0] ))
	argumentofull = argumentofull.replace('&Aacute;','�')
	argumentofull = argumentofull.replace('&Eacute;','�')
	argumentofull = argumentofull.replace('&Iacute;','�')
	argumentofull = argumentofull.replace('&Oacute;','�')
	argumentofull = argumentofull.replace('&Uacute;','�')
	argumentofull = argumentofull.replace('&aacute;','�')
	argumentofull = argumentofull.replace('&eacute;','�')
	argumentofull = argumentofull.replace('&iacute;','�')
	argumentofull = argumentofull.replace('&oacute;','�')
	argumentofull = argumentofull.replace('&uacute;','�')
	argumentofull = argumentofull.replace('&ntilde;','�')
	argumentofull = argumentofull.replace('&Ntilde;','�')
	plot = argumentofull

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )
	#xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://aialanetfs.fplive.net/aialanet?slist=Jardineria/palmera-roebelen.flv", nuevoitem)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   
