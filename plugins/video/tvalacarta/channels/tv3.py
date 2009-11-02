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

	xbmctools.addnewfolder( CHANNELCODE , "hdvideolist", CHANNELNAME , "Alta definici�"  , "http://www.tv3.cat/pprogrames/hd/mhdSeccio.jsp"                , "", "" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "S�ries"          , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=series"     , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TSERIES"    )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Actualitat"      , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=actualitat" , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TACTUALITA" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Esports"         , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=esports"    , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TESPORTS"   )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Cuina"           , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=cuina"      , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TCUINA"     )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Entretenimient"  , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=entretenim" , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TENTRETENI" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Divulgaci�"      , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=divulgacio" , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TDIVULGACI" )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Juvenil"         , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=juvenil"    , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TJUVENIL"   )
	xbmctools.addnewfolder( CHANNELCODE , "videolist1" , CHANNELNAME , "Infantil"        , "http://www.tv3.cat/ptv3/tv3VideosSeccio.jsp?seccio=infantil"   , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TINFANTIL"  )
	#xbmctools.addnewfolder( CHANNELCODE , "videolist"  , CHANNELNAME , "M�sica"          ,   , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TMUSICA"    )
	#xbmctools.addnewfolder( CHANNELCODE , "videolist"  , CHANNELNAME , "Gent TVC"        ,   , "", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TGENTTVC"   )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist1(params,url,category):
	xbmc.output("[tv3.py] videolist1")

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae el paginador
	# --------------------------------------------------------
	# La URL de la siguiente p�gina va en el campo "plot", que en estos casos est� vac�o
	plot = urllib.unquote_plus( params.get("plot") )
	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , "Siguiente" , plot , "" , "" )

	# --------------------------------------------------------
	# Extrae los v�deos
	# --------------------------------------------------------
	'''
	<li>
	<div class="img_p_txt_mes_a">

	<div class="img_left">
	<a href="/videos/1591929/Kromlog">
	<img src="/multimedia/jpg/1/4/1256905876941.jpg" class="w_petita" height="80"/>
	<img title="Play" alt="Play" src="/img/ico_play.gif" class="ico_play151"/>
	</a>
	</div>
	<div class="titulars1">
	<span class="avant">02/11/2009 - Club Super3</span>
	<br/>
	<h2>
	<a href="/videos/1591929/Kromlog">Kromlog</a>
	</h2>
	<p>Un ser d'un altre planeta visita la casa del Super3...</p>
	</div>

	</div>
	</li>
	<li>
	<div class="img_p_txt_mes_a">
	<div class="img_left">
	<a href="/videos/1591589/La-Claudia-i-els-peixos">
	<img src="/multimedia/jpg/1/6/1256897450661.jpg" class="w_petita" height="80"/>
	<img title="Play" alt="Play" src="/img/ico_play.gif" class="ico_play151"/>
	</a>
	</div>
	'''
	patron  = '<li>[^<]+'
	patron += '<div class="img_p_txt_mes_a">[^<]+'
	patron += '<div class="img_left">[^<]+'
	patron += '<a href="([^"]+)">[^<]+'
	patron += '<img src="([^"]+)"[^>]+>.*?'
	patron += '<div class="titulars1">[^<]+<span class="avant">([^<]+)</span>[^<]+<br/>[^<]+'
	patron += '<h2>[^<]+<a [^>]+>([^<]+)</a>[^<]+</h2>[^<]+'
	patron += '<p>([^<]+)</p>[^<]+</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		fecha = match[2][0:10]
		scrapedtitle = match[2][13:] + " - " + match[3] + " (" + fecha + ")"
		scrapedurl = "http://www.tv3.cat%s" % match[0]
		scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedplot = match[4]
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[tv3.py] videolist")

	# --------------------------------------------------------
	# Descarga la p�gina
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
	# Extrae los v�deos
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

		# A�ade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def hdvideolist(params,url,category):
	xbmc.output("[tv3.py] hdvideolist")

	# --------------------------------------------------------
	# Descarga la p�gina
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output("[tv3.py] hdvideolist descargado")
	data = data.replace("\\\"","")
	#xbmc.output("[tv3.py] hdvideolist reemplazado")
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los programas
	# --------------------------------------------------------
	#addItemToVideoList( 0, 
	# 0 "Ana Maria Matute: \"making of\"", 
	# 1 "1427429", 
	# 2 "http://hd.tv3.cat/720/SAVIS_INTERNET_MATUTE_MAKIN_TV3H264_720.mp4" , 
	# 3 "http://hd.tv3.cat/1080/SAVIS_INTERNET_MATUTE_MAKIN_TV3H264_1080.mp4" , 
	# 4 "http://www.tv3.cat/multimedia/jpg/5/4/1253613702545.jpg", 
	# 5 "http://www.tv3.cat/multimedia/jpg/5/4/1253613702545.jpg", 
	# 6 "http://www.tv3.cat/multimedia/jpg/5/4/1253613702545.jpg", 
	# 7 "\"Making of\" del cap�tol de Savis on s'entrevista a Ana Mar�a Matute. Enregistrat al Castell Santa Florentina." , 
	# 8 "0:58" , 
	# 9 " mgb.", 
	#10 " mgb.", 
	#11 "Savis", "http://www.tv3.cat/multimedia/gif/0/5/1250763975650.gif", "http://www.tv3.cat/multimedia/gif/2/9/1250763944192.gif", "Documental" , "http://www.tv3.cat/programa/11605" , "http://www.tv3.cat/multimedia/jpg/5/0/1253613661005.jpg" , "Web de programa", "20091019");
	patron  = 'addItemToVideoList\([^\,]+, "([^"]+)", "([^"]+)", "([^"]+)" , "([^"]+)" , "([^"]+)", "([^"]+)", "([^"]+)", "([^"]+)" , "([^"]+)" , "([^"]+)", "([^"]+)", "([^"]+)", "([^"]+)", "([^"]+)", "([^"]+)" , "([^"]+)" , "([^"]+)" , "([^"]+)", "([^"]+)"\)\;'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[11] + " - " + match[0] + " (" + match[8] + ")"
		# 720 es el 2, 1080 es el 3
		scrapedurl = ""
		scrapedthumbnail = match[4]
		scrapedplot = match[7]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade el video en 720p
		scrapedurl = match[2].replace(" ","%20")
		xbmctools.addnewvideo( CHANNELCODE , "directplay" , CHANNELNAME , "" , scrapedtitle + " (720p)" , scrapedurl , scrapedthumbnail, scrapedplot )
		scrapedurl = match[3].replace(" ","%20")
		xbmctools.addnewvideo( CHANNELCODE , "directplay" , CHANNELNAME , "" , scrapedtitle + " (1080p)" , scrapedurl , scrapedthumbnail, scrapedplot )

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
	dialogWait.create( 'Descargando datos del v�deo...', title )

	# --------------------------------------------------------
	# Saca el codigo de la URL y descarga
	# --------------------------------------------------------
	patron = "/videos/(\d+)/"
	matches = re.compile(patron,re.DOTALL).findall(url)
	scrapertools.printMatches(matches)
	codigo = matches[0]

	# Prueba con el modo 1
	url = geturl1(codigo)
	if url=="":
		url = geturl2(codigo)
	
	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   

def geturl1(codigo):
	#http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID=1594629&QUALITY=H&FORMAT=FLVGES&RP=www.tv3.cat&rnd=796474
	dataurl = "http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="+codigo+"&QUALITY=H&FORMAT=FLV&rnd=481353"
	xbmc.output("[tv3.py] geturl1 dataurl="+dataurl)
	
	req = urllib2.Request(dataurl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	xbmc.output("data="+data)

	patron = "(rtmp://[^\?]+)\?"
	matches = re.compile(patron,re.DOTALL).findall(data)
	url = ""
	if len(matches)>0:
		url = matches[0]
		url = url.replace('rtmp://flv-500-str.tv3.cat/ondemand/g/','http://flv-500.tv3.cat/g/')
	xbmc.output("url="+url)
	return url

def geturl2(codigo):
	#http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID=1594629&QUALITY=H&FORMAT=FLVGES&RP=www.tv3.cat&rnd=796474
	dataurl = "http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="+codigo+"&QUALITY=H&FORMAT=FLVGES&RP=www.tv3.cat&rnd=796474"
	xbmc.output("[tv3.py] geturl2 dataurl="+dataurl)
	
	req = urllib2.Request(dataurl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	xbmc.output("data="+data)

	patron = "(rtmp://[^\?]+)\?"
	matches = re.compile(patron,re.DOTALL).findall(data)
	url = ""
	if len(matches)>0:
		url = matches[0]
		url = url.replace('rtmp://flv-es-500-str.tv3.cat/ondemand/g/','http://flv-500-es.tv3.cat/g/')
	xbmc.output("url="+url)
	return url

def directplay(params,url,category):
	xbmc.output("[tv3.py] directplay")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[tv3.py] thumbnail="+thumbnail)

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Descargando datos del v�deo...', title )

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la a�ade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : CHANNELNAME , "Genre" : category } )
	playlist.add( url, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	# Reproduce
	xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
	xbmcPlayer.play(playlist)   
