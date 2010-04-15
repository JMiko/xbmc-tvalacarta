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

CHANNELNAME = "casttv"

# Esto permite su ejecuci�n en modo emulado
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

	category = "Series"

	addsimplefolder( CHANNELNAME , "listado" , category , "Series VO - �ltimas Actualizaciones" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "listado" , category , "Series VO - Listado Completo" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "search" , category , "Series VO - Buscar","http://www.casttv.com/shows/","http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )

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
	# Descarga la p�gina
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	listaseries = findseries(data,tipolist,"")

	if tipolist == "Actualizaciones":
		addsimplefolder( CHANNELNAME , "listatres" , category , "*** Nuevos Episodios en TVSneak ***" , "http://tvsneak.com/new" , "http://tvsneak.com/wp-content/themes/fresh_trailers/images/logo.png")

	for serie in listaseries:
		addsimplefolder( CHANNELNAME , "listados" , category , serie[0]+serie[1] , serie[2] , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[casttv.py] search")

	tecleado = ""
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	rtdos = 0
        
	opciones = []
	opciones.append("Teclado (Busca en T�tulo y Status)")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("B�squeda por Teclado o por Inicial del T�tulo:", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1 :return
	if seleccion == 0:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			if len(tecleado)>0:	
				# Descarga la p�gina
				data = scrapertools.cachePage(url)				

				if len(tecleado) == 1:
					listaseries = findseries(data,"",tecleado)
				else:
					listaseries = findseries(data,"","")

		if keyboard.isConfirmed() is None or len(tecleado)==0:
			return				

	else:
		# Descarga la p�gina
		data = scrapertools.cachePage(url)		

		listaseries = findseries(data,"",letras[seleccion-1])

	if len(listaseries)==0:
		alertnoresultadosearch()
		return

	for serie in listaseries:
		foldertitle = serie[0]+serie[1]
		if len(tecleado) > 1:
			match = re.search(tecleado,foldertitle,re.IGNORECASE)
			if (match):
				addsimplefolder( CHANNELNAME , "listados" , category , foldertitle , serie[2] , "" )
				rtdos = rtdos+1
		else:
			addsimplefolder( CHANNELNAME , "listados" , category , foldertitle , serie[2] , "" )
	
	if len(tecleado) > 1 and rtdos==0:
		alertnoresultadosearch()
		return	
					
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
		tipolist = '\n\s+(?:&nbsp;<span class="label_updated">Updated!</span>\n\s+|\n\s+)</div>'
	
	if search == "#":
		search = "\d+"

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
	# Descarga la p�gina
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	# ------------------------------------------------------
	# Extrae la car�tula
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
			if episodio[3] == "0":
				addnewfolder( CHANNELNAME , "detaildos" , category , episodio[0] , episodio[1] , thumbnail , plot , episodio[2] , episodio[4] , episodio[5] , episodio[6] , miserievo , episodio[8] )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Sorting by date...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findepisodios(data,miserievo):
	xbmc.output("[casttv.py] findepisodios")
	episodioslist = []
	seasonlist = []
	episodioscasttv = []
	encontrados = set()
	depago = "0"
	datatvsneak = scrapertools.cachePage("http://tvsneak.com")

	# Arregla el titulo de la serie para TVSneak
	titletvsneak = ftitletvsneak(miserievo,datatvsneak)

	patronvideos  = 'class="episode_column01">(\n\s+\n\s+\w+\n\s+|\n\s+[^\n]+)\n\s+</a>\n\s+'
	patronvideos += '<a href="(.*?)" class="episode_column02">(.*?)</a>'
	patronvideos += '.*?class="episode_column03">[^<]+<img src="([^"]+)".*?class="episode_column04">'
	patronvideos += '(\n\s+\n\s+\d{2}.\d{2}.\d{2}\n|\n)'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		# Titulo		
		seasontvsneak = "0"
		seasontv = ""
		episodiotv = 0
		tvsneak = "0"

		# + Temporada y Cap�tulo
		match0 = re.search('\n\s+\n\s+(\w+)\n\s+',match[0],re.IGNORECASE)
		if (match0):
			titulo = miserievo+" - "+match0.group(1)+" - "+match[2]
			# + Season (TVSneak)
			match1 = re.search('S0?(\d+)E0?(\d+)',match0.group(1),re.IGNORECASE)
			if (match1):
				seasontvsneak = match1.group(1)
				seasontv = match0.group(1)
				episodiotv = int(match1.group(2))
		else:
			titulo = miserievo+" - "+match[2]

		# + Fecha de emisi�n
		date = ""		
		match4 = re.search('(\d{2}).(\d{2}).(\d{2})',match[4],re.IGNORECASE)
		if (match4):
			titulo = titulo+" - "+match4.group(2)+"/"+match4.group(1)+"/"+match4.group(3)
			date = match4.group(2)+"/"+match4.group(1)+"/"+match4.group(3)

		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')	

		# URL
		url = urlparse.urljoin("http://www.casttv.com",match[1])
		
		pago = "0"
		# Episodios de pago
		if match[3] == "/images/v3/icon_list_price.png":
			pago = "-1"		
			
		# A�ade al listado los episodios
		episodioslist.append( [ titulo , url , date , pago , titletvsneak , seasontvsneak , seasontv , episodiotv , tvsneak ] )
		if seasontv <> "":
			episodioscasttv.append(seasontv)		
		if seasontvsneak <> "0" and seasontvsneak not in encontrados:
			seasonlist.append(seasontvsneak)
			encontrados.add(seasontvsneak)

	# Si una temporada est� en TVSneak se agregan todos los episodios (los de pago y los que faltan en CastTV)
	for season in seasonlist:
		urltvsneak = titletvsneak+"-season-"+season
		matchtvsneak = re.search('(http://tvsneak.com/category/.*?)(?<='+urltvsneak+')',datatvsneak,re.IGNORECASE)
		if (matchtvsneak):
			for episodio in episodioslist:
				if episodio[5]==season:
					n = episodioslist.index(episodio)
					if episodio[3]=="-1":
						episodio[3] = "0"
					if episodio[8]=="0":
						episodio[8] = "-1"
					if episodio[7] > 1:
						lastseasontv = episodioscasttv[-1]
						if episodio[6] == lastseasontv:
							if n < len(episodioslist)-1 and episodioslist[n+1][6] <> episodio[6] :						
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , "-1" ])
							elif n == len(episodioslist)-1:
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , "-1" ])
						capitvnew = episodio[7]-1
						seasontvnew = episodio[6][0:4]+str(capitvnew)
						if len(seasontvnew) == 5:
							seasontvnew = seasontvnew.replace('E' , 'E0')
						
						if episodioslist[n+1][5] == season and episodioslist[n+1][6] <> episodio[6] and episodioslist[n+1][7] <> capitvnew:
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , "-1" ])
						if episodioslist[n+1][5] == str(int(season)-1) and episodioslist[n+1][5] <> "0":
							episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , "-1" ])

	return episodioslist

def listatres(params,url,category):
	xbmc.output("[casttv.py] listatres")

	data = scrapertools.cachePage(url)
		
	patronvideos = '<a\s+href="([^"]+)" rel="bookmark">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		# Titulo		
		titulo = match[1]
		match0 = re.search('(.*?)\s+(S0?\d+E0?\d+)$',titulo,re.IGNORECASE)
		if (match0):
			titulo = match0.group(1)+" - "+match0.group(2)
		# URL
		url = match[0]		
		
		# A�ade al listado
		addnewfolder( CHANNELNAME , "detaildos" , category , titulo , url , "http://tvsneak.com/wp-content/themes/fresh_trailers/images/logo.png" , "" , "" , "" , "0" , "" , "" , "" )

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
	plot = urllib.unquote_plus( params.get("plot") )
	date = urllib.unquote_plus( params.get("date") )
	miserievo = urllib.unquote_plus( params.get("miserievo") )
	titletvsneak = urllib.unquote_plus( params.get("titletvsneak") )
	seasontvsneak = urllib.unquote_plus( params.get("seasontvsneak") )
	seasontv = urllib.unquote_plus( params.get("seasontv") )
	tvsneak = urllib.unquote_plus( params.get("tvsneak") )
	xbmc.output("[casttv.py] title="+title)
	xbmc.output("[casttv.py] thumbnail="+thumbnail)
	xbmc.output("[casttv.py] plot="+plot)
	titleshort = re.sub('\s\-\s'+date+'$','',title)
	urltvsneak0 = titletvsneak+"-season-"+seasontvsneak
	
	listacasttv = []
	listactmirrors = []
	listaTVSneak = []

	# CastTV
	if url <> "":
		# tipo 1: Megavideo es el tipo de reproducci�n
		data0 = scrapertools.cachePage(url)
		listacasttv = servertools.findvideos(data0)		
		# tipo 2: Megavideo no es el tipo de reproducci�n
		if len(listacasttv)==0:
			# obtiene la url de la p�gina para reproducir con Megavideo si existe	
			match = re.search('<a class="source_row" href="(.*?)"> <img alt="MegaVideo"',data0,re.IGNORECASE)

			# Descarga la p�gina para reproducir con Megavideo si existe
			if (match):
				data = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match.group(1)))
				listacasttv = servertools.findvideos(data)				
				data0 = data

		if len(listacasttv)>0:	
			# obtiene la url de la p�gina para reproducir con Megavideo del mirror si existe	
			match1 = re.search('<a class="source_copies" href="(.*?)">COPY 2',data0,re.IGNORECASE)

			# Descarga la p�gina para reproducir con Megavideo del mirror si existe
			if (match1):
				data1 = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match1.group(1)))
				listactmirrors = servertools.findvideos(data1)
		
	# TVSneak: se busca aunque se haya encontrado enlace por la posibilidad de Divxden
	if tvsneak == "-1":
		datatvsneak0 = scrapertools.cachePage("http://tvsneak.com")
		matchtvsneak0 = re.search('(http://tvsneak.com/category/.*?)(?<='+urltvsneak0+')',datatvsneak0,re.IGNORECASE)
		if (matchtvsneak0):
			datatvsneak = scrapertools.cachePage(matchtvsneak0.group(1))
			urltvsneak = re.sub('category/','',matchtvsneak0.group(1))
			urltvsneak2 = "http://tvsneak.com/new"
			matchtvsneak1 = re.search('<a  href="((?:'+urltvsneak+'|'+urltvsneak2+')/[^"]+)" rel="bookmark">[^<]+(?<='+seasontv+')[^<]*</a>',datatvsneak,re.IGNORECASE)
			if (matchtvsneak1):
				datatvsneak2 = scrapertools.cachePage(matchtvsneak1.group(1))
				listaTVSneak = servertools.findvideos(datatvsneak2)
				# Eliminar cuando haya un patr�n para Divxden en servertools
				patronvideos = '(http\:\/\/www\.divxden\.com/.*?\.html)'
				matches = re.compile(patronvideos).findall(datatvsneak2)
				for match in matches:
					n = matches.index(match)
					if n==0:
						titulo = "[Divxden]"
					else:
						titulo = "[Divxden] - Mirror"
					url = match
					# Por si fue agregado por servertools.findvideos
					if listaTVSneak.count( [ titulo , url , 'Divxden' ] )==0:
						listaTVSneak.append( [ titulo , url , 'Divxden' ] )
													
	if len(listacasttv)==0 and len(listaTVSneak)==0:
		alertnovideo()
		return	
			
	# ------------------------------------------------------------------------------------
	# A�ade los enlaces a los videos
	# ------------------------------------------------------------------------------------
	for video in listacasttv:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - [CastTV]" , video[1] , thumbnail , plot )
	for video in listactmirrors:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - Mirror - [CastTV]" , video[1] , thumbnail , plot )
	for video in listaTVSneak:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - [TVSneak]" , video[1] , thumbnail , plot )
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

def alertnovideo():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('V�deo no disponible' , 'No se ha a�adido a�n a la web un enlace' , 'compatible.')

def alertnoepisodios():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Episodios no disponibles' , 'No se han encontrado episodios gratuitos.' , '')

def alertnoresultadosearch():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'La B�squeda no ha obtenido Resultados.' , '')

def addsimplefolder( canal , accion , category , title , url , thumbnail ):
	xbmc.output("[casttv.py] addsimplefolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , date , titletvsneak , seasontvsneak , seasontv , miserievo , tvsneak ):
	xbmc.output("[casttv.py] addnewfolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&date=%s&titletvsneak=%s&seasontvsneak=%s&seasontv=%s&miserievo=%s&tvsneak=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( date ) , urllib.quote_plus( titletvsneak ) , urllib.quote_plus( seasontvsneak ) , urllib.quote_plus( seasontv ) , urllib.quote_plus( miserievo ) , urllib.quote_plus( tvsneak ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	xbmc.output('[casttv.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def ftitletvsneak(miserievo,datatvsneak):	
	titletvsneak = re.sub('FlashForward','Flash Forward',miserievo)
	titletvsneak = re.sub('CSI: NY','CSI: New York',titletvsneak)
	titletvsneak = re.sub('Spartacus','Spartacus: Blood and Sand',titletvsneak)
	titletvsneak = re.sub('\'','',titletvsneak)
	titletvsneak = re.sub('\&','',titletvsneak)
	titletvsneak = re.sub('\:','',titletvsneak)
	titletvsneak = re.sub('\/','',titletvsneak)
	titletvsneak = re.sub('\(','',titletvsneak)
	titletvsneak = re.sub('\)','',titletvsneak)
	titletvsneak = re.sub('\s+','-',titletvsneak)
	
	matchtvs = re.match('(.*?)\-\d+$',titletvsneak,re.IGNORECASE)
	if (matchtvs):
		matchtvs1 = re.search(titletvsneak,datatvsneak,re.IGNORECASE)
		if matchtvs1 is None:
			titletvsneak = matchtvs.group(1)
	
	return titletvsneak