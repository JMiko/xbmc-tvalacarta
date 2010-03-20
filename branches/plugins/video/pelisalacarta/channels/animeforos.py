# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para "Anime (foros)"
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
import binascii
import xbmctools

CHANNELNAME = "animeforos"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[animeforos.py] init")

DEBUG = True

Generate = False # poner a true para generar listas de peliculas

LoadThumbnails = True # indica si cargar los carteles

def mainlist(params,url,category):
	xbmc.output("[animeforos.py] mainlist")

	category = "Anime"
	aviso = "Esta carpeta contiene una pequeña selección de las series infantiles (para Todos los Públicos), disponibles en este canal. En cuanto al resto de carpetas, se recomienda supervisar los contenidos a los que los menores acceden. Al abrir la carpeta de cada Anime aparecen, antes de los vídeos, sus datos (Clasificación,Género,etc.) o la opción de buscarlos en McAnime-Enciclopedia, además, en el aptdo -Información de la Película- encontrará la información procedente de la propia release, a la que se agrega la de McAnime si se ha encontrado. La disponibilidad de la información por género y edades desde el canal irá mejorando."

	addnewfolder( CHANNELNAME , "clasicos" , category , "Series Clásicas Infantiles TV - [TP] - (***Leer aptdo Información de la película)" , "" , "" , aviso )
	addnewfolder( CHANNELNAME , "astroteamrg" , category , "AstroteamRG - Series" , "" , "" , "Fuente: http://www.astroteamrg.org")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Series - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Series - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Series - Actualmente en Emision" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Ovas - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Ovas - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Ovas - Actualmente en Emision" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Peliculas - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Peliculas - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "listseries" , category , "El Rincón del Manga - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addnewfolder( CHANNELNAME , "search" , category , "El Rincón del Manga - Buscar","http://www.elrincondelmanga.com/foro/showthread.php?t=75282","" ,"Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def clasicos(params,url,category):
	xbmc.output("[animeforos.py] clasicos")

	addnewfolder( CHANNELNAME , "detail2" , category , "La Aldea del Arce (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://spe.fotolog.com/photo/46/13/24/soy_un_sol/1226490296711_f.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail" , category , "Heidi" , "http://www.elrincondelmanga.com/foro/showthread.php?t=1173" , "http://images.mcanime.net/images/anime/433.jpg" , "Fuente: http://www.elrincondelmanga.com")
	addnewfolder( CHANNELNAME , "detail" , category , "Marco" , "http://www.elrincondelmanga.com/foro/showthread.php?t=65463#1" , "http://img115.imageshack.us/img115/8325/1612df65c4rs6.jpg" , "Fuente: http://www.elrincondelmanga.com")
	addnewfolder( CHANNELNAME , "detail2" , category , "Sherlock Holmes (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail" , category , "El Patito Alfred" , "http://www.elrincondelmanga.com/foro/showthread.php?t=63927#1" , "http://www.fotodiario.com/fotos/7596/75967b6200db43e76e7d2d87c3e90191_709x963.jpg" , "Fuente: http://www.elrincondelmanga.com")
	addnewfolder( CHANNELNAME , "detail" , category , "Ulises 31" , "http://www.elrincondelmanga.com/foro/showthread.php?t=3294" , "http://img208.imageshack.us/img208/4820/ulyssesbox9sh.jpg" , "Fuente: http://www.elrincondelmanga.com")
	addnewfolder( CHANNELNAME , "detail2" , category , "Campeones (Oliver y Benji) (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail" , category , "Kochikame [+7] (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=15845" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=15845 por friki100. Colaboradores: curro1")
	addnewfolder( CHANNELNAME , "detail2" , category , "Ponyo en el acantilado (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://www.caratulasdecine.com/Caratulas5/ponyoenelacantilado.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def astroteamrg(params,url,category):
	xbmc.output("[animeforos.py] astroteamrg")

	addnewfolder( CHANNELNAME , "detail" , category , "Kochikame (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=15845" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=15845 por friki100. Colaboradores: curro1")
	addnewfolder( CHANNELNAME , "detail" , category , "Slam Dunk (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16731" , "http://upload.wikimedia.org/wikipedia/en/b/b3/Slamdunk_cover1.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16731 por friki100.")
	addnewfolder( CHANNELNAME , "detail2" , category , "Sherlock Holmes (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail2" , category , "La Aldea del Arce (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://spe.fotolog.com/photo/46/13/24/soy_un_sol/1226490296711_f.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail2" , category , "Ponyo en el acantilado (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://www.caratulasdecine.com/Caratulas5/ponyoenelacantilado.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail2" , category , "Campeones (Oliver y Benji) (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail2" , category , "Conan, el niño del futuro (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img220.imageshack.us/img220/425/50332do7.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail2" , category , "Cowboy Bebop (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://upload.wikimedia.org/wikipedia/en/3/37/CowboyBebopDVDBoxSet.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro.")
	addnewfolder( CHANNELNAME , "detail" , category , "Sailor Moon (by Tuxedo_Mask)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16406" , "http://upload.wikimedia.org/wikipedia/en/4/40/Sailor_Moon_S.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16406 por Tuxedo_Mask.")
	addnewfolder( CHANNELNAME , "detail" , category , "Master Keaton VOSE (by Tom_Bombadil)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16761" , "http://upload.wikimedia.org/wikipedia/en/f/f7/Master_Keaton_cover.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16761 por Tom_Bombadil")
	addnewfolder( CHANNELNAME , "detail" , category , "Eureka Seven VOSE (by skait)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16784" , "http://upload.wikimedia.org/wikipedia/en/4/45/Eureka_Seven_DVD_1_-_North_America.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16784 por skait.")
	addnewfolder( CHANNELNAME , "detail" , category , "Cross Game VOSE (by gatest)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16808" , "http://upload.wikimedia.org/wikipedia/en/c/cf/Cross_Game_DVDv1.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16808 por gatest")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[animeforos.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	match0 = re.search(' \((by \w+)\)$',title,re.IGNORECASE)
	if (match0):
		autor = " - "+match0.group(1)
		title = re.sub(' \(by \w+\)','',title)
	else:
		autor = ""
	title = re.sub('\s*\[.*\]\s*','',title)
	title = re.sub('\s+$','',title)
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	# Se utiliza plot para pasar el tipo de contenido
	tcsearch = "[^\)]+"
	matchTC = re.match('Tipo Contenido\:\s(.*?)$',plot)
	if (matchTC):
		tcsearch = matchTC.group(1)
		tcsearch = re.sub('í','i',tcsearch)
	xbmc.output("[animeforos.py] title="+title)
	xbmc.output("[animeforos.py] thumbnail="+thumbnail)

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Busca la release
	# ------------------------------------------------------
	matchR0 = re.match('.*?#(\d+)$',url)
	if (matchR0):
		post = matchR0.group(1)	
		patronvideos = 'name="'+post+'">#</a>(.*?)<!-- / message -->'
		matches = re.compile(patronvideos,re.DOTALL).search(data)
		if (matches):
			data = matches.group(1)
				
	# ------------------------------------------------------
	# Extrae información del contenido de su página
	# ------------------------------------------------------		
	plot = ""	
	match6 = re.search('(Genero|Género)\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
	if (match6):
		plot = "Género: "+re.sub('\<.*?\>','',match6.group(2))+". "
	match7 = re.search('Episodios\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
	if (match7):
		plot = plot+"Episodios: "+re.sub('\<.*?\>','',match7.group(1))+". "
	match8 = re.search('(Duración|Duracion)\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
	if (match8):
		plot = plot+"Duración: "+re.sub('\<.*?\>','',match8.group(2))+". "
	match9 = re.search('Año\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
	if (match9):
		plot = plot+"Año: "+re.sub('\<.*?\>','',match9.group(1))+". "
	match10 = re.search('Idioma\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
	if (match10):
		plot = plot+"Idioma: "+re.sub('\<.*?\>','',match10.group(1))+". "
	match11 = re.search('Subt(?:í|i)tulos\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
	if (match11):
		plot = plot+"Subtítulos: "+re.sub('\<.*?\>','',match11.group(1))+"."

	# ------------------------------------------------------
	# (Aun no está implantado) Extrae clasificación de edades si existe, no se excluyen por si la información es contradictoria
	# ------------------------------------------------------		
	apto = ""
	# match2 = re.search('http://img393.imageshack.us/img393/7019/clasiftpmv5.png',data,re.IGNORECASE)
	# if (match2):
		# apto = "[TP] "
	# match3 = re.search('http://img393.imageshack.us/img393/8727/clasif13kn3.png',data,re.IGNORECASE)
	# if (match3):
		# apto = "[+13] "
	# match4 = re.search('http://img151.imageshack.us/img151/8885/clasif16sa4.png',data,re.IGNORECASE)
	# if (match4):
		# apto = "[+16] "
	# match5 = re.search('http://img138.imageshack.us/img138/5974/clasif18op4.png',data,re.IGNORECASE)
	# if (match5):
		# apto = "[+18] "

	# ------------------------------------------------------
	# Extrae información del contenido de McAnime - Enciclopedia Beta
	# ------------------------------------------------------

	listavideos = findvideos(data,title)

	if len(listavideos)==0:
		alertnoresultados()
		return

	listainfo = findinfo("",title,tcsearch,"0")
	
	if len(listainfo)==1:
		plot = plot+" "+listainfo[0][5]

		addnewfolder( CHANNELNAME , "searchmc" , category , listainfo[0][0]+": Información McAnime - Enciclopedia Beta" , "" , "" , listainfo[0][5] )

		addnewfolder( CHANNELNAME , "searchmc" , category , "Clasificación: "+listainfo[0][1] , "" , "" , listainfo[0][5] )

		addnewfolder( CHANNELNAME , "searchmc" , category , "Géneros: "+listainfo[0][2] , "" , "" , listainfo[0][5] )

		addnewfolder( CHANNELNAME , "searchmc" , category , "Contenido: "+listainfo[0][3] , "" , "" , listainfo[0][5] )

		addnewfolder( CHANNELNAME , "searchmc" , category , "Sinopsis: "+listainfo[0][4] , "" , "" , listainfo[0][5] )
		

	else:	
		addnewfolder( CHANNELNAME , "searchmc" , category , "***Buscar Información en McAnime - Enciclopedia Beta" , "http://www.mcanime.net/enciclopedia/anime" , "" ,"Fuente: http://www.mcanime.net/enciclopedia/anime" )
		
	for video in listavideos:

		addnewvideo( CHANNELNAME , "play" , category , video[2] , apto+title+" - "+video[0]+" - [Megaupload]"+autor , video[1] , thumbnail , plot )
					
	# Extrae la fecha de la próxima actualización
	patronvideos = '<span style="font-size:12pt;line-height:(100)%"><!--/sizeo-->([^<]+)<!--sizec-->'
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		titulo = matches.group(2)
		url = ""
		# Añade al listado de XBMC 
		addnewvideo( CHANNELNAME , "play" , category , "Megaupload" , titulo , url , "" , plot )
					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
def findvideos(data,title):
	xbmc.output("[animeforos.py] findvideos")
	encontrados = set()
	devuelve = []

	# Extrae los enlaces a los vídeos - Megaupload - Vídeos con título - Skait
	patronvideos  = '(<br /><b>|<br />)\s([^<]+)<br />\s'
	patronvideos += '<a href\="http\:\/\/www.megaupload.com/\?d\=([^"]+)" target="_blank">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[1]
		titulo = titulo.replace(' -  ' , '')
		titulo = titulo.replace(' - Ovas ' , ' Ovas')

		url = match[2]

		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megaupload' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)		

	# Extrae los enlaces a los vídeos - Megaupload - Vídeos con título
	patronvideos = '(\d\d\.\-\s<a|<a) href\="?http\:\/\/www.megaupload.com(?:\/es\/|\/)\?d\=(\w+)[^>]*>(<br[^<]+<img[^>]+>.*?|<img[^>]+>.*?|.*?)(?:</?a>|<img|</a<|</tr>)'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:

		# Titulo quita código html
		titulo = re.sub('\<.*?\>','',match[2])
		titulo = re.sub('^\s+','',titulo)
		titulo = re.sub('\s+$','',titulo)
		titulo = entityunescape(titulo)
		
		# url
		url = match[1]

		# Sailor Moon
		foro = ""
		if title == "Sailor Moon":
			match0 = re.match('(\d\d\.\-\s)<a',match[0])
			if (match0):
				titulo = match0.group(1)+titulo
				foro = "AT"
			if titulo == "01.- La niña llorona se convierte en guerrero":
				titulo = titulo+" - VO (Japonés)"
			match2 = re.match('\d',titulo)
			if match2 is None and foro=="AT":
				url = ""
		
		# Cross Game
		if title == "Cross Game":
			match1 = re.match('\[Rakuen~SnF\] Cross Game HDTV (\d{2,4})$',titulo,re.IGNORECASE)
			if (match1):
				titulo = match1.group(1)+ " - HDTV [Rakuen~SnF]"

		# Kochikame
		if title == "Kochikame":
			if titulo[0:3] == "Cap":
				titulo = titulo[9:]
			if titulo[0:3] == "000":
	             		url = ""

		# Identifica un tipo de formato con el título de la serie en el enlace y el id del episodio fuera.
		parte = ""
		match4 = re.match('(\s*\[TeU\-F\]|'+title+')',titulo,re.IGNORECASE)
		if (match4):
			parte = "-2"
		
		# Elimina el título de la serie del título del episodio (si aparece al ppio o al final)
		if parte <> "-2":
			titulo = re.sub('\s*\-*\s*'+title+'$','',titulo)
			titulo = re.sub('^'+title+'\s*\-*\s*','',titulo)

		# Identifica los videos en partes y sin título
		titulo0 = ""
		match3 = re.match('\s*(?:\[.*?\]|\(?\s*Parte?\s*(?:\d+|\[[^\]]+\])\s*\)?|RAW|\(\d{1,2}\/\d{1,2}\)|Dnf.*?)\s*$',titulo,re.IGNORECASE)
		if (match3):
			parte = "-1"
	
		# Busca el título para los casos anteriores
		if parte <> "":
			match7 = re.search('<img src="[^"]+"[^>]*>\s*(<font color=[^>]+>[^<]+<b>|<a href=[^>]+>[^<]+<b>(?:[^<]+</b></a>|[^<]+)|[^<]+<b>[^<]+</b>|[^<]+)(?:<font color="[^"]+"><i>[^<]+</i></font></font>|</font>|\s*)(?:</td><td align="right">\s*|\s*)<a href\="?http\:\/\/www.megaupload.com(\/es\/|\/)\?d\='+url,data,re.IGNORECASE)
			if (match7):
					titulo0 = re.sub('\<.*?\>','',match7.group(1))
					titulo0 = re.sub('^\s+','',titulo0)
					titulo0 = re.sub('\s+$','',titulo0)
					titulo0 = entityunescape(titulo0)
					titulo = titulo0+" "+titulo
			else:
				match5 = re.search('<img src="[^"]+"[^>]*>\s*((?:<font color="[^"]+">[^<]*|[^<]+<b>)\s*.*?)<a href\="?http\:\/\/www.megaupload.com(?:\/es\/|\/)\?d\=\w+(?<='+url+')',data,re.IGNORECASE)
				if (match5):
					search0 = match5.group(1)
					# Busca si no se trata de la 1ª parte (el resto se modifican más abajo por si la 1ª parte tiene titulo)
					match6 = re.search('<a href\="?http\:\/\/www.megaupload.com',search0,re.IGNORECASE)
					if match6 is None:
						titulo0 = re.sub('\<.*?\>','',search0)
						titulo0 = re.sub('^\s+','',titulo0)
						titulo0 = re.sub('\s+$','',titulo0)
						titulo0 = entityunescape(titulo0)
						titulo = titulo0+" "+titulo

		if url not in encontrados and url <> "":
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megaupload' , parte , titulo0 ] )
			encontrados.add(url)
			if parte == "-1" and titulo0 == "":
				n = devuelve.index([ titulo , url , 'Megaupload' , parte , titulo0 ])
				if devuelve[n-1][3] == "-1" and devuelve[n-1][4] <> "":
					devuelve[n][0] = devuelve[n-1][4]+" "+devuelve[n][0]
					devuelve[n][4] = devuelve[n-1][4]
				# Caso en que el que la 1ª parte tiene título
				if devuelve[n-1][3] == "":
					match32 = re.match('(.*?)(?:\[.*?\]|\(?\s*Parte?\s*(?:\d+|\[[^\]]+\])\s*\)?|RAW|\(\d{1,2}\/\d{1,2}\))\s*$',devuelve[n-1][0],re.IGNORECASE)
					if (match32):
						devuelve[n][0] = match32.group(1)+devuelve[n][0]
						devuelve[n][4] = match32.group(1)
				# Caso
				if devuelve[n-1][3] == "-2":
					match22 = re.match('(.*?)(?:\[.*?\]|\(?\s*Parte?\s*(?:\d+|\[[^\]]+\])\s*\)?|RAW|\(\d{1,2}\/\d{1,2}\)|\[TeU-F\].*?)\s*$',devuelve[n-1][0],re.IGNORECASE)
					if (match22):
						devuelve[n][0] = match22.group(1)+devuelve[n][0]
						devuelve[n][4] = match22.group(1)
			
		else:
			xbmc.output("  url duplicada="+url)


	return devuelve

def detail2(params,url,category):
	xbmc.output("[animeforos.py] detail2")

	title = urllib.unquote_plus( params.get("title") )
	match0 = re.search(' \((by \w+)\)$',title,re.IGNORECASE)
	if (match0):
		autor = " - "+match0.group(1)
		title = re.sub(' \(by \w+\)','',title)
	else:
		autor = ""
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[animeforos.py] title="+title)
	xbmc.output("[animeforos.py] thumbnail="+thumbnail)

	if title == "Conan, el niño del futuro":	
		inicios = "fichaconan.jpg"
		fins = "fichacampeones.jpg"
	if title == "Campeones (Oliver y Benji)":	
		inicios = "fichacampeones.jpg"
		fins = "holmesficha.jpg"
	if title == "Sherlock Holmes":	
		inicios = "holmesficha.jpg"
		fins = "fichamaple.jpg"
	if title == "La Aldea del Arce":	
		inicios = "fichamaple.jpg"
		fins = "fichabebop.jpg"
	if title == "Cowboy Bebop":	
		inicios = "fichabebop.jpg"
		fins = "fichaponyo.jpg"
	if title == "Ponyo en el acantilado":	
		inicios = "fichaponyo.jpg"
		fins = "</div>"

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae la serie
	# ------------------------------------------------------
	patronvideos = inicios+'(.*?)'+fins
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		data = matches.group(1)
		
		listavideos = findvideos(data,title)

		if len(listavideos)==0:
			alertnoresultados()
			return
	
		tcsearch = "[^\)]+"
		listainfo = findinfo("",title,tcsearch,"0")
	
		if len(listainfo)==1:
			plot = plot+" "+listainfo[0][5]

			addnewfolder( CHANNELNAME , "searchmc" , category , listainfo[0][0]+": Información McAnime - Enciclopedia Beta" , "" , "" , listainfo[0][5] )

			addnewfolder( CHANNELNAME , "searchmc" , category , "Clasificación: "+listainfo[0][1] , "" , "" , listainfo[0][5] )

			addnewfolder( CHANNELNAME , "searchmc" , category , "Géneros: "+listainfo[0][2] , "" , "" , listainfo[0][5] )

			addnewfolder( CHANNELNAME , "searchmc" , category , "Contenido: "+listainfo[0][3] , "" , "" , listainfo[0][5] )

			addnewfolder( CHANNELNAME , "searchmc" , category , "Sinopsis: "+listainfo[0][4] , "" , "" , listainfo[0][5] )
		
		else:	
			addnewfolder( CHANNELNAME , "searchmc" , category , "***Buscar Información en McAnime - Enciclopedia Beta" , "http://www.mcanime.net/enciclopedia/anime" , "" ,"Fuente: http://www.mcanime.net/enciclopedia/anime" )
		
		for video in listavideos:

			# Añade al listado de XBMC 
			addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - [Megaupload]"+autor , video[1] , thumbnail , plot )
	else:
		return					
			
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listseries(params,url,category):
	xbmc.output("[animeforos.py] listseries")

	title = urllib.unquote_plus( params.get("title") )
	match = re.search('\s(\w+)$',title)
	tipolist = match.group(1)
	match1 = re.search('\s-\s(\w+)\w\s-\s',title)
	if (match1):
		tipocontenido = match1.group(1)
	else:
		tipocontenido = "[^<]+"
	match2 = re.search('Español\/Dual',title)
	if (match2):
		idioma = "Español"
	else:
		idioma = ""
	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	listaseries = findcontenidos(data,tipolist,tipocontenido,"",idioma)

	for serie in listaseries:

		if tipolist == "Completo":
			if tipocontenido == "[^<]+":
				addnewfolder( CHANNELNAME , "detail" , category , serie[0]+" "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "Tipo Contenido: "+serie[5] )
			else:
				if tipocontenido == "Pelicula":
					addnewfolder( CHANNELNAME , "detail" , category , serie[0]+" "+serie[1] , serie[4] , "" , "Tipo Contenido: "+serie[5] )
				else:
					addnewfolder( CHANNELNAME , "detail" , category , serie[0]+" "+serie[1]+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "Tipo Contenido: "+serie[5] )
		else:
			addnewfolder( CHANNELNAME , "detail" , category , serie[0]+" "+serie[1]+" ["+serie[2]+"]" , serie[4] , "" , "Tipo Contenido: "+serie[5] )


	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findcontenidos(data,tipolist,tipocontenido,search,idioma):
	xbmc.output("[animeforos.py] findcontenidos")
	serieslist = []

	if tipocontenido == "Pelicula":
		tipocontenido = "Película|Pelicula"
	if tipolist == "Emision":
		tipolist = "<td class=Em>"
	else:
		tipolist = "<td class=\w+>"

	patronvideos  = '<a href=([^ ]+) class=\w+>('+search+'[^<]+)<span class=mt>([^<]+)</span>'
	patronvideos += '</a></td><td>('+tipocontenido+')</td><td>([^<]+)</td>('+tipolist+')</td>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulo = match[1]
		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')
                titulo = titulo.replace('&#33;' , '!')
		titulo = re.sub('\s+$','',titulo)
		
		# AnexoTitulo/idioma
		anextitulo = match[2]
		anextitulo = anextitulo.replace('&amp;' , '&')
		anextitulo = anextitulo.replace('&quot;' , '"')
                anextitulo = anextitulo.replace('&#33;' , '!')

		# URL
		url = urlparse.urljoin("http://www.elrincondelmanga.com/foro/",match[0])

		# Contenido
		contenido = match[3]

		# Capitulos
		capitulos = match[4]
		
		# En emisión
		enemision = ""
		if tipolist == "<td class=Em>":
			enemision = " [En Emisión]"
		else:
			if match[5] == "<td class=Co>":
				enemision = " [Terminada]"
			else:
				if match[5] == "<td class=Em>":
		 			enemision = " [En Emisión]"
				else:
					if match[5] == "<td class=Fa>":
		 				enemision = " [Fansubing]"
					else:
						if match[5] == "<td class=Up>":
		 					enemision = " [Uploading]"
						else:
							if match[5] == "<td class=De>":
		 						enemision = " [Detenida]"

		if idioma == "Español":
			match2 = re.search('(Esp|esp|Castellano|Lat|lat)',anextitulo)
			if (match2):
				serieslist.append( [ titulo , anextitulo , capitulos , enemision , url , contenido ] )
		else:
			serieslist.append( [ titulo , anextitulo , capitulos , enemision , url , contenido ] )

	return serieslist

def search(params,url,category):
	xbmc.output("[animeforos.py] search")

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
					listaseries = findcontenidos(data,"Completo","[^<]+",tecleado,"")
					for serie in listaseries:
						addnewfolder( CHANNELNAME , "detail" , category , serie[0]+" "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "Tipo Contenido: "+serie[5] )
				else:
					listaseries = findcontenidos(data,"Completo","[^<]+","","")				
					for serie in listaseries:
						foldertitle = serie[0]+" "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3]
						match = re.search(tecleado,foldertitle,re.IGNORECASE)
						if (match):
							addnewfolder( CHANNELNAME , "detail" , category , foldertitle , serie[4] , "" , "Tipo Contenido: "+serie[5] )

	else:
		# Descarga la página
		data = scrapertools.cachePage(url)
		#xbmc.output(data)

		listaseries = findcontenidos(data,"Completo","[^<]+",letras[seleccion-1],"")

		for serie in listaseries:

			addnewfolder( CHANNELNAME , "detail" , category , serie[0]+" "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "Tipo Contenido: "+serie[5] )
					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )			


def play(params,url,category):
	xbmc.output("[animeforos.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]	
	xbmc.output("[animeforos.py] thumbnail="+thumbnail)
	xbmc.output("[animeforos.py] server="+server)

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def entityunescape(cadena):
	cadena = cadena.replace('&amp;' , '&')
        cadena = cadena.replace('&#33;' , '!')
	cadena = cadena.replace('&Aacute;' , 'Á')
	cadena = cadena.replace('&Eacute;' , 'É')
	cadena = cadena.replace('&Iacute;' , 'Í')
	cadena = cadena.replace('&Oacute;' , 'Ó')
	cadena = cadena.replace('&Uacute;' , 'Ú')
	cadena = cadena.replace('&ntilde;' , 'ñ')
	cadena = cadena.replace('&Ntilde;' , 'Ñ')
	cadena = cadena.replace('&aacute;' , 'á')
	cadena = cadena.replace('&#225;' , 'á')
	cadena = cadena.replace('&eacute;' , 'é')
	cadena = cadena.replace('&#233;' , 'é')
	cadena = cadena.replace('&iacute;' , 'í')
	cadena = cadena.replace('&#237;' , 'í')
	cadena = cadena.replace('&oacute;' , 'ó')
	cadena = cadena.replace('&#243;' , 'ó')
	cadena = cadena.replace('&uacute;' , 'ú')
	cadena = cadena.replace('&#250;' , 'ú')
	cadena = cadena.replace('&iexcl;' , '¡')
	cadena = cadena.replace('&iquest;' , '¿')
	cadena = cadena.replace('&ordf;' , 'ª')
	cadena = cadena.replace('&quot;' , '"')
	cadena = cadena.replace('&hellip;' , '...')
	cadena = cadena.replace('&#39;' , '\'')
	cadena = cadena.replace('&#039;' , '\'')
	cadena = cadena.replace('&#241;' , 'ñ')
	return cadena

def findinfo(data,title,tcsearch,todos):
	xbmc.output("[animeforos.py] findinfo")
	animemclist = []
	listinfomc = []
	url = ""

	match0 = re.match('(?:The\s+|El\s+|La\s+|Los\s+|Las\s+|\s*)(\w|\#)',title,re.IGNORECASE)
	if (match0):
		inicial = match0.group(1)
		match01 = re.match('(\d|\#)',inicial)
		if (match01):
			url = "http://www.mcanime.net/enciclopedia/anime/lista/9"
		else:
			url = urlparse.urljoin("http://www.mcanime.net/enciclopedia/anime/lista/",inicial.lower())

	data = scrapertools.cachePage(url)

	if todos=="-1":
		comodin = "[^<]*"
		if len(title)==1:
			title = "[^<]+"
	else:
		comodin = ""
	
	patronvideos = '<a href\=\"([^\"]+)\">(?:<b>|\s*)('+title+comodin+')(?:</b>|\s*)</a>\s*<i>(\('+tcsearch+'\))</i>\s*</h5>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		
		# Titulo
		titulomc = match[1]+" "+match[2]
		titulomc = entityunescape(titulomc)		
		
		# url
		urlmc = urlparse.urljoin("http://www.mcanime.net/",match[0])

		animemclist.append( [ titulomc , urlmc ] )

	if todos=="-1":

		return animemclist

	if todos=="0":

		if len(animemclist)==1:

			titulomc2 = animemclist[0][0]
			urlmc2 = animemclist[0][1]

			listinfomc = findlistinfo("",titulomc2,urlmc2)
	
		return listinfomc

def findlistinfo(data,title,url):
	xbmc.output("[animeforos.py] findlistinfo")

	infomclist = []

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Busca la info
	# ------------------------------------------------------	

	sinopsis = ""	
	match1 = re.search('<h6>Sinopsis.*?</h6>\n\s*([^<]+)<br />',data,re.IGNORECASE)
	if (match1):
		try:
			sinopsis = unicode( match1.group(1), "utf-8" ).encode("iso-8859-1")
		except:
			sinopsis = match1.group(1)

		sinopsis = entityunescape(sinopsis)

	clasf = ""	
	match2 = re.search('<b>Clasificaci\&oacute\;n\:</b>([^<]+)<br />',data,re.IGNORECASE)
	if (match2):
		try:
			clasf = unicode( match2.group(1), "utf-8" ).encode("iso-8859-1")
		except:
			clasf = match2.group(1)

		clasf = clasf.replace('Adolecentes' , 'Adolescentes')
		clasf = entityunescape(clasf)

	genre = ""	
	match3 = re.search('<b>G\&eacute\;neros\:</b>(.*?)<br />',data,re.IGNORECASE)
	if (match3):
		try:
			genre = unicode( match3.group(1), "utf-8" ).encode("iso-8859-1")
			genre = re.sub('\<.*?\>','',genre)
		except:
			genre = re.sub('\<.*?\>','',match3.group(1))

		genre = re.sub('^\s+','',genre)
		genre = re.sub('\s+$','',genre)
		genre = re.sub(',\s[^\w]{5}',', ',genre)
		genre = entityunescape(genre)

	contenido = ""	
	match4 = re.search('<b>Contenido\:</b>\s*([^<]+)<br />',data,re.IGNORECASE)
	if (match4):
		try:
			contenido = unicode( match4.group(1), "utf-8" ).encode("iso-8859-1")
		except:
			contenido = match4.group(1)
	
		contenido = re.sub(',\s[^\w]{5}',', ',contenido)
		contenido = entityunescape(contenido)

	
	plot = ".***MCANIME-Enciclopedia sobre "+title+". Sinopsis: "+sinopsis+". Clasificación: "+clasf+". Géneros: "+genre+". Contenido: "+contenido+".--"
	try:
		plotmc = unicode( plot, "utf-8" ).encode("iso-8859-1")
	except:
		plotmc = plot	


	infomclist.append([ title , clasf , genre , contenido , sinopsis , plotmc ])
	
	return infomclist

def findinfo2(params,url,category):
	xbmc.output("[animeforos.py] findinfo2")

	title = urllib.unquote_plus( params.get("title") )
	title = re.sub('\s\-\s\[McAnime\-Enciclopedia\]','',title)
	xbmc.output("[animeforos.py] title="+title)

	listainfomc = findlistinfo("",title,url)	

	# Añade al listado de XBMC
	addnewvideo( CHANNELNAME , "play" , category , "" , listainfomc[0][0]+": Información McAnime - Enciclopedia Beta" , "" , "" , listainfomc[0][5] )

	addnewvideo( CHANNELNAME , "play" , category , "" , "Clasificación: "+listainfomc[0][1] , "" , "" , listainfomc[0][5] )

	addnewvideo( CHANNELNAME , "play" , category , "" , "Géneros: "+listainfomc[0][2] , "" , "" , listainfomc[0][5] )

	addnewvideo( CHANNELNAME , "play" , category , "" , "Contenido: "+listainfomc[0][3] , "" , "" , listainfomc[0][5] )

	addnewvideo( CHANNELNAME , "play" , category , "" , "Sinopsis: "+listainfomc[0][4] , "" , "" , listainfomc[0][5] )

		
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )	

def searchmc(params,url,category):
	xbmc.output("[animeforos.py] searchmc")

	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
	opciones = []
	opciones.append("Teclado")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Búsqueda por Inicial del Título en McAnime-Enciclopedia:", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1 :return
	if seleccion == 0:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			if len(tecleado)>0:
				if len(tecleado) == 1:
					listainfo = findinfo("",tecleado,"[^<]+","-1")
					for info in listainfo:
						addnewfolder( CHANNELNAME , "findinfo2" , category , info[0]+" - [McAnime-Enciclopedia]" , info[1] , "" , "" )
				else:
					listainfo = findinfo("",tecleado,"[^<]+","-1")				
					for info in listainfo:
						match = re.search(tecleado,info[0],re.IGNORECASE)
						if (match):
							addnewfolder( CHANNELNAME , "findinfo2" , category , info[0]+" - [McAnime-Enciclopedia]" , info[1] , "" , "" )

	else:

		listainfo = findinfo("",letras[seleccion-1],"[^<]+","-1")

		for info in listainfo:
			addnewfolder( CHANNELNAME , "findinfo2" , category , info[0]+" - [McAnime-Enciclopedia]" , info[1] , "" , "" )
					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )			

def alertnoresultados():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Contenido no disponible' , 'No se han encontrado vídeos.' , '')

def addnewfolder( canal , accion , category , title , url , thumbnail , plot ):
	xbmc.output("[casttv.py] addnewfolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	xbmc.output('[casttv.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)
