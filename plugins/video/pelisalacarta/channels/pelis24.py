# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
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

CHANNELNAME = "pelis24"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[pelis24.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[pelis24.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "list", category , "Peliculas","http://pelis24.com/peliculas/","","")
	xbmctools.addnewfolder( CHANNELNAME , "list", category , "Peliculas VOSE","http://pelis24.com/peliculasvose/","","")
	xbmctools.addnewfolder( CHANNELNAME , "list", category , "Series","http://pelis24.com/series/","","")
	xbmctools.addnewfolder( CHANNELNAME , "list", category , "Novedades","http://pelis24.com/","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def list(params,url,category):
	xbmc.output("[pelis24.py] list")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	'''
	<div class="yjnewsflash_title"><a href="http://www.pelis24.com/estrenos/727-donde-viven-los-monstruos-espanol-online.html">Donde viven los monstruos Español Online</a> </div>
	<p><br>
	<br>
	<div id='news-id-727'><!--TBegin--><a href="http://www.pelis24.com/uploads/posts/2009-12/1261192166_dondevivenlosmonstruoscine-300a.jpg" onclick="return hs.expand(this)" ><img align="left" src="http://www.pelis24.com/uploads/posts/2009-12/thumbs/1261192166_dondevivenlosmonstruoscine-300a.jpg" alt='Donde viven los monstruos Español Online' title='Donde viven los monstruos Español Online'  /></a><!--TEnd-->Max, un niño muy inteligente, incomprendido y rebelde, se escapa de casa tras una fuerte discusión con su madre. Pero no es una huida cualquiera, pues Max se interna en un bosque misterioso creado por su propia imaginación. Su objetivo: llegar a la tierra de unas extraordinarias criaturas, un lugar donde podrá hacer travesuras para siempre.</div><span class="yjnewsflash_date">Hoy, 04:11 | <a href="http://www.pelis24.com/estrenos/">Estrenos</a> | </span></p>
	<div class="linksw"><br /><a href="http://www.pelis24.com/estrenos/727-donde-viven-los-monstruos-espanol-online.html#comment"><img src="/templates/Pelis/img/com.png" border="0" />Comentarios (4)</a> &nbsp;<a href="http://www.pelis24.com/estrenos/727-donde-viven-los-monstruos-espanol-online.html"><img src="/templates/Pelis/images/arr2.png" width="13" height="9" border="0" /><strong>Ver Pelicula Online!</strong></a></div></div><div class="yjnewsflash">
	'''
	patron  = '<div class="yjnewsflash_title"><a href="([^"]+)">([^<]+)</a> </div>[^<]+'
	patron += '<p><br>[^<]+'
	patron += '<br>[^<]+'
	patron += '<div[^>]+><!--TBegin--><a href="([^"]+)".*?'
	patron += '<!--TEnd-->([^<]+)</div>' #,*?<a'#.*?<a href="([^"]+)">'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	'''
	<div class="yjnewsflash_title"><a href="http://www.pelis24.com/series/424-el-mentalista-espanol-online.html">El Mentalista Español Temporada 1</a> </div>
	<p><br>
	<br>
	<div id='news-id-424'><div align="center"><img src="http://i40.tinypic.com/33392ck.jpg" style="border: none;" alt='El Mentalista Español Temporada 1' title='El Mentalista Español Temporada 1' /><br /><br />La historia de El Mentalista comienza cuando Patrick Jane, un hombre que se ganaba la vida como médium televisivo, sufre un duro golpe al perder a su mujer y su hija a manos de un asesino. A partir de ese momento, Patrick Jane toma la determinación de dedicarse de lleno a sus habilidades como detective y trabajar en el Departamento de Investigación de Crímenes de California en la resolución de los casos de asesinato. Él no ve, observa. No oye, escucha. No toca, percibe. No falla.</div></div><span class="yjnewsflash_date">9 enero 2009 | <a href="http://www.pelis24.com/series/">Series</a> | </span></p>
	<div class="linksw"><br /><a href="http://www.pelis24.com/series/424-el-mentalista-espanol-online.html#comment"><img src="/templates/Pelis/img/com.png" border="0" />Comentarios (7)</a> &nbsp;<a href="http://www.pelis24.com/series/424-el-mentalista-espanol-online.html"><img src="/templates/Pelis/images/arr2.png" width="13" height="9" border="0" /><strong>Ver Pelicula Online!</strong></a></div></div><div class="yjnewsflash">
	'''
	patron  = '<div class="yjnewsflash_title"><a href="([^"]+)">([^<]+)<.*?'
	patron  = '<div class="yjnewsflash_title"><a href="([^"]+)">([^<]+)</a> </div>[^<]+'
	patron += '<p><br>[^<]+'
	patron += '<br>[^<]+'
	patron += '<div[^>]+><div[^>]+><img src="([^"]+)".*?>([^<]+)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Extrae la entrada para la siguiente página
	patronvideos  = '<div id="right"><a href="([^"]+)">Siguiente P.gina</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = "!Página siguiente"

		# URL
		scrapedurl = match
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "list" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapeddescription )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
	xbmc.output("[pelis24.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, o a los capítulos de las series...
	# ------------------------------------------------------------------------------------

	xbmc.output("Busca el enlace de página siguiente...")
	try:
		# La siguiente página
		patronvideos  = '<a href="([^"]+)">Sigu'
		matches = re.compile(patronvideos,re.DOTALL).findall(data)
		for match in matches:
			xbmctools.addnewfolder( CHANNELNAME , "list", category , "!Página siguiente",urlparse.urljoin(url,match),"","")
	except:
		xbmc.output("No encuentro la pagina...")

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a videos directos
	# ------------------------------------------------------------------------------------

	patronvideos  = "url:'([^']+)'"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	for match in matches:
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title +" - [Directo]", match, thumbnail , "" )

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)
	
	for video in listavideos:
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , video[2] , title +" - "+video[0], video[1], thumbnail , "" )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[pelis24.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
