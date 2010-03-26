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

	category = "Series"

	addsimplefolder( CHANNELNAME , "listado" , category , "Series VO - Últimas Actualizaciones" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
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
	# Descarga la página
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

	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
	opciones = []
	opciones.append("Teclado (Busca en Título y Status)")
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

				if len(tecleado) == 1:
					listaseries = findseries(data,"",tecleado)
					for serie in listaseries:
						addsimplefolder( CHANNELNAME , "listados" , category , serie[0]+serie[1] , serie[2] , "" )

				else:
					listaseries = findseries(data,"","")				
					for serie in listaseries:
						foldertitle = serie[0]+serie[1]
						match = re.search(tecleado,foldertitle,re.IGNORECASE)
						if (match):
							addsimplefolder( CHANNELNAME , "listados" , category , foldertitle , serie[2] , "" )

	else:
		# Descarga la página
		data = scrapertools.cachePage(url)		

		listaseries = findseries(data,"",letras[seleccion-1])

		for serie in listaseries:
			addsimplefolder( CHANNELNAME , "listados" , category , serie[0]+serie[1] , serie[2] , "" )
					
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
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

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
			if episodio[3] == "0":
				addnewfolder( CHANNELNAME , "detaildos" , category , episodio[0] , episodio[1] , thumbnail , plot , episodio[2] , episodio[4] , episodio[5] , episodio[6] , miserievo )

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

		# + Temporada y Capítulo
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
		
		pago = "0"
		# Episodios de pago
		if match[3] == "/images/v3/icon_list_price.png":
			pago = "-1"		
			
		# Añade al listado los episodios
		episodioslist.append( [ titulo , url , date , pago , titletvsneak , seasontvsneak , seasontv , episodiotv ] )
		if seasontv <> "":
			episodioscasttv.append(seasontv)		
		if seasontvsneak <> "0" and seasontvsneak not in encontrados:
			seasonlist.append(seasontvsneak)
			encontrados.add(seasontvsneak)

	# Si una temporada está en TVSneak se agregan todos los episodios (los de pago y los que faltan en CastTV)
	for season in seasonlist:
		urltvsneak = titletvsneak+"-season-"+season
		matchtvsneak = re.search('(http://tvsneak.com/category/.*?)(?<='+urltvsneak+')',datatvsneak,re.IGNORECASE)
		if (matchtvsneak):
			for episodio in episodioslist:
				if episodio[5]==season:
					n = episodioslist.index(episodio)
					if episodio[3]=="-1":
						episodio[3] = "0"
					if episodio[7] > 1:
						lastseasontv = episodioscasttv[-1]
						if episodio[6] == lastseasontv:
							if n < len(episodioslist)-1 and episodioslist[n+1][6] <> episodio[6] :						
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 ])
							elif n == len(episodioslist)-1:
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 ])
						capitvnew = episodio[7]-1
						seasontvnew = episodio[6][0:4]+str(capitvnew)
						if len(seasontvnew) == 5:
							seasontvnew = seasontvnew.replace('E' , 'E0')
						
						if episodioslist[n+1][5] == season and episodioslist[n+1][6] <> episodio[6] and episodioslist[n+1][7] <> capitvnew:
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew ])
						if episodioslist[n+1][5] == str(int(season)-1) and episodioslist[n+1][5] <> "0":
							episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew ])

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
		
		# Añade al listado
		addnewfolder( CHANNELNAME , "detaildos" , category , titulo , url , "http://tvsneak.com/wp-content/themes/fresh_trailers/images/logo.png" , "" , "" , "" , "0" , "" , "" )

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
	xbmc.output("[casttv.py] title="+title)
	xbmc.output("[casttv.py] thumbnail="+thumbnail)
	xbmc.output("[casttv.py] plot="+plot)

	urltvsneak0 = titletvsneak+"-season-"+seasontvsneak
	
	listavideos = []
	listamirrors = []
	listaTVSneak = []

	# tipo 1: Megavideo es el tipo de reproducción
	if url <> "":
		data0 = scrapertools.cachePage(url)
		listavideos = servertools.findvideos(data0)
		
	# tipo 2: Megavideo no es el tipo de reproducción
	
	if len(listavideos)==0:
		if url <> "":
			# obtiene la url de la página para reproducir con Megavideo si existe	
			match = re.search('<a class="source_row" href="(.*?)"> <img alt="MegaVideo"',data0,re.IGNORECASE)

			# Descarga la página para reproducir con Megavideo si existe
			if (match):
				data = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match.group(1)))
				listavideos = servertools.findvideos(data)
			
				# obtiene la url de la página para reproducir con Megavideo del mirror si existe	
				match1 = re.search('<a class="source_copies" href="(.*?)">COPY 2',data,re.IGNORECASE)

				# Descarga la página para reproducir con Megavideo del mirror si existe
				if (match1):
					data1 = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match1.group(1)))
					listamirrors = servertools.findvideos(data1)
		
		if len(listavideos)==0:
			# Busca episodios en TVSneak
			if seasontvsneak <> "0":
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

			if len(listavideos)==0 and len(listaTVSneak)==0:
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
	for video in listaTVSneak:
			addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - [TVSneak] - "+video[0] , video[1] , thumbnail , plot )
	
	# Prueba: Añade enlace para búsqueda de subtítulos
	# addnewfolder( CHANNELNAME , "listasubs" , category , "Buscar Archivo de Subtítulos de la Temporada "+seasontvsneak , "http://www.tvsubtitles.net/tvshows.html" , "" , "" , date , titletvsneak , seasontvsneak , "" , miserievo )

	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listasubs(params,url,category):
	xbmc.output("[casttv.py] listasubs")

	title = urllib.unquote_plus( params.get("title") )
	date = urllib.unquote_plus( params.get("date") )
	miserievo = urllib.unquote_plus( params.get("miserievo") )
	titletvsneak = urllib.unquote_plus( params.get("titletvsneak") )
	seasontvsneak = urllib.unquote_plus( params.get("seasontvsneak") )

	listasubtitulos = findsubs("",title,miserievo,seasontvsneak)

	if len(listasubtitulos)==1:

		for subtitulo in listasubtitulos:
		
			data = scrapertools.cachePage(subtitulo[1])
			patronvideos = '<a href="'+seriesub[2]+'(\w+)\.html">'
			matches = re.compile(patronvideos,re.DOTALL).findall(data)

			for match in matches:

				# url
				url0 = re,sub('subtitle','download',subtitulo[2])
				url = "http://www.tvsubtitles.net/"+url0+match[0]+".html"
			
				# Idioma
				idioma = match[0]
			
				# Titulo
				titulo = title+" ["+idioma+"] - Temporada:"+seasontvsneak+"[Subtítulos]"
		
				# Añade al listado de XBMC los subtítulos
		
				addnewvideo( CHANNELNAME , "descarga" , category , "Directo" , titulo , url , "" , "" )

	if len(listasubtitulos)<>1:

		tecleado = searchsubs("")

		if len(tecleado) == 1:
			for subtitulo in listasubtitulos:
				match0 = re.match(tecleado,subtitulo[0],re.IGNORECASE)
				if (match0):
					addnewfolder( CHANNELNAME , "listasubs" , category , subtitulo[0] , subtitulo[1] , "" , "" , "" , titletvsneak , seasontvsneak , "" , miserievo )
		else:
			for subtitulo in listasubtitulos:
				match1 = re.search(tecleado,subtitulo[0],re.IGNORECASE)
				if (match1):
					addnewfolder( CHANNELNAME , "listasubs" , category , subtitulo[0] , subtitulo[1] , "" , "" , "" , titletvsneak , seasontvsneak , "" , miserievo )


	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Sorting by date...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findsubs(data,title,miserievo,seasontvsneak):
	xbmc.output("[casttv.py] findsubs")

	seriesubs = []
	seriesubslist = []

	misub = "http://es.tvsubtitles.net/tvshows.html"
	data = scrapertools.cachePage(misub)

	patronvideos = '<a href="tvshow-(\d+)-(\d+).html"><b>([^<]+)</b></a></td>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		
		# Titulo
		titulo = match[2]
		if titulo == "Law and Order UK":
			titulo = "Law & Order: UK"		
		
		# Código serie
		codserie = match[0]

		url=""
		urlL = "http://www.tvsubtitles.net/subtitle-"+codserie+"-"+seasontvsneak+".html"
		urlc = "subtitle-"+codserie+"-"+seasontvsneak+"-"
		# url
		if miserievo.lower() == titulo.lower():
			
			url = "http://www.tvsubtitles.net/subtitle-"+codserie+"-"+seasontvsneak+".html"

		else:
			match2 = re.match('(.*?) \(20\d\d\)$',miserievo,re.IGNORECASE)
			if (match2):
				if match2.group(1).lower() == titulo.lower():
					url = "http://www.tvsubtitles.net/subtitle-"+codserie+"-"+seasontvsneak+".html"
			match1 = re.search('\:',miserievo,re.IGNORECASE)
			if (match1):
				if miserievo.replace(':' , '').lower() == titulo.lower():
					url = "http://www.tvsubtitles.net/subtitle-"+codserie+"-"+seasontvsneak+".html"
			match3 = re.search('\s\&\s',miserievo,re.IGNORECASE)
			if (match3):
				if miserievo.replace('&' , 'and').lower() == titulo.lower():
					url = "http://www.tvsubtitles.net/subtitle-"+codserie+"-"+seasontvsneak+".html"
			match4 = re.search('\sand\s',miserievo,re.IGNORECASE)
			if (match4):
				if miserievo.replace('and' , '&').lower() == titulo.lower():
					url = "http://www.tvsubtitles.net/subtitle-"+codserie+"-"+seasontvsneak+".html"
		
		if url <> "":
			seriesubs.append( [ titulo , url , urlc ] )

		seriesubslist.append( [ titulo , urlL , urlc ] )			

	if len(seriesubs)==1:

		return seriesubs
	else:

		return seriesubslist

def searchsubs(data):
	xbmc.output("[casttv.py] searchsubs")

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
				return tecleado
	else:
		return letras[seleccion-1]

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

def alertnoepisodios():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Episodios no disponibles' , 'No se han encontrado episodios gratuitos.' , '')

def addsimplefolder( canal , accion , category , title , url , thumbnail ):
	xbmc.output("[casttv.py] addsimplefolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , date , titletvsneak , seasontvsneak , seasontv , miserievo ):
	xbmc.output("[casttv.py] addnewfolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&date=%s&titletvsneak=%s&seasontvsneak=%s&seasontv=%s&miserievo=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( date ) , urllib.quote_plus( titletvsneak ) , urllib.quote_plus( seasontvsneak ) , urllib.quote_plus( seasontv ) , urllib.quote_plus( miserievo ) )
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
