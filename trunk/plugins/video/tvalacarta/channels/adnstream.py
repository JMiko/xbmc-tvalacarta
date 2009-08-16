# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para adnstream
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

DEBUG = True
CHANNELNAME = "ADNStream"
CHANNELCODE = "adnstream"

MAINURL = 'http://www.adnstream.tv/canales.php'

def mainlist(params,url,category):
	xbmc.output("[adnstream.py] mainlist")
	videolist(params,MAINURL,category)

def videolist(params,url,category):
	xbmc.output("[adnstream.py] videolist")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#print data

	# Extrae las entradas (carpetas)
	patronvideos  = '<channel title\="([^"]+)" media\:thumbnail\="([^"]+)" clean_name\="([^"]+)"></channel>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[0], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[0]
			
		scrapeddescription = ""

		# URL
		scrapedurl = MAINURL+'?c='+match[2]
		
		# Thumbnail
		scrapedthumbnail = match[1]
		
		# Depuracion
		if (DEBUG):
			print "scrapedtitle="+scrapedtitle
			print "scrapedurl="+scrapedurl
			print "scrapedthumbnail="+scrapedthumbnail

		# Añade al listado de XBMC
		listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
		itemurl = '%s?channel=adnstream&action=videolist&category=%s&url=%s' % ( sys.argv[ 0 ] , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, totalItems=len(matches), isFolder=True)

	# Extrae las entradas (Vídeos)
	patronpubli   = '<item>[^<]+<guid>[^<]+</guid>[^<]+<title>[^<]+</title>[^<]+<description />[^<]+<enclosure type="[^"]+" url="([^"]+)"/>[^<]+<link />[^<]+<category>preroll</category>.*?'
	patronvideos  = '<item>[^<]+<guid>([^<]+)</guid>[^<]+<title>([^<]+)</title>[^<]+<description>([^<]+)</description>[^<]+<enclosure type="([^"]+)" url="([^"]+)"/>[^<]+<media\:thumbnail type="[^"]+" url="([^"]+)"/>'
	matches = re.compile(patronpubli+patronvideos,re.DOTALL).findall(data)
	if (DEBUG):
		scrapertools.printMatches(matches)

	for match in matches:
		# Video page
		scrapedad = match[0]
		
		# Title
		try:
			scrapedtitle = unicode( match[2], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2]

		try:
			scrapeddescription = unicode( match[3], "utf-8" ).encode("iso-8859-1")
		except:
			scrapeddescription = match[3]

		# Video page
		scrapedurl = match[5]
		
		# Thumb
		scrapedthumbnail = match[6]
		
		# Debug info...
		if (DEBUG) :
			print "scrapedad="+scrapedad
			print "scrapedtitle="+scrapedtitle
			print "scrapeddescription="+scrapeddescription
			print "scrapedurl="+scrapedurl
			print "scrapedthumbnail="+scrapedthumbnail
		
		# Add to list...
		listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultVideo.png", thumbnailImage=scrapedthumbnail )
		listitem.setInfo( "video", { "Title" : scrapedtitle, "Plot" : scrapeddescription } )
		itemurl = '%s?channel=adnstream&action=play&category=%s&url=%s&ad=%s' % ( sys.argv[ 0 ] , params["category"] , urllib.quote_plus( scrapedurl ) , urllib.quote_plus( scrapedad ) )
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, totalItems=len(matches), isFolder=False)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
def play(params,url,category):
	xbmc.output("[adnstream.py] play")

	ad = urllib.unquote( params[ "ad" ] )
	print "ad = " + ad

	# Lee la categoría de la página
	if (params.has_key("category")):
		categoria = urllib.unquote_plus( params.get("category") )
	else:
		categoria='ADNStream'

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title )

	# Obtiene el anuncio preroll
	preroll = getpreroll(ad)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Playlist vacia
	launchplayer(preroll,url)
	'''
	if preroll!=None:
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		# Anade el anuncio al playlist
		print "Añadiendo publicidad "+preroll
		#listitem = xbmcgui.ListItem( "Publicidad", iconImage="DefaultVideo.png" )
		#listitem.setInfo( "video", { "Title": "Publicidad", "Studio" : "ADNStream" , "Genre" : categoria } )
		#playlist.add( preroll, listitem )
		# Reproduce
		xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
		xbmcPlayer.play(preroll)   

	while xbmcPlayer.isPlaying():
		print "is playing..."
		xbmc.sleep(2000)
	# Anade el video al playlist
	#if xbmcPlayer.isPlaying()
	print "Añadiendo video "+url
	#listitem2 = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	#listitem2.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : "ADNStream" , "Genre" : categoria } )
	#playlist.add( url, listitem2 )
	#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	#playlist.clear()
	#playlist.add( url )
	#xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(url)
	'''

def launchplayer(preroll,video):

	# Reproduce la publicidad
	if preroll!=None:
		print "Reproduciendo publicidad "+preroll
		xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
		xbmcPlayer.play(preroll)   

		while xbmcPlayer.isPlaying():
			#print "is playing..."
			xbmc.sleep(2000)
	
	# Reproduce el video
	print "Reproduciendo video "+video
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(video)

def getpreroll(url):
	print "url="+url
	data = scrapertools.cachePage(url)
	print "data="
	print data
	patronvideos  = 'publi=([^\|]+)\|\|\|'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	print "matches="
	if (DEBUG):
		scrapertools.printMatches(matches)

	location = None
	for match in matches:
		'''
		urladserver = match.replace("%26","&")
		print "urladserver="+urladserver
		req = urllib2.Request(urladserver)
		#req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		responseinfo = response.info()
		location = responseinfo.getheader("Location")
		print "Location"
		print location
		print "responseinfo"
		print responseinfo
		data=response.read()
		print "headers"
		print response.headers
		response.close()
		#print data
		'''
		import httplib
		parsedurl = urlparse.urlparse(match)
		print "parsedurl=",parsedurl

		try:
			host = parsedurl.netloc
		except:
			host = parsedurl[1]
		print "host=",host

		try:
			query = parsedurl.path+"?"+parsedurl.query
		except:
			query = parsedurl[2]+"?"+parsedurl[4]
		print "query=",query

		import httplib
		conn = httplib.HTTPConnection(host)
		conn.request("GET", query)
		response = conn.getresponse()
		location = response.getheader("location")
		conn.close()
		
		print "location=",location

		if location!=None:
			print "Encontrado header location"
			if not location.endswith(".flv"):
				print "No es un flv, se ignora"
				location=None
		
	#location='http://backup.zappinternet.com/publi/flv/promo-cine-terror.flv'

	return location
