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

	xbmctools.addnewfolder( CHANNELNAME , "listado" , CHANNELNAME , "Series VO - Últimas Actualizaciones" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" , "")
	xbmctools.addnewfolder( CHANNELNAME , "listado" , CHANNELNAME , "Series VO - Listado Completo" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" , "")
	xbmctools.addnewfolder( CHANNELNAME , "search" , CHANNELNAME , "Series VO - Buscar","http://www.casttv.com/shows/","http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg","")
	xbmctools.addnewfolder( CHANNELNAME , "listasubs" , CHANNELNAME , "Consulta Subtítulos - (Subtitulos.es)" , "http://www.subtitulos.es/series" , "http://www.subtitulos.es/images/subslogo.png" , "")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
			
def listado(params,url,category):
	xbmc.output("[casttv.py] listado")

	title = urllib.unquote_plus( params.get("title") )
	match = re.search('\s(\w+)$',title)
	tipolist = match.group(1)

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	listaseries = findseries(data,tipolist,"")

	for serie in listaseries:
			xbmctools.addthumbnailfolder( CHANNELNAME , serie[0]+serie[1] , serie[2] , "" , "listados" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[casttv.py] search")

	letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
	opciones = []
	opciones.append("Teclado (Busca en Título y datos anexos)")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Búsqueda por Teclado o por Inicial del Título:", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1 :return
	if seleccion == 0:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			if len(tecleado)>0:	
				# Descarga la página
				data = scrapertools.cachePage(url)
				#xbmc.output(data)

				if len(tecleado) == 1:
					listaseries = findseries(data,"",tecleado)
					for serie in listaseries:
						xbmctools.addthumbnailfolder( CHANNELNAME , serie[0]+serie[1] , serie[2] , "" , "listados" )

				else:
					listaseries = findseries(data,"","")				
					for serie in listaseries:
						foldertitle = serie[0]+serie[1]
						match = re.search(tecleado,foldertitle,re.IGNORECASE)
						if (match):
							xbmctools.addthumbnailfolder( CHANNELNAME , foldertitle , serie[2] , "" , "listados" )

	else:
		# Descarga la página
		data = scrapertools.cachePage(url)
		#xbmc.output(data)

		listaseries = findseries(data,"",letras[seleccion-1])

		for serie in listaseries:
			xbmctools.addthumbnailfolder( CHANNELNAME , serie[0]+serie[1] , serie[2] , "" , "listados" )
					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findseries(data,tipolist,search):
	xbmc.output("[casttv.py] findseries")
	serieslist = []
	
	if tipolist == "Actualizaciones":
		tipolist = '\n\s+&nbsp;<span class="label_updated">Updated!</span>\n\s+</div>'
	else:
		tipolist = '\n\s+\n\s+</div>'

	patronvideos  = '<div class="gallery_listing_text">\n\s+<a href="(.*?)">('+search+'[^<]+)'
	patronvideos += '</a>'+tipolist+'(\n\s+<div class="icon_current"></div>\n</li>|\n\s+\n</li>)'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulo = match[1]
		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')

		# URL
		url = urlparse.urljoin("http://www.casttv.com",match[0])

		# Status0
		status0 = ""
		match2 = re.search('icon_current',match[2],re.IGNORECASE)
		if (match2):
			status0 = "  -  [Current tv show]"
		else:
			status0 = "  -  [Ended]"

		serieslist.append( [ titulo , status0 , url ] )
	
	mistatus = "http://eztv.it/showlist/"
	data2 = scrapertools.cachePage(mistatus)

	patronvideos  = '<a href="[^"]+" class="thread_link">([^<]+)</a></td>\n\s+'
	patronvideos += '<td class="forum_thread_post"><font class="[^"]+">(.*?)</font>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data2)

	for match in matches:
		
		# Titulo
		titulo2 = match[0]		
		titulo2 = titulo2.replace('<b>' , '')
		titulo2 = titulo2.replace('</b>' , '')
		titulo2 = titulo2.replace('&amp;' , '&')
		titulo2 = titulo2.replace('&quot;' , '"')
		if titulo2 == "Melrose Place":
			titulo2 = "Melrose Place (2009)"
		if titulo2 == "CSI: Crime Scene Investigation":
			titulo2 = "CSI"
		if titulo2 == "Law and Order: Special Victims Unit":
			titulo2 = "Law & Order: SVU"
		match0 = re.match('.*?, The$',titulo2,re.IGNORECASE)
		if (match0):
			titulo2 = titulo2.replace(', The' , '')
			titulo2 = "The "+titulo2
		
		# Status
		status = match[1]
		match1 = re.search('(\d{4})-(\d{2})-(\d{2})',status,re.IGNORECASE)
		if (match1):
			mydate = match1.group(3)+"-"+match1.group(2)+"-"+match1.group(1)
			status = re.sub('\d{4}-\d{2}-\d{2}',mydate,status)
		status = status.replace('<b>' , '')
		status = status.replace('</b>' , '')
		if status <> "Ended":
			status = "Current tv show: "+status

		for serie in serieslist:
			
			if serie[0].lower() == titulo2.lower():
				serie[1] = "  -  ["+status+"]"
			else:
				match2 = re.match('(.*?) \(20\d\d\)$',serie[0],re.IGNORECASE)
				if (match2):
					if match2.group(1).lower() == titulo2.lower():
						serie[1] = "  -  ["+status+"]"
					
				match3 = re.search('\s\&\s',serie[0],re.IGNORECASE)
				if (match3):
					if serie[0].replace('&' , 'and').lower() == titulo2.lower():
						serie[1] = "  -  ["+status+"]"
				
				match4 = re.search('\'s',serie[0],re.IGNORECASE)
				if (match4):
					if serie[0].replace('\'s' , 's').lower() == titulo2.lower():
						serie[1] = "  -  ["+status+"]"
										
	return serieslist
			
def listados(params,url,category):
	xbmc.output("[casttv.py] listados")

	miserievo = urllib.unquote_plus( params.get("title") )
	miserievo = re.sub('  -  \[.*?\]','',miserievo)
	xbmc.output("[casttv.py] miserievo="+miserievo)

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae la carátula
	# ------------------------------------------------------		
	thumbnail = ""
	match1 = re.search('<meta name="image_src" content="(.*?)"',data,re.IGNORECASE)
	if (match1):
		thumbnail = urlparse.urljoin("http://www.casttv.com",match1.group(1))

	# ------------------------------------------------------
	# Extrae el argumento
	# ------------------------------------------------------		
	plot = ""
	patronvideos  = '<span id=".*?_long" style="display: none;">\n\s+'
	patronvideos += '(.*?)\n\s+<a href="#".*?'
	patronvideos += '<strong>Genre:</strong>(.*?)<br />\n\s+\n\s+\n\s+'
	patronvideos += '<strong>Network:</strong>(.*?)\n.*?'
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		argumento = re.sub('<.*?>','',matches.group(1))
		plot = argumento+" Genre: "+matches.group(2)+". Network: "+matches.group(3)
		plot = plot.replace('&amp;' , '&')
		plot = plot.replace('&quot;' , '"')	
	
	# ------------------------------------------------------
	# Extrae los episodios
	# ------------------------------------------------------

	listaepisodios = findepisodios(data,miserievo)

	if len(listaepisodios) == 0:
		alertnoepisodios()
		return
	else:
		for episodio in listaepisodios:
			addnewfolder( CHANNELNAME , "detaildos" , CHANNELNAME , episodio[0] , episodio[1] , thumbnail , plot , episodio[2] )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Sorting by date...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findepisodios(data,miserievo):
	xbmc.output("[casttv.py] findepisodios")
	episodioslist = []

	patronvideos  = 'class="episode_column01">(\n\s+\n\s+\w+\n\s+|\n\s+[^\n]+)\n\s+</a>\n\s+'
	patronvideos += '<a href="(.*?)" class="episode_column02">(.*?)</a>'
	patronvideos += '.*?class="episode_column03">[^<]+<img src="([^"]+)".*?class="episode_column04">'
	patronvideos += '(\n\s+\n\s+\d{2}.\d{2}.\d{2}\n|\n)'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		# Titulo
		# + Temporada y Capítulo
		match0 = re.search('\n\s+\n\s+(\w+)\n\s+',match[0],re.IGNORECASE)
		if (match0):
			titulo = miserievo+" - "+match0.group(1)+" - "+match[2]
		else:
			titulo = miserievo+" - "+match[2]

		# + Fecha de emisión
		date = ""		
		match4 = re.search('(\d{2}).(\d{2}).(\d{2})',match[4],re.IGNORECASE)
		if (match4):
			titulo = titulo+" - "+match4.group(2)+"/"+match4.group(1)+"/"+match4.group(3)
			date = match4.group(2)+"/"+match4.group(1)+"/"+match4.group(3)

		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')	

		# URL
		url = urlparse.urljoin("http://www.casttv.com",match[1])

		# Cambia el título y la url a los episodios de pago (por si en el futuro se necesita)
		if match[3] == "/images/v3/icon_list_price.png":
			titulo = titulo+" - (Episodio de Pago)"
		        titulo = ""
	
		# Añade al listado los episodios que no son de pago
		if match[3] <> "/images/v3/icon_list_price.png":		
			episodioslist.append( [ titulo , url , date ] )
	
	return episodioslist

def detaildos(params,url,category):
	xbmc.output("[casttv.py] detaildos")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[casttv.py] title="+title)
	xbmc.output("[casttv.py] thumbnail="+thumbnail)
	xbmc.output("[casttv.py] plot="+plot)

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
			addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0] , video[1] , thumbnail , plot )
	for video in listamirrors:
			addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - Mirror - "+video[0] , video[1] , thumbnail , plot )
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

def alertnomegavideo():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Vídeo no disponible' , 'No se ha añadido aún a la web un enlace' , 'a Megavideo de este capítulo')

def alertnodescargas():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('¡En Construcción!' , 'Consulta la disponibilidad de subtítulos completados.' , 'No es posible hacer descargas.')

def alertnoepisodios():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Episodios no disponibles' , 'No se han encontrado episodios gratuitos.' , '')

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , date ):
	xbmc.output('[casttv.py] addnewfolder( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot , "Date" : date} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&date=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( date ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	xbmc.output('[casttv.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

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

		# Añade al listado de XBMC
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

		# Añade al listado de XBMC
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
	
	xbmc.output("[casttv.py] playvideo")
	xbmc.output("[casttv.py] playvideo canal="+canal)
	xbmc.output("[casttv.py] playvideo server="+server)
	xbmc.output("[casttv.py] playvideo url="+url)
	xbmc.output("[casttv.py] playvideo category="+category)

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


