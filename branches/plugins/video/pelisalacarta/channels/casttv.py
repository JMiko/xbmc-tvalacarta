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

STARORANGE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','starorangesmall.png' ) )
STARBLUE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','starbluesmall.png' ) )
STARGREEN_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreensmall.png' ) )
STARGREEN2_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreensmall2.png' ) )
STARGB_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreenblue.png' ) )
FOLDERBLUE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','foldericonblue.png' ) )
BUSCADOR_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters','buscador.png' ) )
HELP_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','help.png' ) )


def mainlist(params,url,category):
	xbmc.output("[casttv.py] mainlist")

	category = "CastTV - TVSneak - Series VO"

	addsimplefolder( CHANNELNAME , "listado" , "Series VO - Actualizadas" , "Series VO - Últimas Actualizaciones" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "listado" , category , "Series VO - Listado Completo" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "listado" , "Mis Favoritas" , "Series VO - Mis Favoritas","http://www.casttv.com/shows/",STARORANGE_THUMB )
	addsimplefolder( CHANNELNAME , "search" , "Series VO - Buscar" , "Series VO - Buscar","http://www.casttv.com/shows/",BUSCADOR_THUMB )
	addsimplefolder( CHANNELNAME , "ayuda" , "Series VO - Ayuda" , "Ayuda" , "" , HELP_THUMB )

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

	listadoupdate(tipolist,category,False)

def listadoupdate(tipolist,category,listupdate):
	xbmc.output("[casttv.py] listadoupdate")

	url = "http://www.casttv.com/shows/"
	thumbnail=""
	nuevos = []
	series = []

	#Se cambia el diálogo sólo al entrar a "Mis Favoritas"
	if tipolist=="Favoritas" and listupdate==False:
		Dialogespera = xbmcgui.DialogProgress()
		line1 = 'Buscando información de "Mis Favoritas"...'
		line2 = ''
  		resultado = Dialogespera.create('pelisalacarta' , line1 , line2 )

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	listaseries = []

	listafav = readfav("","")

	if tipolist <> "Favoritas":
		listaseries = findseries(data,tipolist,"")
	else:	
		if len(listafav)>0:
			listaseries=findstatus(listafav)
			listaupdated = findseries(data,"Actualizaciones","")
				
		elif listupdate==False:
			Dialogespera.close()
			alertnofav()
			return
	
	for serie in listaseries:
		if tipolist <> "Favoritas":
			thumbnail=""
			if serie[3]=="-1" and tipolist <> "Actualizaciones":
				#En el propio ldo de act. no se cambia el color
				thumbnail=FOLDERBLUE_THUMB
			if len(listafav)>0:
				for fav in listafav:
					if serie[0]==fav[0]:
						thumbnail=STARORANGE_THUMB
						if serie[3]=="-1" and tipolist <> "Actualizaciones":
							thumbnail=STARBLUE_THUMB
						break
		if tipolist == "Favoritas":
			encontrado="0"
			thumbnail=STARORANGE_THUMB
			listanuevos = []
			listanuevos=findnuevos(serie[0],serie[2],"0")
			for update in listaupdated:			
				if serie[0]==update[0]:
					encontrado="-1"
					thumbnail=STARBLUE_THUMB
					if len(listanuevos)>0:
						thumbnail=STARGB_THUMB
					break
			if len(listanuevos)>0:
				if encontrado=="0":
					thumbnail=STARGREEN_THUMB
				if serie[3]=="-1":
					nuevos.extend(listanuevos)

		series.append( [ tipolist , serie[0]+serie[1] , serie[2] , thumbnail ] )

	if len(nuevos)>0:
		addsimplefolder( CHANNELNAME , "listatres" , "Mis Favoritas - Nuevos Episodios" , "***Nuevos Episodios (Posteriores a [LW])***" , url , STARGREEN2_THUMB )

	for serie in series:
		addsimplefolder( CHANNELNAME , "listados" , serie[0] , serie[1] , serie[2] , serie[3] )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate , cacheToDisc=False )

	if tipolist=="Favoritas":
		if len(listaseries)==0:		
			alertnofav()
		elif listupdate==False:
			Dialogespera.close()

def findnuevos(serie,url,todos):
	xbmc.output("[casttv.py] findnuevos")
	
	listanuevos = []

	listavistos = readvisto(serie,"LW")
	if len(listavistos)==1 and int(listavistos[0][4])>0:
		data = scrapertools.cachePage(url)
		listaepisodios=findepisodios(data,serie)
		for episodio in listaepisodios:
			if episodio[3] == "0":
				if int(episodio[5])>int(listavistos[0][3]):
					listanuevos.append(episodio)								
				if episodio[5]==listavistos[0][3] and episodio[7]>int(listavistos[0][4]):
					listanuevos.append(episodio)
				if todos=="0" and len(listanuevos)>0:
					break
	return listanuevos				

def search(params,url,category):
	xbmc.output("[casttv.py] search")

	searchupdate(-2,"",category,False)

def searchupdate(seleccion,tecleado,category,listupdate):
	xbmc.output("[casttv.py] searchupdate")

	url = "http://www.casttv.com/shows/"
	thumbnail = ""
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	rtdos = 0
        
	if seleccion == -2:
		opciones = []
		opciones.append('Mostrar Series con Episodios Vistos, Distintas de "Mis Favoritas"')
		opciones.append("Teclado (Busca en Título y Status)")
		for letra in letras:
			opciones.append(letra)
		searchtype = xbmcgui.Dialog()
		seleccion = searchtype.select("Búsqueda por Teclado o por Inicial del Título:", opciones)
	if seleccion == -1 :return
	if seleccion == 0:
		data = scrapertools.cachePage(url)
		listaseries = []
		seriesvistas = []
		listavistos = readvisto("","")
		if len(listavistos)==0:
			alertnoresultadosearch()
			return
		listafav = readfav("","")
		for visto in listavistos:
			encontrado="0"
			for fav in listafav:
				if visto[0]==fav[0]:
					encontrado="-1"
			if encontrado=="0" and seriesvistas.count(visto[0])==0:
				seriesvistas.append(visto[0])
		if len(seriesvistas)==0:
			alertnoresultadosearch()
			return			
		listadoseries = findseries(data,"","")
		for visto in seriesvistas:
			for serie in listadoseries:
				if visto==serie[0]:
					listaseries.append(serie)
					break
		category=category+" Vistos"

	elif seleccion == 1:
		if len(tecleado)==0:
			keyboard = xbmc.Keyboard('')
			keyboard.doModal()
			if (keyboard.isConfirmed()):
				tecleado = keyboard.getText()
				tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
			if keyboard.isConfirmed() is None or len(tecleado)==0:
				return
		data = scrapertools.cachePage(url)				
		if len(tecleado) == 1:
			listaseries = findseries(data,"",tecleado)
		else:
			listaseries = findseries(data,"","")

	else:
		data = scrapertools.cachePage(url)
		listaseries = findseries(data,"",letras[seleccion-2])

	if len(listaseries)==0:
		alertnoresultadosearch()
		return

	listafav = readfav("","")

	for serie in listaseries:
		thumbnail=""
		if serie[3]=="-1":
			thumbnail=FOLDERBLUE_THUMB
		if len(listafav)>0:
			for fav in listafav:
				if serie[0]==fav[0]:
					thumbnail=STARORANGE_THUMB
					if serie[3]=="-1":
						thumbnail=STARBLUE_THUMB
					break

		foldertitle = serie[0]+serie[1]
		if len(tecleado) > 1:
			match = re.search(tecleado,foldertitle,re.IGNORECASE)
			if (match):
				addsimplefolder( CHANNELNAME , "listadossearch" , str(seleccion)+";"+tecleado , foldertitle , serie[2] , thumbnail )
				rtdos = rtdos+1
		else:
			addsimplefolder( CHANNELNAME , "listadossearch" , str(seleccion)+";"+tecleado , foldertitle , serie[2] , thumbnail )
	
	if len(tecleado) > 1 and rtdos==0:
		alertnoresultadosearch()
		return

					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate )

def findseries(data,tipolist,search):
	xbmc.output("[casttv.py] findseries")
	serieslist = []
	
	if tipolist == "Actualizaciones":
		tipolists = '\n\s+&nbsp;<span class="label_updated">Updated!</span>\n\s+</div>'
	else:
		tipolists = '\n\s+(?:&nbsp;<span class="label_updated">Updated!</span>\n\s+|\n\s+)</div>'

	if search == "#":
		search = "\d+"

	patronvideos  = '<div class="gallery_listing_text">\n\s+<a href="(.*?)">('+search+'[^<]+)'
	patronvideos += '</a>('+tipolists+')(\n\s+<div class="icon_current"></div>\n</li>|\n\s+\n</li>)'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulo = match[1]
		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')
		titulo = re.sub('\s+$','',titulo)

		# URL
		url = urlparse.urljoin("http://www.casttv.com",match[0])

		# Updated
		updated = "0"
		if tipolist == "Actualizaciones":
			updated = "-1"
		else:
			match1 = re.search('Updated',match[2],re.IGNORECASE)
			if (match1):
				updated = "-1"

		# Status0
		status0 = ""
		match2 = re.search('icon_current',match[3],re.IGNORECASE)
		if (match2):
			status0 = "  -  [Current tv show]"
		else:
			status0 = "  -  [Ended]"

		serieslist.append( [ titulo , status0 , url , updated ] )

	serieslist=findstatus(serieslist)
	
	return serieslist

def findstatus(serieslist):
	xbmc.output("[casttv.py] findstatus")
	
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

	title = urllib.unquote_plus( params.get("title") )
	miserievo = title
	status = ""
	match = re.match('^(.*?)(\s+\-\s+\[.*?\])$',title)
	if (match):
		miserievo = match.group(1)
		status = match.group(2)
	tipolist = category
	category = "Series VO"
	
	respuesta = serieupdate(miserievo,status,url)

	if respuesta<>1 and respuesta<>2:
		category = "Series VO - "+miserievo
		listadosupdate(miserievo,url,category,False)

def listadossearch(params,url,category):
	xbmc.output("[casttv.py] listadossearch")

	title = urllib.unquote_plus( params.get("title") )
	miserievo = title
	status = ""
	match = re.match('^(.*?)(\s+\-\s+\[.*?\])$',title)
	if (match):
		miserievo = match.group(1)
		status = match.group(2)
	match1 = re.match('^(\d+);(.*)$',category)
	seleccion = int(match1.group(1))
	tecleado = match1.group(2)

	respuesta = serieupdate(miserievo,status,url)

	if respuesta==1 or respuesta==2:
		category = "Series VO - Buscar"
		searchupdate(seleccion,tecleado,category,True)
	else:
		category = "Series VO - Buscar - "+miserievo
		listadosupdate(miserievo,url,category,False)
			
def listadosupdate(miserievo,url,category,listupdate):
	xbmc.output("[casttv.py] listadosupdate")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	listaepisodios = findepisodios(data,miserievo)

	if len(listaepisodios) == 0:
		alertnoepisodios(1)
		return
	
	listavistos = readvisto(miserievo,"")
	vistoid2 = ""

	for episodio in listaepisodios:
		if episodio[3] == "0":
			tipovisto = ""
			if len(listavistos)>0:
				vistoid = vistoid2
				if vistoid2<>"":
					tipovisto="1A"
				formato = ""				
				for visto in listavistos:			
					if episodio[0]==visto[1] and episodio[1]==visto[2]:
						tipovisto = visto[5]
						if visto[5]=="1":
							vistoid = "[LW]"
							vistoid2 = "[W]"
						elif visto[5]=="2":
							vistoid = "[LW]"
						elif visto[5]=="3":
							vistoid = "[W]"
							if vistoid2<>"":
								tipovisto="31"
						elif visto[5]=="4":
							vistoid = "[UW]"
						elif visto[5]=="0":
							vistoid = ""
							if vistoid2<>"":
								tipovisto="01"
						break
				if vistoid<>"":
					formato="  -  "							
				addnewfolder( CHANNELNAME , "episodiomenu" , category , episodio[0]+formato+vistoid , episodio[1] , episodio[9] , episodio[10] , episodio[2] , episodio[4] , episodio[5] , episodio[6] , miserievo , episodio[8] , episodio[7] , url , tipovisto )

			else:
				tipovisto = "N"
				addnewfolder( CHANNELNAME , "episodiomenu" , category , episodio[0] , episodio[1] , episodio[9] , episodio[10] , episodio[2] , episodio[4] , episodio[5] , episodio[6] , miserievo , episodio[8] , episodio[7] , url , tipovisto )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Sorting by date...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate )

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
		episodioslist.append( [ titulo , url , date , pago , titletvsneak , seasontvsneak , seasontv , episodiotv , tvsneak , thumbnail , plot ] )
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
					if episodio[8]=="0":
						episodio[8] = "-1"
					if episodio[7] > 1:
						lastseasontv = episodioscasttv[-1]
						if episodio[6] == lastseasontv:
							if n < len(episodioslist)-1 and episodioslist[n+1][6] <> episodio[6] :						
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , "-1" , episodio[9] , episodio[10] ])
							elif n == len(episodioslist)-1:
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , "-1" , episodio[9] , episodio[10] ])
						capitvnew = episodio[7]-1
						seasontvnew = episodio[6][0:4]+str(capitvnew)
						if len(seasontvnew) == 5:
							seasontvnew = seasontvnew.replace('E' , 'E0')
						
						if episodioslist[n+1][5] == season and episodioslist[n+1][6] <> episodio[6] and episodioslist[n+1][7] <> capitvnew:
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , "-1" , episodio[9] , episodio[10] ])
						if episodioslist[n+1][5] == str(int(season)-1) and episodioslist[n+1][5] <> "0":
							episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , "" , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , "-1" , episodio[9] , episodio[10] ])

	return episodioslist

def listatres(params,url,category):
	xbmc.output("[casttv.py] listatres")

	listatresupdate(url,category,False)

def listatresupdate(url,category,listupdate):
	xbmc.output("[casttv.py] listatresupdate")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	listafav = []
	listafav = readfav("","-1")
	nuevos = []

	listaupdated = findseries(data,"Actualizaciones","")
			
	for serie in listafav:
		listanuevos=findnuevos(serie[0],serie[2],"-1")
		if len(listanuevos)>0:
			nuevos.extend(listanuevos)
			for episodio in listanuevos:
				if episodio[3] == "0":
					addnewfolder( CHANNELNAME , "episodiomenu" , category , episodio[0] , episodio[1] , episodio[9] , episodio[10] , episodio[2] , episodio[4] , episodio[5] , episodio[6] , serie[0] , episodio[8] , episodio[7] , url , "New" )

	if len(nuevos)==0:
		alertnoepisodios(2)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate )

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
	titleshort = title
	if date<>"":
		titleshort = re.sub('\s\-\s'+date,'',titleshort)
	urltvsneak0 = titletvsneak+"-season-"+seasontvsneak
	
	listacasttv = []
	listactmirrors = []
	listaTVSneak = []

	# CastTV
	if url <> "":
		# tipo 1: Megavideo es el tipo de reproducción
		data0 = scrapertools.cachePage(url)
		listacasttv = servertools.findvideos(data0)		
		# tipo 2: Megavideo no es el tipo de reproducción
		if len(listacasttv)==0:
			# obtiene la url de la página para reproducir con Megavideo si existe	
			match = re.search('<a class="source_row" href="(.*?)"> <img alt="MegaVideo"',data0,re.IGNORECASE)

			# Descarga la página para reproducir con Megavideo si existe
			if (match):
				data = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match.group(1)))
				listacasttv = servertools.findvideos(data)				
				data0 = data

		if len(listacasttv)>0:	
			# obtiene la url de la página para reproducir con Megavideo del mirror si existe	
			match1 = re.search('<a class="source_copies" href="(.*?)">COPY 2',data0,re.IGNORECASE)

			# Descarga la página para reproducir con Megavideo del mirror si existe
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
				# Eliminar cuando haya un patrón para Divxden en servertools
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
	# Añade los enlaces a los videos
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
	resultado = advertencia.ok('Vídeo no disponible' , 'No se ha añadido aún a la web un enlace' , 'compatible.')

def alertnoepisodios(tipo):
	advertencia = xbmcgui.Dialog()
	if tipo==1:
		resultado = advertencia.ok('Episodios no disponibles' , 'No se han encontrado episodios gratuitos.' , '')
	elif tipo==2:
		resultado = advertencia.ok('Msj. Informativo:' , 'No se han encontrado Nuevos Episodios.' , '')


def alertnoresultadosearch():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'La Búsqueda no ha obtenido Resultados.' , '')

def alertnofav():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'No se han añadido Series a Favoritas.' , '')

def addsimplefolder( canal , accion , category , title , url , thumbnail ):
	xbmc.output("[casttv.py] addsimplefolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , date , titletvsneak , seasontvsneak , seasontv , miserievo , tvsneak , episodiotv , urlback , tipovisto ):
	xbmc.output("[casttv.py] addnewfolder")
	listitem= xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( type="Video", infoLabels={ "Title" : title, "Plot" : plot, "Date" : date } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&date=%s&titletvsneak=%s&seasontvsneak=%s&seasontv=%s&miserievo=%s&tvsneak=%s&episodiotv=%s&urlback=%s&tipovisto=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( date ) , urllib.quote_plus( titletvsneak ) , urllib.quote_plus( seasontvsneak ) , urllib.quote_plus( seasontv ) , urllib.quote_plus( miserievo ) , urllib.quote_plus( tvsneak ) , episodiotv , urllib.quote_plus( urlback ) , urllib.quote_plus( tipovisto ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	xbmc.output('[casttv.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def additem( canal , category , title , url , thumbnail, plot ):
	xbmc.output('[casttv.py] additem')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultHardDisk.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def ayuda(params,url,category):
	xbmc.output("[casttv.py] ayuda")

	additem( CHANNELNAME , category , "***+++++++++++++++ Leyenda +++++++++++++++***" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[LW]: Último Episodio Visto (Last Watched)" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[W]: Episodio Visto (Watched)" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[UW]: Episodio No Visto (UnWatched)" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "Series Actualizadas [excepto Aptdo Actualizaciones]" , "" , FOLDERBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "Series Favoritas" , "" , STARORANGE_THUMB , "" )
	additem( CHANNELNAME , category , "(1) Favoritas Actualizadas [excepto Aptdo Actualizaciones]" , "" , STARBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "(2) Favoritas con Nuevos Episodios [Aptdo Mis Favoritas]" , "" , STARGREEN_THUMB , "" )
	additem( CHANNELNAME , category , "(1) y (2) - [Aptdo Mis Favoritas]" , "" , STARGB_THUMB , "" )
	additem( CHANNELNAME , category , "Nuevos Episodios (posteriores a [LW]) [Aptdo Mis Favoritas]" , "" , STARGREEN2_THUMB , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


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

def serieupdate(miserievo,status,url):
	xbmc.output("[casttv.py] serieupdate")

	listfav=readfav(miserievo,"")
	if len(listfav)==0:
		respuesta = seriemenu("0","0")
		if respuesta==1:
			upgradefav(miserievo,status,url,"-1","1")
	else:
		if listfav[0][3]=="-1":
			respuesta = seriemenu("-1","-1")
			if respuesta==2:
				upgradefav(miserievo,status,url,"0","1")
		elif listfav[0][3]=="0":
			respuesta = seriemenu("-1","0")
			if respuesta==2:
				upgradefav(miserievo,status,url,"-1","1")
		if respuesta==1:
				upgradefav(miserievo,status,url,"-1","0")
	return respuesta

def seriemenu(tipofav,tiponuevos):
	xbmc.output("[casttv.py] seriemenu")

	seleccion = ""
	opciones = []
	opciones.append("Abrir Listado de Episodios  (opción por defecto)")
	if tipofav=="0":
		opciones.append('Añadir a "Mis Favoritas"')
	elif tipofav=="-1":
		opciones.append('Eliminar de "Mis Favoritas"')
		if tiponuevos=="0":
			opciones.append('Activar Seguimiento en "Nuevos Episodios"')
		elif tiponuevos=="-1":
			opciones.append('Desactivar Seguimiento en "Nuevos Episodios"')
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Seleccione una opción:", opciones)

	return seleccion

def episodiomenu(params,url,category):
	xbmc.output("[casttv.py] episodiomenu")

	title = urllib.unquote_plus( params.get("title") )
	title0 = re.sub('\s+\-\s+\[U?L?W\]$','',title)
	tipovisto = urllib.unquote_plus( params.get("tipovisto") )
	miserievo = urllib.unquote_plus( params.get("miserievo") )
	urlback = urllib.unquote_plus( params.get("urlback") )
	season = urllib.unquote_plus( params.get("seasontvsneak") )
	episodio = params.get("episodiotv")

	if tipovisto=="1": textipo="Último Visto y anteriores [LW]/[W]"
	elif tipovisto=="2": textipo="Último Visto [LW]"
	elif tipovisto=="3" or tipovisto=="1A" or tipovisto=="31": textipo="Visto [W]"
	elif tipovisto=="4": textipo="No Visto [UW]"
	elif tipovisto=="New": textipo="Nuevo Episodio"

	opciones = []
	opciones.append("Abrir Listado de Vídeos (opción por defecto)")

	if tipovisto<>"1":
		opciones.append('Marcar: Último Visto y anteriores [LW]/[W]')
	if tipovisto<>"2":
		opciones.append('Marcar: Último Visto [LW]')
	if tipovisto<>"3" and tipovisto<>"31" and  tipovisto<>"1A" and  tipovisto<>"New":
		opciones.append('Marcar: Visto [W]')
	if tipovisto<>"" and tipovisto<>"N" and tipovisto<>"0" and tipovisto<>"01" and tipovisto<>"New":
		opciones.append('Desmarcar: '+textipo)
	if tipovisto=="31" or  tipovisto=="1A" or tipovisto=="01":
		opciones.append('Marcar: No Visto [UW]')
	if tipovisto<>"N" and  tipovisto<>"New":
		opciones.append('Desmarcar: Todo (Serie Completa)')

	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Seleccione una opción:", opciones)

	if seleccion==-1 or seleccion==0:
		detaildos(params,url,category)
		return
	else:
		if tipovisto=="" or tipovisto=="N" or tipovisto=="0" or tipovisto=="New":
			if seleccion==4:
				accion = "T"
			else:
				accion = str(seleccion)
		elif tipovisto=="01" or tipovisto=="31" or  tipovisto=="1A":
			if seleccion==3:
				if tipovisto=="01":
					accion = "31"
				elif tipovisto=="31" or  tipovisto=="1A":
					accion = "0"
			elif seleccion==5:
				accion = "T"
			else:
				accion = str(seleccion)
		elif tipovisto == "1" or tipovisto == "2":
			if seleccion==1:
				if tipovisto == "1":
					accion = "2"
				else:
					accion = "1"
			elif seleccion==2:
				accion = "3"
			elif seleccion==3:
				accion = "0"
			elif seleccion==4:
				accion = "T"
		elif tipovisto == "3" or tipovisto == "4":
			if seleccion==int(tipovisto):
				accion = "0"
			elif seleccion==int(tipovisto)+1:
				accion = "T"
			else:
				accion = str(seleccion)
	
	upgradevisto(miserievo,title0,url,season,episodio,accion)
	
	if tipovisto=="New":
		listatresupdate(urlback,category,True)
	else:
		listadosupdate(miserievo,urlback,category,True)

def readfav(serievo,tiponuevos):
	xbmc.output("[casttv.py] readfav")

	if serievo<>"":	
		seriesearch = re.sub('(?P<signo>\(|\)|\'|\"|\[|\]|\.|\?|\+)','\\\\\g<signo>',serievo)
	else:
		seriesearch = "[^;]+"

	if tiponuevos=="":
		tiponuevos = "[^;]+"

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )

	# Crea el directorio si no existe
	try:
		os.mkdir(VISTO_PATH)
	except:
		pass

	favlist = []
	filename = 'casttvfav.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)
	if not os.path.exists(fullfilename):
		favfile = open(fullfilename,"w")
		favfile.close()
	else:
		favfile = open(fullfilename)
		for line in favfile:
			match = re.match('('+seriesearch+');([^;]+);([^;]+);('+tiponuevos+');\n',line)
			if (match):
				serie = match.group(1)
				status = match.group(2)
				url = match.group(3)
				seguirnuevos = match.group(4)
				favlist.append([ serie , status , url , seguirnuevos ])
				if serievo<>"":
					break
		favfile.close()

	return favlist

def upgradefav(serie,status,url,seguirnuevos,tipo):
	xbmc.output("[casttv.py] upgradefav")

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )
	favlist = []
	encontrado = "0"
	detener = "0"
	OK = "0"
	filename = 'casttvfav.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)

	favfile = open(fullfilename)
	for line in favfile:
		match = re.match('([^;]+);([^;]+);([^;]+);([^;]+);\n',line)
		if (match):
			serief = match.group(1)
			statusf = match.group(2)
			urlf = match.group(3)
			seguirnuevosf = match.group(4)
			if serief<>serie:
				favlist.append([ serief , statusf , urlf , seguirnuevosf ])

	favfile.close()

	if tipo=="1":
		favlist.append([ serie , status , url , seguirnuevos ])

	favlist.sort()

	favfile = open(fullfilename,"w")
	for fav in favlist:
		favfile.write(fav[0]+';'+fav[1]+';'+fav[2]+';'+fav[3]+';\n')
	favfile.close()

def readvisto(serie,tipo):
	xbmc.output("[casttv.py] readvisto")

	if serie<>"":	
		seriesearch = re.sub('(?P<signo>\(|\)|\'|\"|\[|\]|\.|\?|\+)','\\\\\g<signo>',serie)
	else:
		seriesearch="[^;]+"

	if tipo=="LW":
		tipos="(?:1|2)"
	else:
		tipos="[^;]+"

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )

	# Crea el directorio de visto si no existe
	try:
		os.mkdir(VISTO_PATH)
	except:
		pass
	
	encontrado = "0"
	vistolist = []
	filename = 'casttv.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)
	if not os.path.exists(fullfilename):
		vistofile = open(fullfilename,"w")
		vistofile.close()
	else:
		vistofile = open(fullfilename)
		for line in vistofile:
			match = re.match('('+seriesearch+');([^;]+);([^;]+);([^;]+);([^;]+);('+tipos+');\n',line)
			if (match):
				seriev = match.group(1)
				titulo = match.group(2)
				url = match.group(3)
				season = match.group(4)
				episodio = match.group(5)
				tipo = match.group(6)
				vistolist.append([ seriev , titulo , url , season , episodio , tipo ])
				encontrado = "-1"
			elif encontrado == "-1":
				break
		vistofile.close()

	return vistolist

def upgradevisto(serie,titulo,url,season,episodio,tipo):
	xbmc.output("[casttv.py] upgradevisto")

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )
	vistolist = []
	encontrado = "0"
	detener = "0"
	OK = "0"
	filename = 'casttv.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)

	vistofile = open(fullfilename)
	for line in vistofile:
		match = re.match('([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);\n',line)
		if (match):
			serief = match.group(1)
			titulof = match.group(2)
			urlf = match.group(3)
			seasonf = match.group(4)
			episodiof = match.group(5)
			tipof = match.group(6)
			if serief<>serie:
				vistolist.append([ serief , titulof , urlf , seasonf, episodiof , tipof ])
			if serief==serie and tipo=="T" and OK=="0":
				respuesta = alertcontinuarT()
				if respuesta is None:
					detener="-1"
					break
				else:
					OK= "-1"
			if serief==serie and tipo<>"T":
				if tipo=="0" and titulof==titulo and urlf==url:
					encontrado = "-1"
				if titulof<>titulo or urlf<>url:
					if tipo=="1" or tipo=="2":
						if tipo=="2" and tipof=="3":
							if int(seasonf)<int(season):
								vistolist.append([ serief , titulof , urlf , seasonf, episodiof , tipof ])
							elif int(seasonf)==int(season) and int(episodiof)<int(episodio):
								vistolist.append([ serief , titulof , urlf , seasonf, episodiof , tipof ])
						if tipof=="4":
							vistolist.append([ serief , titulof , urlf , seasonf, episodiof , tipof ])
						if tipof=="1" or tipof=="2":
							respuesta = alertcontinuar(tipo,tipof)
							if respuesta:
								if tipo=="2" and tipof=="2":
									if int(seasonf)<int(season):
										vistolist.append([ serief , titulof , urlf , seasonf, episodiof , "3" ])
									elif int(seasonf)==int(season) and int(episodiof)<int(episodio):
										vistolist.append([ serief , titulof , urlf , seasonf, episodiof , "3" ])
							else:
								detener="-1"
								break
					if tipo=="3":
						if tipof=="1" or tipof=="2":
							if int(seasonf)>int(season):
								vistolist.append([ serief , titulof , urlf , seasonf, episodiof , tipof ])
							elif int(seasonf)==int(season) and int(episodiof)>int(episodio):
								vistolist.append([ serief , titulof , urlf , seasonf, episodiof , tipof ])
							else:
								alertnoanterior()
								detener="-1"
								break
						else:
							vistolist.append([ serief , titulof , urlf, seasonf, episodiof , tipof ])
							
					if tipo=="0" or tipo=="4" or tipo=="31":
						vistolist.append([ serief , titulof , urlf, seasonf, episodiof , tipof ])
	vistofile.close()
	if detener=="-1": return


	if tipo=="0" and encontrado=="0":
		vistolist.append([ serie , titulo , url , season, episodio , tipo ])
	if tipo<>"0" and tipo<>"31" and tipo<>"T":
		vistolist.append([ serie , titulo , url , season, episodio , tipo ])

	vistolist.sort()

	vistofile = open(fullfilename,"w")
	for visto in vistolist:
		vistofile.write(visto[0]+';'+visto[1]+';'+visto[2]+';'+visto[3]+';'+visto[4]+';'+visto[5]+';\n')
	vistofile.close()

	
def alertcontinuar(tipo,tipof):
	advertencia = xbmcgui.Dialog()
	linea1 = "Se desmarcará el episodio [LW] actual y Vistos [W]."
	linea2 = "Los No Vistos [UW] no se desmarcan." 
	linea3 = "¿Desea continuar?"
	if tipof=="2" and tipo=="2":
		linea1 = "Se marcará como Visto [W] el episodio [LW] actual,"
		linea2 = "si es anterior. Los Vistos [W] posteriores se"
		linea3 = "desmarcarán. ¿Desea continuar?"
	if tipof=="2" and tipo=="1":
		linea1 = "Se desmarcará el episodio [LW] actual y Vistos [W]"
		linea2 = "posteriores. ¿Desea continuar?"
		linea3 = ""
	resultado = advertencia.yesno('pelisalacarta' , linea1 , linea2 , linea3 )
	return resultado

def alertcontinuarT():
	advertencia = xbmcgui.Dialog()
	linea1 = "Se desmarcarán todos los episodios."
	linea2 = "¿Desea continuar?"
	resultado = advertencia.yesno('pelisalacarta' , linea1 , linea2 )
	return resultado	

def alertnoanterior():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('pelisalacarta' , 'No es posible marcar un episodio como Visto [W]' , 'posterior a uno marcado como [LW]')
