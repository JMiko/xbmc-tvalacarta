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
import tvshack
import config

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
STARGREY_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreysmall.png' ) )
HD_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','harddisk.png' ) )
STARGB_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreenblue.png' ) )
FOLDERBLUE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','foldericonblue.png' ) )
HELP_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','help.png' ) )
DESCARGAS_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','descargados.png' ) )

def mainlist(params,url,category):
	xbmc.output("[casttv.py] mainlist")

	category = "CastTV - TVShack - Series VO"

	addsimplefolder( CHANNELNAME , "listado" , "Series VO - Actualizadas" , "Series VO - Últimas Actualizaciones" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "listado" , category , "Series VO - Listado Completo" , "http://www.casttv.com/shows/" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "listado" , "Mis Favoritas" , "Series VO - Mis Favoritas","http://www.casttv.com/shows/",STARORANGE_THUMB )
	addsimplefolder( CHANNELNAME , "search" , "Series VO - Buscar" , "Series VO - Buscar" , "http://www.casttv.com/shows/","http://www.mimediacenter.info/xbmc/pelisalacarta/posters/buscador.png" )
	addsimplefolder( CHANNELNAME , "searchsub" , "Subtítulos.es" , "Subtítulos.es" , "" , "http://www.subtitulos.es/images/subslogo.png" )
	addsimplefolder( CHANNELNAME , "ayuda" , "Series VO - Ayuda" , "Ayuda" , "" , HELP_THUMB )
	#addsimplefolder( CHANNELNAME , "listtvshack" , "TVShack" , "TVShack" , "" , "" )

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

	if tipolist=="Favoritas":
		Dialogespera = xbmcgui.DialogProgress()
		line1 = 'Buscando información de "Mis Favoritas"...'
		line2 = ''
  		resultado = Dialogespera.create('pelisalacarta' , line1 , line2 )

	url = "http://www.casttv.com/shows/"
	thumbnail=""
	search = ""
	listaseries = []
	nuevos = []
	series = []

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	try:
		data = scrapertools.cachePage(url)
	except:
		alertsinconexion()
		return

	listafav = readfav("","","",CHANNELNAME)

	if tipolist <> "Favoritas":
		listaseries = findseries(data,tipolist,"","","0",0)
	else:	
		if len(listafav)==0:
			alertnofav()
			return
		else:
			listaseries=listafav
			for fav in listafav:
				titulo=re.sub('[\\\\]?(?P<signo>[^\w\s\\\\])','\\\\\g<signo>',fav[0])
				if search=="":
					search=titulo
				else:
					search=search+"|"+titulo
			search="(?:"+search+")"
			listactv = findseries(data,"Completo",search,"","0",0)
	
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
						if fav[3]=="1":
							thumbnail=STARGREY_THUMB
						break

		if tipolist == "Favoritas":
			encontrado = "0"
			if serie[3]=="1":
				thumbnail=STARGREY_THUMB
				for ctv in listactv:			
					if serie[0]==ctv[0]:
						encontrado = "-1"
						# se actualizan los datos de status y url
						serie[1] = ctv[1]
						serie[2] = ctv[2]
						break
			else:
				updated="0"
				thumbnail=STARORANGE_THUMB
				listanuevos = []
				listanuevos=findnuevos(serie[0],serie[2],"0")
				for ctv in listactv:			
					if serie[0]==ctv[0]:
						encontrado = "-1"
						serie[1] = ctv[1]
						serie[2] = ctv[2]
						if ctv[3]=="-1":
							updated="-1"
							thumbnail=STARBLUE_THUMB
							if len(listanuevos)>0:
								thumbnail=STARGB_THUMB
							break
				if len(listanuevos)>0:
					if updated=="0":
						thumbnail=STARGREEN_THUMB
					if serie[3]=="-1":
						nuevos.extend(listanuevos)

			# evita el status desactualizado de fav caso extremo de no encontrarse ya en CastTV
			if encontrado=="0":
				serie[1]=""
		status=""
		if serie[1]<>"":
			status="  -  "+serie[1]

		series.append( [ tipolist , serie[0]+status , serie[2] , thumbnail ] )

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

def findnuevos(serie,url,todos):
	xbmc.output("[casttv.py] findnuevos")
	
	listanuevos = []

	listavistos = readvisto(serie,"LW",CHANNELNAME)
	if len(listavistos)==0:
		return listanuevos
	else:
		listavistos.sort(key=lambda visto: visto[5])
		if listavistos[0][5]=="4":
			return listanuevos

	try:
		data = scrapertools.cachePage(url)
	except:
		return listanuevos

	listaepisodios=findepisodios(data,serie,"","0",0)
	#el listado está ordenado por fecha lo que simplifica la búsqueda
	stop="0"
	for episodio in listaepisodios:
		if episodio[3]<>"0":
			continue
		OK="-1"
		for visto in listavistos:
			if episodio[0]==visto[1] and episodio[5]==visto[3] and episodio[7]==int(visto[4]):
				if visto[5]=="1" or visto[5]=="2":		
					stop="-1"
				elif visto[5]=="4":
					OK="0"
				break
			#por si el LW es un episodio automático y falla la web por la que se añadió
			elif episodio[5]<>"0" and episodio[7]<>0 and visto[3]<>"0" and visto[4]<>"0":
				if visto[5]=="1" or visto[5]=="2":
					if int(episodio[5])<int(visto[3]):		
						stop="-1"
						break
					if int(episodio[5])==int(visto[3]) and episodio[7]<int(visto[4]):
						stop="-1"
						break
		if stop=="-1":
			break
		if OK=="-1":
			listanuevos.append(episodio)
			if todos=="0":
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
		listavistos = readvisto("","",CHANNELNAME)
		if len(listavistos)==0:
			alertnoresultadosearch()
			return
		listafav = readfav("","","",CHANNELNAME)
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
		listadoseries = findseries(data,"","","","0",0)
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
			listaseries = findseries(data,"",tecleado,"","0",0)
		else:
			listaseries = findseries(data,"","","","0",0)

	else:
		data = scrapertools.cachePage(url)
		listaseries = findseries(data,"",letras[seleccion-2],"","0",0)

	if len(listaseries)==0:
		alertnoresultadosearch()
		return

	listafav = readfav("","","",CHANNELNAME)

	for serie in listaseries:
		thumbnail=""
		if serie[3]=="-1":
			thumbnail=FOLDERBLUE_THUMB
		if len(listafav)>0:
			for fav in listafav:
				if serie[0]==fav[0]:
					if fav[3]=="1":
						thumbnail=STARGREY_THUMB
						break
					thumbnail=STARORANGE_THUMB
					if serie[3]=="-1":
						thumbnail=STARBLUE_THUMB
					break

		foldertitle = serie[0]+"  -  "+serie[1]
		if len(tecleado) > 1:
			match = re.search(tecleado,foldertitle,re.IGNORECASE)
			if (match):
				rtdos = rtdos+1
			else:
				continue

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

def findseries(data,tipolist,search,titlesubsearch,season,episodio):
	xbmc.output("[casttv.py] findseries")

	serieslist = []
	listepisodios = []
	miseriectv = ""
	
	if tipolist == "Actualizaciones":
		tipolists = '\n\s+&nbsp;<span class="label_updated">Updated!</span>\n\s+</div>'
	else:
		tipolists = '\n\s+(?:&nbsp;<span class="label_updated">Updated!</span>\n\s+|\n\s+)</div>'

	if search == "#":
		search = "[^a-zA-Z]"

	patronvideos  = '<div class="gallery_listing_text">\n\s+<a href="(.*?)">('+search+'[^<]*)'
	patronvideos += '</a>('+tipolists+')(\n\s+<div class="icon_current"></div>\n</li>|\n\s+\n</li>)'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulo = match[1]
		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')
		titulo = re.sub('\s+$','',titulo)
		titlectvsearch = ftitlectvsearch(titulo)

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
			status0 = "[Current tv show]"
		else:
			status0 = "[Ended]"
		
		serieslist.append( [ titulo , status0 , url , updated , titlectvsearch ] )

	if tipolist<>"listforsubs":
		serieslist=findstatus(serieslist)	
		return serieslist
	else:
		if len(serieslist)>0:
			itemencontrado = searchgate(serieslist,titlesubsearch)
			if len(itemencontrado)==1:
				miseriectv = itemencontrado[0][0]
				urlctv = itemencontrado[0][2]
				data = scrapertools.cachePage(urlctv)
				listepisodios = findepisodios(data,miseriectv,tipolist,season,episodio)
		return miseriectv,listepisodios


def findstatus(serieslist):
	xbmc.output("[casttv.py] findstatus")
	
	mistatus = "http://eztv.it/showlist/"
	try:
		data2 = scrapertools.cachePage(mistatus)
	except:
		return serieslist

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
				serie[1] = "["+status+"]"
			else:
				match2 = re.match('(.*?) \(20\d\d\)$',serie[0],re.IGNORECASE)
				if (match2):
					if match2.group(1).lower() == titulo2.lower():
						serie[1] = "["+status+"]"
					
				match3 = re.search('\s\&\s',serie[0],re.IGNORECASE)
				if (match3):
					if serie[0].replace('&' , 'and').lower() == titulo2.lower():
						serie[1] = "["+status+"]"
				
				match4 = re.search('\'s',serie[0],re.IGNORECASE)
				if (match4):
					if serie[0].replace('\'s' , 's').lower() == titulo2.lower():
						serie[1] = "["+status+"]"
										
	return serieslist

def listados(params,url,category):
	xbmc.output("[casttv.py] listados")

	title = urllib.unquote_plus( params.get("title") )
	miserievo = title
	status = ""
	match = re.match('^(.*?)\s+\-\s+(\[.*?\])$',title)
	if (match):
		miserievo = match.group(1)
		status = match.group(2)
	tipolist = category
	category = "Series VO"
	
	respuesta = serieupdate(miserievo,status,url,"",CHANNELNAME)

	if respuesta<>1 and respuesta<>2 and respuesta<>3:
		category = "Series VO - "+miserievo
		listadosupdate(miserievo,url,category,False)

def listadossearch(params,url,category):
	xbmc.output("[casttv.py] listadossearch")

	title = urllib.unquote_plus( params.get("title") )
	miserievo = title
	status = ""
	match = re.match('^(.*?)\s+\-\s+(\[.*?\])$',title)
	if (match):
		miserievo = match.group(1)
		status = match.group(2)
	match1 = re.match('^(\d+);(.*)$',category)
	seleccion = int(match1.group(1))
	tecleado = match1.group(2)

	respuesta = serieupdate(miserievo,status,url,"",CHANNELNAME)

	if respuesta==1 or respuesta==2 or respuesta==3:
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

	listaepisodios = findepisodios(data,miserievo,"","0",0)

	if len(listaepisodios) == 0:
		alertnoepisodios(1)
		return

	listavistos = readvisto(miserievo,"",CHANNELNAME)
	vistoid2 = ""
	vistotipo2 = "0"

	for episodio in listaepisodios:
		if episodio[3] == "0":
			tipovisto = ""
			if len(listavistos)>0:
				vistoid = vistoid2
				if vistoid2<>"":
					tipovisto="1A"
				formato = ""				
				for visto in listavistos:
					#if episodio[0]==visto[1] and episodio[1]==visto[2]:
					#puede cambiar la url, por si hay algún título duplicado se evita que se duplique la marca [LW]
					if episodio[0]==visto[1]:
						tipovisto = visto[5]
						if visto[5]=="1":
							if vistoid2=="":
								vistoid = "[LW]"
								vistoid2 = "[W]"
						elif visto[5]=="2":
							if vistotipo2=="0":
								vistoid = "[LW]"
								vistotipo2 = "-1"
						elif visto[5]=="3":
							vistoid = "[W]"
							if vistoid2<>"":
								tipovisto="31"
						elif visto[5]=="4":
							vistoid = "[NW]"
							if vistoid2<>"":
								tipovisto="41"
						elif visto[5]=="5":
							vistoid = "[UW]"
							if vistoid2<>"":
								tipovisto="51"
						elif visto[5]=="0":
							vistoid = ""
							if vistoid2<>"":
								tipovisto="01"
						break
				if vistoid<>"":
					formato="  -  "
				titulo = episodio[0]+formato+vistoid							
			else:
				tipovisto = "N"
				titulo = episodio[0]

			addnewfolder( CHANNELNAME , "episodiomenu" , category , titulo , episodio[1] , episodio[9] , episodio[10] , episodio[2] , episodio[4] , episodio[5] , episodio[6] , miserievo , episodio[8] , episodio[7] , url , tipovisto )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Sorting by date útil para invertir el listado (ep 1 1º...) por el momento descartado porque a igualdad de fecha(automáticos) no respeta el orden inicial...
	# Revisar: probar a crear un índice o agregar fecha a los episodios añadidos "automáticamente"
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate )

def findepisodios(data,miserievo,tipolist,seasonsearch,episodiosearch):
	xbmc.output("[casttv.py] findepisodios")
	episodioslist = []
	listepisodio = []
	seasonlist = []
	episodioscasttv = []
	episodiosctvtvs = []
	encontrados = set()
	depago = "0"
	# datatvsneak = scrapertools.cachePage("http://tvsneak.com")

	# Revisar: Arregla el titulo de la serie para la url de TVSneak
	# titletvsneak = ftitletvsneak(miserievo,datatvsneak)
	titletvsneak = ""

	# Arregla el titulo para búsquedas: se podría pasar entre listados (ant. y post.) pero habría que guardarlo en favoritas... 
	titlectvsearch = ftitlectvsearch(miserievo)

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
		# dejé episodiotv como vble numérica por probar, y lo he dejado así, pero no vale la pena :-)
		episodiotv = 0
		tvsneak = "0"

		# + Temporada y Capítulo (si no tiene cap no se guarda la temporada porque no vale para buscar en otras webs...)
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
		year = 0
		month = 0
		day = 0		
		match4 = re.search('(\d{2}).(\d{2}).(\d{2})',match[4],re.IGNORECASE)
		if (match4):
			titulo = titulo+" - "+match4.group(2)+"/"+match4.group(1)+"/"+match4.group(3)
			# cambiar en el 2060 :-)
			if int(match4.group(3)[0:1])<6:
				year = "20"+match4.group(3)
			else:
				year = "19"+match4.group(3)
			# formato dd.mm.yyyy para que se pueda ordenar la salida del directorio por fecha
			date = match4.group(2)+"."+match4.group(1)+"."+year
			# hay que ordenar el listado por fecha para resolver excepciones y simplificar la búsqueda de nuevos episodios
			# no se como definir una vble tipo fecha y he tenido que resolverlo así:
			year = int(year)
			month = int(match4.group(1))
			day = int(match4.group(2))
		elif len(episodioslist)>0:
			date = episodioslist[-1][2]
			year = episodioslist[-1][13]
			month = episodioslist[-1][12]
			day = episodioslist[-1][11]			

		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')	

		# URL
		url = urlparse.urljoin("http://www.casttv.com",match[1])
		
		pago = "0"
		# Episodios de pago
		if match[3] == "/images/v3/icon_list_price.png":
			pago = "-1"		
			
		# Añade al listado los episodios
		episodioslist.append( [ titulo , url , date , pago , titletvsneak , seasontvsneak , seasontv , episodiotv , tvsneak , thumbnail , plot , day , month , year ] )
		if seasontv <> "":
			episodioscasttv.append(seasontv)		
		if seasontvsneak <> "0" and seasontvsneak not in encontrados:
			seasonlist.append(seasontvsneak)
			encontrados.add(seasontvsneak)

	# Si una temporada está en TVShack o TVSneak se agregan todos los episodios (los de pago y los que faltan en CastTV)
	miserietvsh,listseasontvsh = findtvshack(miserievo,"S",titlectvsearch,"0",0)
	for season in seasonlist:
		OKtvsh="0"
		OKtvsn="0"
		#TVShack
		for seasontvsh in listseasontvsh:
			if season==seasontvsh[0]:
				OKtvsh="-1"
				break
		#TVSneak (comprueba en los dos sitios si es lento quitar...)
		#urltvsneak = titletvsneak+"-season-"+season
		#matchtvsneak = re.search('(http://tvsneak.com/category/.*?)(?<='+urltvsneak+')',datatvsneak,re.IGNORECASE)
		#if (matchtvsneak):
			#OKtvsn="-1"

		if OKtvsh=="-1" or OKtvsn=="-1":
			for episodio in episodioslist:
				if episodio[5]==season:
					n = episodioslist.index(episodio)
					if episodio[3]=="-1":
						episodio[3] = "0"
					#if episodio[8]=="0" and OKtvsn=="-1":
						#episodio[8] = "-1"
					if episodio[7] > 1:
						lastseasontv = episodioscasttv[-1]
						if episodio[6] == lastseasontv:
							if n < len(episodioslist)-1 and episodioslist[n+1][6] <> episodio[6] :						
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , OKtvsn , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])
							elif n == len(episodioslist)-1:
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserievo+" - "+seasontvlast , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , OKtvsn , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])
						capitvnew = episodio[7]-1
						seasontvnew = episodio[6][0:4]+str(capitvnew)
						if len(seasontvnew) == 5:
							seasontvnew = seasontvnew.replace('E' , 'E0')
						
						if episodioslist[n+1][5] == season and episodioslist[n+1][6] <> episodio[6] and episodioslist[n+1][7] <> capitvnew:
							episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , OKtvsn , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])
						if episodioslist[n+1][5] == str(int(season)-1) and episodioslist[n+1][5] <> "0":
							episodioslist.insert(n+1,[ miserievo+" - "+seasontvnew , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , OKtvsn , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])

	# Se agregan completas las temporadas de TVShack que faltan en CastTV
	n = len(listseasontvsh)
	for seasontvsh in listseasontvsh:
		#se comprueba que la temporada es menor o igual al nº total porque he encontrado errores tipográficos.. 
		if seasonlist.count(seasontvsh[0])==0 and int(seasontvsh[0])<=n:
			n=int(seasontvsh[1])
			if len(seasontvsh[0])==1:
				seasonT = "S0"+seasontvsh[0]
			else:
				seasonT = "S"+seasontvsh[0]
			date=str(seasontvsh[2])+"."+str(seasontvsh[3])+"."+str(seasontvsh[4])
			while n>0:
				if n<10:
					epT = "E0"+str(n)
				else:
					epT = "E"+str(n)
				episodioslist.append([ miserievo+" - "+seasonT+epT , "" , date , "0" , "" , seasontvsh[0] , seasonT+epT , n , "0" , thumbnail , plot , seasontvsh[2] , seasontvsh[3] , seasontvsh[4]  ])
				n=n-1

	if tipolist<>"listforsubs":
		episodioslist.sort(key=lambda episodio: episodio[5])
		episodioslist.sort(key=lambda episodio: episodio[7])
		episodioslist.sort(key=lambda episodio: episodio[11])
		episodioslist.sort(key=lambda episodio: episodio[12])
		episodioslist.sort(key=lambda episodio: episodio[13])
		episodioslist.reverse()
		return episodioslist
	else:
		for episodio in episodioslist:
			if episodio[5]==seasonsearch and episodio[7]==int(episodiosearch):
				listepisodio.append(episodio)
				break
		return listepisodio

def findsubseries(title,todos,titlectvsearch,season,episodio):
	xbmc.output("[casttv.py] findsubseries")

	subserieslist=[]
	seriesubencontrada=[]
	listsubs = []
	miep = ""

	url = "http://www.subtitulos.es/series"

	data = scrapertools.cachePage(url)
	
	search = ""
	if len(title)==1:
		search = title
		if search=="#":
			search = "[^a-zA-Z]"
	if todos=="V":
		matcht = re.match('^(?:The\s+)?(\w)',title,re.IGNORECASE)
		if (matcht):
			search = "(?:The\s+)?"+matcht.group(1)
		todos = "0"
	
	# ------------------------------------------------------
	# Extrae las Series
	# ------------------------------------------------------
	patronvideos = '<a href="\/show\/([^\"]+)\">('+search+'[^<]+)</a>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulosub = match[1]

		# Titulo para búsquedas
		titlesubsearch = ftitlesubsearch(titulosub)

		# URL
		url = urlparse.urljoin("http://www.subtitulos.es/show/",match[0])

		subserieslist.append( [ titulosub , url , titlesubsearch ] )

	if todos=="-1":

		if len(subserieslist) > 0 and len(title) > 1:
			for subserie in subserieslist:
				forsub = re.search(title,subserie[0],re.IGNORECASE)
				if (forsub):
					seriesubencontrada.append(subserie)
			subserieslist = seriesubencontrada
				
		return subserieslist

	elif todos=="0":

		if len(subserieslist) > 0:
			itemencontrado = searchgate(subserieslist,titlectvsearch)
			if len(itemencontrado)==1:
				titulosubserie2 = itemencontrado[0][0]
				urlsubserie2 = itemencontrado[0][1]
				miep,listsubs = findsubsep(urlsubserie2,"0",season,episodio)

		return miep,listsubs

def findtvshack(title,todos,titlectvsearch,season,episodio):
	xbmc.output("[casttv.py] findtvshack")

	listseries = []
	listepisodios = []
	miserietvsh = ""

	data = scrapertools.cachePage("http://tvshack.net/tv")

	search = ""
	if title<>"":
		#la finalidad es obtener un listado los más corto posible usando el primer carácter
		matcht = re.match('^(?:The\s+)?(\w)',title,re.IGNORECASE)
		if (matcht):
			search = matcht.group(1)

	patronvideos = '<li><a\ href="(?:http://tvshack\.net)?([^"]+)">('+search+'[^<]+)'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		#Serie
		titulotvs = match[1]

		# Titulo para búsquedas
		titletvshsearch = ftitletvshsearch(titulotvs)
  
		#Url
		url = "http://tvshack.net" + match[0]

    		listseries.append([ titulotvs , url , titletvshsearch ])

	if todos=="-1":
		return listseries
	else:
		if len(listseries)>0:
			itemencontrado = searchgate(listseries,titlectvsearch)
			if len(itemencontrado)==1:
				miserietvsh = itemencontrado[0][0]
				urltvsh = itemencontrado[0][1]
				params = {'Serie': miserietvsh}
				listepisodios = findtvshackep(params,urltvsh,"",todos,season,episodio)
				
		return miserietvsh,listepisodios

def searchgate(listforsearchin,titletosearch):
	xbmc.output("[casttv.py] searchgate")
	# listforsearchin tiene que tener en la última columna [-1] el campo para búsquedas
	itemencontrado = []
	itemencontrado2 = []
		
	listforsearchin.sort(key=lambda listfor: listfor[-1])
	for listfor in listforsearchin:
		if len(itemencontrado2)==2:
			break
		titletosearchin = listfor[-1]			
		forin = re.match(titletosearch+'$',titletosearchin,re.IGNORECASE)
		if (forin):
			itemencontrado.append(listfor)
			break
		else:
			# Si se obtuvieran 2 o más coincidencias no serviría
			forin1 = re.match('^'+titletosearch+'.+$',titletosearchin,re.IGNORECASE)
			if (forin1):
				itemencontrado2.append(listfor)

	if len(itemencontrado)==0 and len(itemencontrado2)==0:
		listforsearchin.reverse()
		for listfor in listforsearchin:
			if len(listfor[-1])>1:
				titletosearchin = listfor[-1]								
				forback = re.match('^'+titletosearchin+'.+$',titletosearch,re.IGNORECASE)
				if (forback):
					itemencontrado2.append(listfor)
					break											
	if len(itemencontrado)==0:
		itemencontrado = itemencontrado2
	
	return itemencontrado

def listasubep(params,url,category):
	xbmc.output("[casttv.py] listasubep")

	miserie = urllib.unquote_plus( params.get("title") )
	miserie = re.sub('\s+\-\s+\[Subtítulos\]','',miserie)
	
	listasubep = findsubsep(url,"-1","0",0)

	if len(listasubep)==0:
		alertnoepisodios(3)
		return

	for subep in listasubep:
		addsimplefolder( CHANNELNAME , "listasubs" , category , subep[0]+"  -  [Subtítulos]" , subep[1] , "" )


	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listasubs(params,url,category):
	xbmc.output("[casttv.py] listasubs")

	miep = urllib.unquote_plus( params.get("title") )
	miep = re.sub('\s+\-\s+\[Subtítulos\]','',miep)
	#Buscando subs desde vídeos no se muestra el listado de vídeos
	videos="-1"
	match0 = re.match('Series VO',category)
	if (match0):
		videos="0"
	match = re.match('([^;]+);([^;]+)$',category)
	if (match):
		category = match.group(1)
		miep = match.group(2)
	#Serie, Season y episodio
	seasonep = "0"
	match1=re.match('^(.*?)0*(\d+)x0*(\d+)',miep,re.IGNORECASE)
	if (match1):
		serie = match1.group(1)
		seasonep = match1.group(2)
		episodioep = int(match1.group(3))
		titlesubsearch = ftitlesubsearch(serie)
	idioma = ""
	version = ""
	
	listasubtitulos = findsubs(miep,url)

	if len(listasubtitulos)==0:
		alertnoepisodios(3)
		return
	
	#Encabezados
	additem( CHANNELNAME , category , "SUBTITULOS - [Descargar] :" , "" , "" , "" )
	additem( CHANNELNAME , category , miep , "" , "" , "" )

	for subs in listasubtitulos:
		addsimplefolder( CHANNELNAME , "subtitulo" , subs[4] , subs[0]+" ("+subs[1]+") - ["+subs[2]+"] ("+subs[5]+" descargas)" , subs[3] , DESCARGAS_THUMB )

	if seasonep<>"0" and videos=="-1":
		listacasttv = []
		listaTVSneak = []
		listatvshack = []
		thumbnail=""
		plot=""		

		url = "http://www.casttv.com/shows/"
		data = scrapertools.cachePage(url)
		miserievo,listaepisodios = findseries(data,"listforsubs","",titlesubsearch,seasonep,episodioep)

		if len(listaepisodios)==0:
			#Si la serie no está en CastTV se busca en TVShack
			miserietvsh,listatvshack = findtvshack(serie,"0",titlesubsearch,seasonep,episodioep)

		elif len(listaepisodios)==1:
			title=listaepisodios[0][0]
			thumbnail=listaepisodios[0][9]
			plot=listaepisodios[0][10]
			params = {'miserievo': miserievo, 'title': listaepisodios[0][0], 'date': listaepisodios[0][2], 'titletvsneak': listaepisodios[0][4], 'seasontvsneak': listaepisodios[0][5], 'seasontv': listaepisodios[0][6], 'episodiotv': str(listaepisodios[0][7]), 'tvsneak': listaepisodios[0][8], 'thumbnail': listaepisodios[0][9], 'plot': listaepisodios[0][10] }
			miserietvsh,listacasttv,listactmirrors,listaTVSneak,listatvshack = detaildos(params,listaepisodios[0][1],"listforsubs")

		if len(listacasttv)>0 or len(listaTVSneak)>0 or len(listatvshack)>0:

			additem( CHANNELNAME , category , "VIDEOS :" , "" , "" , "" )

		if len(listacasttv)>0 or len(listaTVSneak)>0:
			for video in listacasttv:
				addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - [CastTV]" , video[1] , thumbnail , plot )
			for video in listactmirrors:
				addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - Mirror - [CastTV]" , video[1] , thumbnail , plot )
			#for video in listaTVSneak:
				#addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - [TVSneak]" , video[1] , thumbnail , plot )
		if len(listatvshack)>0:
			for ep in listatvshack:
				#se deja la fecha porque no se muestra previamente el ltdo de episodios...
				titletvsh = re.sub('\s+\(',' - (',ep['title'])
				if thumbnail=="":
					thumbnail=ep['thumbnail']
					plot=ep['plot']
				xbmctools.addnewvideo( CHANNELNAME , "tvshack.listaVideosEpisodio" , category , "" , titletvsh+" - [TVShack]" , ep['url'] , thumbnail , plot , Serie=miserietvsh )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findsubsep(url,todos,seasonsearch0,episodiosearch):
	xbmc.output("[casttv.py] findsubsep")

	listseason = []
	listepisodios = []
	listsubtitulos = []
	miep = ""

	seasonsearch = "\d{1,2}"
	if todos=="0":
		seasonsearch=seasonsearch0

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	
	# ------------------------------------------------------
	# Extrae las Temporadas
	# ------------------------------------------------------
	patronvideos  = '<a href="javascript:loadShow\((\d{1,4}),('+seasonsearch+')\)">'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Season
		season = match[1]

		# URL
		mishow = str(match[0])
		miseason= str(match[1])
		miquery = "ajax_loadShow.php?show="+mishow+"&season="+miseason

		url = urlparse.urljoin("http://www.subtitulos.es/",miquery)
		
		listseason.append([ season , url ])

	if len(listseason)==0:
		if todos=="-1":
			return listseason
		else:
			return miep,listseason

	for season in listseason:

		data = scrapertools.cachePage(season[1])
		
		# ------------------------------------------------------
		# Extrae los Episodios
		# ------------------------------------------------------
		patronvideos  = '<a href=\'([^\']+)\'>(?!descargar)([^<]+)</a>'
		matches = re.compile(patronvideos,re.IGNORECASE).findall(data)
	
		for match in matches:
			# Titulo
			tituloep = match[1]
			tituloep = tituloep.replace('\n' , '')

			#Season y episodio
			seasonep = "0"
			episodioep = 0
			match1=re.search('0*(\d+)x0*(\d+)',tituloep,re.IGNORECASE)
			if (match1):
				seasonep = match1.group(1)
				episodioep = int(match1.group(2))

			# URL
			url = match[0]
		
			if todos=="0" and episodioep==int(episodiosearch):
				listepisodios.append([ tituloep , url , seasonep , episodioep ])
				break
			if todos=="-1":
				listepisodios.append([ tituloep , url , seasonep , episodioep ])
	
	if todos=="-1":
		listepisodios.reverse()
		return listepisodios

	elif todos=="0" and len(listepisodios)==0:
		return miep,listsubtitulos

	else:
		url = listepisodios[0][1]
		miep = listepisodios[0][0]
		listsubtitulos = findsubs(miep,url)
		return miep,listsubtitulos

def findsubupdates():
	xbmc.output("[casttv.py] findsubupdates")

	listsubupdates = []

	url = "http://www.subtitulos.es"

	data = scrapertools.cachePage(url)

	# ------------------------------------------------------
	# Extrae los Episodios
	# ------------------------------------------------------
	patronvideos  = '<a href="([^"]+)">([^<]+)</a></li><li>([^<]+)<span[^>]+>([^<]+)'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)
	
	for match in matches:
		# Titulo
		titulo = match[1]
		titulo = titulo.replace('\n' , '')
		# Idioma
		try:
			idioma = unicode( match[2], "utf-8" ).encode("iso-8859-1")
		except:
			idioma = match[2]
		# Tiempo
		tiempo = formatostring(match[3])
		# Tituloupdate
		tituloupdate = titulo+" - "+idioma+" "+tiempo
		# URL
		url = urlparse.urljoin("http://www.subtitulos.es",match[0])

		listsubupdates.append([ titulo , url , tituloupdate ])

	return listsubupdates

def findsubs(miep,url):
	xbmc.output("[casttv.py] findsubs")

	listsubtitulos = []

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	# ------------------------------------------------------
	# Extrae las versiones
	# ------------------------------------------------------
	patronvideos  = 'class="NewsTitle"><img[^>]+>\s*\n(Versi[^<]+)</td>'
	patronvideos += '(.*?)</table>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
		
	for match in matches:
		version = match[0]
		version = formatostring(version)

		# para a anexar al nombre del archivo
		versionf = ""
		match0=re.search('^[^\s]+\s+(\w{3})',version,re.IGNORECASE)
		if (match0):
			versionf = " "+match0.group(1)
		data1 = match[1]

		# ------------------------------------------------------
		# Extrae los Subtítulos
		# ------------------------------------------------------
		patronvideos  = '<td width="21%" class="language">\n([^<]+)</td>\n\s+<td width="19%"><strong>\n([^<]*Completado)\s+</strong>'
		patronvideos += '.*?<a href="([^"]+)"[^>]+>(?:descargar|<b>m&aacute;s actualizado</b>)</a>.*?&middot\s+(\d+)\s+descargas'
		subs = re.compile(patronvideos,re.DOTALL).findall(data1)

		for sub in subs:
			# Titulo
			try:
				idioma = unicode( sub[0], "utf-8" ).encode("iso-8859-1")
			except:
				idioma = sub[0]
			idioma = re.sub('\s+$','',idioma)

			# nombre del archivo
			idiomaf = ""
			match1=re.search('(\w{2})[^\(]+(\((?!España)[^\)]+\)|\s*)',idioma,re.IGNORECASE)
			if (match1):
				idiomaf = " "+match1.group(1).upper()
				if match1.group(2)<>"":
					idiomaf2 = match1.group(2)[0:3]+")"
					idiomaf2 = re.sub('(?i)La','Lat',idiomaf2)
					idiomaf = idiomaf+idiomaf2
			n=38-len(idiomaf)-len(versionf)
			if n<len(miep):
				miep = miep[0:n]

			# Status
			status = sub[1]
			status = re.sub('\s+$','',status)

			# NºDescargas
			descargas = sub[3]

			# URL
			url = sub[2]
		
			listsubtitulos.append([ idioma , status, version , url , miep+";"+idiomaf+versionf , descargas ])

	if len(listsubtitulos)>1:
		listsubtitulos.sort(key=lambda subs: int(subs[5]))
		listsubtitulos.reverse()
	return listsubtitulos

def searchsub(params,url,category):
	xbmc.output("[casttv.py] searchsub")

	listasubseries = []
	tecleado=""
	category0 = category

	opciones = []
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
	opciones.append("Mostrar Todo")
	opciones.append("Mostrar Últimas Actualizaciones")
	opciones.append("Teclado")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Búsqueda por Listados, Título o Inicial en Subtitulos.es:", opciones)
	if seleccion == -1 :return
	if seleccion == 0:
		listasubseries = findsubseries("","-1","","0",0)
	elif seleccion == 1:
		listasubupdates = findsubupdates()
	elif seleccion == 2:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
			if len(tecleado)>0:
				listasubseries = findsubseries(tecleado,"-1","","0",0)
		if keyboard.isConfirmed() is None or len(tecleado)==0:
			return
	else:
		listasubseries = findsubseries(letras[seleccion-3],"-1","","0",0)

	if len(listasubseries)==0 and len(listasubupdates)==0:
		alertnoresultadosearch()
		return

	if seleccion>1:
		category = category+" - Buscar"
		category0 = category
		if seleccion > 2:
			category = category+" - "+letras[seleccion-3]
 
	if len(listasubseries)>0:
		for subserie in listasubseries:
			addsimplefolder( CHANNELNAME , "listasubep" , category0+" - "+subserie[0] , subserie[0]+"  -  [Subtítulos]" , subserie[1] , "" )
	else:
		category=category+" - Últimas Actualizaciones"
		listasubupdates.sort()
		for subupdate in listasubupdates:
			addsimplefolder( CHANNELNAME , "listasubs" , category+";"+subupdate[0], subupdate[2] , subupdate[1] , "" )

					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


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
	listafav = readfav("","","-1",CHANNELNAME)
	nuevos = []

	listaupdated = findseries(data,"Actualizaciones","","","0",0)
			
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
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

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
	episodiotv = params.get("episodiotv")
	episodiotv = int(episodiotv)

	titleshort = title
	if date<>"":
		titleshort = re.sub('\s\-\s\d+\/\d+\/\d+','',titleshort)
	titleshort = re.sub('\s+\-\s+',' - ',titleshort)
	visto = ""
	matchv = re.search('\[(?:LW|NW|UW|W)\]',titleshort)
	if (matchv):
		visto = " - "+matchv.group(0)
	
	#urltvsneak0 = titletvsneak+"-season-"+seasontvsneak
	
	listacasttv = []
	listactmirrors = []
	listaTVSneak = []
	listasubtitulos = []
	listatvshack = []
	miserietvsh = ""

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
		
	#TVSneak
	#if tvsneak == "-1":
	#	datatvsneak0 = scrapertools.cachePage("http://tvsneak.com")
	#	matchtvsneak0 = re.search('(http://tvsneak.com/category/.*?)(?<='+urltvsneak0+')',datatvsneak0,re.IGNORECASE)
	#	if (matchtvsneak0):
	#		datatvsneak = scrapertools.cachePage(matchtvsneak0.group(1))
	#		urltvsneak = re.sub('category/','',matchtvsneak0.group(1))
	#		urltvsneak2 = "http://tvsneak.com/new"
	#		matchtvsneak1 = re.search('<a  href="((?:'+urltvsneak+'|'+urltvsneak2+')/[^"]+)" rel="bookmark">[^<]+(?<='+seasontv+')[^<]*</a>',datatvsneak,re.IGNORECASE)
	#		if (matchtvsneak1):
	#			datatvsneak2 = scrapertools.cachePage(matchtvsneak1.group(1))
	#			listaTVSneak = servertools.findvideos(datatvsneak2)
	#			# Eliminar cuando haya un patrón para Divxden en servertools
	#			patronvideos = '(http\:\/\/www\.divxden\.com/.*?\.html)'
	#			matches = re.compile(patronvideos).findall(datatvsneak2)
	#			for match in matches:
	#				n = matches.index(match)
	#				if n==0:
	#					titulo = "[Divxden]"
	#				else:
	#					titulo = "[Divxden] - Mirror"
	#				url = match
	#				# Por si fue agregado por servertools.findvideos
	#				if listaTVSneak.count( [ titulo , url , 'Divxden' ] )==0:
	#					listaTVSneak.append( [ titulo , url , 'Divxden' ] )

	if category=="listforsubs":
		titlectvsearch = ftitlectvsearch(miserievo)
		miserietvsh,listatvshack = findtvshack(miserievo,"0",titlectvsearch,seasontvsneak,episodiotv)

		return miserietvsh,listacasttv,listactmirrors,listaTVSneak,listatvshack
													

	# Si el episodio tiene dato de temporada se busca en Subtítulos.es y en TVShack
	if seasontvsneak<>"0":
		titlectvsearch = ftitlectvsearch(miserievo)
		miep,listasubtitulos = findsubseries(miserievo,"V",titlectvsearch,seasontvsneak,episodiotv)	
		miserietvsh,listatvshack = findtvshack(miserievo,"0",titlectvsearch,seasontvsneak,episodiotv)
	
	if len(listacasttv)==0 and len(listaTVSneak)==0 and len(listatvshack)==0:
		alertnovideo()
		return
			
	# ------------------------------------------------------------------------------------
	# Añade los enlaces a los videos
	# ------------------------------------------------------------------------------------
	for video in listacasttv:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - [CastTV]" , video[1] , thumbnail , plot )
	for video in listactmirrors:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - Mirror - [CastTV]" , video[1] , thumbnail , plot )
	#for video in listaTVSneak:
		#addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - [TVSneak]" , video[1] , thumbnail , plot )
	for ep in listatvshack:
		#quita la fecha (como arriba, para acortar)
		titletvsh = re.sub('\s+\([^\)]+\)$','',ep['title'])
		#se usa el thumbnail y el plot de CastTV, porque hay carátulas equivocadas (mirar)
		xbmctools.addnewvideo( CHANNELNAME , "tvshack.listaVideosEpisodio" , category , "" , titletvsh+visto+" - [TVShack]" , ep['url'] , thumbnail , plot , Serie=miserietvsh )
	# ------------------------------------------------------------------------------------
	# Añade los enlaces a los Subtítulos
	# ------------------------------------------------------------------------------------

	if len(listasubtitulos)>0:
		addsimplefolder( CHANNELNAME , "searchsub" , "Series VO - Subtítulos.es" , "SUBTITULOS - [Descargar] :" , "" , "" )
		additem( CHANNELNAME , category , miep , "" , "" , "" )
		for subs in listasubtitulos:
			addsimplefolder( CHANNELNAME , "subtitulo" , subs[4] , subs[0]+" ("+subs[1]+") - ["+subs[2]+"] ("+subs[5]+" descargas)" , subs[3] , DESCARGAS_THUMB )
	else:
		addsimplefolder( CHANNELNAME , "searchsub" , "Subtítulos.es" , "Buscar Subtitulos" , "" , "" )
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
	elif tipo==3:
		resultado = advertencia.ok('Msj. Informativo:' , 'No se han encontrado Subtítulos.' , '')

def alertsinconexion():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'Servidor o Contenido no disponible' , 'en este momento.' )

def alertnoresultadosearch():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'La Búsqueda no ha obtenido Resultados.' , '')

def alertnofav():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'No se han añadido Series a "Mis Favoritas".' , '')

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
	listitem = xbmcgui.ListItem( title, iconImage=HD_THUMB, thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def ayuda(params,url,category):
	xbmc.output("[casttv.py] ayuda")

	additem( CHANNELNAME , category , "------------------------------------------ Leyenda ------------------------------------------" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[LW]: Último Episodio Visto [Last Watched]" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[W]: Episodio Visto [Watched]" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[UW]: Episodio No Visto [UnWatched]" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[NW]: No para Ver [Not to Watch] (excluido de Nvos Episodios) " , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "Series Actualizadas [excepto Aptdo Actualizaciones]" , "" , FOLDERBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "Series Favoritas" , "" , STARORANGE_THUMB , "" )
	additem( CHANNELNAME , category , "Series Favoritas Desactivadas", "" , STARGREY_THUMB , "" )
	additem( CHANNELNAME , category , "(1) Favoritas Actualizadas [excepto Aptdo Actualizaciones]" , "" , STARBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "(2) Favoritas con Nuevos Episodios [Aptdo Mis Favoritas]" , "" , STARGREEN_THUMB , "" )
	additem( CHANNELNAME , category , "(1) y (2) - [Aptdo Mis Favoritas]" , "" , STARGB_THUMB , "" )
	additem( CHANNELNAME , category , "Nuevos Episodios (posteriores a [LW]) [Aptdo Mis Favoritas]" , "" , STARGREEN2_THUMB , "" )
	additem( CHANNELNAME , category , "Subtítulo - [Descargar]" , "" , DESCARGAS_THUMB , "" )
	additem( CHANNELNAME , category , "Mensaje o Encabezado (sin acción)" , "" , HD_THUMB , "" )

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

def ftitlectvsearch(title):
	title = re.sub('Doctor Who','Doctor Who 2005',title)	
	title = re.sub('Life on Mars','Life on Mars (USA)',title)
	title = re.sub('All In','(Korean) All In',title)
	title = title.lower()
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def ftitlesubsearch(title):
	title = re.sub('House MD','House',title)
	title = re.sub('Krod Mandoon','Kröd Mändoon',title)
	title = re.sub('Shippuden','Shippuuden',title)
	title = re.sub('Roomates','Roommates',title)
	title = re.sub('The Prisoner (1967)','The Prisoner',title)
	title = title.lower()
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def ftitletvshsearch(title):
	title = re.sub('CSI: Crime Scene Investigation','CSI',title)
	title = re.sub('Law & Order: Special Victims Unit','Law & Order: SVU',title)
	title = re.sub('Pokémon','Pokemon',title)
	title = re.sub('City (2008)','City',title)
	title = re.sub('Knight Rider (2008)','Knight Rider',title)
	title = re.sub("Hell\'s Kitchen (US)","Hell's Kitchen",title)
	title = title.lower()
	title = re.sub('[^\w]+the$','',title)
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def serieupdate(miserievo,status,url,tipocontenido,channel):
	xbmc.output("[casttv.py] serieupdate")

	urlsearch0 = ""
	if channel=="animeforos":
		urlsearch0=url

	listfav=readfav(miserievo,urlsearch0,"",channel)
	if len(listfav)==0:
		respuesta = seriemenu("0","0",tipocontenido,channel)
		if respuesta==1:
			upgradefav(miserievo,status,url,"-1","1",channel)
	else:
		if listfav[0][3]=="-1":
			respuesta = seriemenu("-1","-1",tipocontenido,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"1","1",channel)
			elif respuesta==3:
				upgradefav(miserievo,status,url,"0","1",channel)
		elif listfav[0][3]=="0":
			respuesta = seriemenu("-1","0",tipocontenido,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"1","1",channel)
			elif respuesta==3:
				upgradefav(miserievo,status,url,"-1","1",channel)
		elif listfav[0][3]=="1":
			respuesta = seriemenu("-1","1",tipocontenido,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"-1","1",channel)
		if respuesta==1:
				upgradefav(miserievo,status,url,"-1","0",channel)
	return respuesta

def seriemenu(tipofav,tiponuevos,tipocontenido,channel):
	xbmc.output("[casttv.py] seriemenu")

	misfavtext="Mis Favoritas"
	if channel=="animeforos":
		misfavtext="Mis Favoritos"

	tipocontext=" Listado de Episodios "
	if tipocontenido<>"" and tipocontenido.lower()<>"serie":
		tipocontext=""

	seleccion = ""
	opciones = []
	opciones.append("Abrir"+tipocontext+" (opción por defecto)")
	if tipofav=="0":
		opciones.append('Añadir a "'+misfavtext+'"')
	elif tipofav=="-1":
		opciones.append('Eliminar de "'+misfavtext+'"')
		if tiponuevos=="1":
			opciones.append('Activar en "'+misfavtext+'"')
		else:
			opciones.append('Desactivar en "'+misfavtext+'"')
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
	tipovisto = urllib.unquote_plus( params.get("tipovisto") )
	miserievo = urllib.unquote_plus( params.get("miserievo") )
	urlback = urllib.unquote_plus( params.get("urlback") )
	season = urllib.unquote_plus( params.get("seasontvsneak") )
	episodio = params.get("episodiotv")

	episodiomenugnral(params,title,url,category,miserievo,urlback,season,episodio,tipovisto,CHANNELNAME,"-1")

def episodiomenugnral(params,title,url,category,miserie,urlback,season,episodio,tipovisto,channel,urlOK):
	xbmc.output("[casttv.py] episodiomenugnral")

	title0 = re.sub('\s+\-\s+\[U?L?N?W\]$','',title)

	if tipovisto=="1": textipo="Último Visto y anteriores [LW]/[W]"
	elif tipovisto=="2": textipo="Último Visto [LW]"
	elif tipovisto=="3" or tipovisto=="1A" or tipovisto=="31": textipo="Visto [W]"
	elif tipovisto=="4" or tipovisto=="41": textipo="No para Ver [NW]"
	elif tipovisto=="5" or tipovisto=="51": textipo="No Visto [UW]"
	elif tipovisto=="New": textipo="Nuevo Episodio"

	opciones = []
	if channel=="casttv":
		opciones.append("Abrir Listado de Vídeos (opción por defecto)")
	elif channel=="animeforos":
		opciones.append("Continuar (opción por defecto)")

	if tipovisto<>"1":
		opciones.append('Marcar: Último Visto y anteriores [LW]/[W]')
	if tipovisto<>"2":
		opciones.append('Marcar: Último Visto [LW]')
	if tipovisto<>"3" and tipovisto<>"31" and  tipovisto<>"1A" and  tipovisto<>"New":
		opciones.append('Marcar: Visto [W]')
	if tipovisto<>"4" and  tipovisto<>"41":
		opciones.append('Marcar: No para Ver [NW]')
	if tipovisto<>"" and tipovisto<>"N" and tipovisto<>"0" and tipovisto<>"01" and tipovisto<>"New":
		opciones.append('Desmarcar: '+textipo)
	if tipovisto=="31" or  tipovisto=="1A" or tipovisto=="01" or tipovisto=="41":
		opciones.append('Marcar: No Visto [UW]')
	if tipovisto<>"N" and  tipovisto<>"New":
		opciones.append('Desmarcar: Todo (Serie Completa)')

	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Seleccione una opción:", opciones)

	if seleccion==-1 or seleccion==0:
		if channel=="casttv":
			detaildos(params,url,category)
			return

	else:
		if tipovisto=="" or tipovisto=="N" or tipovisto=="0" or tipovisto=="New":
			if seleccion==3:
				if tipovisto=="New":
					accion = "4"
				else:
					accion = "3"
			elif seleccion==5:
				accion = "T"
			else:
				accion = str(seleccion)
		elif tipovisto=="01" or tipovisto=="31" or  tipovisto=="1A":
			if seleccion==3:
				if tipovisto=="01":
					accion = "31"
				elif tipovisto=="31" or  tipovisto=="1A":
					accion = "4"
			elif seleccion==4:
				if tipovisto=="01":
					accion = "4"
				elif tipovisto=="31" or  tipovisto=="1A":
					accion = "0"
			elif seleccion==6:
				accion = "T"
			else:
				accion = str(seleccion)
		elif tipovisto == "1" or tipovisto == "2" or tipovisto == "3":
			if seleccion==1:
				if tipovisto == "1":
					accion = "2"
				else:
					accion = "1"
			elif seleccion==2:
				if tipovisto == "3":
					accion = "2"
				else:
					accion = "3"
			elif seleccion==3:
				accion = "4"
			elif seleccion==4:
				accion = "0"
			elif seleccion==5:
				accion = "5"
			elif seleccion==6:
				accion = "T"
		elif tipovisto == "4" or tipovisto == "41":
			if seleccion==3:
				if tipovisto == "41":
					accion = "31"
				else:
					accion = "3"
			elif seleccion==4:
				if tipovisto == "41":
					accion = "041"
				else:
					accion = "0"
			elif seleccion==5:
				if tipovisto == "41":
					accion = "5"
				else:
					accion = "T"
			elif seleccion==6:
				accion = "T"
			else:
				accion = str(seleccion)
		elif tipovisto == "5" or tipovisto == "51":
			if seleccion==3:
				if tipovisto == "51":
					accion = "31"
				else:
					accion = "3"
			elif seleccion==5:
				if tipovisto == "51":
					accion = "051"
				else:
					accion = "0"
			elif seleccion==6:
				accion = "T"
			else:
				accion = str(seleccion)

		upgradevisto(miserie,title0,url,season,episodio,accion,channel,urlOK)

	if channel=="animeforos":
		return seleccion

	if tipovisto=="New":
		listatresupdate(urlback,category,True)
	else:
		listadosupdate(miserie,urlback,category,True)

def readfav(seriesearch0,urlsearch0,tiponuevos,channel):
	xbmc.output("[casttv.py] readfav")

	if seriesearch0<>"":	
		seriesearch = re.sub('(?P<signo>\(|\)|\'|\"|\[|\]|\.|\?|\+)','\\\\\g<signo>',seriesearch0)
	else:
		seriesearch = "[^;]+"

	if urlsearch0<>"":	
		urlsearch = re.sub('(?P<signo>\(|\)|\'|\"|\[|\]|\.|\?|\+|\#)','\\\\\g<signo>',urlsearch0)
	else:
		urlsearch = "[^;]+"

	if tiponuevos=="":
		tiponuevos = "[^;]+"

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )

	# Crea el directorio si no existe
	try:
		os.mkdir(VISTO_PATH)
	except:
		pass

	favlist = []
	filename = channel+'fav.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)
	if not os.path.exists(fullfilename):
		favfile = open(fullfilename,"w")
		favfile.close()
	else:
		favfile = open(fullfilename)
		for line in favfile:
			match = re.match('('+seriesearch+');([^;]*);('+urlsearch+');('+tiponuevos+');\n',line)
			if (match):
				serie = match.group(1)
				status = match.group(2)
				url = match.group(3)
				seguirnuevos = match.group(4)
				favlist.append([ serie , status , url , seguirnuevos ])
				if seriesearch0<>"":
					break
		favfile.close()

	return favlist

def upgradefav(serie,status,url,seguirnuevos,tipo,channel):
	xbmc.output("[casttv.py] upgradefav")

	#el status se podría quitar, se guarda sólo por mantener el formato...

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )
	favlist = []
	encontrado = "0"
	detener = "0"
	OK = "0"
	filename = channel+'fav.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)

	favfile = open(fullfilename)
	for line in favfile:
		match = re.match('([^;]+);([^;]*);([^;]+);([^;]+);\n',line)
		if (match):
			serief = match.group(1)
			statusf = match.group(2)
			urlf = match.group(3)
			seguirnuevosf = match.group(4)
			if serief<>serie:
				favlist.append([ serief , statusf , urlf , seguirnuevosf ])
			if channel=="animeforos" and serief==serie and urlf<>url:
				favlist.append([ serief , statusf , urlf , seguirnuevosf ])

	favfile.close()

	if tipo=="1":
		favlist.append([ serie , status , url , seguirnuevos ])

	favlist.sort()

	favfile = open(fullfilename,"w")
	for fav in favlist:
		favfile.write(fav[0]+';'+fav[1]+';'+fav[2]+';'+fav[3]+';\n')
	favfile.close()

def readvisto(serie,tipo,channel):
	xbmc.output("[casttv.py] readvisto")

	if serie<>"":	
		seriesearch = re.sub('(?P<signo>\(|\)|\'|\"|\[|\]|\.|\?|\+)','\\\\\g<signo>',serie)
	else:
		seriesearch="[^;]+"

	if tipo=="LW":
		tipos="(?:1|2|4)"
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
	filename = channel+'.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)
	if not os.path.exists(fullfilename):
		vistofile = open(fullfilename,"w")
		vistofile.close()
	else:
		vistofile = open(fullfilename)
		for line in vistofile:
			match = re.match('('+seriesearch+');([^;]+);([^;]*);([^;]+);([^;]+);('+tipos+');\n',line)
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

def upgradevisto(serie,titulo,url,season,episodio,tipo,channel,urlOK):
	xbmc.output("[casttv.py] upgradevisto")

	#urlOK añadido para Mcanime en Anime(Foros) por los enlaces que genéricos sin títulos...  
	#urlOK indica si se usa la url ("0") o no ("-1") para identificar los episodios vistos 

	VISTO_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks/vistos' ) )
	vistolist = []
	encontrado = "0"
	detener = "0"
	OK = "0"
	filename = channel+'.txt'
	fullfilename = os.path.join(VISTO_PATH,filename)

	vistofile = open(fullfilename)

	for line in vistofile:
		match = re.match('([^;]+);([^;]+);([^;]*);([^;]+);([^;]+);([^;]+);\n',line)
		if (match):
			Addlist="0"
			serief = match.group(1)
			titulof = match.group(2)
			urlf = match.group(3)
			seasonf = match.group(4)
			episodiof = match.group(5)
			tipof = match.group(6)
			if serief<>serie:
				vistolist.append([ serief , titulof , urlf , seasonf , episodiof , tipof ])
				continue
			elif serief==serie and tipo=="T":
				if OK=="-1":
					continue
				elif OK=="0":
					respuesta = alertcontinuarT()
					if respuesta:
						OK= "-1"
						continue
					else:
						detener="-1"
						break
			elif serief==serie and tipo<>"T":
				if urlOK=="-1":
					if titulof==titulo:
						diferenteOK = "0"
					else:
						diferenteOK = "-1"
				else: 
					if titulof==titulo and urlf==url:
						diferenteOK = "0"
					else:
						diferenteOK = "-1"
				if diferenteOK=="0":
					if tipo[0:1]=="0":
						if tipo=="041" and tipof=="4":
							continue
						elif tipo=="051" and tipof=="5":
							continue
						else:
							encontrado = "-1"
							continue
					elif tipo=="31" and tipof=="4":
						continue
					elif tipo=="31" and tipof=="5":
						continue
				else:
					if tipo=="1" or tipo=="2":
						if tipo=="2" and tipof=="3":
							if int(seasonf)<int(season):
								Addlist="-1"
							elif int(seasonf)==int(season) and int(episodiof)<int(episodio):
								Addlist="-1"
						if tipof=="4" or tipof=="5":
							Addlist="-1"
						if tipof=="1" or tipof=="2":
							respuesta = alertcontinuar(tipo,tipof)
							if respuesta:
								if tipo=="2" and tipof=="2":
									if int(seasonf)<int(season):
										Addlist="-1"
										tipof="3"
									elif int(seasonf)==int(season) and int(episodiof)<int(episodio):
										Addlist="-1"
										tipof="3"
							else:
								detener="-1"
								break
					elif tipo=="3":
						#if tipof=="1":
							#alertnoanterior()
							#detener="-1"
							#break
						if tipof=="1" or tipof=="2":
							if int(seasonf)>int(season):
								Addlist="-1"
							elif int(seasonf)==int(season) and int(episodiof)>int(episodio):
								Addlist="-1"
							else:
								alertnoanterior()
								detener="-1"
								break
						else:
							Addlist="-1"
							
					elif tipo[0:1]=="0" or tipo=="4" or tipo=="31" or tipo=="5":
						Addlist="-1"

			if Addlist=="-1":
				vistolist.append([ serief , titulof , urlf, seasonf, episodiof , tipof ])
			

	vistofile.close()
	if detener=="-1": return

	if tipo[0:1]=="0" and encontrado=="0":
		vistolist.append([ serie , titulo , url , season, episodio , "0" ])
	if tipo[0:1]<>"0" and tipo<>"31" and tipo<>"T":
		vistolist.append([ serie , titulo , url , season, episodio , tipo ])

	vistolist.sort()

	vistofile = open(fullfilename,"w")
	for visto in vistolist:
		vistofile.write(visto[0]+';'+visto[1]+';'+visto[2]+';'+visto[3]+';'+visto[4]+';'+visto[5]+';\n')
	vistofile.close()

	
def alertcontinuar(tipo,tipof):
	advertencia = xbmcgui.Dialog()
	linea1 = "Se desmarcará el episodio [LW] actual y Vistos [W]."
	linea2 = "Los No Vistos [UW] y [NW] no se desmarcan." 
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

def alertnocompletado(porcentaje):
	advertencia = xbmcgui.Dialog()
	linea1 = "Hasta el momento, el Subtitulo solo "
	linea2 = "ha sido completado en un "+porcentaje
	linea3 = "¿Desea descargarlo?"
	resultado = advertencia.yesno('pelisalacarta' , linea1 , linea2 , linea3 )
	return resultado

def alertdescarga(filename):
	advertencia = xbmcgui.Dialog()
	linea0='Descargando Subtítulo en:'
	linea1='(Ruta Directorio de Descargas)/Subtitulos/'
	linea2=filename
	linea3='¿Desea Continuar?'
	resultado = advertencia.yesno(linea0 , linea1 , linea2 , linea3 )
	return resultado

def alerttituloarchivo(archivo):
	advertencia = xbmcgui.Dialog()
	linea1 = archivo
	linea2 = '(Si elige "No" se añadirá al nombre un nº de copia)'
	linea3 = '¿Desea Sobreescribirlo?'
	resultado = advertencia.yesno('Ya existe un archivo con ese nombre:' , linea1 , linea2 , linea3 )
	return resultado

def subtitulo(params,url,category):
	xbmc.output("[casttv.py] subtitulo")

	misub = urllib.unquote_plus( params.get("title") )
	matchC = re.search('\(([^\)]+)Completado\)',misub)
	if (matchC):
		respuesta = alertnocompletado(matchC.group(1))
		if respuesta:
			pass 
		else:
			return

	titulosub = category

	titulosub = re.sub('(?:\\\\|\/|\:|\*|\?|\"|\<|\>|\|)','',titulosub)
		
	downloadpath = downloadtools.getDownloadPath()

	SUB_PATH = xbmc.translatePath( os.path.join( downloadpath , 'Subtitulos' ) )

	# Crea el directorio si no existe
	try:
		os.mkdir(SUB_PATH)
	except:
		pass

	match = re.match('([^;]+);([^;]+)$',titulosub)
	titulo1 = match.group(1)
	titulo2 = match.group(2)

	filename = titulo1+titulo2+'.srt'
	fullfilename = os.path.join(SUB_PATH,filename)
	# Si ya existe el título si no se quiere sobreescribir se guarda con un nº de copia
	if os.path.exists(fullfilename):
		respuesta = alerttituloarchivo(filename)
		if respuesta:
			pass
		else:
			n=2
			OK="0"
			while OK=="0":
				l = len(titulo1+titulo2)
				lright = 38-len(str(n))-2
				lrightd = 0
				if l>lright:
					lrightd = l-lright
				lright1=len(titulo1)-lrightd
				titulo1_2 = titulo1[0:lright1]
				titulo2_2 = titulo2+"("+str(n)+")"
				filename = titulo1_2+titulo2_2+'.srt'
				fullfilename = os.path.join(SUB_PATH,filename)
				if not os.path.exists(fullfilename):
					OK="-1"
				else:
					n=n+1

	# mensaje de confirmación para mostrar la ruta (un msj OK después de la descarga la mayoría de las veces bloquea la Xbox)
	respuesta = alertdescarga(filename)
	if respuesta:
		pass 
	else:
		return

	downloadtools.downloadfileGzipped(url,fullfilename)

	#Este cuadro es para evitar que la pantalla se quede medio congelada en la Xbox... (lo puse fuera de la condición harta de bloqueos :-))
	Dialogfin = xbmcgui.DialogProgress()
	resultado = Dialogfin.create('pelisalacarta' , 'Copiando en archivo de Subtítulo temporal...' , '(activable en la configuración del plugin)' )

	if os.path.exists(fullfilename): # Añadido por bandavi
		from shutil import copy2	 # copia los subt descargados a los subt temporales para poder activarlos con el setting del plugin
		copy2(fullfilename,xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib', 'subtitulo.srt' )))

	Dialogfin.close()

def listtvshack(params,url,category):
	xbmc.output("[casttv.py] listtvshack")

	listseries = findtvshack("","-1","","0",0)

	for serie in listseries:
		#addsimplefolder( CHANNELNAME , "listtvshackep" , category , serie[0] , serie[1] , "" )
    		xbmctools.addnewfolder( CHANNELNAME , "listtvshackep" , category , serie[0] , serie[1] , "" , "" , Serie=serie[0] , totalItems=len(listseries))

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , cacheToDisc=False )

def findtvshackep(params,url,category,todos,season,episodio):
	xbmc.output("[casttv.py] findtvshackep")

	listepisodios = []
	listepisodio = []
	listseason = []
	
	listepisodios = tvshack.devuelveListaEpisodios(params,url,category)
	
	if todos=="-1":
		return listepisodios
	elif todos=="0":
		for ep in listepisodios:
			match1=re.search('0*(\d+)x0*(\d+)',ep['title'],re.IGNORECASE)
			if (match1):
				seasonep = match1.group(1)
				episodioep = int(match1.group(2))
				if seasonep==season and episodioep==int(episodio):
					listepisodio.append(ep)
					break

		return listepisodio
	elif todos=="S":
		listepisodios.reverse()
		for ep in listepisodios:
			match1=re.search('0*(\d+)x0*(\d+)',ep['title'],re.IGNORECASE)
			if (match1):
				seasonep = match1.group(1)
				episodioep = int(match1.group(2))
				match2=re.search('\((\d+)\/(\d+)\/(\d+)\)$',ep['title'],re.IGNORECASE)
				if (match2):
					day = int(match2.group(1))
					month = int(match2.group(2))
					year = int(match2.group(3))
				else:
					day = 0
					month = 0
					year = 0
				if listseason.count(seasonep)==0:
					listepisodio.append([ seasonep , episodioep , day , month , year ])
					listseason.append(seasonep)
				else:
					n = listseason.index(seasonep)
					if episodioep>listepisodio[n][1]:
						listepisodio[n][1]=episodioep
						listepisodio[n][2]=day
						listepisodio[n][3]=month
						listepisodio[n][4]=year

		return listepisodio

def listtvshackep(params,url,category):
	xbmc.output("[casttv.py] listtvshackep")

	serie = urllib.unquote_plus( params.get("title") )

	listepisodios = findtvshackep(params,url,category,"-1","0",0)

	for ep in listepisodios:
		xbmctools.addnewvideo( CHANNELNAME , "tvshack.listaVideosEpisodio" , category , "" , ep['title'] , ep['url'] , ep['thumbnail'] , ep['plot'] , Serie=serie)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def formatostring(cadena):
	#cadena = cadena.replace('\n' , '')
	cadena = re.sub('(?:&amp;|&#38;)','&',cadena)
        cadena = cadena.replace('&#33;' , '!')
	cadena = cadena.replace('&Aacute;' , 'Á')
	cadena = cadena.replace('&Eacute;' , 'É')
	cadena = cadena.replace('&Iacute;' , 'Í')
	cadena = cadena.replace('&Oacute;' , 'Ó')
	cadena = cadena.replace('&Uacute;' , 'Ú')
	cadena = re.sub('(?:&ntilde;|&#241;)','ñ',cadena)
	cadena = cadena.replace('&Ntilde;' , 'Ñ')
	cadena = cadena.replace('&aacute;' , 'á')
	cadena = cadena.replace('&#225;' , 'á')
	cadena = cadena.replace('&eacute;' , 'é')
	cadena = cadena.replace('&#233;' , 'é')
	cadena = cadena.replace('&iacute;' , 'í')
	cadena = cadena.replace('&#237;' , 'í')
	cadena = cadena.replace('&oacute;' , 'ó')
	cadena = cadena.replace('&#243;' , 'ó')
	cadena = cadena.replace('&#333;' , 'o')
	cadena = cadena.replace('&uacute;' , 'ú')
	cadena = cadena.replace('&#250;' , 'ú')
	cadena = re.sub('(?:&iexcl;|&#161;)','¡',cadena)
	cadena = re.sub('(?:&iquest;|&#191;)','¿',cadena)
	cadena = re.sub('&#63;','\?',cadena)
	cadena = cadena.replace('&ordf;' , 'ª')
	cadena = cadena.replace('&quot;' , '"')
	cadena = cadena.replace('&nbsp;' , ' ')
	# cadena = cadena.replace('&hellip;' , '...')
	cadena = re.sub('(?:&#39;|&#039;)','\'',cadena)
	cadena = re.sub('&sup2;','^2',cadena)
	cadena = re.sub('&middot;','-',cadena)
	cadena = re.sub('&frac12;','1/2',cadena)
	cadena = re.sub('&#\d{3};','-',cadena)
	cadena = re.sub('&#\d{4};','',cadena)
	return cadena
