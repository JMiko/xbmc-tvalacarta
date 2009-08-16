# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools

CHANNELNAME = "peliculasyonkis"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[peliculasyonkis.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[peliculasyonkis.py] mainlist")

	# Añade al listado de XBMC
	addfolder("Últimas películas","http://www.peliculasyonkis.com/ultimas-peliculas.php","listnovedades")
	addfolder("Listado por categorias","http://www.peliculasyonkis.com/","listcategorias")
	addfolder("Listado alfabético","http://www.peliculasyonkis.com/","listalfabetico")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetico(params, url, category):
	addfolder("0-9","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasNumeric.php","listvideos")
	addfolder("A","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasA.php","listvideos")
	addfolder("B","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasB.php","listvideos")
	addfolder("C","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasC.php","listvideos")
	addfolder("D","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasD.php","listvideos")
	addfolder("E","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasE.php","listvideos")
	addfolder("F","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasF.php","listvideos")
	addfolder("G","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasG.php","listvideos")
	addfolder("H","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasH.php","listvideos")
	addfolder("I","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasI.php","listvideos")
	addfolder("J","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasJ.php","listvideos")
	addfolder("K","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasK.php","listvideos")
	addfolder("L","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasL.php","listvideos")
	addfolder("M","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasM.php","listvideos")
	addfolder("N","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasN.php","listvideos")
	addfolder("O","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasO.php","listvideos")
	addfolder("P","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasP.php","listvideos")
	addfolder("Q","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasQ.php","listvideos")
	addfolder("R","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasR.php","listvideos")
	addfolder("S","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasS.php","listvideos")
	addfolder("T","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasT.php","listvideos")
	addfolder("U","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasU.php","listvideos")
	addfolder("V","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasV.php","listvideos")
	addfolder("W","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasW.php","listvideos")
	addfolder("X","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasX.php","listvideos")
	addfolder("Y","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasY.php","listvideos")
	addfolder("Z","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasZ.php","listvideos")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listnovedades(params,url,category):
	xbmc.output("[peliculasyonkis.py] listnovedades")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<td align=\'center\'><center><span style=\'font-size: 0.7em\'><a href="([^"]+)" title="([^"]+)"><img.*?src=\'([^\']+)\'[^>]+>.*?<img src="(http://images.peliculasyonkis.com/images/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , "detail" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listcategorias(params,url,category):
	xbmc.output("[peliculasyonkis.py] listcategorias")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<li class="page_item"><a href="(http\://www.peliculasyonkis.com/genero/[^"]+)"[^>]+>([^<]+)</a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[0]
		
		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , "listvideos" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


def listvideos(params,url,category):
	xbmc.output("[peliculasyonkis.py] listvideos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = "<a href='([^']+)'>Siguiente &gt;&gt;</a>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = "#Siguiente"

		# URL
		scrapedurl = match
		
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
		addfolder( scrapedtitle , scrapedurl , "listvideos" )

	# Extrae las entradas (carpetas)
	patronvideos  = '<li>[^<]+<a href="([^"]+)" title="([^"]+)"><img.*?src="([^"]+)"[^>]+>.*?<span[^>]+>(.*?)<img.*?src="([^"])+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapeddescription = match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , "detail" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
	xbmc.output("[peliculasyonkis.py] detail")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	patronvideos  = 'href="(http://www.peliculasyonkis.com/player/visor_pymeno2.php[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	data = scrapertools.cachePage('http://www.atrapavideo.com/es/videomonkey/yonkis/url='+matches[0])
	addvideo( "Ver el vídeo" , data , category , "Megavideo" )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

'''
def play(params,url,category):
	xbmc.output("[peliculasyonkis.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[peliculasyonkis.py] thumbnail="+thumbnail)
	xbmc.output("[peliculasyonkis.py] server="+server)
	
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title )

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Averigua la URL del vídeo
	mediaurl=servertools.findurl(url,server)
	xbmc.output("[peliculasyonkis.py] mediaurl="+mediaurl)

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : "peliculasyonkis.us" , "Genre" : category } )
	playlist.add( mediaurl, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   
'''

def play(params,url,category):
	xbmc.output("[peliculasyonkis.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[peliculasyonkis.py] thumbnail="+thumbnail)
	xbmc.output("[peliculasyonkis.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def addfolder(nombre,url,accion):
	xbmc.output('[peliculasyonkis.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=peliculasyonkis&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category,server):
	xbmc.output('[peliculasyonkis.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=peliculasyonkis&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , urllib.quote_plus(url) , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[peliculasyonkis.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	itemurl = '%s?channel=peliculasyonkis&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

#mainlist(None,"","mainlist")
#listnovedades(None,"http://www.peliculasyonkis.com/ultimas-peliculas.php","")
#listcategorias(None,"http://www.peliculasyonkis.com/","")
#listvideos(None,"http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasG.php","")
#detail(None,"http://www.peliculasyonkis.com/pelicula/guerra-de-novias-bride-wars2009/","")
