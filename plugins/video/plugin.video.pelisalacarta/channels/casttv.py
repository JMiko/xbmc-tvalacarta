# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal CastTV by Lily
# http://www.mimediacenter.info/foro/viewtopic.php?f=14&t=401
# Last Updated: 31/07/2010
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import servertools
import xbmctools
import downloadtools
import animeforos
import seriesyonkis
import config

CHANNELNAME = "casttv"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

CTVURL = "http://www.casttv.com/shows/"
SYURL = "http://www.seriesyonkis.com/"
FTURL = "http://www.thefutoncritic.com/showatch/"
SUBURL = "http://www.subtitulos.es"
EZURL = "http://eztv.it/showlist/"

VISTO_PATH = xbmc.translatePath( os.path.join( config.DATA_PATH , 'bookmarks/vistos' ) )
if not os.path.exists(VISTO_PATH):
	try:
		os.mkdir(VISTO_PATH)
	except:
		os.mkdir(os.path.join( config.DATA_PATH , 'bookmarks' ))
		os.mkdir(VISTO_PATH)

SUB_PATH = xbmc.translatePath( os.path.join( downloadtools.getDownloadPath() , 'Subtitulos' ) )
if not os.path.exists(SUB_PATH):
	os.mkdir(SUB_PATH)

SUBTEMP_PATH = xbmc.translatePath( os.path.join( config.DATA_PATH , 'subtitulo.srt' ) )

STARORANGE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','starorangesmall.png' ) )
STARBLUE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','starbluesmall.png' ) )
STARGREEN_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreensmall.png' ) )
STARGB_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreenblue.png' ) )
STARGREEN2_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreensmall2.png' ) )
STARGREY_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreysmall.png' ) )
STARGREYBLUE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','stargreyblue.png' ) )
STAR4COLORS_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','star4colors.png' ) )
HD_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','harddisk.png' ) )
FOLDERBLUE_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','foldericonblue.png' ) )
HELP_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','help.png' ) )
DESCARGAS_THUMB = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'casttv','descargados.png' ) )

def mainlist(params,url,category):
	category = "Series VO : CastTV - SeriesYonkis"
	addsimplefolder( CHANNELNAME , "searchfuton" , "The Futon Critic" , "The Futon Critic  -  Series VO" , "" , "http://www.thefutoncritic.com/images/logo.gif" )
	addsimplefolder( CHANNELNAME , "searchsub" , "Subtítulos.es" , "Subtítulos.es  -  Series VO" , "" , "http://www.subtitulos.es/images/subslogo.png" )
	addsimplefolder( CHANNELNAME , "listado" , "Series VO - Actualizadas" , "Series VO  -  CastTV - Últimas Actualizaciones" , "" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "listado" , "Series VO" , "Series VO  -  CastTV - Listado Completo" , "" , "http://www.casttv.com/misc/webapp/tn_shows/tn_casttv.jpg" )
	addsimplefolder( CHANNELNAME , "search" , "Series VO - Buscar" , "Series VO  -  Buscar" , "" ,"http://www.mimediacenter.info/xbmc/pelisalacarta/posters/buscador.png" )
	addsimplefolder( CHANNELNAME , "listado" , "Mis Favoritas" , "Series VO  -  Mis Favoritas" , "" , STARORANGE_THUMB )
	addsimplefolder( CHANNELNAME , "listado" , "Todos Mis Favoritos" , "Todos Mis Favoritos", "" ,STAR4COLORS_THUMB )
	addsimplefolder( CHANNELNAME , "ayuda" , "Series VO - Ayuda" , "Ayuda" , "" , HELP_THUMB )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def listado(params,url,category):
	title = urllib.unquote_plus( params.get("title") )
	match = re.search('\s(\w+)$',title)
	tipolist = match.group(1)

	listadoupdate(tipolist,category,False)

def listadoupdate(tipolist,category,listupdate):
	listanime = []
	todostitulo = ""

	if tipolist[0:3]=="Fav":
		Dialogespera = xbmcgui.DialogProgress()
		line1 = 'Buscando información de "'+category+'"...'
  		resultado = Dialogespera.create('pelisalacarta' , line1 , '' )
		tipolist = "Favoritas"

	series,nuevos = findlistado(tipolist)

	if category=="Todos Mis Favoritos":
		listanime,animenuevos = animeforos.findfavoritos("Mis Favoritos","[^<]+","Completo","")
		todostitulo = "Series VO - "

	if len(series)==0 and len(listanime)==0:
		return

	if category=="Todos Mis Favoritos":
		if len(nuevos)>0 or len(animenuevos)>0:
			addsimplefolder( CHANNELNAME , "listadonuevos" , "Todos Mis Favoritos - Nuevos Contenidos" , "-*-Todos Mis Favoritos - Nuevos Contenidos Posteriores a [LW]" , "" , STARGREEN2_THUMB )
		if len(series)>0:
			additem( CHANNELNAME , category , "----------------------------- CASTTV - SERIESYONKIS -----------------------------" , "" , "" , "" )
	if len(nuevos)>0:
		addsimplefolder( CHANNELNAME , "listadonuevos" , todostitulo+"Mis Favoritas - Nuevos Episodios" , "-*-"+todostitulo+"Nuevos Episodios (Posteriores a [LW])" , "" , STARGREEN2_THUMB )
	for serie in series:
		addseriefolder( CHANNELNAME , "listados" , serie[0] , serie[1] , serie[2] , serie[3] , "" , serie[4] , serie[5] )

	if category=="Todos Mis Favoritos" and len(listanime)>0:
		additem( CHANNELNAME , category , "------------------------------------ ANIME - FOROS ------------------------------------" , "" , "" , "" )
		if len(animenuevos)>0:
			addsimplefolder( CHANNELNAME , "animeforos.listadonuevos" , "Anime - Mis Favoritos - Nuevos Contenidos" , "-*-Anime - Nuevos Episodios (Posteriores a [LW])" , "" , STARGREEN2_THUMB )
		for anime in listanime:
			animeforos.adderdmfolder( CHANNELNAME , "animeforos.listados" , anime[0] , anime[1] , anime[2] , anime[3] , anime[4] , anime[5] , anime[6] , anime[7] )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",listupdate,False)
	# ------------------------------------------------------------------------------------

def findlistado(tipolist):
	thumbnail=""
	search = ""
	iniciosearchT=""
	listaseries = []
	listforstatus = []
	listactv = []
	nuevos = []
	series = []

	listafav = readfav("","","",CHANNELNAME)

	if tipolist <> "Favoritas":
		listaseries = findcasttv(tipolist,"","","","")
		if len(listaseries)==0:
			return series,nuevos
	else:	
		if len(listafav)==0:
			alertnofav()
			return series,nuevos
		else:
			for fav in listafav:
				listaseries.append([ fav[0] , fav[1] , fav[2] , fav[3] , "" , "" ])
				if "casttv" in fav[2]:
					titulo=re.sub('[\\\\]?(?P<signo>[^\w\s\\\\])','\\\\\g<signo>',fav[0])
					if search=="":
						search=titulo
					else:
						search=search+"|"+titulo
				else:
					iniciosearch,titlesearch = findtsearch(fav[0],fav[2])
					if iniciosearchT=="":
						iniciosearchT=iniciosearch
					elif iniciosearch not in iniciosearchT:
						iniciosearchT=iniciosearchT+"|"+iniciosearch
					n = listafav.index(fav)
					listforstatus.append([ fav[0] , fav[1] , iniciosearchT , n , "" , titlesearch ])
			if len(listforstatus)>0:
				listforstatus=findfutonstatus(listforstatus,"noctv")
				for status in listforstatus:
					n = status[3]
					listaseries[n][1]=status[1]
					listaseries[n][4]=status[4]
					listaseries[n][5]=status[5]
			if search<>"":		
				search="(?:"+search+")"
				listactv = findcasttv("Completo",search,"","","")
	
	for serie in listaseries:
		dataweb = ""
		serievistos = ""
		if tipolist <> "Favoritas":
			thumbnail=""
			if serie[3]=="-1" and tipolist <> "Actualizaciones":
				#En el propio ldo de act. no se cambia el color
				thumbnail=FOLDERBLUE_THUMB
			if len(listafav)>0:
				for fav in listafav:
					if serie[0]==fav[0]:
						if thumbnail==FOLDERBLUE_THUMB:
							if fav[3]=="1":
								thumbnail=STARGREYBLUE_THUMB
							else:
								thumbnail=STARBLUE_THUMB
						elif fav[3]=="1":
							thumbnail=STARGREY_THUMB
						else:
							thumbnail=STARORANGE_THUMB
						break
		if tipolist == "Favoritas":
			encontrado = "0"
			if serie[3]=="1":
				thumbnail=STARGREY_THUMB
				if "casttv" in serie[2]:
					for ctv in listactv:			
						if serie[0]==ctv[0]:
							encontrado = "-1"
							# se actualiza: url, status, datafuton y titlesearch
							serie[1] = ctv[1]
							serie[2] = ctv[2]
							serie[4] = ctv[4]
							serie[5] = ctv[5]
							if ctv[3]=="-1":
								thumbnail=STARGREYBLUE_THUMB
							break

			else:
				updated="0"
				thumbnail=STARORANGE_THUMB
				listanuevos = []
				serievistos,dataweb,listanuevos=findnuevos(serie[0],serie[2],"0")
				if "casttv" in serie[2]:
					for ctv in listactv:			
						if serie[0]==ctv[0]:
							encontrado = "-1"
							serie[1] = ctv[1]
							serie[2] = ctv[2]
							serie[4] = ctv[4]
							serie[5] = ctv[5]
							if ctv[3]=="-1":
								updated="-1"
								thumbnail=STARBLUE_THUMB
								if len(listanuevos)>0:
									thumbnail=STARGB_THUMB
								break
				if len(listanuevos)>0:
					if updated=="0":
						thumbnail=STARGREEN_THUMB
					if serie[3]=="-1" or serie[3]=="-2":
						nuevos.extend(listanuevos)

			# evita el status desactualizado de fav caso extremo de no encontrarse ya en CastTV
			if "casttv" in serie[2] and encontrado=="0":
				serie[1]=""
		status=""
		network=""
		if serie[1]<>"":
			status="  -  "+serie[1]
		if serie[4]=="ended" or serie[4]=="bbc" or serie[4]=="varios":
			if serie[4]=="bbc":
				network=" (BBC)"
			serie[4]=serie[4]+";"+serie[0]+";"+serie[2]+";"+serie[1]+";"+serie[5]
		elif serie[4]<>"":
			matchnet=re.match('^[^;]*;[^;]*;[^;]*;([^;]+);',serie[4])
			if (matchnet):
				network=" ("+matchnet.group(1)+")"

		series.append( [ tipolist+";"+serie[0]+";"+serie[1]+";"+serie[4] , serie[0]+network+status , serie[2] , thumbnail , serievistos , dataweb ] )

	return series,nuevos

def findnuevos(serie,url,todos):
	listanuevos = []

	serievistos,dataweb,listavistos = checkvistosfav(serie,url,"nuevos")

	if len(listavistos)==0:
		if todos=="0":
			return serievistos,dataweb,listanuevos
		else:
			return serievistos,listanuevos
	else:
		listavistos.sort(key=lambda visto: visto[5])
		if listavistos[0][5]=="4":
			if todos=="0":
				return serievistos,dataweb,listanuevos
			else:
				return serievistos,listanuevos

	listaepisodios=findepisodios(url,serie,dataweb)
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
					if int(episodio[5])==int(visto[3]) and episodio[7]<=int(visto[4]):
						stop="-1"
						break
		if stop=="-1":
			break
		if OK=="-1":
			listanuevos.append(episodio)
			if todos=="0":
				break
	if todos=="0":
		return serievistos,dataweb,listanuevos
	else:
		return serievistos,listanuevos

def search(params,url,category):
	searchupdate(-2,"",category,"",False)

def searchupdate(seleccion,tecleado,category,web,listupdate):
	thumbnail = ""
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	rtdos = 0
        
	if seleccion == -2:
		opciones = []
		opciones.append('Mostrar Series con Episodios Vistos, Distintas de "Mis Favoritas"')
		opciones.append('Teclado   (Busca en Título y Status)                         (ver "Ayuda")')
		for letra in letras:
			opciones.append(letra)
		searchtype = xbmcgui.Dialog()
		seleccion = searchtype.select("Búsqueda por Teclado o por Inicial del Título:", opciones)
	if seleccion == -1 :return
	if seleccion == 0:
		listaseries = []
		listaseries2 = []
		listavistos2 = []
		listavistos = readvisto("","",CHANNELNAME)
		if len(listavistos)==0:
			alertnoresultadosearch()
			if listupdate==True:
				EndDirectory(category,"",listupdate,True)
			return
		listadoseries = findcasttv("","","","","")
		for visto in listavistos:
			encontrado="0"
			for serie in listadoseries:
				if visto[0]==serie[0]:
					encontrado="-1"
					listaseries.append(serie)
					break
			if encontrado=="0":
				listavistos2.append(visto)
		if len(listavistos2)>0:
		#	listavistos=[]
			listaseriesnoctv=[]
			listadoseries = findseriesyonkis("","-1","","")
			for visto in listavistos2:
		#		encontrado="0"
				for serie in listadoseries:
					if visto[0]==serie[0]:
		#				encontrado="-1"
						listaseriesnoctv.append(serie)
						break
		#		if encontrado=="0":
		#			listavistos.append(visto)
		#if len(listavistos)>0:
		#	listadoseries = findtv("","-1","")
		#	for visto in listavistos:
		#		for serie in listadoseries:
		#			if visto[0]==serie[0]:
		#				listaseriesnoctv.append(serie)
		#				break
		if len(listaseriesnoctv)>0:
			listaseriesnoctvst=[]
			listaseriesnoctv2=[]
			iniciosearchT=""
			for serienoctv in listaseriesnoctv:
				iniciosearch,titlesearch = findtsearch(serienoctv[0],serienoctv[2])
				if iniciosearchT=="":
					iniciosearchT=iniciosearch
				elif iniciosearch not in iniciosearchT:
					iniciosearchT=iniciosearchT+"|"+iniciosearch
				n = listaseriesnoctv.index(serienoctv)
				listaseriesnoctvst.append([ serienoctv[0] , "" , iniciosearchT , n , "" , titlesearch ])
				listaseriesnoctv2.append([ serienoctv[0] , "" , serienoctv[2] , "0" , "" , titlesearch ])

			listaseriesnoctvst=findfutonstatus(listaseriesnoctvst,"noctv")
			for status in listaseriesnoctvst:
				n = status[3]
				listaseriesnoctv2[n][1]=status[1]
				listaseriesnoctv2[n][4]=status[4]
			listaseries.extend(listaseriesnoctv2)

		if len(listaseries)==0:
			alertnoresultadosearch()
			if listupdate==True:
				EndDirectory(category,"",listupdate,True)
			return
		for serie in listaseries:
			encontrado="0"
			listafav = readfav(serie[0],"","",CHANNELNAME)
			if len(listafav)==0:
				seriefav = checkvistosfav(serie[0],serie[2],"searchfav")
				if seriefav<>"":
					encontrado="-1"
			else:
				encontrado="-1"
			if encontrado=="0" and listaseries2.count(serie)==0:
				listaseries2.append(serie)
		if len(listaseries2)==0:
			alertnoresultadosearch()
			if listupdate==True:
				EndDirectory(category,"",listupdate,True)
			return
		listaseries = listaseries2
		listaseries.sort()

	elif seleccion == 1:
		if len(tecleado)==0:
			keyboard = xbmc.Keyboard('')
			keyboard.doModal()
			if (keyboard.isConfirmed()):
				tecleado = keyboard.getText()
				tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
			if keyboard.isConfirmed() is None or len(tecleado)==0:
				return
		if len(tecleado) == 1:
			search = tecleado
		else:
			search = ""
	else:
		search = letras[seleccion-2]

	if seleccion>0:
		if web=="" or web=="ctv":
			listaseries = findcasttv("",search,"","","")
			if len(listaseries)==0 and len(tecleado)<=1:
				alertnoresultadosearch()
				return
	if seleccion==0:
		listafav=[]
		category=category+" Vistos"

	else:
		listafav = readfav("","","",CHANNELNAME)
		category = "Series VO - Buscar - CastTV"

	if web=="" or web=="ctv":
		for serie in listaseries:
			thumbnail=""
			if serie[3]=="-1":
				thumbnail=FOLDERBLUE_THUMB
			if len(listafav)>0:
				for fav in listafav:
					if serie[0]==fav[0]:
						if thumbnail==FOLDERBLUE_THUMB:
							if fav[3]=="1":
								thumbnail=STARGREYBLUE_THUMB
							else:
								thumbnail=STARBLUE_THUMB
						elif fav[3]=="1":
							thumbnail=STARGREY_THUMB
						else:
							thumbnail=STARORANGE_THUMB
						break
			if serie[1]<>"":
				foldertitle = serie[0]+"  -  "+serie[1]
			else:
				foldertitle = serie[0]
			if len(tecleado) > 1:
				match = re.search(tecleado,foldertitle,re.IGNORECASE)
				if (match):
					rtdos = rtdos+1
				else:
					continue

			network = ""
			if serie[4]=="ended" or serie[4]=="bbc" or serie[4]=="varios":
				if serie[4]=="bbc":
					network=" (BBC)"
				serie[4]=serie[4]+";"+serie[0]+";"+serie[2]+";"+serie[1]+";"+serie[5]
			elif serie[4]<>"":
				matchnet=re.match('^[^;]*;[^;]*;[^;]*;([^;]+);',serie[4])
				if (matchnet):
					network=" ("+matchnet.group(1)+")"
			if network<>"":
				foldertitle=re.sub('^'+serie[0],serie[0]+network,foldertitle)

			addsimplefolder( CHANNELNAME , "listadossearch" , str(seleccion)+";"+tecleado+";ctv;"+serie[0]+";"+serie[1]+";"+serie[4] , foldertitle , serie[2] , thumbnail )

	if len(tecleado) > 1 and rtdos==0:
		#category = "Series VO - Buscar - TV"
		#tipo = "tv"
		sy = "0"
		listaseries = []
		#if web=="" or web=="tv":
		#	listaseries = findtv(tecleado,"-1S","")
		#if len(listaseries)==0:
		category = "Series VO - Buscar - SeriesYonkis"
		tipo = "sy"
		try:
			sy = "-1"
			httpsearch = tecleado.replace(" ", "+")
			listaseries = seriesyonkis.performsearch(httpsearch)
		except:
			sy = "0"
			listaseries = findseriesyonkis(tecleado,"-1S","","")
		if len(listaseries)==0:
			alertnoresultadosearch()
			return

		listaseries2=[]
		listaseriesst=[]
		iniciosearchT=""
		for serie in listaseries:
			if sy=="0":
				titlertdo=serie[0]
				urlrtdo=serie[2]
				thumbrtdo=""
			else:
				titlertdo=serie[3]
				urlrtdo=serie[4]
				thumbrtdo=serie[5]
			iniciosearch,titlesearch = findtsearch(titlertdo,urlrtdo)
			if iniciosearchT=="":
				iniciosearchT=iniciosearch
			elif iniciosearch not in iniciosearchT:
				iniciosearchT=iniciosearchT+"|"+iniciosearch
			n = listaseries.index(serie)
			listaseriesst.append([ titlertdo , "" , iniciosearchT , n , "" , titlesearch ])
			listaseries2.append([ titlertdo , "" , urlrtdo , thumbrtdo , "" , titlesearch ])

		listaseries = listaseries2
		listaseriesst=findfutonstatus(listaseriesst,"noctv")
		for status in listaseriesst:
			n = status[3]
			listaseries[n][1]=status[1]
			listaseries[n][4]=status[4]

		for serie in listaseries:
			status = ""
			network = ""
			thumbnail=""
			if len(listafav)>0:
				for fav in listafav:
					if serie[0]==fav[0]:
						if fav[3]=="1":
							thumbnail=STARGREY_THUMB
						else:
							thumbnail=STARORANGE_THUMB
						break
			if sy=="-1" and thumbnail=="":
				thumbnail=serie[3]
			if serie[1]<>"":
				status="  -  "+serie[1]
			if serie[4]=="ended" or serie[4]=="bbc" or serie[4]=="varios":
				if serie[4]=="bbc":
					network=" (BBC)"
				serie[4]=serie[4]+";"+serie[0]+";"+serie[2]+";"+serie[1]+";"+serie[5]
			elif serie[4]<>"":
				matchnet=re.match('^[^;]*;[^;]*;[^;]*;([^;]+);',serie[4])
				if (matchnet):
					network=" ("+matchnet.group(1)+")"

			addsimplefolder( CHANNELNAME , "listadossearch" , str(seleccion)+";"+tecleado+";"+tipo+";"+serie[0]+";"+serie[1]+";"+serie[4] , serie[0]+network+status , serie[2] , thumbnail )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",listupdate,True)
	# ------------------------------------------------------------------------------------

def findcasttv(tipolist,search,titlesearch,tptitlesearch,dataweb):
	serieslist = []
	listepisodios = []
	episodioscasttv = []
	listseasepctv = []
	seasonlist = []
	miseriectv = ""
	urlctv = ""
	statusctv = ""
	thumbnail = ""
	plot = ""

	try:
		data = scrapertools.cachePage(CTVURL)
	except:
		alertservidor(CTVURL)
		if tipolist<>"listforsubs" and tipolist<>"S" and tipolist<>"CheckFav":
			return serieslist
		elif tipolist=="S":
			return miseriectv,urlctv,listepisodios,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot
		elif tipolist=="CheckFav":
			return miseriectv,urlctv
		else:
			return miseriectv,urlctv,statusctv
	
	if tipolist == "Actualizaciones":
		tipolists = '\n\s+&nbsp;<span class="label_updated">Updated!</span>\n\s+</div>'
	else:
		tipolists = '\n\s+(?:&nbsp;<span class="label_updated">Updated!</span>\n\s+|\n\s+)</div>'

	if search == "#":
		search = "[^a-zA-Z]"

	if tipolist=="S" or tipolist=="listforsubs" or tipolist=="CheckFav":
		search = "(?:The\s+)?[^\w]*(?:"+search+")"

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
			status0 = "[Current]"
		else:
			status0 = "[Ended]"
		
		serieslist.append( [ titulo , status0 , url , updated , "" , titlectvsearch ] )

	if tipolist<>"listforsubs" and tipolist<>"S" and tipolist<>"CheckFav":
		serieslist=findfutonstatus(serieslist,"current")
		return serieslist
	else:
		if len(serieslist)>0:
			itemencontrado = searchgate(serieslist,titlesearch,"",tptitlesearch)
			if len(itemencontrado)==1:
				miseriectv = itemencontrado[0][0]
				urlctv = itemencontrado[0][2]
				dataweb = dataweb+";"+miseriectv+";"+urlctv
				if tipolist=="S":
					listepisodios,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot = findcasttvep(urlctv,miseriectv,"S","0",0,dataweb)
				elif tipolist=="listforsubs":
					statusctv = itemencontrado[0][1]
		if tipolist=="S":
			return miseriectv,urlctv,listepisodios,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot
		elif tipolist=="CheckFav":
			return miseriectv,urlctv
		else:
			return miseriectv,urlctv,statusctv

def listados(params,url,category):
	title = urllib.unquote_plus( params.get("title") )
	tipocontenido=""
	datafuton = category
	matchcat = re.match('^([^;]*);([^;]*);([^;]*);',datafuton)
	category = matchcat.group(1)
	miserievo = matchcat.group(2)
	status = matchcat.group(3)

	if "Futon" in category:
		datafuton = ""
	else:
		datafuton = re.sub('^([^;]*);([^;]*);([^;]*);','',datafuton)
	if datafuton=="":
		tipocontenido="NoFuton"

	serievistos,dataweb,respuesta = serieupdate(miserievo,status,url,tipocontenido,CHANNELNAME)

	if respuesta=="Futon":
		listinfofuton(params,url,datafuton)
	elif respuesta<>1 and respuesta<>2 and respuesta<>3 and respuesta<>4:
		if "Consulta" in category:
			category = "Series VO - Consulta - "+miserievo
		elif "Favoritas" in category:
			category = "Mis Favoritas - "+miserievo
		else:
			category = "Series VO - "+miserievo
		if dataweb=="":
			dataweb = urllib.unquote_plus( params.get("dataweb") )
			serievistos = urllib.unquote_plus( params.get("serievistos") )
		listadosupdate(miserievo,url,category,serievistos,dataweb,False)

def listadossearch(params,url,category):
	title = urllib.unquote_plus( params.get("title") )
	tipocontenido=""
	match1 = re.match('^(\d+);([^;]*);([^;]*);([^;]*);([^;]*);(.*?)$',category)
	seleccion = int(match1.group(1))
	tecleado = match1.group(2)
	web = match1.group(3)
	miserievo = match1.group(4)
	status = match1.group(5)
	datafuton = match1.group(6)

	if datafuton=="":
		tipocontenido="NoFuton"

	serievistos,dataweb,respuesta = serieupdate(miserievo,status,url,tipocontenido,CHANNELNAME)

	if respuesta=="Futon":
		listinfofuton(params,url,datafuton)
	elif respuesta==1 or respuesta==2 or respuesta==3 or respuesta==4:
		category = "Series VO - Buscar"
		searchupdate(seleccion,tecleado,category,web,True)
	else:
		category = "Series VO - Buscar - "+miserievo
		listadosupdate(miserievo,url,category,serievistos,dataweb,False)
			
def listadosupdate(miserievo,url,category,serievistos,dataweb,listupdate):
	if dataweb=="":
		serievistos,dataweb,listavistos = checkvistosfav(miserievo,url,"listadosupdate")
	else:
		if serievistos=="":
			listavistos=[]
		else:
			listavistos = readvisto(serievistos,"",CHANNELNAME)

	listaepisodios = findepisodios(url,miserievo,dataweb)

	if len(listaepisodios) == 0:
		alertnoepisodios(1)
		return
			
	if serievistos=="":		
		serievistos = miserievo

	vistoid2 = ""
	vistotipo2 = "0"

	for episodio in listaepisodios:
		if episodio[3] == "0":
			tipovisto = ""
			if len(listavistos)>0:
				#check: audio en otra variable
				eptitle = re.sub('\s\-\s(?:ES|LT)$','',episodio[0])
				vistoid = vistoid2
				if vistoid2<>"":
					tipovisto="1A"
				formato = ""
				diferenteOK = "-1"				
				for visto in listavistos:
					#por si hay algún duplicado se evita que se duplique la marca [LW]
					if eptitle==visto[1]:
						diferenteOK = "0"
					elif episodio[1]=="" or visto[2]=="":
						if episodio[7]==int(visto[4]) and episodio[7]<>0 and episodio[5]==visto[3] and episodio[5]<>"0":					
							#posible caso de un visto de otra web que es añadido a CastTV o CastTV caido
							diferenteOK = "0"
					if diferenteOK=="0":
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

			addnewfolder( CHANNELNAME , "episodiomenu" , category , titulo , episodio[1] , episodio[9] , episodio[10] , episodio[2] , episodio[4] , episodio[5] , episodio[6] , serievistos , episodio[8] , episodio[7] , miserievo+";"+url , tipovisto )

	# Sorting by date útil para invertir el listado (ep 1 1º...) por el momento descartado porque a igualdad de fecha(automáticos) no respeta el orden inicial...
	# Revisar: probar a crear un índice
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",listupdate,True)
	# ------------------------------------------------------------------------------------

def checkvistosfav(miserievo,url,tipo):
	listseries = [ miserievo ]
	listfav=[]
	listavistos=[]
	seriefav=""
	urlfav=""
	serievistos = ""

	iniciosearch,titlesearch = findtsearch(miserievo,url)
	if "casttv" in url:
		miseriectv = miserievo
		urlctv = url
		#miserietv,urltv = findtv(iniciosearch,"CheckFav",titlesearch)
		miseriesy,urlsy = findseriesyonkis("","CheckFav",titlesearch,"")
		miserie1=miseriesy
		url1=urlsy
		#miserie2=miserietv
		#url2=urltv
		if miseriesy<>"":
			listseries.append(miseriesy)
		#if miserietv<>"":
		#	listseries.append(miserietv)
	elif "seriesyonkis" in url:
		miseriesy = miserievo
		urlsy = url
		miseriectv,urlctv = findcasttv("CheckFav",iniciosearch,titlesearch,"","")
		#miserietv,urltv = findtv(iniciosearch,"CheckFav",titlesearch)
		miserie1=miseriectv
		url1=urlctv
		#miserie2=miserietv
		#url2=urltv
		if miseriectv<>"":
			listseries.append(miseriectv)
		#if miserietv<>"":
		#	listseries.append(miserietv)
	#elif "tv???" in url:
	#	miserietv = miserievo
	#	urltv = url
	#	miseriectv,urlctv = findcasttv("CheckFav",iniciosearch,titlesearch,"","")
	#	miseriesy,urlsy = findseriesyonkis("","CheckFav",titlesearch,"")
	#	miserie1=miseriectv
	#	url1=urlctv
	#	miserie2=miseriesy
	#	url2=urlsy
	#	if miseriectv<>"":
	#		listseries.append(miseriectv)
	#	if miseriesy<>"":
	#		listseries.append(miseriesy)
	
	dataweb = iniciosearch+";"+titlesearch+";"+miseriesy+";"+urlsy+";"+miseriectv+";"+urlctv

	if tipo=="nuevos":
		for item in listseries:
			listavistos = readvisto(item,"LW",CHANNELNAME)
			if len(listavistos)>0:
				serievistos=item
				break
		return serievistos,dataweb,listavistos

	if tipo=="listadosupdate" or tipo=="fav" or tipo=="datafav":
		for item in listseries:
			listavistos = readvisto(item,"",CHANNELNAME)
			if len(listavistos)>0:
				serievistos=item
				break
	if tipo=="listadosupdate":
		return serievistos,dataweb,listavistos
	elif tipo=="datafav":
		return serievistos,dataweb
	elif tipo=="fav" or tipo=="searchfav":
		if miserie1<>"":
			listfav=readfav(miserie1,"","","casttv")
			if len(listfav)>0:
				if tipo=="fav":
					return miserie1,url1,serievistos,dataweb,listfav
				elif tipo=="searchfav":
					return miserie1
		#if miserie2<>"":
		#	listfav=readfav(miserie2,"","","casttv")
		#	if len(listfav)>0:
		#		if tipo=="fav":
		#			return miserie2,url2,serievistos,dataweb,listfav
		#		elif tipo=="searchfav":
		#			return miserie2
		if tipo=="fav":
			return seriefav,urlfav,serievistos,dataweb,listfav
		elif tipo=="searchfav":
			return seriefav

def findtsearch(miserievo,url):
	matchini = re.match('^(?:The\s+)?(.)',miserievo.lower(),re.IGNORECASE)
	iniciosearch = re.sub('(?P<signo>[^\w])','\\\\\g<signo>',matchini.group(1))

	if "casttv" in url:
		titlesearch = ftitlectvsearch(miserievo)
	elif "seriesyonkis" in url:
		titlesearch = ftitlesysearch(miserievo)
	elif "subtitulos" in url:
		titlesearch = ftitlesubsearch(miserievo)
	elif "thefutoncritic" in url:
		titlesearch = ftitlefutonsearch(miserievo)
	#elif "tv???" in url:
	#	titlesearch = ftitletvsearch(miserievo)

	if titlesearch[0:1]<>matchini.group(1):
		iniciosearch = iniciosearch+"|"+titlesearch[0:1]

	if "seriesyonkis" in url:
		matchini2 = re.search('\((.).*?\)$',titlesearch,re.IGNORECASE)
		if (matchini2):
			iniciosearch2 = re.sub('(?P<signo>[^\w])','\\\\\g<signo>',matchini2.group(1))
			matchini3 = re.search('\((.).*?\)$',miserievo.lower(),re.IGNORECASE)
			if matchini3.group(1)<>matchini2.group(1):
				iniciosearch3 = re.sub('(?P<signo>[^\w])','\\\\\g<signo>',matchini3.group(1))
				iniciosearch = iniciosearch+"|"+iniciosearch2+"|"+iniciosearch3
			else:
				iniciosearch = iniciosearch+"|"+iniciosearch2

	return iniciosearch,titlesearch

def findepisodios(url,miserievo,dataweb):
	episodioslist = []
	miserie = ""
	thumbnail = ""
	plot = ""

	if dataweb<>"":
		matchwebs=re.match('^([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*)$',dataweb)
		iniciosearch=matchwebs.group(1)
		titlesearch=matchwebs.group(2)
		miseriesy=matchwebs.group(3)
		urlsy=matchwebs.group(4)
		miseriectv=matchwebs.group(5)
		urlctv=matchwebs.group(6)
		
		if urlctv<>"":
			episodioslist,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot = findcasttvep(urlctv,miseriectv,"S","0",0,dataweb)
		else:
			episodioslist =	[]
			episodioscasttv = []
			listseasepctv = []
			seasonlist = []
			thumbnail = ""
			plot = ""
		if urlsy<>"":
			listseasepsy,listseasonsy,listaudio,thumbnailsy,plotsy = findsyep(urlsy,"S","0",0)
		else:
			listseasepsy = []
			listseasonsy = []
			listaudio = []
			thumbnailsy = ""
			plotsy = ""
		#if urltv<>"":
		#	params = {'Serie': miserietv}
		#	listseaseptv,listseasontv = findtvep(params,urltv,"","S","0",0)
		#else:
		#	listseaseptv = []
		#	listseasontv = []
	else:
		iniciosearch,titlesearch = findtsearch(miserievo,url)
		if "casttv" in url:
			miseriectv = miserievo
			urlctv = url
			#miserietv,urltv,listseaseptv,listseasontv = findtv(iniciosearch,"S",titlesearch)
			miseriesy,urlsy,listseasepsy,listseasonsy,listaudio,thumbnailsy,plotsy = findseriesyonkis("","S",titlesearch,"")
			#dataweb = iniciosearch+";"+titlesearch+";"+miserietv+";"+urltv+";"+miseriesy+";"+urlsy+";"+miseriectv+";"+urlctv
			dataweb = iniciosearch+";"+titlesearch+";"+miseriesy+";"+urlsy+";"+miseriectv+";"+urlctv
			episodioslist,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot = findcasttvep(url,miserievo,"S","0",0,dataweb)
		elif "seriesyonkis" in url:
			miseriesy = miserievo
			urlsy = url
			listseasepsy,listseasonsy,listaudio,thumbnailsy,plotsy = findsyep(url,"S","0",0)
			#miserietv,urltv,listseaseptv,listseasontv = findtv(iniciosearch,"S",titlesearch)
			#dataweb0 = iniciosearch+";"+titlesearch+";"+miserietv+";"+urltv+";"+miseriesy+";"+urlsy
			dataweb0 = iniciosearch+";"+titlesearch+";"+miseriesy+";"+urlsy
			miseriectv,urlctv,episodioslist,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot = findcasttv("S",iniciosearch,titlesearch,"",dataweb0)
			dataweb = dataweb0+";"+miseriectv+";"+urlctv
		#elif "tv???" in url:
		#	miserietv = miserievo
		#	urltv = url
		#	params = {'Serie': miserietv}
		#	listseaseptv,listseasontv = findtvep(params,url,"","S","0",0)
		#	miseriesy,urlsy,listseasepsy,listseasonsy,listaudio,thumbnailsy,plotsy = findseriesyonkis("","S",titlesearch,"")
		#	dataweb0 = iniciosearch+";"+titlesearch+";"+miserietv+";"+urltv+";"+miseriesy+";"+urlsy
		#	miseriectv,urlctv,episodioslist,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot = findcasttv("S",iniciosearch,titlesearch,"",dataweb0)
		#	dataweb = dataweb0+";"+miseriectv+";"+urlctv
		else:
			return episodioslist

	if miseriectv<>"":
		miserie = miseriectv
	elif "seriesyonkis" in url:
		miserie = miseriesy
		thumbnail = thumbnailsy
		plot = plotsy
	#elif "tv???" in url:
	#	miserie = miserietv
	#	thumbnail = thumbnailsy
	#	plot = plotsy

	# Si una temporada está en SeriesYonkis se agregan todos los episodios (los de pago y los que faltan en CastTV)
	for season in seasonlist:
		#OKtv="0"
		OKsy="0"
		#TV
		#if listseasontv.count(season)==1:
		#	OKtv="-1"
		#SeriesYonkis
		if listseasonsy.count(season)==1:
			OKsy="-1"
		#if OKtv=="-1" or OKsy=="-1":
		if OKsy=="-1":
			for episodio in episodioslist:
				if episodio[5]==season:
					n = episodioslist.index(episodio)
					if episodio[3]=="-1":
						episodio[3] = "0"
					if episodio[8]=="ctv":
						episodio[8] = "ctv-sy"
						#if OKtv=="-1" and OKsy=="-1":
						#	episodio[8] = "ctv-tv-sy"
						#elif OKtv=="-1":
						#	episodio[8] = "ctv-tv"
					if episodio[7] > 1:
						lastseasontv = episodioscasttv[-1]
						if episodio[6] == lastseasontv:
							if n < len(episodioslist)-1 and episodioslist[n+1][6] <> episodio[6] :						
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserie+" - "+seasontvlast , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , episodio[8] , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])
							elif n == len(episodioslist)-1:
								seasontvlast = lastseasontv[0:4]+"01"
								episodioslist.insert(n+1,[ miserie+" - "+seasontvlast , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvlast , 1 , episodio[8] , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])
						capitvnew = episodio[7]-1
						seasontvnew = episodio[6][0:4]+str(capitvnew)
						if len(seasontvnew) == 5:
							seasontvnew = seasontvnew.replace('E' , 'E0')
						
						if episodioslist[n+1][5] == season and episodioslist[n+1][6] <> episodio[6] and episodioslist[n+1][7] <> capitvnew:
							episodioslist.insert(n+1,[ miserie+" - "+seasontvnew , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , episodio[8] , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])
						if episodioslist[n+1][5] == str(int(season)-1) and episodioslist[n+1][5] <> "0":
							episodioslist.insert(n+1,[ miserie+" - "+seasontvnew , "" , episodio[2] , episodio[3] , episodio[4] , episodio[5] , seasontvnew , capitvnew , episodio[8] , episodio[9] , episodio[10], episodio[11] , episodio[12] , episodio[13] ])

	# Si faltan temporadas se añaden al listado que tenga fechas de emisión
	for seasonsy in listseasonsy:
		if seasonlist.count(seasonsy)==0:
			i = listseasonsy.index(seasonsy)
			#arriesgado check: condición para evitar añadir temporadas por errores tipográficos
			#si solo hay un episodio y es superior al tercero no se añade
			if listseasepsy[i][6]==1 and listseasepsy[i][1]>3:
				continue
			listseasepctv.append(listseasepsy[i])
			j=1
			while int(seasonsy)-j>0:
				seasonwhile = str(int(seasonsy)-j)
				if seasonlist.count(seasonwhile)<>0:
					k = seasonlist.index(seasonwhile)
					listseasepctv[-1][2]=listseasepctv[k][2]
					listseasepctv[-1][3]=listseasepctv[k][3]
					listseasepctv[-1][4]=listseasepctv[k][4]
					break
				j=j+1
		else:
			i = seasonlist.index(seasonsy)
			listseasepctv[i][5] = "ctv-sy"

	# Se agregan completas las temporadas de SeriesYonkis que faltan en CastTV
	#totalseasons = len(listseasepctv)
	for seasontv in listseasepctv:
		if seasonlist.count(seasontv[0])==0:
			n=seasontv[1]
			m=0
		elif seasonlist.count(seasontv[0])<>0 and listseasonsy.count(seasontv[0])<>0:
			s = listseasonsy.index(seasontv[0])
			lastepsy = listseasepsy[s][1]
			if lastepsy>seasontv[1]:
				n=lastepsy
				m=seasontv[1]
			else:
				continue
		else:
			continue

		if len(seasontv[0])==1:
			seasonT = "S0"+seasontv[0]
		else:
			seasonT = "S"+seasontv[0]
		date=str(seasontv[2])+"."+str(seasontv[3])+"."+str(seasontv[4])
		while n>m:
			if n<10:
				epT = "E0"+str(n)
			else:
				epT = "E"+str(n)
			episodioslist.append([ miserie+" - "+seasonT+epT , "" , date , "0" , dataweb , seasontv[0] , seasonT+epT , n , seasontv[5] , thumbnail , plot , seasontv[2] , seasontv[3] , seasontv[4] ])
			n=n-1

	if len(listaudio)>0:
		for episodio in episodioslist:
			for audio in listaudio:
				if audio[0]==episodio[5] and audio[1]==episodio[7]:
					episodio[0]=episodio[0]+audio[2]
					break

	episodioslist.sort(key=lambda episodio: episodio[7])
	episodioslist.sort(key=lambda episodio: int(episodio[5]))
	episodioslist.sort(key=lambda episodio: episodio[11])
	episodioslist.sort(key=lambda episodio: episodio[12])
	episodioslist.sort(key=lambda episodio: episodio[13])
	episodioslist.reverse()
	return episodioslist

def findcasttvep(url,miserievo,todos,seasonsearch,episodiosearch,dataweb):
	episodioslist = []
	seasonlist = []
	listseasepctv = []
	episodioscasttv = []
	thumbnail = ""
	plot = ""
	try:
		data = scrapertools.cachePage(url)
	except:
		if todos=="S":
			return episodioslist,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot
		elif todos=="0":
			return episodioslist,thumbnail,plot


	# ------------------------------------------------------
	# Extrae la carátula
	# ------------------------------------------------------		
	match1 = re.search('<meta name="image_src" content="(.*?)"',data,re.IGNORECASE)
	if (match1):
		thumbnail = urlparse.urljoin("http://www.casttv.com",match1.group(1))

	# ------------------------------------------------------
	# Extrae el argumento
	# ------------------------------------------------------		
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
		plot = plot.replace('&nbsp;' , ' ')

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
		seasontvid = "0"
		seasontv = ""
		# dejé episodiotv como vble numérica por probar, y lo he dejado así, pero no vale la pena :-)
		episodiotv = 0

		# + Temporada y Capítulo
		match0 = re.search('\n\s+\n\s+(\w+)\n\s+',match[0],re.IGNORECASE)
		if (match0):
			titulo = miserievo+" - "+match0.group(1)+" - "+match[2]
			# + Season
			match1 = re.search('S0?(\d+)E0?(\d+)',match0.group(1),re.IGNORECASE)
			if (match1):
				seasontvid = match1.group(1)
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
			url = ""

		if todos=="S":
			episodioslist.append( [ titulo , url , date , pago , dataweb , seasontvid , seasontv , episodiotv , "ctv" , thumbnail , plot , day , month , year ] )
			if seasontv <> "":
				episodioscasttv.append(seasontv)		
			if seasontvid <> "0":
				if seasonlist.count(seasontvid)==0:
					seasonlist.append(seasontvid)
					listseasepctv.append([ seasontvid , episodiotv , day , month , year , "ctv" , 0 ])
				else:
					n = seasonlist.index(seasontvid)
					if episodiotv>listseasepctv[n][1]:
						listseasepctv[n][1]=episodiotv
						listseasepctv[n][2]=day
						listseasepctv[n][3]=month
						listseasepctv[n][4]=year
		elif todos=="0" and url<>"":
			if seasontvid==seasonsearch and episodiotv==int(episodiosearch):
				episodioslist.append( [ titulo , url , date , pago , dataweb , seasontvid , seasontv , episodiotv , "ctv" , thumbnail , plot , day , month , year ] )
				break
	if todos=="S":
		return episodioslist,episodioscasttv,listseasepctv,seasonlist,thumbnail,plot
	elif todos=="0":
		return episodioslist,thumbnail,plot

def findtvep(params,url,category,todos,season,episodio):
	listepisodios = []
	listepisodio = []
	listseason = []
	try:	
		listepisodios = []
	except:
		if todos=="-1" or todos=="0":
			return listepisodios
		elif todos=="S":
			return listepisodio,listseason
	
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
					listepisodio.append([ seasonep , episodioep , day , month , year , "tv" , 0 ])
					listseason.append(seasonep)
				else:
					n = listseason.index(seasonep)
					if episodioep>listepisodio[n][1]:
						listepisodio[n][1]=episodioep
						listepisodio[n][2]=day
						listepisodio[n][3]=month
						listepisodio[n][4]=year

		return listepisodio,listseason

def findsyep(url,todos,season,episodio):
	listepisodios = []
	listepisodio = []
	listseason = []
	listaudio = []
	thumbnail = ""
	plot = ""
	try:
		data = scrapertools.cachePage(url)
	except:
		if todos=="-1":
			return listepisodios
		elif todos=="0":
			return listepisodio,thumbnail,plot
		elif todos=="S":
			return listepisodio,listseason,listaudio,thumbnail,plot

	# Thumbnail
	matchthumb = re.search('<img title="[^"]+" src="(http\:\/\/images.seriesyonkis[^"]+)"',data,re.IGNORECASE)
	if (matchthumb):
		thumbnail = matchthumb.group(1)

	# Plot
	patronvideos = '<h3>Descripci.n.</h3>(.*?)<div'
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		plot = matches.group(1)
		plot = re.sub('(?:<.*?>|\n)','',plot)

	# Episodios
	patronvideos = '<a href="(http://www.seriesyonkis.com/capitulo[^"]+)"[^>]+>([^<]+)</a>([^>]*)'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)
	for match in matches:
		# Titulo
		title = match[1]
		# audio (solo audio español)
		audio = ""
		if "spanish.png" in match[2]:
			audio = " - ES"
		elif "latino.png" in match[2]:
			audio = " - LT"
		# URL
		url = match[0]	
		listepisodios.append([ title , url , audio ])
	
	if todos=="-1":
		return listepisodios
	elif todos=="0":
		for ep in listepisodios:
			match1=re.search('0*(\d+)x0*(\d+)',ep[0],re.IGNORECASE)
			if (match1):
				seasonep = match1.group(1)
				episodioep = int(match1.group(2))
				if seasonep==season and episodioep==int(episodio):
					listepisodio.append(ep)
					break

		return listepisodio,thumbnail,plot
	elif todos=="S":
		listepisodios.reverse()
		for ep in listepisodios:
			match1=re.search('0*(\d+)x0*(\d+)',ep[0],re.IGNORECASE)
			if (match1):
				seasonep = match1.group(1)
				episodioep = int(match1.group(2))
				if listseason.count(seasonep)==0:
					listepisodio.append([ seasonep , episodioep , 0 , 0 , 0 , "sy" , 1 ])
					listseason.append(seasonep)
				else:
					n = listseason.index(seasonep)
					listepisodio[n][6]=listepisodio[n][6]+1
					if episodioep>listepisodio[n][1]:
						listepisodio[n][1]=episodioep
				if ep[2]<>"":
					listaudio.append([ seasonep , episodioep , ep[2] ])					
		return listepisodio,listseason,listaudio,thumbnail,plot

def findsubseries(title,todos,titlesearch,season,episodio):
	url = "http://www.subtitulos.es/series"
	subserieslist=[]
	seriesubencontrada=[]
	listsubs = []
	miep = ""
	miseriesub = ""
	urlsub = ""
	try:
		data = scrapertools.cachePage(url)
	except:
		alertservidor(url)
		if todos=="-1":
			return subserieslist
		elif todos=="0":
			return miseriesub,urlsub
		elif todos=="V":
			return miseriesub,urlsub,miep,listsubs
	
	search = ""
	if len(title)==1:
		search = title
		if search=="#":
			search = "[^a-zA-Z]"
	if todos=="V" or todos=="0":
		search = "(?:The\s+)?[^\w]*(?:"+title+")"
	
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

	elif todos=="0" or todos=="V":
		if len(subserieslist) > 0:
			itemencontrado = searchgate(subserieslist,titlesearch,"","")
			if len(itemencontrado)==1:
				miseriesub = itemencontrado[0][0]
				urlsub = itemencontrado[0][1]
				if todos=="V":
					miep,listsubs = findsubsep(urlsub,"0",season,episodio)
		if todos=="0":
			return miseriesub,urlsub
		elif todos=="V":
			return miseriesub,urlsub,miep,listsubs

def findtv(title,todos,titlesearch):
	url = ""
	listseries = []
	listepisodios = []
	listseason = []
	miserietv = ""
	urltv = ""
	try:
		data = scrapertools.cachePage(url)
	except:
		alertservidor(url)
		if todos=="-1" or todos=="-1S":
			return listseries
		elif todos=="S":
			return miserietv,urltv,listepisodios,listseason
		elif todos=="CheckFav":
			return miserietv,urltv

	search = "[^<]+"
	if todos=="-1S":
		search = "[^<]*"+title+"[^<]*"
	elif title<>"":
		search = "[^\w]*(?:"+title+")[^<]+"

	patronvideos = '<li><a\ href="([^"]+)">('+search+')'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		#Serie
		titulotv = match[1]
		titulotv = re.sub('\s+$','',titulotv)

		# Titulo para búsquedas
		titletvsearch = ftitletvsearch(titulotv)
  
		#Url
		url = match[0]

    		listseries.append([ titulotv , "" , url , "0" , "" , titletvsearch ])

	if todos=="-1" or todos=="-1S":
		return listseries
	else:
		if len(listseries)>0:
			itemencontrado = searchgate(listseries,titlesearch,"","")
			if len(itemencontrado)==1:
				miserietv = itemencontrado[0][0]
				urltv = itemencontrado[0][2]
				params = {'Serie': miserietv}
				if todos=="S":
					listepisodios,listseason = findtvep(params,urltv,"",todos,"0",0)
		if todos=="S":
			return miserietv,urltv,listepisodios,listseason
		elif todos=="CheckFav":
			return miserietv,urltv

def findseriesyonkis(title,todos,titlesearch,tptitlesearch):
	listseries = []
	listepisodios = []
	listseason = []
	listaudio = []
	miseriesy = ""
	urlsy = ""
	thumbnail = ""
	plot = ""

	try:
		data = scrapertools.cachePage(SYURL)
	except:
		alertservidor(SYURL)
		if todos=="-1" or todos=="-1S":
			return listseries
		elif todos=="S":
			return miseriesy,urlsy,listepisodios,listseason,listaudio,thumbnail,plot
		elif todos=="CheckFav":
			return miseriesy,urlsy

	search = "[^<]+"
	if todos=="-1S":
		#apaño para buscar en seriesyonkis títulos con acentos (el teclado de la Xbox no los soporta?)
		#o quitar los acentos de los títulos y luego buscar...
		search = re.sub('(?:a|e|i|o|u)','[^<]{1,2}',title)
		search = "[^<]*"+search+"[^<]*"

	# Extrae el bloque de las series
	patronvideos = '<h4><a.*?id="series".*?<ul>(.*?)</ul>.*?<h4><a.*?id="miniseries".*?<ul>(.*?)</ul>'
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		data = matches.group(1)+matches.group(2)

	# Extrae las entradas (carpetas)
	patronvideos  = '<li class="page_item"><a href="(http://www.seriesyonkis.com/serie[^"]+)"[^>]+>('+search+')</a></li>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		#Serie
		titulosy = match[1]

		# Titulo para búsquedas
		titlesysearch = ftitlesysearch(titulosy)
  
		#Url
		url = match[0]

    		listseries.append([ titulosy , "" , url , "0" , "" , titlesysearch ])

	if todos=="-1" or todos=="-1S":
		return listseries
	else:
		if len(listseries)>0:
			itemencontrado = searchgate(listseries,titlesearch,"seriesyonkis",tptitlesearch)
			if len(itemencontrado)==1:
				miseriesy = itemencontrado[0][0]
				urlsy = itemencontrado[0][2]
				if todos=="S":
					listepisodios,listseason,listaudio,thumbnail,plot = findsyep(urlsy,todos,"0",0)
		if todos=="S":
			return miseriesy,urlsy,listepisodios,listseason,listaudio,thumbnail,plot
		elif todos=="CheckFav":
			return miseriesy,urlsy

def searchgate(listforsearchin,titletosearch,tplistsearch,tptitlesearch):
	# listforsearchin tiene que tener en la última columna [-1] el campo para búsquedas

	itemencontrado = []
	itemencontrado2 = []
	group1search = ".*?"
	reverse=True
	topn=2
	titletosearch2 = titletosearch
	if tptitlesearch=="titleerdm":
		titletosearch2 = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',titletosearch)
	matchtitle = re.match('(.*?)\((.*?)\)$',titletosearch)
	if (matchtitle):
		option1 = re.sub('(?:\(|\))','',titletosearch)
		option2 = matchtitle.group(1)
		option3 = matchtitle.group(2)
		titletosearch2 = "(?:"+option1+"|"+option2+"|"+option3+")"
	titletosearch = re.sub('(?:\(|\))','',titletosearch)

	if tplistsearch=="futon" or tptitlesearch=="futon":
		reverse=False
		if tplistsearch=="futon":
			matchbottom = re.search('[a-z]((?:1|2)\d{3}|us)$',titletosearch)
			if (matchbottom):
				reverse=True

	if tptitlesearch=="varios":
		topn=10
	if tptitlesearch=="futon":
		group1search = "(?:\d+|usa?|uk)?"
		
	listforsearchin.sort(key=lambda listfor: listfor[-1])
	n = 0
	for listfor in listforsearchin:
		if n==topn:
			break
		elif topn==10 and len(itemencontrado)>0 and n==2:
			break
		elif topn==10 and len(itemencontrado2)>0 and len(itemencontrado2)<n:
			break
		titletosearchin = listfor[-1]
		if tplistsearch=="seriesyonkis":
			titletosearchin = re.sub('(?:\(|\))','',titletosearchin)
		forin = re.match(titletosearch2+'('+group1search+')$',titletosearchin,re.IGNORECASE)
		if (forin):
			if forin.group(1)=="":
				itemencontrado.append(listfor)
				if tplistsearch=="futon":
					n = n+1
					continue
				else:
					break
		if tplistsearch=="seriesyonkis":
			forinsy0 = re.match('(.*?)\((.*?)\)$',listfor[-1])
			if (forinsy0):
				titletosearchinsy = forinsy0.group(2)
				forinsy = re.match(titletosearch2+'('+group1search+')$',titletosearchinsy,re.IGNORECASE)
				if (forinsy):
					if forinsy.group(1)=="":
						itemencontrado.append(listfor)
						break
				else:
					titletosearchinsy = forinsy0.group(1)
					forinsy2 = re.match(titletosearch2+'('+group1search+')$',titletosearchinsy,re.IGNORECASE)
					if (forinsy2):
						if forinsy2.group(1)=="":						
							itemencontrado.append(listfor)
							break
		# Si se obtuvieran 2 o más coincidencias no serviría
		if (forin):
			if forin.group(1)<>"":
				itemencontrado2.append(listfor)
				n = n+1
				continue
		if tplistsearch=="seriesyonkis":
			if (forinsy0):
				if (forinsy):
					if forinsy.group(1)<>"":
						itemencontrado2.append(listfor)
						n = n+1
						continue
				else:
					if (forinsy2):
						if forinsy2.group(1)<>"":						
							itemencontrado2.append(listfor)
							n = n+1
							continue
		if n>0:
			n = n+1

	if reverse==True and len(itemencontrado)==0 and len(itemencontrado2)==0:
		n = 0
		listforsearchin.reverse()
		for listfor in listforsearchin:
			if n==topn:
				break
			elif topn==10 and len(itemencontrado2)>0 and len(itemencontrado2)<n:
				break
			if len(listfor[-1])>1:
				titletosearchin = listfor[-1]
				if tptitlesearch=="titleerdm":
					titletosearchin = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',titletosearchin)
				elif tplistsearch=="seriesyonkis":
					matchtitle = re.match('(.*?)\((.*?)\)$',titletosearchin)
					if (matchtitle):
						option1 = re.sub('(?:\(|\))','',titletosearchin)
						option2 = matchtitle.group(1)
						option3 = matchtitle.group(2)
						titletosearchin = "(?:"+option1+"|"+option2+"|"+option3+")"
				forback = re.match('^'+titletosearchin+'.+$',titletosearch,re.IGNORECASE)
				if (forback):
					itemencontrado2.append(listfor)
					if tptitlesearch=="titleerdm":
						break
					else:
						n = n+1
				elif n>0:
					n = n+1
											
	if len(itemencontrado)==0:
		itemencontrado = itemencontrado2
	
	return itemencontrado

def listasubep(params,url,category):
	miseriesub = urllib.unquote_plus( params.get("title") )
	miseriesub = re.sub('\s+\-\s+\[Subtítulos\]','',miseriesub)
	
	listasubep = findsubsep(url,"-1","0",0)

	if len(listasubep)==0:
		alertnoepisodios(3)
		return

	for subep in listasubep:
		addsimplefolder( CHANNELNAME , "listasubs" , category , subep[0]+"  -  [Subtítulos]" , subep[1] , "" )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def listasubs(params,url,category):
	miep = urllib.unquote_plus( params.get("title") )
	miep = re.sub('\s+\-\s+\[Subtítulos\]','',miep)
	#Buscando subs desde vídeos no se muestra el listado de vídeos
	videos="-1"
	updates="0"
	if 'Series VO' in category:
		videos="0"
	elif 'Actualizaciones' in category:
		updates="-1"
	match = re.match('([^;]+);([^;]+)$',category)
	if (match):
		category = match.group(1)
		miep = match.group(2)
	#Serie, Season y episodio
	seasonep = "0"
	match1=re.match('^(.*?)0*(\d+)x0*(\d+)',miep,re.IGNORECASE)
	if (match1):
		serie = match1.group(1)
		serie = re.sub('\s*\-*\s*$','',match1.group(1))
		seasonep = match1.group(2)
		episodioep = int(match1.group(3))
	idioma = ""
	version = ""
	
	listasubtitulos = findsubs(miep,url)

	if len(listasubtitulos)==0:
		alertnoepisodios(3)
		return

	iniciosearch,titlesearch = findtsearch(serie,url)
	if updates=="-1":
		miseriesub,urlsub = findsubseries(iniciosearch,"0",titlesearch,"0",0)
	
	#Encabezados
	additem( CHANNELNAME , category , "SUBTITULOS - [Descargar] :" , "" , "" , "" )
	if updates=="-1":
		addsimplefolder( CHANNELNAME , "listasubep" , "Subtítulos.es - "+miseriesub , miseriesub+"  -  [Subtítulos]" , urlsub , "" )
	additem( CHANNELNAME , category , miep , "" , "" , "" )

	for subs in listasubtitulos:
		addsimplefolder( CHANNELNAME , "subtitulo" , subs[4] , subs[0]+" ("+subs[1]+") - ["+subs[2]+"] ("+subs[5]+" descargas)" , subs[3] , DESCARGAS_THUMB )

	if seasonep<>"0" and videos=="-1":
		listacasttv = []
		listasy = []
		listatv = []
		tituloserie = ""
		urlserie = ""
		thumbnail=""
		plot=""
		network=""

		miseriectv,urlctv,statusctv = findcasttv("listforsubs",iniciosearch,titlesearch,"","")
		miseriesy,urlsy = findseriesyonkis("","CheckFav",titlesearch,"")
		#miserietv,urltv = findtv(iniciosearch,"CheckFav",titlesearch)

		if urlctv<>"":
			episodioslist,thumbnail,plot = findcasttvep(urlctv,miseriectv,"0",seasonep,episodioep,"")
			if len(episodioslist)==1:
				titlectv = episodioslist[0][0]
				urlepctv = episodioslist[0][1]
				listacasttv,listactmirrors = findvideoscasttv(urlepctv)
			if tituloserie=="":
				tituloserie = miseriectv
				urlserie = urlctv
		if urlsy<>"":
			listasy,thumbnailsy,plotsy = findsyep(urlsy,"0",seasonep,episodioep)
			if tituloserie=="":
				tituloserie = miseriesy
				urlserie = urlsy
			if thumbnail=="":
				thumbnail = thumbnailsy
				plot = plotsy
		#if urltv<>"":
		#	params = {'Serie': miserietv}
		#	listatv = findtvep(params,urltv,"","0",seasonep,episodioep)
		#	if tituloserie=="":
		#		tituloserie = miserietv
		#		urlserie = urltv

		subserielist = [ [ iniciosearch , statusctv , "" , "" , "" , titlesearch ] ]
		subserielist = findfutonstatus(subserielist,"foritem")
		statusfuton = subserielist[0][1]
		datafuton = subserielist[0][4]
		if datafuton=="ended" or datafuton=="bbc" or datafuton=="varios":
			if datafuton=="bbc":
				network=" (BBC)"
			datafuton = datafuton+";"+tituloserie+";"+urlserie+";"+statusfuton+";"+subserielist[0][5]
		elif datafuton<>"":
			matchnet=re.match('^[^;]*;[^;]*;[^;]*;([^;]+);',datafuton)
			if (matchnet):
				network=" ("+matchnet.group(1)+")"
			
		additem( CHANNELNAME , category , "VIDEOS :" , "" , "" , "" )
		if tituloserie<>"":
			foldertitle = tituloserie+network+"  -  "+statusfuton
			foldertitle = re.sub('\s+\-\s+$','',foldertitle)
			addseriefolder( CHANNELNAME , "listados" , category+";"+tituloserie+";"+statusfuton+";"+datafuton , foldertitle , urlserie , "" , "" , "" , "" )
		elif datafuton<>"":
			addsimplefolder( CHANNELNAME , "listinfofuton" , datafuton , serie+"  -  [The Futon Critic]" , "thefutoncritic" , "" )
		else:
			addsimplefolder( CHANNELNAME , "searchfuton" , "The Futon Critic" , "The Futon Critic" , "" , "http://www.thefutoncritic.com/images/logo.gif" )
			addsimplefolder( CHANNELNAME , "search" , category , "Series VO - Buscar" , "" , "" )

		if len(listacasttv)>0:
			for video in listacasttv:
				addnewvideo( CHANNELNAME , "play" , category , video[2] , titlectv+" - "+video[0]+" - [CastTV]" , video[1] , thumbnail , plot )
			for video in listactmirrors:
				addnewvideo( CHANNELNAME , "play" , category , video[2] , titlectv+" - "+video[0]+" - Mirror - [CastTV]" , video[1] , thumbnail , plot )
		if len(listasy)>0:
			for ep in listasy:
				xbmctools.addnewvideo( CHANNELNAME , "seriesyonkis.detail" , category , "Megavideo" , ep[0]+ep[2]+" - [SeriesYonkis]" , ep[1] , thumbnail , plot , Serie=miseriesy )
		#if len(listatv)>0:
		#	for ep in listatv:
		#		#se deja la fecha porque no se muestra previamente el ltdo de episodios...
		#		titletv = re.sub('\s+\(',' - (',ep['title'])
		#		if thumbnail=="":
		#			thumbnail=ep['thumbnail']
		#			plot=ep['plot']
		#		xbmctools.addnewvideo( CHANNELNAME , "" , category , "" , titletv+" - [TV]" , ep['url'] , thumbnail , plot , Serie=miserietv )

	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def findsubsep(url,todos,seasonsearch0,episodiosearch):
	listseason = []
	listepisodios = []
	listsubtitulos = []
	miep = ""

	seasonsearch = "\d{1,2}"
	if todos=="0":
		seasonsearch=seasonsearch0

	try:
		data = scrapertools.cachePage(url)
	except:
		if todos=="-1":
			return listepisodios
		else:
			return miep,listsubtitulos
	
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
	listsubupdates = []
	try:
		data = scrapertools.cachePage(SUBURL)
	except:
		alertservidor(SUBURL)
		return listsubupdates

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
		tiempo = animeforos.formatostring(match[3])
		# Tituloupdate
		tituloupdate = titulo+" - "+idioma+" "+tiempo
		# URL
		url = urlparse.urljoin("http://www.subtitulos.es",match[0])

		listsubupdates.append([ titulo , url , tituloupdate ])

	return listsubupdates

def findsubs(miep,url):
	listsubtitulos = []
	try:
		data = scrapertools.cachePage(url)
	except:
		return listsubtitulos

	# ------------------------------------------------------
	# Extrae las versiones
	# ------------------------------------------------------
	patronvideos  = 'class="NewsTitle"><img[^>]+>\s*\n(Versi[^<]+)</td>'
	patronvideos += '(.*?)</table>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
		
	for match in matches:
		version = match[0]
		version = animeforos.formatostring(version)

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
	listasubseries = []
	listasubupdates = []
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
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def searchfuton(params,url,category):
	listaseries = []
	tecleado = ""
	search = ""

	opciones = []
	letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
	opciones.append("Mostrar Todo")
	opciones.append("Mostrar Estrenos de los últimos tres meses")
	opciones.append("Teclado")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Búsqueda por Teclado o por Inicial del Título:", opciones)
	if seleccion == -1 :return
	if seleccion == 1:
		search = "3mpre"
		category = category+" - Premieres"
	elif seleccion == 2:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
			if len(tecleado)>0:
				category = category+" - Buscar"				
				search = tecleado			
		if keyboard.isConfirmed() is None or len(tecleado)==0:
			return

	elif seleccion > 2:
		search = letras[seleccion-3]
		category = category+" - Buscar - "+search

	listaseries = futonfilters(search)

	if len(listaseries)==0:
		alertnoresultadosearch()
		return
	else:
		searchfutonlist(category,listaseries)

def searchfutonlist(category,listaseries):
	listafav = readfav("","","",CHANNELNAME)

	for serie in listaseries:
		thumbnail=""
		if len(listafav)>0:
			for fav in listafav:
				seriesearch=re.sub('^(.*?), the$',lambda ppal: 'the '+ppal.group(1),serie[0].lower())
				if seriesearch==fav[0].lower():
					if fav[3]=="1":
						thumbnail=STARGREY_THUMB
						break
					thumbnail=STARORANGE_THUMB
					break
		if serie[8]<>"":
			status = "  -  "+serie[8]

		title = serie[0]+" ("+serie[3]+")"
		plot = serie[0].upper()+": Network: "+serie[3]+". Broadcast History: "+serie[2]+". Status: "+serie[7]+". "+serie[5]+": "+serie[6]+". Time Slot: "+serie[4]

		addfolder( CHANNELNAME , "listinfofuton" , serie[0]+";"+serie[1]+";"+serie[2]+";"+serie[3]+";"+serie[4]+";"+serie[5]+";"+serie[6]+";"+serie[7]+";"+serie[8] , title+status , serie[1] , thumbnail , plot )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def futonoptions(data,filter):
	options = []
	listoptions = []
	# ------------------------------------------------------
	# Extrae el bloque de opciones
	# ------------------------------------------------------
	patronvideos = '<select name="'+filter+'">(.*?)</select>'
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		data = matches.group(1)
	else:
		return options,listoptions
	# ------------------------------------------------------
	# Extrae las opciones
	# ------------------------------------------------------
	patronvideos = '<option value="([^"]*)">([^<]+)</option>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)
	for match in matches:
		#option
		option = match[1]
		if "network" in filter and option<>"all":
			option = option.upper()
		elif "daycode" in filter or "genre" in filter:
			option = option.capitalize()
		elif "statuscode" in filter:
			option = formattitle(option)
		if option=="all" or option=="All":
			option = "All  (opción por defecto)"

		#value
		value = match[0]
		value = value.replace(" ","+")

		options.append(option)
		listoptions.append([ option , value ])

	if filter=="statuscode":
		options.insert(10,options[1])
		options.insert(10,options[2])
		options.pop(1)
		options.pop(1)
		listoptions.insert(10,listoptions[1])
		listoptions.insert(10,listoptions[2])
		listoptions.pop(1)
		listoptions.pop(1)

	return options,listoptions

def futonfilters(search):
	listseries = []
	inicial = ""
	tipostatus = ""

	try:
		data = scrapertools.cachePage(FTURL)
	except:
		alertservidor(FTURL)
		return listseries

	listvalue = [ "" , "" , "" , "" , "" ]

	listfilters = [ [ "una Cadena de TV" , "network" ] , [ "un Horario" , "daycode" ] , [ "un Tipo de Status" , "statuscode" ] , [ "un Género" , "genre" ] , [ "un Estudio" , "studio" ] ]

	if search=="3mpre":
		tipostatus="premiere"
		listfilters.pop(2)
		search=""
	n=0	
	for filter in listfilters:
		options,listoptions = futonoptions(data,filter[1])
		searchtype = xbmcgui.Dialog()
		seleccion = searchtype.select("Seleccione "+filter[0]+":", options)
		if seleccion==-1:
			value = ""
		else:
			value = listoptions[seleccion][1]
		listvalue[n] = value
		n = n+1

	if len(search)==1:
		inicial = search
		search = ""
	
	urlsearch = "http://www.thefutoncritic.com/showatch.aspx?series="+inicial+"&network="+listvalue[0]+"&daycode="+listvalue[1]+"&statuscode="+listvalue[2]+"&genre="+listvalue[3]+"&studio="+listvalue[4]
	listseries = findfuton(search,urlsearch,tipostatus)

	return listseries

def findfuton(search,url,tipostatus):
	listseries = []
	try:
		data = scrapertools.cachePage(url)
	except:
		return listseries

	if tipostatus=="bbc":
		search = search.upper()
	elif tipostatus=="ended" or tipostatus=="foritem" or tipostatus=="noctv":
		search = "(?:"+search.upper()+")[^<]*"
	elif search<>"":
		search = re.sub('^(?:The|the|THE)\s+(.+)$',lambda s: s.group(1),search)
		search = "[^<]*"+search.upper()+"[^<]*"
	else:
		search = "[^<]+"

	if tipostatus=="noctv":
		tipostatus="current"

	patronseries  = '<td><a href="([^"]+)">('+search+')</a></td>.?\s*'
	patronseries += '<td>(.*?)</td>.?\s*'
	patronseries += '<td>(.*?)</td>.?\s*'
	patronseries += '<td>(.*?)</td>.?\s*'
	patronseries += '<td>(.*?)</td>.?\s*'
	patronseries += '<td>(.*?)</td>.?\s*</tr>'
	matches = re.compile(patronseries,re.DOTALL).findall(data)
	for match in matches:
		if tipostatus=="current" and "canceled" in match[6]:
			continue
		elif tipostatus=="ended" and "canceled" not in match[6] and "hiatus" not in match[6]:
			continue
		elif tipostatus=="premiere" and "airing" not in match[6]:
			continue

		titulo = match[1]
		titulo = formattitle(titulo)

		url = "http://www.thefutoncritic.com"+match[0]

		broadcast = match[2]
		broadcast = re.sub('(?:\s+|<.*?>|\n)','',broadcast)
		broadcast = re.sub(r"(\d+)/(\d+)/(\d+)",lambda date: date.group(2)+"/"+date.group(1)+"/"+date.group(3),broadcast)
		broadcast = re.sub('-',' - ',broadcast)

		updated = match[3]
		matchup = re.match('(\d+)/(\d+)/(\d+)',updated)
		if (matchup):
			updated = matchup.group(2)+"/"+matchup.group(1)+"/"+matchup.group(3)

		premiere = "0"
		if "airing" in match[6]:
			matchpre=re.match('^(\d+)/(\d+)/(\d+)',broadcast)
			if (matchpre) and (matchup):
				if matchpre.group(3)==matchup.group(3) and int(matchup.group(1))-int(matchpre.group(2))<=3:
					premiere = "-1"
				elif int(matchpre.group(3))==int(matchup.group(3))-1 and int(matchup.group(1))+12-int(matchpre.group(2))<=3:
					premiere = "-1"
			if tipostatus=="premiere" and premiere=="0":
				continue

		network = match[4]
		network = re.sub('<.*?>','',network)
		network = re.sub('\s+',' ',network)

		timeslot = match[5]
		timeslot = re.sub('(?:<.*?>|\n)','',timeslot)
		timeslot = re.sub('\s+',' ',timeslot)
		timeslot = re.sub(r"^[A-Za-z].*?$",lambda tslot: tslot.group(0)[0].upper()+tslot.group(0)[1:],timeslot)

		status = match[6]
		status = re.sub('<.*?>','',status)
		status = re.sub('\s+',' ',status)

		typeupdate = "Last Updated"
		statusbroadcast=""
		if "canceled" in status:
			statusbroadcast="[Ended]"
		elif "hiatus" in status:
			statusbroadcast="[Current: Unknown at "+updated+"]"
		elif "airing" in status:
			if premiere=="0":
				airtxt = "Current"
			else:
				airtxt = "Premiere"
			matchday = re.match('(?:Mondays|Tuesdays|Wednesdays|Thursdays|Fridays|Saturdays|Sundays)',timeslot)
			if (matchday):
				day=" "+matchday.group(0)
			else:
				day=""
			statusbroadcast="["+airtxt+": Airing"+day+", next: "+updated+"]"
			typeupdate = "Next Broadcast"
		else:
			updated2=updated
			if updated2=="???":
				matchyear = re.search('\d{4}',status)
				if (matchyear):
					updated2=matchyear.group(0)+" or beyond"
				else:
					matchup = re.search('this\s[^\s]+',status)
					if (matchup):
						updated2=matchup.group(0).title()
			if "new" in status:
				statusbroadcast="[New: starts: "+updated2+"]"
				typeupdate = "Starts"
			elif "returning" in status:
				statusbroadcast="[Current: On break, returns: "+updated2+"]"
				typeupdate = "Returns"

		status = formattitle(status)

		titlefutonsearch = ftitlefuton(titulo,network)
		titlefutonsearch = ftitlefutonsearch(titlefutonsearch)

		listseries.append([ titulo , url , broadcast , network , timeslot , typeupdate , updated , status , statusbroadcast , titlefutonsearch ])

	return listseries

def findfutonstatus(serieslist,tipostatus):
	search = ""
	if tipostatus=="bbc" or tipostatus=="ended" or tipostatus=="foritem":
		search=serieslist[0][0]
	elif tipostatus=="noctv":
		search=serieslist[-1][2]

	statuslist = findfuton(search,"http://www.thefutoncritic.com/showatch.aspx?series=",tipostatus)
	if len(statuslist)==0:
		return serieslist

	if tipostatus=="noctv" or  tipostatus=="foritem":
		tipostatus="current"

	tptitlesearch = ""
	if tipostatus=="ended" or tipostatus=="varios":
		tptitlesearch = "varios"

	#check
	titleeztvbbc = "Being Human|Doctor Who|Kitchen Nightmares|Primeval|Skins|Top Gear|Torchwood"
	titlesearchbbc = "beinghumanuk|doctorwho2005|kitchennightmares|primeval|skins2008|topgear|torchwood|"

	OKBBC="0"
	for serie in serieslist:
		if serie[1]=="[Ended]" and tipostatus=="current":
			serie[4] = "ended"
			continue
		elif serie[-1]+"|" in titlesearchbbc and tipostatus=="current":
			if OKBBC=="0":
				statusBBC = findeztvstatus(titleeztvbbc)
				OKBBC="-1"
			for status in statusBBC:
				if serie[0]==status[0]:
					serie[1] = status[1]
					serie[4] = "bbc"
					break
			if serie[4]=="bbc":
				continue
		itemencontrado = searchgate(statuslist,serie[-1],"futon",tptitlesearch)
		if len(itemencontrado)==1:
			if "New" in itemencontrado[0][8] and tipostatus=="current":
				serie[1] = re.sub('New','Current/New US',itemencontrado[0][8])
			else:
				serie[1] = itemencontrado[0][8]
			serie[4] = itemencontrado[0][0]+";"+itemencontrado[0][1]+";"+itemencontrado[0][2]+";"+itemencontrado[0][3]+";"+itemencontrado[0][4]+";"+itemencontrado[0][5]+";"+itemencontrado[0][6]+";"+itemencontrado[0][7]+";"+serie[1]
		elif len(itemencontrado)>1:
			serie[4]="varios"

	if tipostatus=="bbc" or tipostatus=="ended" or tipostatus=="varios":
		if len(itemencontrado)>1:
			serieslist = itemencontrado

	return serieslist

def findeztvstatus(search):
	BBCstatus = []
	try:
		data = scrapertools.cachePage(EZURL)
	except:
		return BBCstatus

	patronvideos  = '<a href="[^"]+" class="thread_link">('+search+')</a></td>\n\s+'
	patronvideos += '<td class="forum_thread_post"><font class="[^"]+">(.*?)</font>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:		
		# Titulo
		titulo = match[0]		
		# Status
		status = match[1]
		match1 = re.search('\d{2}(\d{2})-(\d{2})-(\d{2})',status,re.IGNORECASE)
		if (match1):
			day = int(match1.group(3))+1
			month = int(match1.group(2))
			year = int(match1.group(1))
			if day>31:
				day = 1
				if month<12:
					month = month+1
				else:
					month = 1
					year = year+1
			elif day>28 and month==2:
				day = 1
				month=3
			elif day>30:
				if month==4 or month==6 or month==9 or month==11:
					day = 1
					month = month+1				
			mydate = str(day)+"/"+str(month)+"/"+str(year)
			status = re.sub('\d{4}-\d{2}-\d{2}',mydate,status)
		status = re.sub('(?:<b>|</b>)','',status)
		if status=="Pending":
			status = "On break, returns: ???"
		if status<>"Ended":
			status = "Current: "+status
		status = "["+status+"]"

		BBCstatus.append([ titulo , status ])

	return BBCstatus

def listinfofuton(params,url,category):
	plot = ""
	if params.has_key("plot"):
		plot = urllib.unquote_plus( params.get("plot") )
	datafuton = category
	category = "The Futon Critic"
	tipostatus = ""
	statusS = ""
	statustitle = ""

	matchinfo2=re.match('^([^;]*);([^;]*);([^;]*);([^;]*);([^;]*)$',datafuton)
	if (matchinfo2):
		tipostatus=matchinfo2.group(1)
		titleS=matchinfo2.group(2)
		urlS=matchinfo2.group(3)
		statusS=matchinfo2.group(4)
		titlesearch=matchinfo2.group(5)
		if tipostatus=="bbc":
			search = titleS
			search = re.sub('[\\\\]?(?P<signo>[^\w\s\\\\])','\\\\\g<signo>',search)
		else:
			iniciosearch,titlesearch = findtsearch(titleS,urlS)
			search = iniciosearch
		serieslist=[ [ search , "" , "" , "" , "" , titlesearch ] ]
		serieslist=findfutonstatus(serieslist,tipostatus)
		i = len(serieslist)
		if i>1:
			alertvariossearch(i)
			searchfutonlist(category,serieslist)
			return
		elif i==1 and serieslist[0][4]=="":
			alertnoresultadosearch()
			return
		datafuton = serieslist[0][4]

	matchinfo=re.match('^([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*)$',datafuton)
	titulo=matchinfo.group(1)
	urlf=matchinfo.group(2)
	broadcast=matchinfo.group(3)
	network=matchinfo.group(4)
	timeslot=matchinfo.group(5)
	typeupdate=matchinfo.group(6)
	updated=matchinfo.group(7)
	status=matchinfo.group(8)
	statusbroadcast=matchinfo.group(9)

	if "thefutoncritic" in url:
		titulofuton = ftitlefuton(titulo,network)
		iniciosearch,titlesearch = findtsearch(titulofuton,urlf)
		titlesearchbbc = "beinghumanuk|doctorwho2005|kitchennightmares|primeval|skins2008|topgear|torchwood|"
		if titlesearch+"|" in titlesearchbbc:
			tipostatus = "bbc"
			statusBBC = findeztvstatus(titulo)
			if len(statusBBC)==1:
				if "beyond" in status and "???" in statusBBC[0][1]:
					pass
				else:
					statusS = statusBBC[0][1]
		tituloserie = urlserie = ""
		miseriectv,urlctv = findcasttv("CheckFav",iniciosearch,titlesearch,"futon","")
		if urlctv<>"":
			tituloserie = miseriectv
			urlserie = urlctv
		else:
			miseriesy,urlsy = findseriesyonkis("","CheckFav",titlesearch,"futon")
			if urlsy<>"":
				tituloserie = miseriesy
				urlserie = urlsy

	if "Current/New" in statusbroadcast:
		statustitle="no US"
		statusS = "Current"

	if tipostatus=="bbc" and statusS<>"":
		statustitle="BBC UK"

	titulo = titulo.upper()
	futoninfo = findfutoninfo(urlf)
	if plot=="":
		plot = titulo+": Network: "+network+". Broadcast History: "+broadcast+". Status: "+status+". "+typeupdate+": "+updated+". Time Slot: "+timeslot
	plot = plot+futoninfo[6]

	additem( CHANNELNAME , category , titulo , "" , "" , plot )
	additem( CHANNELNAME , category , "Network: "+network , "" , "" , plot )
	additem( CHANNELNAME , category , "Broadcast History (Date Start/End): "+broadcast , "" , "" , plot )
	additem( CHANNELNAME , category , "Status: "+status , "" , "" , plot )
	if statustitle<>"":
		statusST = re.sub('(?:\[|\])','',statusS)
		additem( CHANNELNAME , category , "Status "+statustitle+": "+statusST , "" , "" , plot )
	additem( CHANNELNAME , category , typeupdate+": "+updated , "" , "" , plot )
	additem( CHANNELNAME , category , "Time Slot: "+timeslot , "" , "" , plot )
	if futoninfo[0]<>"":	
		additem( CHANNELNAME , category , futoninfo[0]+": "+futoninfo[1] , "" , "" , plot )
	if futoninfo[2]<>"":
		additem( CHANNELNAME , category , "Additional Notes: "+futoninfo[2] , "" , "" , plot )
	if futoninfo[4]<>"":
		additem( CHANNELNAME , category , "Genre: "+futoninfo[4] , "" , "" , plot )
	if futoninfo[5]<>"":
		additem( CHANNELNAME , category , "Studio Information: "+futoninfo[5] , "" , "" , plot )
	if futoninfo[3]<>"":
		additem( CHANNELNAME , category , "Description: "+futoninfo[3] , "" , "" , plot )

	additem( CHANNELNAME , category , "Episodios:" , "" , "" , "" )

	if "thefutoncritic" in url:
		if tituloserie<>"":
			if tipostatus=="bbc":
				folderstatus = statusS
			else:
				folderstatus = statusbroadcast
			foldertitle = tituloserie+"  -  "+folderstatus
			addseriefolder( CHANNELNAME , "listados" , category+";"+tituloserie+";"+folderstatus+";"+datafuton , foldertitle , urlserie , "" , plot , "" , "" )
		else:
			addsimplefolder( CHANNELNAME , "search" , category , "Buscar Serie" , "" , "" )
	elif "casttv" in url or "seriesyonkis" in url:
		title = urllib.unquote_plus( params.get("title") )
		categoryback = urllib.unquote_plus( params.get("category") )
		thumbnail = urllib.unquote_plus( params.get("thumbnail") )
		if params.has_key("dataweb"):
			serievistos = urllib.unquote_plus( params.get("serievistos") )
			dataweb = urllib.unquote_plus( params.get("dataweb") )
			categoryback = "Futon"+categoryback
		else:
			serievistos = ""
			dataweb = ""
			categoryback = re.sub('^(\d+);([^;]*);([^;]*);','',categoryback)
			categoryback = "Futon;"+categoryback
		addseriefolder( CHANNELNAME , "listados" , categoryback , title , url , "" , plot , serievistos , dataweb )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def findfutoninfo(url):
	try:
		data = scrapertools.cachePage(url)
	except:
		info = [ "" , "" , "" , "" , "" , "" , "" ]
		return info

	tseasons = seasons = plotseasons = ""
	match1 = re.search('<td>(CURRENT SEASON|SEASON\(S\)):<br>([^<]+)</td>',data,re.IGNORECASE)
	if (match1):
		seasons = match1.group(2)
		tseasons = match1.group(1)
		if tseasons=="CURRENT SEASON":
			tseasons = tseasons.title()
		else:
			tseasons = tseasons.capitalize()
		plotseasons = ". "+tseasons+": "+seasons

	notes = plotnotes = ""
	match2 = re.search('<td>ADDITIONAL NOTES:<br>([^<]+)</td>',data,re.IGNORECASE)
	if (match2):
		notes = match2.group(1)
		notes = re.sub(r"(\d+)/(\d+)/(\d+)",lambda date: date.group(2)+"/"+date.group(1)+"/"+date.group(3),notes)
		plotnotes = ". Additional Notes: "+notes

	description = plotdesc = ""
	match3 = re.search('<td>DESCRIPTION:<br>([^<]+)</td>',data,re.IGNORECASE)
	if (match3):
		description = match3.group(1)
		plotdesc = ". Description: "+description

	genre = plotgenre = ""
	match4 = re.search('<td>GENRE\(S\):<br>(.*?)\s+</td>',data,re.DOTALL)
	if (match4):
		genre = match4.group(1)
		genre = re.sub('\n','',genre)
		genre = re.sub('&middot;','',genre)
		genre = re.sub('<br>','.',genre)
		genre = genre.title()
		plotgenre = ". Genre: "+genre

	studio = plotstudio = ""
	match5 = re.search('<td>STUDIO INFORMATION:<br>(.*?)\s+</td>',data,re.DOTALL)
	if (match5):
		studio = match5.group(1)
		studio = re.sub('\n','',studio)
		studio = re.sub('&middot;','',studio)
		studio = re.sub('<br>','.',studio)
		plotstudio = ". Studio Information: "+studio+"."

	plot = plotseasons+plotnotes+plotdesc+plotgenre+plotstudio

	info = [ tseasons , seasons , notes , description , genre , studio , plot ]

	return info

def listadonuevos(params,url,category):
	listadonvosupdate(category,False)

def listadonvosupdate(category,listupdate):
	animenuevos=[]
	tipo = 2

	if "Todos" in category:
		animenuevos = animeforos.findlistadonvos(category)
		tipo = 4

	nuevos = findlistadonvos()

	if len(nuevos)==0 and len(animenuevos)==0:
		alertnoepisodios(tipo)

	if tipo==4 and len(nuevos)>0:
		additem( CHANNELNAME , category , "----------------------------- CASTTV - SERIESYONKIS -----------------------------" , "" , "" , "" )
	for item in nuevos:
		addnewfolder( CHANNELNAME , "episodiomenu" , category , item[0] , item[1] , item[2] , item[3] , item[4] , item[5] , item[6] , item[7] , item[8] , item[9] , item[10] , ";" , "New" )

	if len(animenuevos)>0:
		additem( CHANNELNAME , category , "------------------------------------ ANIME - FOROS ------------------------------------" , "" , "" , "" )
		for item in animenuevos:
			animeforos.addvideofolder( CHANNELNAME , "animeforos.episodiomenu" , item[0] , item[1] , item[2] , item[3] , "" , "" )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",listupdate,True)
	# ------------------------------------------------------------------------------------

def findlistadonvos():
	listafav = readfav("","","-1|-2",CHANNELNAME)
	nuevos = []

	for serie in listafav:
		serievistos,listanuevos=findnuevos(serie[0],serie[2],"-1")
		if len(listanuevos)>0:
			listanuevos.reverse()
			n=0
			for episodio in listanuevos:
				if episodio[3] == "0":
					nuevos.append([ episodio[0] , episodio[1] , episodio[9] , episodio[10] , episodio[2] , episodio[4] , episodio[5] , episodio[6] , serievistos , episodio[8] , episodio[7] ])
					n=n+1
					if serie[3]=="-2" and n==3:
						break
	return nuevos

def detaildos(params,url,category):
	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	date = urllib.unquote_plus( params.get("date") )
	dataweb = urllib.unquote_plus( params.get("dataweb") )
	seasontvid = urllib.unquote_plus( params.get("seasontvid") )
	seasontv = urllib.unquote_plus( params.get("seasontv") )
	web = urllib.unquote_plus( params.get("web") )
	episodiotv = params.get("episodiotv")
	episodiotv = int(episodiotv)
	matchwebs=re.match('^([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*)$',dataweb)
	iniciosearch=matchwebs.group(1)
	titlesearch=matchwebs.group(2)
	miseriesy=matchwebs.group(3)
	urlsy=matchwebs.group(4)
	miseriectv=matchwebs.group(5)
	urlctv=matchwebs.group(6)

	titleshort = title
	if date<>"":
		titleshort = re.sub('\s\-\s\d+\/\d+\/\d+','',titleshort)
	titleshort = re.sub('\s\-\s(?:ES|LT)','',titleshort)
	titleshort = re.sub('\s+\-\s+',' - ',titleshort)
	visto = ""
	matchv = re.search('\[(?:LW|NW|UW|W)\]',titleshort)
	if (matchv):
		visto = " - "+matchv.group(0)
	
	listacasttv = []
	listactmirrors = []
	listasubtitulos = []
	listatv = []
	listasy = []
	miseriesub = ""

	# CastTV
	if url<>"":
		listacasttv,listactmirrors = findvideoscasttv(url)
		
	# Si el episodio tiene dato de temporada se busca en SeriesYonkis
	if seasontvid<>"0":
		#if "-tv-" in web:
		#	params = {'Serie': miserietv}
		#	listatv = findtvep(params,urltv,"","0",seasontvid,episodiotv)
		if "sy" in web:
			listasy,thumbnailsy,plotsy = findsyep(urlsy,"0",seasontvid,episodiotv)
			if thumbnail=="":
				thumbnail = thumbnailsy
				plot = plotsy

	if len(listacasttv)==0 and len(listatv)==0 and len(listasy)==0:
		alertnovideo()
		return

	# Si el episodio tiene dato de temporada se busca en Subtítulos.es
	if seasontvid<>"0":
		miseriesub,urlsub,miep,listasubtitulos = findsubseries(iniciosearch,"V",titlesearch,seasontvid,episodiotv)

	additem( CHANNELNAME , category , "VIDEOS :" , "" , "" , "" )
	if "Nuevos" in category:
		if urlctv<>"":
			tituloserie = miseriectv
			urlserie = urlctv
		else:
			tituloserie = miseriesy
			urlserie = urlsy
		#pasar a función = listasubs
		serielist = [ [ iniciosearch , "" , "" , "" , "" , titlesearch ] ]
		serielist = findfutonstatus(serielist,"foritem")
		statusfuton = serielist[0][1]
		datafuton = serielist[0][4]
		network = ""
		if datafuton=="ended" or datafuton=="bbc" or datafuton=="varios":
			if datafuton=="bbc":
				network=" (BBC)"
			datafuton = datafuton+";"+tituloserie+";"+urlserie+";"+statusfuton+";"+serielist[0][5]
		elif datafuton<>"":
			matchnet=re.match('^[^;]*;[^;]*;[^;]*;([^;]+);',datafuton)
			if (matchnet):
				network=" ("+matchnet.group(1)+")"

		foldertitle = tituloserie+network+"  -  "+statusfuton
		foldertitle = re.sub('\s+\-\s+$','',foldertitle)
			
		addseriefolder( CHANNELNAME , "listados" , "Series VO - Consulta - ;"+tituloserie+";"+statusfuton+";"+datafuton , foldertitle , urlserie , "" , "" , "" , "" )
	# ------------------------------------------------------------------------------------
	# Añade los enlaces a los videos
	# ------------------------------------------------------------------------------------
	for video in listacasttv:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - [CastTV]" , video[1] , thumbnail , plot )
	for video in listactmirrors:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , titleshort+" - "+video[0]+" - Mirror - [CastTV]" , video[1] , thumbnail , plot )
	#for ep in listatv:
	#	#quita la fecha (como arriba, para acortar)
	#	titletv = re.sub('\s+\([^\)]+\)$','',ep['title'])
	#	xbmctools.addnewvideo( CHANNELNAME , "" , category , "" , titletv+visto+" - [TV]" , ep['url'] , thumbnail , plot , Serie=miserietv )
	for ep in listasy:
		xbmctools.addnewvideo( CHANNELNAME , "seriesyonkis.detail" , category , "Megavideo" , ep[0]+ep[2]+visto+" - [SeriesYonkis]" , ep[1] , thumbnail , plot , Serie=miseriesy )

	# ------------------------------------------------------------------------------------
	# Añade los enlaces a los Subtítulos
	# ------------------------------------------------------------------------------------
	if len(listasubtitulos)>0:
		additem( CHANNELNAME , category , "SUBTITULOS - [Descargar] :" , "" , "" , "" )
		addsimplefolder( CHANNELNAME , "listasubep" , "Series VO - Subtítulos.es - "+miseriesub , miseriesub+"  -  [Subtítulos]" , urlsub , "" )
		additem( CHANNELNAME , category , miep , "" , "" , "" )
		for subs in listasubtitulos:
			addsimplefolder( CHANNELNAME , "subtitulo" , subs[4] , subs[0]+" ("+subs[1]+") - ["+subs[2]+"] ("+subs[5]+" descargas)" , subs[3] , DESCARGAS_THUMB )
	else:
		if miseriesub<>"":
			addsimplefolder( CHANNELNAME , "searchsub" , "Series VO - Subtítulos.es" , "SUBTITULOS - [Descargar] :" , "" , "" )
			addsimplefolder( CHANNELNAME , "listasubep" , "Series VO - Subtítulos.es - "+miseriesub , miseriesub+"  -  [Subtítulos]" , urlsub , "" )
		else:
			addsimplefolder( CHANNELNAME , "searchsub" , "Series VO - Subtítulos.es" , "Buscar Subtítulos" , "" , "" )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def findvideoscasttv(url):
	listacasttv = []
	listactmirrors = []	
	try:
		data = scrapertools.cachePage(url)
	except:
		alertservidor(url)
		return listacasttv,listactmirrors

	# tipo 1: Megavideo es el tipo de reproducción
	listacasttv = servertools.findvideos(data)
		
	# tipo 2: Megavideo no es el tipo de reproducción
	if len(listacasttv)==0:
		# obtiene la url de la página para reproducir con Megavideo si existe	
		match = re.search('<a class="source_row" href="(.*?)"> <img alt="MegaVideo"',data,re.IGNORECASE)
		if (match):
			data2 = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match.group(1)))
			listacasttv = servertools.findvideos(data2)				
			data = data2

	if len(listacasttv)>0:	
		# obtiene la url de la página para reproducir con Megavideo del mirror si existe	
		match1 = re.search('<a class="source_copies" href="(.*?)">COPY 2',data,re.IGNORECASE)
		if (match1):
			data2 = scrapertools.cachePage(urlparse.urljoin("http://www.casttv.com",match1.group(1)))
			listactmirrors = servertools.findvideos(data2)

	return listacasttv,listactmirrors

def play(params,url,category):
	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def serieupdate(miserievo,status,url,tipocontenido,channel):
	urlsearch0 = ""
	if channel=="animeforos":
		urlsearch0=url
	seriefav = ""
	dataweb = ""
	serievistos = ""

	listfav=readfav(miserievo,urlsearch0,"",channel)

	if channel=="casttv":
		if len(listfav)==0:
			seriertdo,urlrtdo,serievistos,dataweb,listfav=checkvistosfav(miserievo,url,"fav")
			if len(listfav)>0 and seriertdo<>miserievo:
				miserievo = seriertdo
				seriefav = seriertdo
				url = urlrtdo
		elif listfav[0][3]=="1":
			serievistos,dataweb=checkvistosfav(miserievo,url,"datafav")

	if len(listfav)==0:
		respuesta = seriemenu("0","0",tipocontenido,seriefav,channel)
		if respuesta==1:
			upgradefav(miserievo,status,url,"-2","1",channel)
	else:
		if listfav[0][3]=="-1":
			respuesta = seriemenu("-1","-1",tipocontenido,seriefav,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"1","1",channel)
			elif respuesta==3:
				upgradefav(miserievo,status,url,"0","1",channel)
			elif respuesta==4:
				upgradefav(miserievo,status,url,"-2","1",channel)
		elif listfav[0][3]=="-2":
			respuesta = seriemenu("-1","-2",tipocontenido,seriefav,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"1","1",channel)
			elif respuesta==3:
				upgradefav(miserievo,status,url,"0","1",channel)
			elif respuesta==4:
				upgradefav(miserievo,status,url,"-1","1",channel)
		elif listfav[0][3]=="0":
			respuesta = seriemenu("-1","0",tipocontenido,seriefav,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"1","1",channel)
			elif respuesta==3:
				upgradefav(miserievo,status,url,"-2","1",channel)
		elif listfav[0][3]=="1":
			respuesta = seriemenu("-1","1",tipocontenido,seriefav,channel)
			if respuesta==2:
				upgradefav(miserievo,status,url,"-2","1",channel)
		if respuesta==1:
				upgradefav(miserievo,status,url,"","0",channel)
	if channel=="casttv":
		return serievistos,dataweb,respuesta
	else:
		return respuesta

def seriemenu(tipofav,tiponuevos,tipocontenido,seriefav,channel):
	misfavtext="Mis Favoritas"
	anexofavtext=""
	if channel=="animeforos":
		misfavtext="Mis Favoritos"
	if seriefav<>"":
		anexofavtext="  ("+seriefav+")"

	tipocontext=" Listado de Episodios "
	if tipocontenido<>"" and tipocontenido.lower()<>"serie" and tipocontenido<>"NoFuton":
		tipocontext=""

	seleccion = ""
	opciones = []
	opciones.append("Abrir"+tipocontext+" (opción por defecto)")
	if channel=="casttv" and tipocontenido<>"NoFuton":
		opciones.append('Abrir Ficha en "The Futon Critic"')
	if tipofav=="0":
		opciones.append('Añadir a "'+misfavtext+'"'+anexofavtext)
	elif tipofav=="-1":
		opciones.append('Eliminar de "'+misfavtext+'"'+anexofavtext)
		if tiponuevos=="1":
			opciones.append('Activar en "'+misfavtext+'"'+anexofavtext)
		else:
			opciones.append('Desactivar en "'+misfavtext+'"'+anexofavtext)
			if tiponuevos=="0":
				opciones.append('Activar Seguimiento en "Nuevos Episodios"')
			else:
				opciones.append('Desactivar Seguimiento en "Nuevos Episodios"')
				if tiponuevos=="-1":
					opciones.append('Activar Límite de 3 episodios en "Nuevos Episodios"')
				elif tiponuevos=="-2":
					opciones.append('Desactivar Límite de 3 episodios en "Nuevos Episodios"')

	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Seleccione una opción:", opciones)

	if channel=="casttv" and tipocontenido<>"NoFuton":
		if seleccion==1:
			seleccion="Futon"
		elif seleccion>1:
			seleccion= seleccion-1

	return seleccion

def episodiomenu(params,url,category):
	title = urllib.unquote_plus( params.get("title") )
	tipovisto = urllib.unquote_plus( params.get("tipovisto") )
	serievistos = urllib.unquote_plus( params.get("serievistos") )
	databack = urllib.unquote_plus( params.get("databack") )
	season = urllib.unquote_plus( params.get("seasontvid") )
	episodio = params.get("episodiotv")
	dataweb = urllib.unquote_plus( params.get("dataweb") )
	matchdataback=re.match('([^;]*);([^;]*)$',databack)
	serieback= matchdataback.group(1)
	urlback= matchdataback.group(2)

	if "Consulta" in category:
		detaildos(params,url,category)
	else:
		episodiomenugnral(params,title,url,category,serievistos,serieback,urlback,season,episodio,dataweb,tipovisto,CHANNELNAME,"-1")

def episodiomenugnral(params,title,url,category,serievistos,serieback,urlback,season,episodio,dataweb,tipovisto,channel,urlOK):
	title0 = re.sub('\s+\-\s+\[U?L?N?W\]$','',title)
	title0 = re.sub('\s\-\s(?:ES|LT)$','',title0)

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

		upgradevisto(serievistos,title0,url,season,episodio,accion,channel,urlOK)

	if channel=="animeforos":
		return seleccion

	if tipovisto=="New":
		listadonvosupdate(category,True)
	else:
		listadosupdate(serieback,urlback,category,serievistos,dataweb,True)

def readfav(seriesearch0,urlsearch0,tiponuevos,channel):
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
	#el status se podría quitar, se guarda sólo por mantener el formato...
	favlist = []
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
	if serie<>"":	
		seriesearch = re.sub('(?P<signo>\(|\)|\'|\"|\[|\]|\.|\?|\+)','\\\\\g<signo>',serie)
	else:
		seriesearch="[^;]+"

	if tipo=="LW":
		tipos="(?:1|2|4)"
	else:
		tipos="[^;]+"
	
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
	#urlOK añadido para Mcanime en Anime(Foros) por los enlaces genéricos sin títulos...  
	#urlOK indica si se usa la url ("0") o no ("-1") para identificar los episodios vistos 
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
			diferenteOK = "-1"
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
					elif channel=="casttv":
						if urlf=="" or url=="":
							#posible caso de un visto de otra web que es añadido a CastTV o CastTV caido
							if episodiof==episodio and episodiof<>"0" and seasonf==season and seasonf<>"0":
								diferenteOK = "0"
				else: 
					if titulof==titulo and urlf==url:
						diferenteOK = "0"
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

def subtitulo(params,url,category):
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
		
	match = re.match('([^;]+);([^;]+)$',titulosub)
	titulo1 = match.group(1)
	titulo2 = match.group(2)

	filename = titulo1+titulo2+'.srt'
	fullfilename = os.path.join(SUB_PATH,filename)

	#OKuser = "0"
	if os.path.exists(fullfilename):
		#quito por ahora la posibilidad de sobreescribir
		#respuesta = alerttituloarchivo(filename)
		#if respuesta:
		#	OKuser = "-1"
		#else:

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

	# mensaje de confirmación para mostrar la ruta
	#if OKuser=="0":
	respuesta = alertdescarga(filename)
	if respuesta:
		pass 
	else:
		return

	try:
		downloadtools.downloadfileGzipped(url,fullfilename)
	except:
		return

	Dialogfin = xbmcgui.DialogProgress()
	resultado = Dialogfin.create('pelisalacarta' , 'El Subtítulo descargado se activará' , 'automáticamente en la próxima reproducción' )
	if os.path.exists(fullfilename): # Añadido por bandavi
		from shutil import copy2
		copy2(fullfilename,SUBTEMP_PATH)
		config.setSetting("subtitulo", "true")
	Dialogfin.close()

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

def alertnovideo():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Vídeo no disponible' , 'No se ha añadido aún a ninguna de las webs' , 'un enlace compatible.')

def alertnoepisodios(tipo):
	advertencia = xbmcgui.Dialog()
	if tipo==1:
		resultado = advertencia.ok('Episodios no disponibles' , 'No se han encontrado episodios gratuitos.' , '')
	elif tipo==2:
		resultado = advertencia.ok('pelisalacarta' , 'No se han encontrado Nuevos Episodios.' , '')
	elif tipo==3:
		resultado = advertencia.ok('pelisalacarta' , 'No se han encontrado Subtítulos.' , '')
	elif tipo==4:
		resultado = advertencia.ok('pelisalacarta' , 'No se han encontrado Nuevos Contenidos.' , '')

def alertservidor(url):
	advertencia = xbmcgui.Dialog()
	linea2="en este momento."
	if url<>"":
		linea2=url
	resultado = advertencia.ok('pelisalacarta' , 'Servidor o Contenido no disponible' , linea2 )

def alertnoresultadosearch():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('pelisalacarta' , 'La Búsqueda no ha obtenido Resultados.' , '')

def alertvariossearch(nitems):
	advertencia = xbmcgui.Dialog()
	itemstxt=""
	line2=""
	if nitems==10:
		itemstxt='al menos '
		line2='(se muestran sólo los 10 primeros)'
	resultado = advertencia.ok('pelisalacarta' , 'La Búsqueda ha obtenido '+itemstxt+str(nitems)+' Resultados.' , line2 )

def alertnofav():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('CastTV' , 'No se han añadido Series a "Mis Favoritas".' , '')

def addfolder( canal , accion , category , title , url , thumbnail, plot ):
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addsimplefolder( canal , accion , category , title , url , thumbnail ):
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addseriefolder( canal , accion , category , title , url , thumbnail , plot , serievistos , dataweb ):
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( type="Video", infoLabels={ "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&serievistos=%s&dataweb=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( serievistos ) , urllib.quote_plus( dataweb ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , date , dataweb , seasontvid , seasontv , serievistos , web , episodiotv , databack , tipovisto ):
	listitem= xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( type="Video", infoLabels={ "Title" : title, "Plot" : plot, "Date" : date } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&date=%s&dataweb=%s&seasontvid=%s&seasontv=%s&serievistos=%s&web=%s&episodiotv=%s&databack=%s&tipovisto=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( date ) , urllib.quote_plus( dataweb ) , urllib.quote_plus( seasontvid ) , urllib.quote_plus( seasontv ) , urllib.quote_plus( serievistos ) , urllib.quote_plus( web ) , episodiotv , urllib.quote_plus( databack ) , urllib.quote_plus( tipovisto ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def additem( canal , category , title , url , thumbnail, plot ):
	listitem = xbmcgui.ListItem( title, iconImage=HD_THUMB, thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def ayuda(params,url,category):
	info1 = "Canal [excepto Aptdo Mis Favoritas]: Para conocer el status de Favorita de una serie, compruebe el menú que se muestra al abrir la carpeta correspondiente. El icono de los listados puede no indicar el status correcto, porque se busca únicamente por el literal del título para no ralentizar. El menú de Serie si indicará el status real, conforme a las variantes de títulos recogidas, hasta el momento, en el canal."
	info2 = "Series VO - Buscar - Teclado: búsqueda alternativa en CastTV y SeriesYonkis (hasta encontrar resultados)."
	info3 = "Premiere: Estreno de los últimos tres meses"
	additem( CHANNELNAME , category , "--------------------------------------------- Info ----------------------------------------------" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , info1 , "" , HELP_THUMB , info1 )
	additem( CHANNELNAME , category , info2 , "" , "http://www.mimediacenter.info/xbmc/pelisalacarta/posters/buscador.png" , info2 )
	additem( CHANNELNAME , category , info3 , "" , HELP_THUMB , info3 )
	additem( CHANNELNAME , category , "------------------------------------------ Leyenda ------------------------------------------" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[LW]: Último Episodio Visto [Last Watched]" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[W]: Episodio Visto [Watched]" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[UW]: Episodio No Visto [UnWatched]" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "[NW]: No para Ver [Not to Watch] (excluido de Nvos Episodios)" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "ES/LT: Existe enlace de vídeo con Audio Español/Latino" , "" , HELP_THUMB , "" )
	additem( CHANNELNAME , category , "Series Actualizadas [excepto Aptdo Actualizaciones]" , "" , FOLDERBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "Series Favoritas" , "" , STARORANGE_THUMB , "" )
	additem( CHANNELNAME , category , "(1) Favoritas Actualizadas [excepto Aptdo Actualizaciones]" , "" , STARBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "(2) Favoritas con Nuevos Episodios [Aptdo Mis Favoritas]" , "" , STARGREEN_THUMB , "" )
	additem( CHANNELNAME , category , "(1) y (2) - [Aptdo Mis Favoritas]" , "" , STARGB_THUMB , "" )
	additem( CHANNELNAME , category , "Series Favoritas Desactivadas", "" , STARGREY_THUMB , "" )
	additem( CHANNELNAME , category , "Desactivadas Actualizadas - [excepto Aptdo Actualizaciones]" , "" , STARGREYBLUE_THUMB , "" )
	additem( CHANNELNAME , category , "Nuevos Episodios (posteriores a [LW]) [Aptdo Mis Favoritas]" , "" , STARGREEN2_THUMB , "" )
	additem( CHANNELNAME , category , "Subtítulo - [Descargar]" , "" , DESCARGAS_THUMB , "" )
	additem( CHANNELNAME , category , "Mensaje o Encabezado (sin acción)" , "" , HD_THUMB , "" )
	# ------------------------------------------------------------------------------------
	EndDirectory(category,"",False,True)
	# ------------------------------------------------------------------------------------

def ftitlectvsearch(title):
	title = re.sub('^All In$','(Korean) All In',title)
	title = re.sub('^Being Human$','Being Human (UK)',title)
	title = re.sub('^Crash$','Crash (US)',title)
	title = re.sub('^Doctor Who$','Doctor Who 2005',title)
	title = re.sub('^Hawaii Five.*?$','Hawaii Five0',title)
	title = re.sub('^Hell\'s Kitchen$','Hells Kitchen (US)',title)
	title = re.sub('^Heroes$','Heroes (USA)',title)
	title = re.sub('^House$','House MD',title)
	title = re.sub('^Law \& Order$','Law & Order (1990)',title)
	title = re.sub('^Life$','Life (USA)',title)
	title = re.sub('^Life on Mars$','Life on Mars (USA)',title)
	title = re.sub('^Lost$','Lost (2004)',title)
	title = re.sub('^Skins$','Skins (2008)',title)
	title = re.sub('^Survivor$','Survivor (Reality Show)',title)
	title = re.sub('^Swords: Lives on the Line$','Swords: Life on the Line',title)
	title = re.sub('^The Beast$','The Beast (2009)',title)
	title = re.sub('^The City','City (2008)',title)
	title = re.sub('^The Legend$','The Legend (MBC)',title)
	title = re.sub('^The Office$','The Office (US)',title)
	title = re.sub('^The Prisoner$','The Prisoner (1967)',title)
	title = title.lower()
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def ftitlesubsearch(title):
	title = re.sub('^Alice$','Alice (BR)',title)
	title = re.sub('^Being Human$','Being Human (UK)',title)
	title = re.sub('^Crash$','Crash (US)',title)
	title = re.sub('^Heroes$','Heroes (USA)',title)
	title = re.sub('^jonas$','Jonas LA',title)
	title = re.sub('^Krod Mandoon$','Kröd Mändoon',title)
	title = re.sub('^Law \& Order$','Law & Order (1990)',title)
	title = re.sub('^Life$','Life (USA)',title)
	title = re.sub('^Life 2009$','Life (UK)',title)
	title = re.sub('^Life on Mars$','Life on Mars (UK)',title)
	title = re.sub('^Lost$','Lost (2004)',title)
	title = re.sub('^Roomates$','Roommates',title)
	title = re.sub('^Scrubs Interns$','Webisode Series Scrubs Interns',title)
	title = re.sub('^Shippuden$','Shippuuden',title)
	title = re.sub('^Skins$','Skins (2008)',title)
	title = re.sub('^Survivor$','Survivor (Reality Show)',title)
	title = re.sub('^The Beast$','The Beast (2009)',title)
	title = re.sub('^The Office$','The Office (US)',title)
	title = title.lower()
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def ftitletvsearch(title):
	title = re.sub('^ALF$','ALF (Alien Life Form)',title)
	title = re.sub('^Beast, The$','The Beast (2009)',title)
	title = re.sub('^Being Human$','Being Human (UK)',title)
	title = re.sub('^Crash$','Crash (US)',title)
	title = re.sub('^CSI\: Crime Scene Investigation$','CSI',title)
	title = re.sub('^Highlander\: The Raven$','The Raven Highlander',title)
	title = re.sub('^Heroes$','Heroes (USA)',title)
	title = re.sub('^House$','House MD',title)
	title = re.sub('^Knight Rider \(2008\)$','Knight Rider',title)
	title = re.sub('^Law \& Order\: Special Victims Unit$','Law & Order: SVU',title)
	title = re.sub('^Law \& Order$','Law & Order (1990)',title)
	title = re.sub('^Lost$','Lost (2004)',title)
	title = re.sub('^Life$','Life (USA)',title)
	title = re.sub('^Pok..mon$','Pokemon',title)
	title = re.sub('^Skins$','Skins (2008)',title)
	title = re.sub('^Survivor$','Survivor (Reality Show)',title)
	title = re.sub('^Survivors$','Survivors 70s',title)
	title = re.sub('^Office, The$','The Office (US)',title)
	title = title.lower()
	title = re.sub('[^\w]+the$','',title)
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def ftitlefutonsearch(title):
	title = title.lower()
	title = re.sub('^city, the','city (2008)',title)
	title = re.sub('^crash$','crash (us)',title)
	title = re.sub('^csi\: crime scene investigation$','csi',title)
	title = re.sub('^csi\: new york$','csi ny',title)
	title = re.sub('^doctor who$','doctor who 2005',title)
	title = re.sub('^hawaii five.*?$','hawaii five0',title)
	title = re.sub('^heroes$','heroes (usa)',title)
	title = re.sub('^hell\'s kitchen$','hells kitchen (us)',title)
	title = re.sub('^house$','house md',title)
	title = re.sub('^law \& order\: special victims unit$','law & order: svu',title)
	title = re.sub('^law \& order$','law & order (1990)',title)
	title = re.sub('^survivor$','survivor (reality show)',title)
	title = re.sub('^survivors$','survivors 2008',title)
	title = re.sub('^office, the$','the office (us)',title)
	title = re.sub('^v$','v (2009)',title)
	title = re.sub('[^\w]+the$','',title)
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('[^\w]+and[^\w]+','',title)
	title = re.sub('[^\w]+','',title)
	return title

def ftitlefuton(title,network):
	title = title.lower()
	if network=="ABC":
		title = re.sub('^life on mars$','life on mars (usa)',title)
		title = re.sub('^lost$','lost (2004)',title)
		title = re.sub('^beast, the$','beast (2001)',title)
	elif network=="A&E":
		title = re.sub('^beast, the$','beast (2009)',title)
	elif network=="BBC AMERICA":
		title = re.sub('^being human$','being human (uk)',title)
		title = re.sub('^life on mars$','life on mars (uk)',title)
		title = re.sub('^skins$','skins (2008)',title)
	elif network=="DISCOVERY":
		title = re.sub('^life$','life (uk)',title)
	elif network=="FOX":
		title = re.sub('^skin$','skin (2003)',title)
	elif network=="MTV":
		title = re.sub('^skins$','skins (mtv)',title)
	elif network=="NBC":
		title = re.sub('^life$','life (usa)',title)
		title = re.sub('^lost$','lost (2001)',title)
	elif network=="SYFY":
		title = re.sub('^being human$','being human (usa)',title)
	return title

def ftitlesysearch(title):
	inicial = title[0:1]
	inicial3 = title[0:3]
	#en los títulos de substitución no dejar los paréntesis porque en el caso de "SY" se comprueban
	#tres variantes: título completo sin paréntesis, fuera del paréntesis y dentro...
	#Ej. "Crash (US)" correspondería a "Crash" y "Crash (UK)" hay que dejar "Crash US" o "CrashUS"
	#si el título original tiene algún paréntesis para diferenciarlo de otra serie con un nombre parecido
	#tb podría ser necesario quitarlo por lo como V (2009)...
	if inicial=="A":
		title = re.sub('^A Dos Metros Bajo Tierra$','Six Feet Under',title)
		title = re.sub('^A Trav..s Del Tiempo$','Quantum Leap',title)
		title = re.sub('^Abducidos$','Taken',title)
		title = re.sub('^Al descubierto$','In Plain Sight',title)
		title = re.sub('^Alfred Hitchcock Presenta$','The Alfred Hitchcock Hour',title)
		title = re.sub('^Almac..n 13$','Warehouse 13',title)
		title = re.sub('^Alice \(2009\)$','Alice 2009',title)
		title = re.sub('^Anatom..a de Grey$','Greys Anatomy',title)
		title = re.sub('^Apocalipsis de Stephen King$','The Stand',title)
		title = re.sub('^Aquellos Maravillosos Años$','The Wonder Years',title)
		title = re.sub('^Aquellos Maravillosos 70$','That 70s Show',title)
		title = re.sub('^Asi somos$','As If',title)
	elif inicial=="B":
		title = re.sub('^Battlestar Galactica$','Battlestar Galactica 70s',title)
		title = re.sub('^Battlestar Galactica 2003$','Battlestar Galactica',title)
		title = re.sub('^Being Human$','Being Human UK',title)
		title = re.sub('^Beverly Hills, 90210$','90210',title)
		title = re.sub('^Buffy Cazavampiros$','Buffy the Vampire Slayer',title)
	elif inicial=="C":
		title = re.sub('^Caminando entre dinosaurios$','Walking with Dinosaurs',title)
		title = re.sub('^Caso Abierto$','Cold Case',title)
		title = re.sub('^Caso cerrado$','Waking the Dead',title)
		title = re.sub('^Cinco Hermanos$','Brothers & Sisters',title)
		title = re.sub('^Colgados en Filadelfia$','Its Always Sunny in Philadelphia',title)
		title = re.sub('^C..mo Conoc.. A Vuestra Madre$','How I Met Your Mother',title)
		title = re.sub('^Corrupci..n en Miami$','Miami Vice',title)
		title = re.sub('^Cosas de casa$','Family Matters',title)
		title = re.sub('^Cosas de Marcianos$','3rd Rock from the Sun',title)
		title = re.sub('^Crash$','Crash US',title)
		title = re.sub('^Crimenes Imperfectos$','Forensic Files',title)
		title = re.sub('^CSI Las Vegas$','CSI',title)
		title = re.sub('^CSI New York$','CSI NY',title)
		title = re.sub('^Cuentos Asombrosos$','Amazing Stories',title)
	elif inicial=="D":
		title = re.sub('^Dinast..a$','Dynasty',title)
		title = re.sub('^Dinosaurios$','Dinosaurs',title)
		title = re.sub('^Doble identidad$','Spooks',title)
		title = re.sub('^Doctor En Alaska$','Northern Exposure',title)
		title = re.sub('^Doctor Who$','Doctor Who 2005',title)
		title = re.sub('^Doctoras de Filadelfia$','Strong Medicine',title)
	elif inicial=="E":
		if inicial3=="El ":
			title = re.sub('^El abogado$','The Practice',title)
			title = re.sub('^El Ala Oeste de la Casa Blanca$','The West Wing',title)
			title = re.sub('^El club contra el crimen$','Womens murder club',title)
			title = re.sub('^El club de medianoche$','Are you afraid of the dark?',title)
			title = re.sub('^El color de la Magia$','The Colour of Magic',title)
			title = re.sub('^El d..cimo reino$','The 10th Kingdom',title)
			title = re.sub('^El equipo A$','The A-Team',title)
			title = re.sub('^El fin del mundo$','The End of the World',title)
			title = re.sub('^El Gran Heroe Americano$','The Greatest American Hero',title)
			title = re.sub('^El Halc..n Callejero$','Street Hawk',title)
			title = re.sub('^El Pr..ncipe De Bel Air$','The Fresh Prince of Bel-Air',title)
			title = re.sub('^El misterio de Salem\'s Lot$','Salems Lot',title)
			title = re.sub('^El t..nel del tiempo$','The Time Tunnel',title)
			title = re.sub('^El tri..ngulo de las bermudas$','The Triangle',title)
			title = re.sub('^El trueno azul$','Blue Thunder',title)
			title = re.sub('^El ..ltimo superviviente$','Man vs Wild',title)
			title = re.sub('^El Universo$','The Universe',title)
			title = re.sub('^El Universo Elegante \(la teor..a de las cuerdas\)$','The elegant Universe',title)
			title = re.sub('^El Valle secreto$','Secret Valley',title)
		else:
			title = re.sub('^Embrujada$','Bewitched ',title)
			title = re.sub('^Embrujadas$','Charmed',title)
			title = re.sub('^Entre Fantasmas$','Ghost Whisperer',title)
			title = re.sub('^Espacio\: 1999$','Space: 1999',title)
			title = re.sub('^Espartaco\: Sangre y arena$','Spartacus',title)
			title = re.sub('^Expediente X$','The X Files',title)
	elif inicial=="G":
		title = re.sub('^Guerra y Paz \(miniserie\)$','War and Peace',title)
	elif inicial=="H":
		title = re.sub('^Hasta que la muerte nos separe$','Til Death',title)
		title = re.sub('^Heroes$','Heroes USA',title)
		title = re.sub('^Hombre rico, hombre pobre$','Rich Man, Poor Man',title)
		title = re.sub('^Hospital Kingdom$','Kingdom Hospital',title)
		title = re.sub('^Hotel Dulce Hotel$','The Suite Life of Zack and Cody',title)
		title = re.sub('^House$','House MD',title)
	elif inicial=="I":
		title = re.sub('^Infelices para siempre$','Unhappily Ever After',title)
		title = re.sub('^Invasion Tierra$','Invasion Earth',title)	
	elif inicial=="J":
		title = re.sub('^Jonas$','Jonas Brothers',title)
		title = re.sub('^Juzgado de Guardia$','Night Court',title)
	elif inicial=="L":
		if inicial3=="La ":
			title = re.sub('^La Clave Da Vinci$','Da Vincis inquest',title)
			title = re.sub('^La dimensi..n desconocida$','The Twilight Zone',title)
			title = re.sub('^La doctora Quinn$','Dr Quinn, Medicine Woman',title)
			title = re.sub('^La Familia Monster$','The Munsters',title)
			title = re.sub('^La fuga de Logan$','Logans Run',title)
			title = re.sub('^La Habitacion Perdida$','The Lost Room',title)
			title = re.sub('^La Hora De Bill Cosby$','The Cosby Show',title)
			title = re.sub('^La inquilina de Wildfell Hall$','The Tenant of Wildfell Hall',title)
			title = re.sub('^La guerra en casa$','The War at Home',title)
			title = re.sub('^La joya de la Corona$','The Jewel in the Crown',title)
			title = re.sub('^La juez Amy$','Judging Amy',title)
			title = re.sub('^La Plantaci..n$','Cane',title)
			title = re.sub('^La t..a de Frankenstein$','Frankensteins tante',title)
			title = re.sub('^La Zona Muerta$','The Dead Zone',title)
		else:
			title = re.sub('^Ladr..n$','Thief',title)
			title = re.sub('^Las aventuras de Sherlock Holmes \(Jeremy Brett\)$','The Adventures of Sherlock Holmes',title)
			title = re.sub('^Las Aventuras del Joven Indiana Jones$','The Young Indiana Jones Chronicles',title)
			title = re.sub('^Las chicas de oro$','The Golden Girls',title)
			title = re.sub('^Ley y Orden: Acci..n Criminal$','Law & Order: Criminal Intent',title)
			title = re.sub('^Ley y Orden U\.V\.E.$','Law & Order: SVU',title)
			title = re.sub('^Lex$','Lex ES',title)
			title = re.sub('^Life$','Life USA',title)
			title = re.sub('^Life on Mars$','Life on Mars USA',title)
			title = re.sub('^Life on Mars \(UK\)$','Life on Mars UK',title)
			title = re.sub('^Loco por ti$','Mad About You',title)
			title = re.sub('^Locos por la ciencia$','Wicked Science',title)
			title = re.sub('^Londres\: Distrito criminal$','Law & Order: UK',title)
			title = re.sub('^Los 4400$','4400',title)
			title = re.sub('^Los Colby$','The Colby',title)
			title = re.sub('^Los Hijos De Dune$','Children of Dune',title)
			title = re.sub('^Los J..venes Jinetes$','The Young Riders',title)
			title = re.sub('^Los Magos de Waverly Place$','Wizards of Waverly Place',title)
			title = re.sub('^Los Soprano$','Sopranos',title)
			title = re.sub('^Lost \(Perdidos\)$','Lost 2004 (Perdidos)',title)
	elif inicial=="M":
		title = re.sub('^Matrimonio Con Hijos \(USA\)$','Married with Children',title)
		title = re.sub('^Me Llamo Earl$','My Name is Earl',title)
		title = re.sub('^Melrose Place 2\.0$','Melrose Place 2009',title)
		title = re.sub('^Mentes Criminales$','Criminal Minds',title)
		title = re.sub('^Mujeres Desesperadas$','Desperate Housewives',title)
	elif inicial=="N":
		title = re.sub('^Napole..n$','Napoleon',title)
		title = re.sub('^Navy\: investigacion criminal L\.A\.$','NCIS: Los Angeles',title)
		title = re.sub('^Navy\: Investigaci..n Criminal$','NCIS',title)
	elif inicial=="O":
		title = re.sub('^Orgullo y prejuicio$','Pride and Prejudice',title)
	elif inicial=="P":
		title = re.sub('^Padres Forzosos$','Full House',title)
		title = re.sub('^Policias de Nueva York$','NYPD Blue',title)
	elif inicial=="Q":
		title = re.sub('^Quark, la escoba espacial$','Quark',title)
	elif inicial=="R":
		title = re.sub('^Ra..ces$','Roots',title)
		title = re.sub('^Reglas de Compromiso$','Rules of Engagement',title)
		title = re.sub('^Retorno a Ed..n$','Return to Eden',title)
		title = re.sub('^Roma$' , 'Rome',title)
	elif inicial=="S":
		title = re.sub('^Sabrina\: La bruja adolescente$','Sabrina, the Teenage Witch 1996',title)
		title = re.sub('^Salvando a Grace$','Saving Grace',title)
		title = re.sub('^Salvados por la Campana\: Años de universidad$','Saved by the Bell: The College Years',title)
		title = re.sub('^Salvados por la Campana$','Saved by the Bell',title)
		title = re.sub('^Se ha escrito un crimen$','Murder, She Wrote',title)
		title = re.sub('^Seis Grados$','Six degrees',title)
		title = re.sub('^Sexo en Nueva York$','Sex and the City',title)
		title = re.sub('^Sin Rastro$','Without a Trace',title)
		title = re.sub('^Sin identificar \(The forgotten\)$','The Forgotten 2009',title)
		title = re.sub('^S.., Ministro$','Yes Minister',title)
		title = re.sub('^Skins$','Skins 2008',title)
		title = re.sub('^Star Trek\: La nueva Generacion$','Star Trek: The Next Generation',title)
		title = re.sub('^Superagente 86$','Get Smart',title)
		title = re.sub('^Survivors$','Survivors 2008',title)
	elif inicial=="T":
		title = re.sub('^Tan muertos como yo$','Dead Like Me',title)
		title = re.sub('^Todo El Mundo Odia A Chris$','Everybody Hates Chris',title)
		title = re.sub('^Todo es relativo$','Its all relative',title)
		title = re.sub('^Todos mis novios$','The Ex List',title)
		title = re.sub('^Treinta y tantos$','Thirtysomething',title)
		title = re.sub('^Triunfadores$','Big Shots',title)
		title = re.sub('^Turno de Guardia$','Third Watch',title)
		title = re.sub('^The Beast$','The Beast 2009',title)
		title = re.sub('^The Office$','The Office US',title)
		title = re.sub('^The Office \(UK\)$','The Office UK',title)
	elif inicial=="U":
		title = re.sub('^Un chapuzas en casa$','Home Improvement',title)
	elif inicial=="V":
		title = re.sub('^V \(2009\)$','V 2009',title)
		title = re.sub('^V Invasi..n Extraterrestre$','V 1983',title)
		title = re.sub('^Viaje al fondo del mar$','Voyage to the Bottom of the Sea',title)
		title = re.sub('^Vida secreta de una adolescente$','The Secret Life of the American Teenager',title)
		title = re.sub('^Viviendo con Derek$','Life with Derek',title)
		title = re.sub('^Vuelo 29\: Perdidos$','Flight 29 Down',title)
	elif inicial=="Y":
		title = re.sub('^Yo y el mundo$','Boy Meets World',title)
		title = re.sub('^Yo, Claudio$',' I Claudius',title)
	else:
		title = re.sub('^5 Dias para Morir$','5ive Days to Midnight',title)
		title = re.sub('^7 d..as$','7 Days',title)
		title = re.sub('^10 razones para odiarte$','10 Things I Hate About You',title)
	title = title.lower()
	title = re.sub('^the[^\w]+','',title)
	title = re.sub('\s+\(the\s+',' (',title)
	title = re.sub('[^\w]+(?:and|y)[^\w]+','',title)
	title = re.sub('[^\w\(\)]+','',title)
	return title

def formattitle(title):
	title = re.sub(r"[A-Za-z]+('[A-Za-z]+)?",lambda misub: misub.group(0)[0].upper()+misub.group(0)[1:].lower(),title)
	title = re.sub(r"\s\(?(?:At|And|A|By|In|Of|On|Or|That|These|The|This|Those|To)\s",lambda misub: misub.group(0).lower(),title)
	return title

def EndDirectory(category,sortmethod,listupdate,cachedisc):
	if sortmethod=="":
		sortmethod=xbmcplugin.SORT_METHOD_NONE
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=sortmethod)
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate , cacheToDisc=cachedisc  )