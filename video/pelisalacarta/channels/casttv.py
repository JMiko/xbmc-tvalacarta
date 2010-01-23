# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para casttv
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
import megaupload
import servertools
import binascii
import xbmctools
import downloadtools

CHANNELNAME = "casttv"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[casttv.py] init")

DEBUG = True

Generate = False # poner a true para generar listas de peliculas

LoadThumbnails = True # indica si cargar los carteles

def mainlist(params,url,category):
	xbmc.output("[casttv.py] mainlist")

	xbmctools.addnewfolder( CHANNELNAME , "listaupdate" , CHANNELNAME , "Series VO - Últimas Actualizaciones" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" , "")
	xbmctools.addnewfolder( CHANNELNAME , "listado" , CHANNELNAME , "Series VO - Listado Completo" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" , "")
	xbmctools.addnewfolder( CHANNELNAME , "listasubs" , CHANNELNAME , "Consulta Subtítulos - (Subtitulos.es)" , "http://www.subtitulos.es/series" , "http://www.subtitulos.es/images/subslogo.png" , "")


	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
			
def listado(params,url,category):
	xbmc.output("[casttv.py] listado")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	patronvideos = '<div class="gallery_listing_text">(.*?)<a href="(.*?)">(.*?)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[2]
		scrapedtitle = scrapedtitle.replace('&amp;' , '&')
		scrapedtitle = scrapedtitle.replace('&quot;' , '"')


		# URL
		scrapedurl = urlparse.urljoin("http://www.casttv.com",match[1])
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listados" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listaupdate(params,url,category):
	xbmc.output("[casttv.py] listaupdate")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	patronvideos = '<a href="([^"]+)">([^<]+)</a>\n\s+&nbsp;<span class="label_updated">(Updated!)</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		scrapedtitle = scrapedtitle.replace('&amp;' , '&')
		scrapedtitle = scrapedtitle.replace('&quot;' , '"')

		# URL
		scrapedurl = urlparse.urljoin("http://www.casttv.com",match[0])
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listados" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listasubs(params,url,category):
	xbmc.output("[casttv.py] listasubs")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	alertnodescargas()
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	patronvideos = '<a href="\/show\/([^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]+" - [Subtitulos]"

		# URL
		scrapedurl = urlparse.urljoin("http://www.subtitulos.es/show/",match[0])
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listasubst" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listados(params,url,category):
	xbmc.output("[casttv.py] listados")

	miserievo = urllib.unquote_plus( params.get("title") )
	xbmc.output("[casttv.py] miserievo="+miserievo)

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae las entradas que tienen Temporada o Temporada y Capítulo
	# ------------------------------------------------------
	patronvideos  = 'class="episode_column01">\n\s+\n\s+(S[^\n]+)\n\s+\n\s+</a>\n\s+<a href="(.*?)" class="episode_column02">(.*?)</a>'
	patronvideos += '.*?class="episode_column03">[^<]+<img src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = miserievo+" - "+match[0]+" - "+match[2]
		scrapedtitle = scrapedtitle.replace('&amp;' , '&')
		scrapedtitle = scrapedtitle.replace('&quot;' , '"')	

		# URL
		scrapedurl = urlparse.urljoin("http://www.casttv.com",match[1])

		# Cambia el título y la url a los episodios de pago
		if match[3] == "/images/v3/icon_list_price.png":
			scrapedtitle = scrapedtitle+" - (Episodio de Pago)"
		        scrapedurl = ""
	
		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC los episodios gratuitos
		if scrapedurl <> "":
			xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detaildos" )

	# ------------------------------------------------------
	# Extrae las entradas que no tienen Temporada o Capítulo
	# ------------------------------------------------------
	patronvideos  = 'class="episode_column01">\n[^\n]+\n\s+</a>\n\s+<a href="(.*?)" class="episode_column02">(.*?)</a>'
	patronvideos += '.*?class="episode_column03">[^<]+<img src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = miserievo+" - "+match[1]
		scrapedtitle = scrapedtitle.replace('&amp;' , '&')
		scrapedtitle = scrapedtitle.replace('&quot;' , '"')	

		# URL
		scrapedurl = urlparse.urljoin("http://www.casttv.com",match[0])

		# Cambia el título y la url a los episodios de pago
		if match[2] == "/images/v3/icon_list_price.png":
			scrapedtitle = scrapedtitle+" - (Episodio de Pago)"
		        scrapedurl = ""
	
		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC los episodios gratuitos
		if scrapedurl <> "":
			xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detaildos" )


	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listasubst(params,url,category):
	xbmc.output("[casttv.py] listasubst")

	miserie = urllib.unquote_plus( params.get("title") )
	miserie = miserie.replace('[Subtitulos]' , '')
	xbmc.output("[casttv.py] miserie="+miserie)

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae las Temporadas
	# ------------------------------------------------------
	patronvideos  = '<a href="javascript:loadShow\((\d{1,4}),(\d{1,2})\)">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = miserie+"Temporada "+match[1]+" - [Subtitulos]"

		# URL
		mishow = str(match[0])
		xbmc.output("[casttv.py] mishow="+mishow)
		miseason= str(match[1])
		xbmc.output("[casttv.py] miseason="+miseason)
		miquery = "ajax_loadShow.php?show="+mishow+"&season="+miseason
		xbmc.output("[casttv.py] miquery="+miquery)

		scrapedurl = urlparse.urljoin("http://www.subtitulos.es/",miquery)

		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC los episodios gratuitos
		if scrapedurl <> "":
			xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listasubstc" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listasubstc(params,url,category):
	xbmc.output("[casttv.py] listasubstc")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae los Capítulos
	# ------------------------------------------------------
	patronvideos  = '<a href=\'([^\']+)\'>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]+" - [Subtitulos]"

		# URL
		scrapedurl = match[0]
		
		# Elimina las entradas que no son capítulos
		if scrapedtitle == "descargar":
			     scrapedurl = ""

		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC los episodios gratuitos
		if scrapedurl <> "":
			xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listasubstcd" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listasubstcd(params,url,category):
	xbmc.output("[casttv.py] listasubstcd")

	micapt = urllib.unquote_plus( params.get("title") )
	micapt = micapt.replace('[Subtitulos]' , 'Subtitulo')
	xbmc.output("[casttv.py] micapt="+micapt)

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae los Subtítulos
	# ------------------------------------------------------
	patronvideos  = '<td width="(21%)" class="language">\n([^<]+)</td>\n\s+<td width="19%"><strong>\nCompletado\s+</strong>'
	patronvideos += '\n\s+</td>\n\s+<td colspan="3">\n\s+<img[^>]+>\s+\n<a href="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]+" - "+micapt+" Versión ? - [Descarga]"

                scrapedtitle = scrapedtitle.replace('Ã±' , 'ñ')
		scrapedtitle = re.sub("\s+"," ",scrapedtitle) 

		# URL
		scrapedurl = match[2]

		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC los subtítulos
		
		xbmctools.addnewvideo( CHANNELNAME , "descarga" , category , "Directo" , scrapedtitle , match[2] , "" , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


def detaildos(params,url,category):
	xbmc.output("[casttv.py] detaildos")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	xbmc.output("[casttv.py] title="+title)
	xbmc.output("[casttv.py] thumbnail="+thumbnail)

	# tipo 1: Megavideo es el tipo de reproducción
	data0 = scrapertools.cachePage(url)
	listavideos = servertools.findvideos(data0)
	sinmirrors = []
	listamirrors = sinmirrors
	
	# tipo 2: Megavideo no es el tipo de reproducción
	
	if len(listavideos)==0:
		# obtiene la url de la página para reproducir con Megavideo si existe	
		match = re.search('<a class="source_row" href="(.*?)"> <img alt="MegaVideo"',data0,re.IGNORECASE)

		# Descarga la página para reproducir con Megavideo si existe
		if (match):
			data = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match.group(1)))
			#xbmc.output(data)
			listavideos = servertools.findvideos(data)
			
			# obtiene la url de la página para reproducir con Megavideo del mirror si existe	
			match1 = re.search('<a class="source_copies" href="(.*?)">COPY 2',data,re.IGNORECASE)

			# Descarga la página para reproducir con Megavideo del mirror si existe
			if (match1):
				data1 = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match1.group(1)))
				#xbmc.output(data1)
				listamirrors = servertools.findvideos(data1)
		else:
			alertnomegavideo()
			return
	else:
		# obtiene la url de la página para reproducir con Megavideo del mirror si existe	
		match1 = re.search('<a class="source_copies" href="(.*?)">COPY 2',data0,re.IGNORECASE)

		# Descarga la página para reproducir con Megavideo del mirror si existe
		if (match1):
			data1 = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match1.group(1)))
			#xbmc.output(data1)
			listamirrors = servertools.findvideos(data1)
				
	# ------------------------------------------------------------------------------------
	# Añade los enlaces a los videos
	# ------------------------------------------------------------------------------------
	for video in listavideos:
			xbmctools.addvideo( CHANNELNAME , title+" - "+video[0] , video[1] , category , video[2] )
	for video in listamirrors:
			xbmctools.addvideo( CHANNELNAME , title+" - Mirror - "+video[0] , video[1] , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[casttv.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]	
	xbmc.output("[casttv.py] thumbnail="+thumbnail)
	xbmc.output("[casttv.py] server="+server)

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def descarga(params,url,category):
	xbmc.output("[casttv.py] descarga")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]	
	xbmc.output("[casttv.py] thumbnail="+thumbnail)
	xbmc.output("[casttv.py] server="+server)

	descargasub(CHANNELNAME,server,url,category,title,thumbnail,plot)

def descargasub(canal,server,url,category,title,thumbnail,plot):
	
	xbmc.output("[xbmctools.py] playvideo")
	xbmc.output("[xbmctools.py] playvideo canal="+canal)
	xbmc.output("[xbmctools.py] playvideo server="+server)
	xbmc.output("[xbmctools.py] playvideo url="+url)
	xbmc.output("[xbmctools.py] playvideo category="+category)

	# Abre el diálogo de selección
	opciones = []
	opciones.append("Descargar")
	
	dia = xbmcgui.Dialog()
	seleccion = dia.select("Elige una opción", opciones)
	xbmc.output("seleccion=%d" % seleccion)
		
	if seleccion==-1:
		return
	if seleccion==0:
		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			title = keyboard.getText()
		downloadtools.downloadtitle(url,title)
		return

def alertnomegavideo():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Vídeo no disponible' , 'No se ha añadido aún a la web un enlace' , 'a Megavideo de este capítulo')

def alertnodescargas():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('¡En Construcción!' , 'Consulta la disponibilidad de subtítulos completados.' , 'No es posible hacer descargas.')

