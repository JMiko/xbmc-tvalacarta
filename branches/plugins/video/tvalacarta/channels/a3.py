# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para antena3videos.com
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmctools
import scrapertools
import binascii

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[a3.py] init")

DEBUG = True
CHANNELNAME = "Antena3"
CHANNELCODE = "a3"

def mainlist(params,url,category):
	xbmc.output("[a3.py] mainlist")
	#videolist(params,"http://www.antena3videos.com/cooliris.rss",category)

	url = "http://www.antena3videos.com/cooliris.rss"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos = '<item>[^<]+<title><\!\[CDATA\[([^\]]+)\]\]></title>[^<]+<link>([^<]+)</link>[^<]+<description><\!\[CDATA\[([^\]]+)\]\]></description>[^<]+<media:thumbnail url=\'([^\']+)\'/>[^<]+<media:content type=\'([^\']+)\' url=\'([^\']+)\'/>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	encontrados = set()

	for match in matches:
		# Titulo de la serie
		try:
			scrapedtitle = unicode( match[0], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[0]
		xbmc.output("[a3.py] mainlist scrapedtitle="+scrapedtitle)
		
		patrontitulo = '(.*?)-'
		matchestitulo = re.compile(patrontitulo,re.DOTALL).findall(scrapedtitle)
		
		if len(matchestitulo)>0:
			scrapedtitle = matchestitulo[0].strip()

		xbmc.output("[a3.py] mainlist scrapedtitle="+scrapedtitle)

		if scrapedtitle not in encontrados:
			xbmc.output("[a3.py] mainlist   nueva serie "+scrapedtitle)
			encontrados.add(scrapedtitle)

			# URL
			scrapedurl = url
			
			# Thumbnail
			scrapedthumbnail = urlparse.urljoin("http://www.antena3videos.com",match[3])
			
			scrapedplot = ""

			# Depuracion
			if (DEBUG):
				xbmc.output("scrapedtitle="+scrapedtitle)
				xbmc.output("scrapedurl="+scrapedurl)
				xbmc.output("scrapedthumbnail="+scrapedthumbnail)

			# Añade al listado de XBMC
			xbmctools.addnewfolder( CHANNELCODE , "videolist" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
			#addvideodescripcionthumbnail( scrapedtitle , scrapeddescription, scrapedthumbnail, scrapedurl , category , len(matches) )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def videolist(params,url,category):
	xbmc.output("[a3.py] videolist")

	# El título es el de la serie
	title = urllib.unquote_plus( params.get("title") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos = '<item>[^<]+<title><\!\[CDATA\[([^\]]+)\]\]></title>[^<]+<link>([^<]+)</link>[^<]+<description><\!\[CDATA\[([^\]]+)\]\]></description>[^<]+<media:thumbnail url=\'([^\']+)\'/>[^<]+<media:content type=\'([^\']+)\' url=\'([^\']+)\'/>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[0], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[0]

		# Sólo añade los de la serie elegida
		if scrapedtitle.startswith(title):
			# URL
			scrapedurl = urlparse.urljoin("http://www.antena3videos.com",urllib.unquote(match[5]))
			
			# Thumbnail
			scrapedthumbnail = urlparse.urljoin("http://www.antena3videos.com",match[3])
			
			# procesa el resto
			try:
				scrapeddescription = unicode( match[2], "utf-8" ).encode("iso-8859-1")
			except:
				scrapeddescription = match[2]
				
			# Depuracion
			if (DEBUG):
				xbmc.output("scrapedtitle="+scrapedtitle)
				xbmc.output("scrapedurl="+scrapedurl)
				xbmc.output("scrapedthumbnail="+scrapedthumbnail)

			# Añade al listado de XBMC
			addvideodescripcionthumbnail( scrapedtitle , scrapeddescription, scrapedthumbnail, scrapedurl , category , len(matches) )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[a3.py] play")

	# Titulo
	infotitle = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	#xbmc.output("[a3.py] infotitle="+infotitle)
	
	# Averigua la descripcion (plot)
	infoplot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	#xbmc.output("[a3.py] infoplot="+infoplot)

	# Averigua el thumbnail
	infothumbnail = unicode( xbmc.getInfoLabel( "ListItem.Thumb" ), "utf-8" )
	xbmc.output("[a3.py] infothumbnail="+infothumbnail)

	# Averigua la URL del video
	mediaurl = url
	xbmc.output("[a3.py] mediaurl="+mediaurl)

	# Abre dialogo
	#dialogWait = xbmcgui.DialogProgress()
	#dialogWait.create( 'Descargando datos del vídeo...', infotitle )

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( infotitle, iconImage="DefaultVideo.png", thumbnailImage=infothumbnail )
	listitem.setInfo( "video", { "Title": infotitle, "Plot" : infoplot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( mediaurl, listitem )

	# Cierra dialogo
	#dialogWait.close()
	#del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   

def addfolder(nombre,url,accion):
	xbmc.output('[a3.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=%s&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , CHANNELCODE , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category):
	xbmc.output('[a3.py] addvideo( "'+nombre+'" , "' + url + '" , "'+category+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=%s&action=play&category=%s&url=%s' % ( sys.argv[ 0 ] , CHANNELCODE , category , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addvideodescripcionthumbnail(nombre,descripcion,thumbnail,url,category,totalitems):
	xbmc.output('[a3.py] addvideo( "'+nombre+'" , "' + url + '" , "'+category+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : descripcion } )
	itemurl = '%s?channel=%s&action=play&category=%s&url=%s' % ( sys.argv[ 0 ] , CHANNELCODE , category , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False, totalItems=totalitems)

def addvideodirecto(nombre,url,category):
	xbmc.output('[a3.py] addvideodirecto( "'+nombre+'" , "' + url + '" , "'+category+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : "Emision en directo" } )
	itemurl = '%s?channel=%s&action=directplay&category=%s&url=%s' % ( sys.argv[ 0 ] , CHANNELCODE , category , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[a3.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	itemurl = '%s?channel=%s&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , CHANNELCODE , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)
