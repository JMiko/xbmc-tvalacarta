# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para TV3
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

xbmc.output("[tv3.py] init")

DEBUG = True
CHANNELNAME = "TV3"
CHANNELCODE = "tv3"

def mainlist(params,url,category):
	xbmc.output("[tv3.py] mainlist")

	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Sèries"          , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TSERIES"      , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Actualitat"      , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TACTUALITA"   , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Esports"         , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TESPORTS"     , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Cuina"           , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TCUINA"       , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Entretenimient"  , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TENTRETENI"   , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Divulgació"      , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TDIVULGACI"   , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Juvenil"         , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TJUVENIL"     , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Infantil"        , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TINFANTIL"    , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Música"          , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TMUSICA"      , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Gent TVC"        , "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TGENTTVC"     , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[tv3.py] videolist")

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae el paginador
	# --------------------------------------------------------
	# Desde que numero debe empezar
	patron = "javascript:send\('frmSearcher',(\d+)\)"
	numeros = re.compile(patron,re.DOTALL).findall(data)

	#<input type="hidden" name="acat" value="TINFANTIL"/>
	patron = '<input type="hidden" name="acat" value="([^"]+)"'
	categoria = re.compile(patron,re.DOTALL).findall(data)

	#<input type="hidden" name="endDate" value="01/02/2009"/>
	patron = '<input type="hidden" name="endDate" value="([^"]+)"'
	fecha = re.compile(patron,re.DOTALL).findall(data)

	# Si hay 2, coger el primero
	# Si hay 4, coger los dos primeros
	if len(numeros) == 2:
		xbmc.output("hay 2 paginadores")
		txthiStartValue = numeros[0]
		urlpaginador = "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + txthiStartValue + "&hiTarget=searchingVideos.jsp&acat=" + categoria[0] + "&hiCategory=VID&textBusca=&startDate=&endDate=" + fecha[0].replace("/","%2F")
		xbmc.output(urlpaginador)
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Siguiente" , urlpaginador , "" , "" )
	else:
		xbmc.output("hay 4 paginadores")
		'''
		txthiStartValue = numeros[0]
		urlpaginador = "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + txthiStartValue + "&hiTarget=searchingVideos.jsp&acat=" + categoria[0] + "&hiCategory=VID&textBusca=&startDate=&endDate=" + fecha[0].replace("/","%2F")
		xbmc.output(urlpaginador)
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Anterior" , urlpaginador , "" , "" )
		'''
		txthiStartValue = numeros[1]
		urlpaginador = "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + txthiStartValue + "&hiTarget=searchingVideos.jsp&acat=" + categoria[0] + "&hiCategory=VID&textBusca=&startDate=&endDate=" + fecha[0].replace("/","%2F")
		xbmc.output(urlpaginador)
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Siguiente" , urlpaginador , "" , "" )

	# --------------------------------------------------------
	# Extrae los vídeos
	# --------------------------------------------------------
	patron = '<li>\W*<div class="img_p_txt_mes_a">\W*<div class="img_left">\W*<a title="(?:")?[^"]+"(?:")? href="([^"]+)">\W*<img src="([^"]+)" [^>]+>\W*</a>\W*<a href="#"></a>\W*</div>\W*<div class="titulars1">\W*<span class="avant">([^<]+)</span>\W*<br />\W*<h2>\W*<a [^>]+>([^<]+)</a>\W*</h2>\W*<p>([^<]+)</p>\W*</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		fecha = match[2][-10:]
		scrapedtitle = match[2][0:-13] + " - " + match[3] + " (" + fecha + ")"
		scrapedurl = "http://www.tv3.cat%s" % match[0]
		scrapedthumbnail = match[1]
		scrapedplot = match[4]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[tv3.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[tv3.py] thumbnail="+thumbnail)

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del vídeo...', title )

	# --------------------------------------------------------
	# Saca el codigo de la URL y descarga
	# --------------------------------------------------------
	patron = "/videos/(\d+)/"
	matches = re.compile(patron,re.DOTALL).findall(url)
	scrapertools.printMatches(matches)
	codigo = matches[0]

	req = urllib2.Request("http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="+codigo+"&QUALITY=H&FORMAT=FLV&rnd=481353")
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	#xbmc.output("data="+data)

	patron = "(rtmp://[^\?]+)\?"
	matches = re.compile(patron,re.DOTALL).findall(data)

	url = matches[0]
	url = url.replace('rtmp://flv-500-str.tv3.cat/ondemand/g/','http://flv-500.tv3.cat/g/')
	xbmc.output("url="+url)
	
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
