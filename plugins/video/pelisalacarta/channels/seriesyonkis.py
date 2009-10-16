# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesyonkis
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

CHANNELNAME = "seriesyonkis"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[seriesyonkis.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[seriesyonkis.py] mainlist")
	
	xbmctools.addnewfolder( CHANNELNAME , "lastepisodeslist" , category , "Últimos capítulos","http://www.seriesyonkis.com/ultimos-capitulos.php","","")
	xbmctools.addnewfolder( CHANNELNAME , "listalfabetico"   , category , "Listado alfabético","","","")
	xbmctools.addnewfolder( CHANNELNAME , "alltvserieslist"  , category , "Listado completo de series","http://www.seriesyonkis.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "allcartoonslist"  , category , "Listado completo de dibujos animados","http://www.seriesyonkis.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "allanimelist"     , category , "Listado completo de anime","http://www.seriesyonkis.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "search"           , category , "Buscar","","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[seriesyonkis.py] search")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.seriesyonkis.com/buscarSerie.php?s="+tecleado
			searchresults(params,searchUrl,category)

def searchresults(params,url,category):
	xbmc.output("[seriesyonkis.py] searchresults")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#<h2><li><a href="http://www.seriesyonkis.com/serie/house/" title="House"><img height="84" src="http://images.seriesyonkis.com/images/house.jpg" alt="House" align="right" /><div align="left"><strong>House</strong></div></a></h2><span style="font-size: 0.7em">Descripción: <h2 align="center"><u><strong><a href="http://www.seriesyonkis.com/serie/house/" title="House">Dr House</a></strong></u></h2>
	#<center><a href='http://tienda.seriesyonkis.com/house.htm'><img src='http://images.seriesyonkis.com/tienda/dr-house.gif' /></a></center>
	#Serie de TV (2004-Actualidad). 5 Nominaciones a los premios Emmy / Serie sobre un antipático médico especializado en enfermedades infecciosas. Gregory House es, seguramente, el mejor medico del Hospital, pero su carácter, rebeldía y su honestidad con los pacientes y su equipo le hacen único. Prefiere evitar el contacto directo con los pacientes, le interesa por encima de todo la investigación de las enfermedades. Además de no cumplir las normas, se niega a ponerse la bata de médico. Es adicto a los calmantes y a las series de hospitales, ¿contradictorio? No, es House. (FILMAFFINITY)<br /></span><br /><br /><br /><br /></li>
	#<h2><li><a href="http://www.seriesyonkis.com/serie/dollhouse/" title="Dollhouse"><img 
	
	patronvideos  = '<h2><li><a href="([^"]+)" title="([^"]+)"><img.*?src="([^"]+)".*?'
	patronvideos += '<span[^>]+>(.*?)</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "list" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetico(params, url, category):
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "0-9","http://www.seriesyonkis.com/lista-series/listaSeriesNumeric.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "A","http://www.seriesyonkis.com/lista-series/listaSeriesA.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "B","http://www.seriesyonkis.com/lista-series/listaSeriesB.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "C","http://www.seriesyonkis.com/lista-series/listaSeriesC.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "D","http://www.seriesyonkis.com/lista-series/listaSeriesD.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "E","http://www.seriesyonkis.com/lista-series/listaSeriesE.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "F","http://www.seriesyonkis.com/lista-series/listaSeriesF.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "G","http://www.seriesyonkis.com/lista-series/listaSeriesG.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "H","http://www.seriesyonkis.com/lista-series/listaSeriesH.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "I","http://www.seriesyonkis.com/lista-series/listaSeriesI.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "J","http://www.seriesyonkis.com/lista-series/listaSeriesJ.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "K","http://www.seriesyonkis.com/lista-series/listaSeriesK.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "L","http://www.seriesyonkis.com/lista-series/listaSeriesL.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "M","http://www.seriesyonkis.com/lista-series/listaSeriesM.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "N","http://www.seriesyonkis.com/lista-series/listaSeriesN.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "O","http://www.seriesyonkis.com/lista-series/listaSeriesO.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "P","http://www.seriesyonkis.com/lista-series/listaSeriesP.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "Q","http://www.seriesyonkis.com/lista-series/listaSeriesQ.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "R","http://www.seriesyonkis.com/lista-series/listaSeriesR.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "S","http://www.seriesyonkis.com/lista-series/listaSeriesS.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "T","http://www.seriesyonkis.com/lista-series/listaSeriesT.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "U","http://www.seriesyonkis.com/lista-series/listaSeriesU.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "V","http://www.seriesyonkis.com/lista-series/listaSeriesV.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "W","http://www.seriesyonkis.com/lista-series/listaSeriesW.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "X","http://www.seriesyonkis.com/lista-series/listaSeriesX.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "Y","http://www.seriesyonkis.com/lista-series/listaSeriesY.php","","")
	xbmctools.addnewfolder(CHANNELNAME , "listseriesthumbnails" , category , "Z","http://www.seriesyonkis.com/lista-series/listaSeriesZ.php","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listseriesthumbnails(params,url,category):
	xbmc.output("[seriesyonkis.py] listseriesthumbnails")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#<td><center><a href='http://www.seriesyonkis.com/serie/a-camara-super-lenta/' title='A cámara súper lenta'><img src='http://images.seriesyonkis.com/images/a-camara-super-lenta.jpg' alt='A cámara súper lenta'/><br />A cámara súper lenta</a></center></td>
	
	patronvideos  = "<td><center><a href='([^']+)' title='([^']+)'><img src='([^']+)'.*?</td>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "list" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def lastepisodeslist(params,url,category):
	xbmc.output("[seriesyonkis.py] lastepisodeslist")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#<div class="ficha" style="background:url(http://images.seriesyonkis.com/images/house.jpg) #000000 center top no-repeat"><a href="http://www.seriesyonkis.com/capitulo/house/capitulo-01/44647/" title="(y 6x2) Broken">House - 6x01 - (y 6x2) Broken</a><br /><br /><img src="http://images.peliculasyonkis.com/images/tmegavideo.png" alt="Megavideo" style="vertical-align: middle;" /><img height="30" src="http://images.seriesyonkis.com/images/f/spanish.png" alt="Audio Español" title="Audio Español" style="vertical-align: middle;" /></div>
	#<div class="ficha" style="background:url(http://images.seriesyonkis.com/images/cinco-hermanos.jpg) #000000 center top no-repeat"><a href="http://www.seriesyonkis.com/capitulo/cinco-hermanos/capitulo-15/29162/" title="Capitulo 15">Cinco Hermanos - 3x15 - Capitulo 15</a><br /><br /><img src="http://images.peliculasyonkis.com/
	
	patronvideos  = '<div class="ficha" style="background:url\(([^\)]+)\)[^>]+><a href="([^"]+)"[^>]+>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[2]

		# URL
		scrapedurl = match[1]
		
		# Thumbnail
		scrapedthumbnail = match[0]
		
		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def alltvserieslist(params,url,category):
	allserieslist(params,url,category,"series")

def allcartoonslist(params,url,category):
	allserieslist(params,url,category,"dibujos")

def allanimelist(params,url,category):
	allserieslist(params,url,category,"anime")

def allserieslist(params,url,category,clave):
	xbmc.output("[seriesyonkis.py] allserieslist")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae el bloque de las series
	patronvideos = '<h4><a.*?id="'+clave+'".*?<ul>(.*?)</ul>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	data = matches[0]

	# Extrae las entradas (carpetas)
	patronvideos  = '<li class="page_item"><a href="(http://www.seriesyonkis.com/serie[^"]+)"[^>]+>([^<]+)</a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "list" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def list(params,url,category):
	xbmc.output("[seriesyonkis.py] list")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="(http://www.seriesyonkis.com/capitulo[^"]+)"[^>]+>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
	xbmc.output("[seriesyonkis.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	data = scrapertools.cachePage(url)
	patronvideos  = 'href="(http://www.seriesyonkis.com/player/visor_pymeno2.php[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	if len(matches)==0:
		xbmctools.alertnodisponible()
		return
	
	url = scrapertools.cachePage('http://www.atrapavideo.com/es/videomonkey/yonkis/url='+matches[0])
	xbmc.output("url="+url)

	xbmctools.playvideo(CHANNELNAME,"Megavideo",url,category,title,thumbnail,plot)
	# ------------------------------------------------------------------------------------

	'''
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	'''

'''
def play(params,url,category):
	xbmc.output("[seriesyonkis.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[seriesyonkis.py] thumbnail="+thumbnail)
	xbmc.output("[seriesyonkis.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
'''