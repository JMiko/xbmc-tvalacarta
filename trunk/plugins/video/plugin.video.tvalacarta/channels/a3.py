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

	url = "http://www.antena3.com/ps3/canales/canales.xml"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<canal>[^<]+'
	patronvideos += '<indice><..CDATA.([^\]]+)\].></indice>[^<]+'
	patronvideos += '<nombre><..CDATA.([^\]]*)\].></nombre>[^<]+'
	patronvideos += '<imagen src="([^"]+)" alt="" />[^<]+'
	patronvideos += '<nombre2><..CDATA.([^\]]+)\].></nombre2>[^<]+'
	patronvideos += '<descripcion><..CDATA.([^\]]+)\].></descripcion>[^<]+'
	patronvideos += '</canal>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		try:
			scrapedtitle = unicode( match[3], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[3]
		
		scrapedurl = match[0]
		scrapedthumbnail = match[2]
		scrapedplot = match[4]
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[a3.py] videolist")

	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patron = '<urlVideoFlv><\!\[CDATA\[([^\]]+)\]\]></urlVideoFlv>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	baseflv = ""
	if len(matches)>0: baseflv = matches[0]
	xbmc.output("[a3.py] baseflv="+baseflv)

	# Extrae las entradas (carpetas)
	patron = '<urlVideoMp4><\!\[CDATA\[([^\]]+)\]\]></urlVideoMp4>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	basemp4 = ""
	if len(matches)>0: basemp4 = matches[0]
	xbmc.output("[a3.py] basemp4="+basemp4)

	# Extrae las entradas (carpetas)
	patron = '<multimedia[^>]+>(.*?)</multimedia>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		
		patronvideos  = '<archivoMultimedia>[^<]+'
		patronvideos += '<archivo><\!\[CDATA\[([^\]]+)\]\]></archivo>[^<]+'
		patronvideos += '<alt><\!\[CDATA\[([^\]]+)\]\]></alt>[^<]+'
		patronvideos += '</archivoMultimedia>'
		matchesvideos = re.compile(patronvideos,re.DOTALL).findall(match)
		if DEBUG: scrapertools.printMatches(matches)

		for matchvideos in matchesvideos:
			scrapedtitle = matchvideos[1]
			scrapedurl = basemp4+matchvideos[0]
			scrapedthumbnail = ""
			scrapedplot = ""
			if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
			xbmctools.addnewvideo( CHANNELCODE , "play" , category , "Directo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[a3.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	if url.startswith("rtmp"):
		# Playlist vacia
		playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		playlist.clear()

		'''
		C:\util\rtmpdump-2.2>rtmpdump.exe -V -r "rtmp://antena3tvfs.fplive.net/antena3tv/ps3/doctormateo/Mateo-Temp3-cap5-parte1.mp4" -o out.mp4
		RTMPDump v2.2
		(c) 2010 Andrej Stepanchuk, Howard Chu, The Flvstreamer Team; license: GPL
		DEBUG: Parsing...
		DEBUG: Parsed protocol: 0
		DEBUG: Parsed host    : antena3tvfs.fplive.net
		DEBUG: Parsed app     : antena3tv/ps3
		DEBUG: Protocol : RTMP
		DEBUG: Hostname : antena3tvfs.fplive.net
		DEBUG: Port     : 1935
		DEBUG: Playpath : mp4:doctormateo/Mateo-Temp3-cap5-parte1
		DEBUG: tcUrl    : rtmp://antena3tvfs.fplive.net:1935/antena3tv/ps3
		DEBUG: swfUrl   : (null)
		DEBUG: pageUrl  : (null)
		DEBUG: app      : antena3tv/ps3
		DEBUG: auth     : (null)
		DEBUG: subscribepath : (null)
		DEBUG: flashVer : WIN 10,0,22,87
		DEBUG: live     : no
		'''
		#url=rtmp://antena3tvfs.fplive.net/antena3tv/ps3/doctormateo/Mateo-Temp3-cap5-parte1.mp4
		hostname = "antena3tvfs.fplive.net"
		xbmc.output("[a3.py] hostname="+hostname)
		portnumber = "1935"
		xbmc.output("[a3.py] portnumber="+portnumber)
		tcurl = "rtmp://antena3tvfs.fplive.net/antena3tv/ps3"
		xbmc.output("[a3.py] tcurl="+tcurl)
		#playpath = "mp4:doctormateo/Mateo-Temp3-cap5-parte1"
		playpath = "mp4:"+url[44:-4]
		xbmc.output("[a3.py] playpath="+playpath)
		app = "antena3tv/ps3"
		xbmc.output("[a3.py] app="+app)
		
		listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
		#listitem.setProperty("SWFPlayer", "http://www.plus.es/plustv/carcasa.swf")
		listitem.setProperty("Hostname",hostname)
		listitem.setProperty("Port",portnumber)
		listitem.setProperty("tcUrl",tcurl)
		listitem.setProperty("Playpath",playpath)
		listitem.setProperty("app",app)
		listitem.setProperty("flashVer","WIN 10,0,22,87")

		listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
		playlist.add( url, listitem )

		# Reproduce
		xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
		xbmcPlayer.play(playlist)   
	elif url.startswith("http"):
		xbmctools.playvideo(CHANNELNAME,"Directo",url,category,title,thumbnail,plot)
	else:
		xbmctools.alertnodisponible()