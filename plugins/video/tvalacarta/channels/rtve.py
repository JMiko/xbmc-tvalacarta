# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVE
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

xbmc.output("[rtve.py] init")

DEBUG = True
CHANNELNAME = "TVE"
CHANNELCODE = "rtve"

def mainlist(params,url,category):
	xbmc.output("[rtve.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Recomendados"   , "http://www.rtve.es/alacarta/todos/recomendados/index.html"  , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Últimos 7 días" , "http://www.rtve.es/alacarta/todos/ultimos/index.html"       , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Temas"          , "http://www.rtve.es/alacarta/todos/temas/index.html"         , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Todos A-Z"      , "http://www.rtve.es/alacarta/todos/abecedario/index.html"    , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Archivo TVE"    , "http://www.rtve.es/alacarta/archivo/index.html"             , "" , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[rtve.py] videolist")

	title = urllib.unquote_plus( params.get("title") )

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	xbmc.output("[rtve.py] videolist descarga página principal "+url)
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae las categorias (carpetas)
	# --------------------------------------------------------
	patron  = '<a href="(/alacarta/todos/[^"]+)">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Datos
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin("http://www.rtve.es", match[0])
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		if scrapedtitle=="Recomendados" or scrapedtitle=="Temas" or scrapedtitle=="Todos A-Z" or scrapedtitle=="Archivo TVE" or scrapedtitle=="Ultimos 7 dias":
			pass
		else:
			xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# --------------------------------------------------------
	# Extrae los videos de la página actual
	# --------------------------------------------------------
	patron  = '<li id="video-(\d+)">\W*<div>\W*<a rel="facebox" href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"><img alt="Reproducir" src="/css/i/mediateca/play.png" class="play_mini"></a>\W+<h3>\W+<a[^<]+</a>\W+</h3>\W+<p>([^<]+)</p>[^<]+<span>([^<]+)<'
	matches = re.compile(patron,re.DOTALL).findall(data)
	anyadevideos(matches)

	# --------------------------------------------------------
	# Extrae los videos del resto de páginas
	# --------------------------------------------------------
	patronpaginas = '\?page=(\d+)'
	paginas = re.compile(patronpaginas,re.DOTALL).findall(data)
	#logFile.debug("*** Paginas siguientes")
	#logFile.debug(paginas)

	# Hay al menos otra página
	if len(paginas)>0:
		pagina = paginas[ len(paginas)-1 ]
		xbmc.output("***")
		xbmc.output("*** Pagina " + pagina)
		xbmc.output("***")

		urlpagina = '%s?page=%s' % (url , pagina)
		xbmc.output("urlpagina="+urlpagina)

		# Abre la segunda página
		xbmc.output("[rtve.py] videolist descarga página "+pagina+" "+url)
		datapagina = scrapertools.cachePage(urlpagina)
		
		#extrae los vídeos
		matches = re.compile(patron,re.DOTALL).findall(datapagina)
		anyadevideos(matches)

		# siguiente página
		paginas = re.compile(patronpaginas,re.DOTALL).findall(datapagina)
		xbmc.output("*** Paginas siguientes")
		#xbmc.output(paginas)
		
		while len(paginas)>1:
			pagina = paginas[ len(paginas)-1 ]
			xbmc.output("***")
			xbmc.output("*** Pagina " + pagina)
			xbmc.output("***")
			urlpagina = '%s?page=%s' % (url , pagina)
			xbmc.output("urlpagina="+urlpagina)

			xbmc.output("[rtve.py] videolist descarga página "+pagina+" "+url)
			datapagina = scrapertools.cachePage(urlpagina)

			#extrae los vídeos
			matches = re.compile(patron,re.DOTALL).findall(datapagina)
			anyadevideos(matches)

			paginas = re.compile(patronpaginas,re.DOTALL).findall(datapagina)
			xbmc.output("*** Paginas siguientes")
			#xbmc.output(paginas)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def anyadevideos(matches):
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Datos
		patron = "Emitido:\s+([^\s]+)\s+\[\s+(\d+)\s+\:\s+(\d+)"
		fechahora = re.compile(patron,re.DOTALL).findall(match[5])
		scrapedtitle = match[3] + " ("+fechahora[0][0]+") (" + fechahora[0][1]+"'"+fechahora[0][2]+"s)"
		scrapedurl = "http://www.rtve.es/alacarta/player/%s.xml" % match[0]

		scrapedthumbnail = "http://www.rtve.es%s" % match[2]
		scrapedplot = match[4]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

def play(params,url,category):
	xbmc.output("[rtve.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[rtve.py] thumbnail="+thumbnail)

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del vídeo...', title )

	# --------------------------------------------------------
	# Descarga pagina detalle
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	patron = '<location>([^<]+)</location>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	try:
		url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
	except:
		url = ""
	xbmc.output("[rtve.py] url="+url)

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   
