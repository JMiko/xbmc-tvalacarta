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
import servertools
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
	categoryerdm = "El Rincón del Manga  -  Anime"
	aviso = "Esta carpeta contiene una pequeña selección de series infantiles (TP), en cuanto al resto, se recomienda supervisar los contenidos a los que los menores acceden. Al abrir la carpeta de cada Anime aparecen, antes de los vídeos, sus datos (Clasificación,Género,etc.) o la opción de buscarlos en McAnime-Enciclopedia. En el aptdo -Información de la Película- encontrará información procedente de la propia release y de McAnime. La disponibilidad de información por género y edades desde el canal irá mejorando."

	addsimplefolder( CHANNELNAME , "clasicos" , category , "Series Clásicas Infantiles TV - [TP] - (***Leer aptdo Información de la película)" , "" , "" , aviso)
	addsimplefolder( CHANNELNAME , "astroteamrg" , "AstroteamRG  -  Anime" , "AstroteamRG - Series" , "" , "" , "Fuente: http://www.astroteamrg.org")
	addsimplefolder( CHANNELNAME , "genres" , "Géneros  -  McAnime-Enciclopedia" , "El Rincón del Manga y McAnime - Buscar por Géneros","http://www.mcanime.net/enciclopedia/anime","" ,"Fuentes: http://www.mcanime.net/enciclopedia/anime y http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "search" , categoryerdm , "El Rincón del Manga - Buscar","http://www.elrincondelmanga.com/foro/showthread.php?t=75282","" ,"Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Series - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Series - Actualmente en Emision" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Series - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Ovas - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Ovas - Actualmente en Emision" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Ovas - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Películas - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Películas - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Especiales - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Español/Dual - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	addsimplefolder( CHANNELNAME , "listseries" , categoryerdm , "El Rincón del Manga - Listado Completo" , "http://www.elrincondelmanga.com/foro/showthread.php?t=75282" , "" , "Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def clasicos(params,url,category):
	xbmc.output("[animeforos.py] clasicos")

	addnewfolder( CHANNELNAME , "detail2" , category , "La Aldea del Arce (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://spe.fotolog.com/photo/46/13/24/soy_un_sol/1226490296711_f.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Heidi" , "http://www.elrincondelmanga.com/foro/showthread.php?t=1173" , "http://images.mcanime.net/images/anime/433.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Marco, de los Apeninos a los Andes" , "http://www.elrincondelmanga.com/foro/showthread.php?t=65463#1" , "http://img115.imageshack.us/img115/8325/1612df65c4rs6.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie", "" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Sherlock Holmes (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Detective Holmes" , "Serie" )
	adderdmfolder( CHANNELNAME , "detail" , category , "El Patito Alfred" , "http://www.elrincondelmanga.com/foro/showthread.php?t=63927#1" , "http://www.fotodiario.com/fotos/7596/75967b6200db43e76e7d2d87c3e90191_709x963.jpg" , "Fuente: http://www.elrincondelmanga.com" , "Alfred J. Quack" , "Serie", "" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Ulises 31" , "http://www.elrincondelmanga.com/foro/showthread.php?t=3294" , "http://img208.imageshack.us/img208/4820/ulyssesbox9sh.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie", "" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Campeones (Oliver y Benji) (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Captain Tsubasa" , "Serie" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Kochikame [+7] (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=15845" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=15845 por friki100. Colaboradores: curro1" , "" , "Serie", "" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Ponyo en el acantilado (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://www.caratulasdecine.com/Caratulas5/ponyoenelacantilado.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Ponyo on the Cliff by the Sea" , "Película" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def astroteamrg(params,url,category):
	xbmc.output("[animeforos.py] astroteamrg")

	adderdmfolder( CHANNELNAME , "detail" , category , "Kochikame (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=15845" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=15845 por friki100. Colaboradores: curro1" , "" , "Serie", "" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Slam Dunk (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16731" , "http://upload.wikimedia.org/wikipedia/en/b/b3/Slamdunk_cover1.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16731 por friki100." , "" , "Serie", "" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Sherlock Holmes (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Detective Holmes" , "Serie" )
	addnewfolder( CHANNELNAME , "detail2" , category , "La Aldea del Arce (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://spe.fotolog.com/photo/46/13/24/soy_un_sol/1226490296711_f.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Ponyo en el acantilado (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://www.caratulasdecine.com/Caratulas5/ponyoenelacantilado.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Ponyo on the Cliff by the Sea" , "Película" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Campeones (Oliver y Benji) (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Captain Tsubasa" , "Serie" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Conan, el niño del futuro (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img220.imageshack.us/img220/425/50332do7.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Conan, the Boy in Future" , "Serie" )
	addnewfolder( CHANNELNAME , "detail2" , category , "Cowboy Bebop (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://upload.wikimedia.org/wikipedia/en/3/37/CowboyBebopDVDBoxSet.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Sailor Moon (by Tuxedo_Mask)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16406" , "http://upload.wikimedia.org/wikipedia/en/4/40/Sailor_Moon_S.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16406 por Tuxedo_Mask." , "" , "Serie", "" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Master Keaton VOSE (by Tom_Bombadil)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16761" , "http://upload.wikimedia.org/wikipedia/en/f/f7/Master_Keaton_cover.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16761 por Tom_Bombadil" , "" , "Serie", "" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Eureka Seven VOSE (by skait)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16784" , "http://upload.wikimedia.org/wikipedia/en/4/45/Eureka_Seven_DVD_1_-_North_America.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16784 por skait." , "" , "Serie", "" )
	adderdmfolder( CHANNELNAME , "detail" , category , "Cross Game VOSE (by gatest)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16808" , "http://upload.wikimedia.org/wikipedia/en/c/cf/Cross_Game_DVDv1.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16808 por gatest" , "" , "Serie", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[animeforos.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	autor = ""
	match0 = re.search('\s+\((by \w+)\)$',title,re.IGNORECASE)
	if (match0):
		autor = " - "+match0.group(1)
	title = re.sub('(?:\s+VOSE|\s+\[.*\]|\s+\(by \w+\)$|\s+$)','',title)
	titleinfo = urllib.unquote_plus( params.get("titleinfo") )
	if titleinfo=="":
		titleinfo = title
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	tcsearch = urllib.unquote_plus( params.get("tcsearch") )
	if plot=="eRdM":
		title = titleinfo
		tcsearch = re.sub('í','i',tcsearch)
	if tcsearch=="":
		tcsearch = "[^\)]+"
	titleerdm = urllib.unquote_plus( params.get("titleerdm") )
	if titleerdm == "":
		titleerdm = searchtitle(titleinfo)
	xbmc.output("[animeforos.py] title="+title)
	
	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

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
	# Extrae información del contenido, de su página
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
	# Extrae información del contenido de McAnime - Enciclopedia Beta
	# ------------------------------------------------------

	listavideos = findvideos(data,title)

	if len(listavideos)==0:
		alertnoresultados()
		return

	listainfo = findinfo("",titleinfo,tcsearch,"0","",titleerdm)

	if len(listainfo)==1:

		if  thumbnail == "":
			thumbnail = listainfo[0][6]

		plot = plot+" "+listainfo[0][5]

		addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , listainfo[0][0]+": Información McAnime - Enciclopedia Beta" , "" , "" , listainfo[0][5] )

		addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Clasificación: "+listainfo[0][1] , "" , "" , listainfo[0][5] )

		addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Géneros: "+listainfo[0][2] , "" , "" , listainfo[0][5] )

		addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Contenido: "+listainfo[0][3] , "" , "" , listainfo[0][5] )

		addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Sinopsis: "+listainfo[0][4] , "" , "" , listainfo[0][5] )
		

	else:	
		addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "***Buscar Información en McAnime - Enciclopedia Beta" , "http://www.mcanime.net/enciclopedia/anime" , "" ,"Fuente: http://www.mcanime.net/enciclopedia/anime" )
		
	for video in listavideos:

		addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - [Megaupload]"+autor , video[1] , thumbnail , plot )
					
	# Extrae la fecha de la próxima actualización
	patronvideos = '<span style="font-size:12pt;line-height:(100)%"><!--/sizeo-->([^<]+)<!--sizec-->'
	matches = re.compile(patronvideos,re.DOTALL).search(data)
	if (matches):
		titulo = matches.group(2)
		# Añade al listado de XBMC 
		additem( CHANNELNAME , category , titulo , "" , "" , plot )
					
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

	# Extrae los enlaces a los vídeos - Megaupload - Vídeos con título
	patronvideos = '(\d\d\.\-\s<a|<a) href\="?http\:\/\/www.megaupload.com(?:\/es\/|\/)\?d\=(\w+)[^>]*>(<br[^<]+<img[^>]+>.*?|<img[^>]+>.*?|.*?)(?:</?a>|<img|</a<|</tr>)'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:

		# Titulo quita código html
		titulo = re.sub('\<.*?\>','',match[2])
		titulo = re.sub('^\s+','',titulo)
		titulo = re.sub('\s+$','',titulo)
		titulo = formatostring(titulo)
		
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
		match4 = re.match('(\s*\[TeU\-F\]|'+title+'[^\w]*$)',titulo,re.IGNORECASE)
		if (match4):
			parte = "-2"
		
		# Elimina el título de la serie del título del episodio (si aparece al ppio o al final)
		if parte <> "-2":
			titulo = re.sub('[^\w\]\)\"\']*'+title+'[^\w]*$','',titulo)
			titulo = re.sub('^'+title+'[^\w\[\(\"\']*','',titulo)
			titulo = re.sub('^1\[','[',titulo)
			
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
					titulo0 = formatostring(titulo0)
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
						titulo0 = formatostring(titulo0)
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
			

	return devuelve

def detail2(params,url,category):
	xbmc.output("[animeforos.py] detail2")

	title = urllib.unquote_plus( params.get("title") )
	autor = ""
	match0 = re.search(' \((by \w+)\)$',title,re.IGNORECASE)
	if (match0):
		autor = " - "+match0.group(1)
	title = re.sub('(?:\s+VOSE|\s+\[.*\]|\s+\(by \w+\)$|\s+$)','',title)
	titleinfo = urllib.unquote_plus( params.get("titleinfo") )
	if titleinfo=="":
		titleinfo = title
	tcsearch = urllib.unquote_plus( params.get("tcsearch") )
	if tcsearch=="":
		tcsearch = "[^\)]+"
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	# Titulo para búsquedas
	titleargen = searchtitle(titleinfo)
	xbmc.output("[animeforos.py] title="+title)
	
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
	
		listainfo = findinfo("",titleinfo,tcsearch,"0","",titleargen)
	
		if len(listainfo)==1:
			plot = plot+" "+listainfo[0][5]

			addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , listainfo[0][0]+": Información McAnime - Enciclopedia Beta" , "" , "" , listainfo[0][5] )

			addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Clasificación: "+listainfo[0][1] , "" , "" , listainfo[0][5] )

			addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Géneros: "+listainfo[0][2] , "" , "" , listainfo[0][5] )

			addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Contenido: "+listainfo[0][3] , "" , "" , listainfo[0][5] )

			addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Sinopsis: "+listainfo[0][4] , "" , "" , listainfo[0][5] )
		
		else:	
			addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "***Buscar Información en McAnime - Enciclopedia Beta" , "http://www.mcanime.net/enciclopedia/anime" , "" ,"Fuente: http://www.mcanime.net/enciclopedia/anime" )
		
		for video in listavideos:

			# Añade al listado de XBMC 
			addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - [Megaupload]"+autor , video[1] , thumbnail , plot )
	else:
		alertnoresultados()
		return					
			
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail3(params,url,category):
	xbmc.output("[animeforos.py] detail3")

	title = urllib.unquote_plus( params.get("title") )
	title = re.sub('\s+-\s+\[.*?\]$','',title)
	info1 = urllib.unquote_plus( params.get("info1") )
	info2 = urllib.unquote_plus( params.get("info2") )
	info3 = urllib.unquote_plus( params.get("info3") )
	info4 = urllib.unquote_plus( params.get("info4") )
	info5 = urllib.unquote_plus( params.get("info5") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	xbmc.output("[animeforos.py] title="+title)
	
	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	# listavideos = findvideos(data,title)

	listavideos = servertools.findvideos(data)

	if len(listavideos)==0:
		alertnoresultados()
		return
	
	additem( CHANNELNAME , category , info1 , "" , "" , plot )
	additem( CHANNELNAME , category , info2 , "" , "" , plot )
	additem( CHANNELNAME , category , info3 , "" , "" , plot )
	additem( CHANNELNAME , category , info4 , "" , "" , plot )
	additem( CHANNELNAME , category , info5 , "" , "" , plot )

	for video in listavideos:
		addnewvideo( CHANNELNAME , "play" , category , video[2] , title+" - "+video[0]+" - [Megaupload]" , video[1] , thumbnail , plot )
			
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
	match1 = re.search('\s-\s(Especial|[^s]+)e?s\s-\s',title)
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

	listaseries = findcontenidos(data,tipolist,tipocontenido,"",idioma)
	listaseries.sort(key=lambda serie: serie[0].lower())

	for serie in listaseries:

		if tipolist == "Completo":
			if tipocontenido == "[^<]+":
				adderdmfolder( CHANNELNAME , "detail" , category , serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )
			else:
				if tipocontenido == "Pelicula":
					adderdmfolder( CHANNELNAME , "detail" , category , serie[0]+"  -  "+serie[1] , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )
				else:
					adderdmfolder( CHANNELNAME , "detail" , category , serie[0]+"  -  "+serie[1]+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )
		else:
			adderdmfolder( CHANNELNAME , "detail" , category , serie[0]+"  -  "+serie[1]+" ["+serie[2]+"]" , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )


	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findcontenidos(data,tipolist,tipocontenido,search,idioma):
	xbmc.output("[animeforos.py] findcontenidos")
	serieslist = []

	tipocontenido = tipocontenido.lower()
	tipocontenido = re.sub('pel(?:í|i)cula','Pel(?:í|i)cula',tipocontenido)
	tipocontenido = re.sub('web','(?:Ova|Web)',tipocontenido)

	if tipolist == "Emision":
		tipolist = "<td class=Em>"
	else:
		tipolist = "<td class=\w+>"
	if search == "#":
		search = "[^a-zA-Z]"
	
	patronvideos  = '<a href=([^\s]+)\sclass=\w+>('+search+'[^<]+)<span class=mt>([^<]+)</span>'
	patronvideos += '</a></td><td>('+tipocontenido+')</td><td>([^<]+)</td>('+tipolist+')</td>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulo = match[1]
		titulo = titulo.replace('&amp;' , '&')
		titulo = titulo.replace('&quot;' , '"')
                titulo = titulo.replace('&#33;' , '!')
		titulo = re.sub('\s+$','',titulo)

		# Titulo para búsquedas
		titleerdm = searchtitle(titulo)
				
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
		elif match[5] == "<td class=Co>":
			enemision = " [Terminada]"
		elif match[5] == "<td class=Em>":
		 	enemision = " [En Emisión]"
		elif match[5] == "<td class=Fa>":
		 	enemision = " [Fansubing]"
		elif match[5] == "<td class=Up>":
		 	enemision = " [Uploading]"
		elif match[5] == "<td class=De>":
		 	enemision = " [Detenida]"

		if idioma == "Español":
			match2 = re.search('(Esp|esp|Castellano|Lat|lat)',anextitulo)
			if (match2):
				serieslist.append( [ titulo , anextitulo , capitulos , enemision , url , contenido , titleerdm ] )
		else:
			serieslist.append( [ titulo , anextitulo , capitulos , enemision , url , contenido , titleerdm ] )
	
	return serieslist

def search(params,url,category):
	xbmc.output("[animeforos.py] search")
	
	tecleado = ""
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	tipocontenido = "[^<]+"
        
	opciones = []
	opciones.append("Teclado (Busca en Título y datos anexos)")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Búsqueda por Teclado o por Inicial del Título:", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1 :return
	if seleccion <> 0:
		selecciontc = searchmctc()
		if selecciontc <> "":
			tipocontenido = selecciontc
	if seleccion == 0:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
			if len(tecleado)>0:
				selecciontc = searchmctc()
				if selecciontc <> "":
					tipocontenido = selecciontc	
				
				data = scrapertools.cachePage(url)
				
				if len(tecleado) == 1:
					listaseries = findcontenidos(data,"Completo",tipocontenido,tecleado,"")
				else:
					listaseries = findcontenidos(data,"Completo",tipocontenido,"","")				
			
		if keyboard.isConfirmed() is None or len(tecleado)==0:
			return		
	else:
		# Descarga la página
		data = scrapertools.cachePage(url)
		
		listaseries = findcontenidos(data,"Completo",tipocontenido,letras[seleccion-1],"")

	if len(listaseries)==0:
		alertnoresultadosearch()
		return

	listaseries.sort(key=lambda serie: serie[0].lower())
	for serie in listaseries:
		foldertitle = serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3]
		if len(tecleado)>1:
			match = re.search(tecleado,foldertitle,re.IGNORECASE)
			if (match):
				adderdmfolder( CHANNELNAME , "detail" , category , foldertitle , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )
		else:
			adderdmfolder( CHANNELNAME , "detail" , category , foldertitle , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )
					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )			


def findinfo(data,title,tcsearch,todos,genre,titleerdm):
	xbmc.output("[animeforos.py] findinfo")
	animemclist = []
	listinfomc = []
	url = genre
	infoencontrada = []
	infoencontrada2 = []
	tituloencontrado = "0"
	tcsearch = tcsearch.lower()
	tcsearch = re.sub('pel(?:í|i)cula','Pel(?:í|i)cula',tcsearch)
	tcsearch = re.sub('ova','(?:Ova|Web)',tcsearch)

	# Inicial
	inicial = "#"
	match0 = re.match('(?:The\s+|Las?\s+|Los\s+|An?\s+|[^\w\#]*)(\w|\#)',title,re.IGNORECASE)
	if (match0):
		inicial = match0.group(1)
	
	if url == "":
		match01 = re.match('[^a-zA-Z]',inicial)
		if (match01):
			url = "http://www.mcanime.net/enciclopedia/anime/lista/9"
		else:
			url = urlparse.urljoin("http://www.mcanime.net/enciclopedia/anime/lista/",inicial.lower())

		data = scrapertools.cachePage(url)
		
	else:
		data0 = scrapertools.cachePage(url)

		if len(title)==1:
			patronvideos = '<div class="letter">'+inicial.upper()+'</div>.*?<a name="\w">'
			match03 = re.compile(patronvideos,re.DOTALL).search(data0)
			if (match03):				
				data = match03.group(0)
		else:
			data = data0
	

	patronvideos = '<a href\=\"([^\"]+)\">(?:<b>|\s*)([^<]+)(?:</b></a>|</a>)\s*<i>(\('+tcsearch+'\))</i>\s*</h5>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		
		# Titulo
		titlemc = match[1]
		titlemc = re.sub('\s+$','',titlemc)
		titlemc = formatostring(titlemc)
		titulomc = titlemc+" "+match[2]

		# Titulo para búsquedas
		titlemcanime = searchtitle(titlemc)

		# Tipo contenido
		tpcontenidomc = re.sub('(?:\(|\))','',match[2])
						
		# url
		urlmc = urlparse.urljoin("http://www.mcanime.net/",match[0])

		animemclist.append( [ titulomc , urlmc , titlemc , tpcontenidomc , titlemcanime ] )

	if todos=="-1":

		if len(animemclist) > 0 and len(title) > 1:
			for animemc in animemclist:
				forinfo = re.search(title,animemc[2],re.IGNORECASE)
				if (forinfo):
					infoencontrada.append(animemc)
			animemclist = infoencontrada
				
		return animemclist

	if todos=="0":

		if len(animemclist) > 0:
			titlesearch = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',titleerdm)
			animemclist.sort(key=lambda animemc: animemc[4])
			for animemc in animemclist:
				if tituloencontrado == "-1" or len(infoencontrada2)==2:
					break
				titlemcanime = animemc[4]			
				forinfo = re.match(titlesearch+'$',titlemcanime,re.IGNORECASE)
				if (forinfo):
					infoencontrada.append(animemc)
					tituloencontrado = "-1"
				else:
					# Si se obtuvieran 2 o más coincidencias no serviría
					forinfo1 = re.match('^'+titlesearch+'.+$',titlemcanime,re.IGNORECASE)
					if (forinfo1):
						infoencontrada2.append(animemc)											
			
			# Último intento :-) supuesto que el listado de McAnime es más completo...
			if len(infoencontrada)==0 and len(infoencontrada2)==0:
				animemclist.reverse()
				for animemc in animemclist:
					if len(infoencontrada2)==1:
						break
					if len(animemc[2])>1:
						titlemcanimesearch = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',animemc[4])								
						forerdm = re.match('^'+titlemcanimesearch+'.+$',titleerdm,re.IGNORECASE)
						if (forerdm):
							infoencontrada2.append(animemc)
												
			if len(infoencontrada)==0:
				infoencontrada = infoencontrada2
			
			if len(infoencontrada)==1:
				titulomc2 = infoencontrada[0][0]
				urlmc2 = infoencontrada[0][1]

				listinfomc = findlistinfo("",titulomc2,urlmc2)

		return listinfomc

def findlistinfo(data,title,url):
	xbmc.output("[animeforos.py] findlistinfo")

	infomclist = []

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	if data == "":
		data = scrapertools.cachePage(url)
	
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

		sinopsis = formatostring(sinopsis)

	clasf = ""	
	match2 = re.search('<b>Clasificaci\&oacute\;n\:</b>([^<]+)<br />',data,re.IGNORECASE)
	if (match2):
		try:
			clasf = unicode( match2.group(1), "utf-8" ).encode("iso-8859-1")
		except:
			clasf = match2.group(1)

		clasf = clasf.replace('Adolecentes' , 'Adolescentes')
		clasf = formatostring(clasf)

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
		genre = formatostring(genre)

	contenido = ""	
	match4 = re.search('<b>Contenido\:</b>\s*([^<]+)<br />',data,re.IGNORECASE)
	if (match4):
		try:
			contenido = unicode( match4.group(1), "utf-8" ).encode("iso-8859-1")
		except:
			contenido = match4.group(1)
	
		contenido = re.sub(',\s[^\w]{5}',', ',contenido)
		contenido = formatostring(contenido)

	thumbnail = ""	
	match5 = re.search('<img src="([^"]+)"[^c]+class="title_pic"',data,re.IGNORECASE)
	if (match5):
		thumbnail = match5.group(1)

	plot = ".***MCANIME-Enciclopedia sobre "+title+". Sinopsis: "+sinopsis+". Clasificación: "+clasf+". Géneros: "+genre+". Contenido: "+contenido+".--"
	try:
		plotmc = unicode( plot, "utf-8" ).encode("iso-8859-1")
	except:
		plotmc = plot	


	infomclist.append([ title , clasf , genre , contenido , sinopsis , plotmc , thumbnail ])
	
	return infomclist

def findinfo2(params,url,category):
	xbmc.output("[animeforos.py] findinfo2")

	title = urllib.unquote_plus( params.get("title") )
	title = re.sub('\s+\-\s+\[McAnime\-Enciclopedia\]','',title)
	plot = urllib.unquote_plus( params.get("plot") )
	titleinfo = urllib.unquote_plus( params.get("titleinfo") )
	titlesearch = ""
	matchtitlesearch = re.match('\w',titleinfo)
	if (matchtitlesearch):
		titlesearch = matchtitlesearch.group(0)
	titlemcanime = urllib.unquote_plus( params.get("titlemcanime") )
	tcsearch = urllib.unquote_plus( params.get("tcsearch") )
	listaseries = []
	listaseriesmc = []
	seriesencontradas = []
	genero = category

	listainfomc = findlistinfo("",title,url)

	if plot == "McAnime-Enciclopedia":
		data = scrapertools.cachePage("http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
		listaseries = findcontenidos(data,"Completo",tcsearch,titlesearch,"")
		urltodas = re.sub('enciclopedia','descarga_directa',url)
		listaseriesmc = findseriesmc(urltodas)
			
	# Añade al listado de XBMC
	additem( CHANNELNAME , category , listainfomc[0][0]+": Información McAnime - Enciclopedia Beta" , "" , "" , listainfomc[0][5] )
	additem( CHANNELNAME , category , "Clasificación: "+listainfomc[0][1] , "" , "" , listainfomc[0][5] )
	additem( CHANNELNAME , category , "Géneros: "+listainfomc[0][2] , "" , "" , listainfomc[0][5] )
	additem( CHANNELNAME , category , "Contenido: "+listainfomc[0][3] , "" , "" , listainfomc[0][5] )
	additem( CHANNELNAME , category , "Sinopsis: "+listainfomc[0][4] , "" , "" , listainfomc[0][5] )

	if len(listaseries)>0:
		listaseries.sort(key=lambda serie: serie[6].lower())
		tituloencontrado = "0"
		tituloencontrado2 = "0"
		titlemcanimesearch = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',titlemcanime)
		for serie in listaseries:
			titleerdm = serie[6]			
			forgenre = re.match(titlemcanimesearch+'$',titleerdm,re.IGNORECASE)
			if (forgenre):
				seriesencontradas.append(serie)
				tituloencontrado = "-1"
			else:
				forgenre1 = re.match('^'+titlemcanimesearch+'.+$',titleerdm,re.IGNORECASE)
				if (forgenre1):
					if tituloencontrado == "-1":
						break
					elif tituloencontrado2 == "-1" and serie[0]<>seriesencontradas[-1][0]:
						break
					else:
						seriesencontradas.append(serie)
						tituloencontrado2 == "-1"
													
		if len(seriesencontradas)>0:
			additem( CHANNELNAME , category , "Releases encontradas en El Rincón del Manga: " , "" , "" , "" )
			seriesencontradas.sort(key=lambda serie: serie[0].lower())
			for serie in seriesencontradas:	
				adderdmfolder( CHANNELNAME , "detail" , genero+"  -  El Rincón del Manga" , serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , listainfomc[0][6] , "eRdM" , serie[0] , serie[5] , serie[6] )
	
	if plot == "McAnime-Enciclopedia":
		category = category+"  -  McAnime-Enciclopedia  -  Releases"
		addsimplefolder( CHANNELNAME , "search" , "El Rincón del Manga  -  Anime" , "[+] Buscar en El Rincón del Manga","http://www.elrincondelmanga.com/foro/showthread.php?t=75282", "" ,"Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
	else:
		category = "McAnime-Enciclopedia"

	if len(listaseriesmc)>0:
		additem( CHANNELNAME , category , "Releases en McAnime: " , "" , "" , "" )
		for seriemc in listaseriesmc:	
			addmcarelfolder( CHANNELNAME , "detail3" , genero+"  -  McAnime" , seriemc[0]+seriemc[2] , seriemc[1] , listainfomc[0][6] , listainfomc[0][5] , listainfomc[0][0]+": Información McAnime - Enciclopedia Beta" , "Clasificación: "+listainfomc[0][1] , "Géneros: "+listainfomc[0][2] , "Contenido: "+listainfomc[0][3] , "Sinopsis: "+listainfomc[0][4] )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )	

def searchmc(params,url,category):
	xbmc.output("[animeforos.py] searchmc")

	title = urllib.unquote_plus( params.get("title") )
	plot = urllib.unquote_plus( params.get("plot") )
	category = "McAnime-Enciclopedia"
	resultado = ""
	tecleado = ""
	seriesencontradas = []
	tcsearch = "[^\)]+"
	tipocontenido = "[^<]+"
	genreurl = ""
	genre = ""
	tecseleccion = 0
	opciones = []
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
	if plot == "genreTodos":
		genre = "McAnime-Enciclopedia"
	if plot == "genre":
		opciones.append("Listado búsqueda directa en El Rincón del Manga")
		opciones.append("Mostrar Todos")
		tecseleccion = 2
		genreurl = url
		genre = "McAnime-Enciclopedia"
		category = title+"  -  McAnime-Enciclopedia"
	opciones.append("Teclado")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	if plot == "genre":
		seleccion = searchtype.select("Búsqueda por Título o Inicial en McAnime-Enciclopedia:", opciones)
	else:
		seleccion = searchtype.select("Búsqueda por Inicial del Título en McAnime-Enciclopedia:", opciones)
	if seleccion == -1 :return
	if seleccion == 0 and tecseleccion == 2:
		inicial = searchinicial()	
	if seleccion <> tecseleccion:
		selecciontc = searchmctc()
		if selecciontc <> "":
			tcsearch = tipocontenido = selecciontc

	if seleccion == 0 and tecseleccion == 2:
		category = unicode( title, "utf-8" ).encode("iso-8859-1")+"  -  El Rincón del Manga"
		listainfo = findinfo("",inicial,tcsearch,"-1",genreurl,"")
		# Cuadro de diálogo de espera
		if len(listainfo) > 300:
			respuesta = alertcontinuar(inicial,selecciontc)
			if respuesta:
				Dialogespera = xbmcgui.DialogProgress()
  				resultado = Dialogespera.create('pelisalacarta' , 'Espere por favor, la búsqueda puede llevar muchos' , 'minutos...')
			else:
				return
		data = scrapertools.cachePage("http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
		listaseries = findcontenidos(data,"Completo",tipocontenido,inicial,"")
		listaseries.sort(key=lambda serie: serie[6].lower())
		for info in listainfo:
			tituloencontrado = "0"
			tituloencontrado2 = "0"
			titlemcanimesearch = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',info[4])
			for serie in listaseries:
				tcok = "0"
				if info[3][0:3].lower()==serie[5][0:3].lower():
					tcok = "-1"
				elif info[3][0:3].lower()=="w" and serie[5][0:3].lower()=="ova":
					tcok = "-1"
				if seriesencontradas.count(serie)==0 and tcok=="-1":
					titleerdm = serie[6]			
					forgenre = re.match(titlemcanimesearch+'$',titleerdm,re.IGNORECASE)
					if (forgenre):
						seriesencontradas.append(serie)
						tituloencontrado = "-1"
					else:
						forgenre1 = re.match('^'+titlemcanimesearch+'.+$',titleerdm,re.IGNORECASE)
						if (forgenre1):
							if tituloencontrado == "-1":
								break
							elif tituloencontrado2 == "-1" and serie[0]<>seriesencontradas[-1][0]:
								break
							else:
								seriesencontradas.append(serie)
								tituloencontrado2 == "-1"


	elif seleccion == 1 and tecseleccion == 2:
		listainfo = findinfo("","",tcsearch,"-1",genreurl,"")

	elif seleccion == tecseleccion:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
			if len(tecleado)>0:
				selecciontc = searchmctc()
				if selecciontc <> "":
					tcsearch = selecciontc
				listainfo = findinfo("",tecleado,tcsearch,"-1",genreurl,"")
		if keyboard.isConfirmed() is None or len(tecleado)==0:
			return
	else:
		listainfo = findinfo("",letras[seleccion-1-tecseleccion],tcsearch,"-1",genreurl,"")

	if len(listainfo)==0:
		alertnoresultadosearch()
		return

	if len(seriesencontradas)==0:	
		for info in listainfo:
			addmcafolder( CHANNELNAME , "findinfo2" , title , info[0]+"  -  [McAnime-Enciclopedia]" , info[1] , "" , genre , info[2] , info[3] , info[4] )
	else:
		seriesencontradas.sort(key=lambda serie: serie[0].lower())
		for serie in seriesencontradas:	
			adderdmfolder( CHANNELNAME , "detail" , category , serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )

					
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

	if len(listainfo)>300 and resultado<>"":
		Dialogespera.close()

def searchmctc():
	xbmc.output("[animeforos.py] searchmctc")

	selecciontctx = ""
	opciones = []
	opciones.append("Todos  (opción por defecto)")
	opciones.append("Series")
	opciones.append("Ovas")
	opciones.append("Películas")
	opciones.append("Especiales")
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Seleccione un Tipo de Contenido:", opciones)

	if seleccion == 1:
		selecciontctx = "Serie"
	elif seleccion == 2:
		selecciontctx = "Ova"
	elif seleccion == 3:
		selecciontctx = "Pelicula"
	elif seleccion == 4:
		selecciontctx = "Especial"
	
	return selecciontctx

def searchinicial():
	xbmc.output("[animeforos.py] searchinicial")

	opciones = []
	letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	opciones.append("Mostrar Todos  (opción por defecto)")
	for letra in letras:
		opciones.append(letra)
	searchtype = xbmcgui.Dialog()
	seleccion = searchtype.select("Filtrado por Inicial del Título:", opciones)

	selinicial = ""	
	if seleccion > 0:
		selinicial = letras[seleccion-1]

	return selinicial

def genres(params,url,category):
	xbmc.output("[animeforos.py] genres")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)

	listagenres = findgenres(data)

	addsimplefolder( CHANNELNAME , "searchmc" , category , "Todos" , "" , "" , "genreTodos" )

	for genre in listagenres:
		addsimplefolder( CHANNELNAME , "searchmc" , category , genre[0] , genre[1] , "" , "genre" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def findgenres(data):
	xbmc.output("[animeforos.py] findgenres")
	genreslist = []

	patronvideos  = '<a\s+href="(/enciclopedia/anime/genero/[^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Género
		genre = match[1]
		if genre == "Suspenso":
			genre = "Suspense"
				
		# URL
		url = urlparse.urljoin("http://www.mcanime.net",match[0])

		genreslist.append( [ genre , url ] )

	return genreslist

def findseriesmc(url):
	xbmc.output("[animeforos.py] findseriesmc")
	seriesmclist = []

	data = scrapertools.cachePage(url)

	patronvideos  = '<li class="dd_type"><img.*?title="([^"]+)"\s*/></li>\n'
	patronvideos += '\s+<li class="dd_update">[^<]+<img[^>]+>([^<]+)</li>\n'
	patronvideos += '\s+<li class="dd_title">\n\s+<h5><a href="(/descarga_directa/anime/detalle/[^"]+)">([^<]*\[MU\][^<]*)</a>'
	matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

	for match in matches:
		# Titulo
		titulo = match[3]
		titulo = formatostring(titulo)

		# Fecha Actualización
		match0 = re.search('(\d{4}).(\d{2}).(\d{2})',match[1],re.IGNORECASE)
		if (match0):
			update = match0.group(3)+"-"+match0.group(2)+"-"+match0.group(1)
		else:
			update = match[1]
		
		# Status-Actualización
		status = "  -  ["+match[0]+" ("+update+")]"
		
		# URL
		url = urlparse.urljoin("http://www.mcanime.net",match[2])

		seriesmclist.append( [ titulo , url , status] )

	return seriesmclist

def play(params,url,category):
	xbmc.output("[animeforos.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]	
	xbmc.output("[animeforos.py] thumbnail="+thumbnail)
	xbmc.output("[animeforos.py] server="+server)

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def searchtitle(title):
	title = title.lower()
	title = re.sub('^(?:the|el|las?|los?)[^\w]+','',title)
	title = re.sub('[^\w]+(?:the|el|las?|los?)[^\w]+',' ',title)
	title = re.sub('[^\w]+(?:pel(?:í|i)cula|movie|vs|versus)[^\w]+',' ',title)
	title = re.sub('[^\w]+(?:pel(?:í|i)cula|movie)$','',title)
	title = re.sub('[^\w]+','',title)
	return title

def formatostring(cadena):
	cadena = cadena.replace('\n' , '')
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
	cadena = re.sub('^X$','X- Clamp',cadena)
	cadena = re.sub('&#\d{3};','-',cadena)
	cadena = re.sub('&#\d{4};','',cadena)
	return cadena

def alertnoresultados():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'Contenido no disponible.' , 'No se han encontrado vídeos.')

def alertnoresultadosearch():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Msj. Informativo:' , 'La Búsqueda no ha obtenido Resultados.' , '')

def alertcontinuar(inicial,selecciontc):
	advertencia = xbmcgui.Dialog()
	linea2 = ""
	linea3 = "¿Desea continuar?"
	if inicial=="" and selecciontc=="":
		linea2 = "Para buscar más rápido seleccione una Inicial y/o"
		linea3 = "un Tipo de Contenido. ¿Desea continuar?"
	elif inicial=="" and selecciontc<>"":
		linea2 = "Para buscar más rápido seleccione una Inicial."
	elif inicial<>"" and selecciontc=="":
		linea2 = "Para buscar más rápido seleccione un Tipo de Contenido."
	resultado = advertencia.yesno('pelisalacarta' , 'La Búsqueda puede llevar muchos minutos.' , linea2 , linea3 )
	return resultado

def addsimplefolder( canal , accion , category , title , url , thumbnail , plot ):
	xbmc.output("[animeforos.py] addsimplefolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , titleinfo , tcsearch):
	xbmc.output("[animeforos.py] addnewfolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&titleinfo=%s&tcsearch=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( titleinfo ) , urllib.quote_plus( tcsearch ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def adderdmfolder( canal , accion , category , title , url , thumbnail , plot , titleinfo , tcsearch , titleerdm):
	xbmc.output("[animeforos.py] adderdmfolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&titleinfo=%s&tcsearch=%s&titleerdm=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( titleinfo ) , urllib.quote_plus( tcsearch ) , urllib.quote_plus( titleerdm ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addmcafolder( canal , accion , category , title , url , thumbnail , plot , titleinfo , tcsearch , titlemcanime):
	xbmc.output("[animeforos.py] addmcafolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&titleinfo=%s&tcsearch=%s&titlemcanime=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( titleinfo ) , urllib.quote_plus( tcsearch ) , urllib.quote_plus( titlemcanime ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addmcarelfolder( canal , accion , category , title , url , thumbnail , plot , info1 , info2 , info3 , info4 , info5):
	xbmc.output("[animeforos.py] addmcarelfolder")
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&info1=%s&info2=%s&info3=%s&info4=%s&info5=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) ,  urllib.quote_plus( info1 ) , urllib.quote_plus( info2 ) , urllib.quote_plus( info3 ) , urllib.quote_plus( info4 ) , urllib.quote_plus( info5 ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
	xbmc.output('[animeforos.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")"')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def additem( canal , category , title , url , thumbnail, plot ):
	xbmc.output('[animeforos.py] additem')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultHardDisk.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
	itemurl = '%s?channel=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)
