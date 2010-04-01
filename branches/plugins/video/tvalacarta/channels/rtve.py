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
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
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
		scrapedtitle = scrapertools.entityunescape(match[1])
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
		scrapedtitle = scrapertools.entityunescape(match[3] + " ("+fechahora[0][0]+") (" + fechahora[0][1]+"'"+fechahora[0][2]+"s)")
		scrapedurl = "http://www.rtve.es/alacarta/player/%s.xml" % match[0]

		scrapedthumbnail = "http://www.rtve.es%s" % match[2]
		scrapedplot = scrapertools.entityunescape(match[4])

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
'''
def play(params,url,category):
	xbmc.output("[rtve.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

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
		#url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
		url = matches[0]
	except:
		url = ""
	xbmc.output("[rtve.py] url="+url)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
'''
def play(params,url,category):
	xbmc.output("[rtve.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

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
		#url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
		url = matches[0]
	except:
		url = ""
	xbmc.output("[rtve.py] url="+url)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	'''
	flvstreamer  -r "rtmp://stream.rtve.es/stream/resources/alacarta/flv/5/3/1270074791935.flv" -o out.flv
	FLVStreamer v1.7
	(c) 2009 Andrej Stepanchuk, license: GPL
	DEBUG: Parsing...
	DEBUG: Parsed protocol: 0
	DEBUG: Parsed host    : stream.rtve.es
	DEBUG: Parsed app     : stream/resources
	DEBUG: Parsed playpath: alacarta/flv/5/3/1270074791935
	DEBUG: Setting buffer time to: 36000000ms
	Connecting ...
	DEBUG: Protocol : RTMP
	DEBUG: Hostname : stream.rtve.es
	DEBUG: Port     : 1935
	DEBUG: Playpath : alacarta/flv/5/3/1270074791935
	DEBUG: tcUrl    : rtmp://stream.rtve.es:1935/stream/resources
	DEBUG: app      : stream/resources
	DEBUG: flashVer : LNX 9,0,124,0
	DEBUG: live     : no
	DEBUG: timeout  : 300 sec
	DEBUG: Connect, ... connected, handshaking
	DEBUG: HandShake: Type Answer   : 03
	DEBUG: HandShake: Server Uptime : 1463582178
	DEBUG: HandShake: FMS Version   : 3.5.2.1
	DEBUG: Connect, handshaked
	Connected...
	'''
	#url=rtmp://stream.rtve.es/stream/resources/alacarta/flv/5/3/1270074791935.flv
	hostname = "stream.rtve.es"
	xbmc.output("[rtve.py] hostname="+hostname)
	portnumber = "1935"
	xbmc.output("[rtve.py] portnumber="+portnumber)
	tcurl = "rtmp://stream.rtve.es/stream/resources"
	xbmc.output("[rtve.py] tcurl="+tcurl)
	#playpath = "alacarta/flv/5/3/1270074791935"
	playpath = url[39:-4]
	xbmc.output("[rtve.py] playpath="+playpath)
	app = "stream/resources"
	xbmc.output("[rtve.py] app="+app)
	
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	#listitem.setProperty("SWFPlayer", "http://www.plus.es/plustv/carcasa.swf")
	listitem.setProperty("Hostname",hostname)
	listitem.setProperty("Port",portnumber)
	listitem.setProperty("tcUrl",tcurl)
	listitem.setProperty("Playpath",playpath)
	listitem.setProperty("app",app)
	listitem.setProperty("flashVer","LNX 9,0,124,0")
	listitem.setProperty("pageUrl","LNX 9,0,124,0")

	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   
