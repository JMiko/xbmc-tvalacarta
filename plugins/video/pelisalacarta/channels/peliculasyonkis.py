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

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(50)") #full list

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listnovedades"  , category , "Últimas películas","http://www.peliculasyonkis.com/ultimas-peliculas.php","","")
	xbmctools.addnewfolder( CHANNELNAME , "listcategorias" , category , "Listado por categorias","http://www.peliculasyonkis.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listalfabetico" , category , "Listado alfabético","http://www.peliculasyonkis.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "buscaporanyo"   , category , "Busqueda por Año","http://www.peliculasyonkis.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "search"         , category , "Buscar","","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[peliculasyonkis.py] search")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.peliculasyonkis.com/buscarPelicula.php?s="+tecleado
			searchresults(params,searchUrl,category)

def searchresults(params,url,category):
	xbmc.output("[peliculasyonkis.py] searchresults")

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#<li> <a href="http://www.peliculasyonkis.com/pelicula/las-edades-de-lulu-1990/" title="Las edades de Lulú (1990)"><img width="77" height="110" src="http://images.peliculasyonkis.com/thumbs/las-edades-de-lulu-1990.jpg" alt="Las edades de Lulú (1990)" align="right" />
	
	patronvideos  = '<li> <a href="([^"]+)" title="([^"]+)"><img.*?src="([^"]+)"'
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
		xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetico(params, url, category):

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(50)") #full list

	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "0-9","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasNumeric.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "A","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasA.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "B","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasB.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "C","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasC.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "D","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasD.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "E","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasE.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "F","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasF.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "G","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasG.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "H","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasH.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "I","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasI.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "J","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasJ.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "K","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasK.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "L","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasL.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "M","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasM.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "N","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasN.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "O","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasO.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "P","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasP.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Q","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasQ.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "R","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasR.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "S","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasS.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "T","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasT.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "U","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasU.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "V","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasV.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "W","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasW.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "X","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasX.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Y","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasY.php","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Z","http://www.peliculasyonkis.com/lista-peliculas/listaPeliculasZ.php","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listnovedades(params,url,category):
	xbmc.output("[peliculasyonkis.py] listnovedades")

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<td align=\'center\'><center><span style=\'font-size: 0.7em\'><a href="([^"]+)" title="([^"]+)">'
	patronvideos += '<img.*?src=\'([^\']+)\'[^>]+>.*?<img src="(http://simages.peliculasyonkis.com/images/[^"]+)"'
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

def listcategorias(params,url,category):
	xbmc.output("[peliculasyonkis.py] listcategorias")

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(50)") #full list

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
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def buscaporanyo(params,url,category):
	xbmc.output("[peliculasyonkis.py] buscaporanyo")

	anyoactual = 2010
	anyoinic   = 1977
	opciones = []
	for i in range(34):
		opciones.append(str(anyoactual))
		anyoactual = anyoactual - 1           
	dia = xbmcgui.Dialog()
	seleccion = dia.select("Listar desde el Año: ", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1 :return
	if seleccion == 0:
		url = "http://www.peliculasyonkis.com/estreno/"+opciones[seleccion]+"/"+opciones[seleccion]+"/0/"
		listvideos(params,url,category)
		return

	anyoactual = 2010
	desde      = opciones[seleccion]
	rangonuevo = seleccion + 1
	opciones2 = []
	for j in range(rangonuevo):
		opciones2.append(str(anyoactual))
		anyoactual = anyoactual - 1
	dia2 = xbmcgui.Dialog()
	seleccion2 = dia2.select("Listar hasta el año:",opciones2)
	if seleccion == -1 :
		url = "http://www.peliculasyonkis.com/estreno/"+desde+"/"+desde+"/0/"
		listvideos(params,url,category)
		return
	url = "http://www.peliculasyonkis.com/estreno/"+desde+"/"+opciones2[seleccion2]+"/0/"
	listvideos(params,url,category)
	return

def listvideos(params,url,category):
	xbmc.output("[peliculasyonkis.py] listvideos")

	if xbmcplugin.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

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
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Extrae las entradas (carpetas)
	patronvideos  = '<li>[^<]+<a href="([^"]+)" title="([^"]+)"><img.*?src="([^"]+)"[^>]+>.*?<span[^>]+>(.*?)</span>'
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
		try:
			scrapedplot = unicode( match[3], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedplot = match[3]
		
		scrapedplot = scrapedplot.replace("\r"," ")
		scrapedplot = scrapedplot.replace("\n"," ")
		scrapedplot = scrapedplot.replace("&quot;","'")
		scrapedplot = scrapedplot.replace("<br />","|")
		patronhtml = re.compile( '<img[^>]+>' )
		scrapedplot = patronhtml.sub( "", scrapedplot )
		patronhtml = re.compile( 'Uploader:[^\|]+\|' )
		scrapedplot = patronhtml.sub( "", scrapedplot )
		patronhtml = re.compile( 'Idioma:[^\|]+\|' )
		scrapedplot = patronhtml.sub( "", scrapedplot )
		patronhtml = re.compile( 'Tiene descarga directa:[^\|]+\|' )
		scrapedplot = patronhtml.sub( "", scrapedplot )
		patronhtml = re.compile( '\W*\|\W*' )
		scrapedplot = patronhtml.sub( "|", scrapedplot )
		patronhtml = re.compile( '\|Descripci.n:' )
		scrapedplot = patronhtml.sub( "\n\n", scrapedplot )
		
		scrapedplot = scrapedplot.replace("|b>Servidor:</b|","")

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
	xbmc.output("[peliculasyonkis.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	patronvideos  = 'href="(http://www.peliculasyonkis.com/player/visor_pymeno2.php[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	url = scrapertools.cachePage('http://www.atrapavideo.com/es/videomonkey/yonkis/url='+matches[0])
	xbmc.output("url="+url)
	
	xbmctools.playvideo(CHANNELNAME,"Megavideo",url,category,title,thumbnail,plot)
