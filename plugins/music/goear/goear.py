# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# goear - XBMC Plugin
# Main
# http://blog.tvalacarta.info/plugin-xbmc/goear/
#------------------------------------------------------------

# Librerias de sistema
import os
import sys
import xbmc
import urllib,urllib2
import urlparse
import re
import xbmcplugin
import xbmcgui
from xml.dom import minidom

# Configura los directorios donde hay librerías
sys.path.append (xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) ))

# Resto de librerias
import scrapertools

DEBUG=True

def mainlist(params,url,category):
	xbmc.output("[goear.py] mainlist")

	# Verifica actualizaciones solo en el primer nivel
	if xbmcplugin.getSetting("updatecheck2") == "true":
		xbmc.output("updatecheck2=true")
		import updater
		updater.checkforupdates()
	else:
		xbmc.output("updatecheck2=false")

	addnewfolder( "categorias"   , "Categorías"    , "http://www.goear.com/categories.php" )
	addnewfolder( "grupos"       , "Grupos"        , "http://www.goear.com/groups.php" )
	addnewfolder( "search"       , "Buscar"        , "" )
	addnewfolder( "configuracion", "Configuración" , "" )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="Canales" )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def configuracion(params,url,category):
	xbmc.output("[goear.py] configuracion")
	xbmcplugin.openSettings( sys.argv[ 0 ] )

def grupos(params, url, category):
	xbmc.output("[goear.py] grupos")

	addnewfolder( "listgrupos", "A","http://www.goear.com/groups.php?o=a")
	addnewfolder( "listgrupos", "B","http://www.goear.com/groups.php?o=b")
	addnewfolder( "listgrupos", "C","http://www.goear.com/groups.php?o=c")
	addnewfolder( "listgrupos", "D","http://www.goear.com/groups.php?o=d")
	addnewfolder( "listgrupos", "E","http://www.goear.com/groups.php?o=e")
	addnewfolder( "listgrupos", "F","http://www.goear.com/groups.php?o=f")
	addnewfolder( "listgrupos", "G","http://www.goear.com/groups.php?o=g")
	addnewfolder( "listgrupos", "H","http://www.goear.com/groups.php?o=h")
	addnewfolder( "listgrupos", "I","http://www.goear.com/groups.php?o=i")
	addnewfolder( "listgrupos", "J","http://www.goear.com/groups.php?o=j")
	addnewfolder( "listgrupos", "K","http://www.goear.com/groups.php?o=k")
	addnewfolder( "listgrupos", "L","http://www.goear.com/groups.php?o=l")
	addnewfolder( "listgrupos", "M","http://www.goear.com/groups.php?o=m")
	addnewfolder( "listgrupos", "N","http://www.goear.com/groups.php?o=n")
	addnewfolder( "listgrupos", "O","http://www.goear.com/groups.php?o=o")
	addnewfolder( "listgrupos", "P","http://www.goear.com/groups.php?o=p")
	addnewfolder( "listgrupos", "Q","http://www.goear.com/groups.php?o=q")
	addnewfolder( "listgrupos", "R","http://www.goear.com/groups.php?o=r")
	addnewfolder( "listgrupos", "S","http://www.goear.com/groups.php?o=s")
	addnewfolder( "listgrupos", "T","http://www.goear.com/groups.php?o=t")
	addnewfolder( "listgrupos", "U","http://www.goear.com/groups.php?o=u")
	addnewfolder( "listgrupos", "V","http://www.goear.com/groups.php?o=v")
	addnewfolder( "listgrupos", "W","http://www.goear.com/groups.php?o=w")
	addnewfolder( "listgrupos", "X","http://www.goear.com/groups.php?o=x")
	addnewfolder( "listgrupos", "Y","http://www.goear.com/groups.php?o=y")
	addnewfolder( "listgrupos", "Z","http://www.goear.com/groups.php?o=z")
	addnewfolder( "listgrupos", "0","http://www.goear.com/groups.php?o=0")
	addnewfolder( "listgrupos", "1","http://www.goear.com/groups.php?o=1")
	addnewfolder( "listgrupos", "2","http://www.goear.com/groups.php?o=2")
	addnewfolder( "listgrupos", "3","http://www.goear.com/groups.php?o=3")
	addnewfolder( "listgrupos", "4","http://www.goear.com/groups.php?o=4")
	addnewfolder( "listgrupos", "5","http://www.goear.com/groups.php?o=5")
	addnewfolder( "listgrupos", "6","http://www.goear.com/groups.php?o=6")
	addnewfolder( "listgrupos", "7","http://www.goear.com/groups.php?o=7")
	addnewfolder( "listgrupos", "8","http://www.goear.com/groups.php?o=8")
	addnewfolder( "listgrupos", "9","http://www.goear.com/groups.php?o=9")

	# Cerrar directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def categorias(params,url,category):
	xbmc.output("[goear.py] listcategorias")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="cate-tipos"><a href="([^"]+)">([^<]+)</a></div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"]")

		# Añade al listado de XBMC
		addnewfolder( "categoryresults" , scrapedtitle , scrapedurl )
	
	patronvideos  = '<div class="flechas" style="float:right;"><a href="([^"]+)"><strong>Siguiente  »</strong></a></div></div>'

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def categoryresults(params,url,category):
	xbmc.output("[goear.py] categoryresults")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#<div class="separador">
	#<div class="b1"> <a href="listen/3540cd8/under-my-skin-rachael-yamagata" class="b1">Under My Skin - (rachael yamagata)</a></div>
	#<div class="b2">i\'m not strong as i seem</div>
	
	patronvideos  = '<div class="separador">[^<]+'
	patronvideos += '<div class="b1"> <a href="([^"]+)" class="b1">([^<]+)</a></div>[^<]+'
	patronvideos += '<div class="b2">([^<]+)</div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]+" - "+match[2]
		scrapedtitle = scrapedtitle.strip()
		scrapedtitle = scrapedtitle.replace("\n"," ")
		scrapedtitle = scrapedtitle.replace("\r"," ")
		scrapedurl = urlparse.urljoin(url,match[0])
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"]")

		# Añade al listado de XBMC
		addnewfile( "play" , scrapedtitle , scrapedurl )
	
	patronvideos  = '<div class="flechas.*?<a href="(.*?)">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches) > 0:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		addnewfolder( "categoryresults" ,scrapedtitle,scrapedurl)
	
	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listgrupos(params,url,category):
	xbmc.output("[goear.py] listgrupos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	'''
	<div class="separador">
	<div class="b1"> <a href="search.php?q=o bahia" class="b1">o bahia</a></div>
	<div class="b2"></div>
	</div>
	'''
	
	patronvideos  = '<div class="separador">[^<]+'
	patronvideos += '<div class="b1"> <a href="([^"]+)" class="b1">([^<]+)</a></div>[^<]+'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"]")

		# Añade al listado de XBMC
		addnewfolder( "searchresults" , scrapedtitle , scrapedurl )
		
	
	patronvideos = '<div class="flechas" style="float:right;"><a href="([^"]+)"><strong>Siguiente.*?'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches) > 0:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		
		addnewfolder( "listgrupos" ,scrapedtitle,scrapedurl)

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[goear.py] search")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.goear.com/search.php?q="+tecleado
			searchresults(params,searchUrl,category)

def searchresults(params,url,category):
	xbmc.output("[goear.py] searchresults")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#<div style="padding-left:13px;"><a title="Escuchar Estopa de estopa" href="listen/77198b5/estopa-estopa" class="b1">Estopa</a></div><div style="color:#978080;font-size:11px;padding-left:13px;">Cancion de estopa, estopa dios</div><div>&nbsp;</div><div style="padding-left:13px;"><a title="Escuchar Estopa de estopa" href="listen/c3950a5/estopa-estopa" class="b1">Estopa</a></div>
	#<div style="padding-left:13px;"><a title="Escuchar Fado Da Adica de amalia rodrigues" href="listen/880e504/fado-da-adica-amalia-rodrigues" class="b1">Fado Da Adica</a></div><div style="float:right"><a target="_blank" onclick="window.open('http://www.goear.com/listenwin.php?v=880e504','Escuchar Fado Da Adica','width=500,height=350,resizable=yes')"><img src="http://www.goear.com/img2/newwin.gif"></a></div><div style="color:#978080;font-size:11px;padding-left:13px;">amalia rodrigues, fado da adica </div><div>&nbsp;</div>
	
	patronvideos  = '<div style="padding-left.13px.">'
	patronvideos += '<a title="([^"]+)" href="([^"]+)" class="b1">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[2]+" - "+match[0]
		scrapedurl = urlparse.urljoin(url,match[1])
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"]")

		# Añade al listado de XBMC
		addnewfile( "play" , scrapedtitle , scrapedurl )
	
	patronvideos = '<div class="flechas" style="float:right;"><a href="([^"]+)"><strong>Siguiente.*?'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches) > 0:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		
		addnewfolder( "searchresults" ,scrapedtitle,scrapedurl)
	

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def addnewfile( accion , title , url ):
	try:
		xbmc.output('[goear.py] addnewfile( "'+accion+'" , "'+title+'" , "' + url + '")')
	except:
		xbmc.output('[goear.py] addnewfile(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultAudio.png" )
	listitem.setInfo( "audio", { "Title" : title } )
	itemurl = '%s?action=%s&title=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( title ) , urllib.quote_plus( url ) )
	xbmcplugin.addDirectoryItem( handle = int( sys.argv[ 1 ] ), url=itemurl, listitem=listitem, isFolder=False)

def addnewfolder( accion , title , url ):
	try:
		xbmc.output('[goear.py] addnewfolder( "'+accion+'" , "'+title+'" , "' + url + '")')
	except:
		xbmc.output('[goear.py] addnewfolder(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png" )
	listitem.setInfo( "audio", { "Title" : title } )
	itemurl = '%s?action=%s&title=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( title ) , urllib.quote_plus( url ) )
	xbmcplugin.addDirectoryItem( handle = int( sys.argv[ 1 ] ), url = itemurl , listitem=listitem, isFolder=True)

def play(params,url,category):
	xbmc.output("[goear.py] play")

	# Recupera el título
	title = urllib.unquote_plus( params.get("title") )

	# A partir de la URL obtiene la URL del MP3
	mediaurl = getmediaurl(url)
	
	# Crea un playlist con la canción
	playlist = createplaylist(title,mediaurl)
	
	launchplayer(playlist)

# Algoritmo para deducir la URL del audio a partir de la URL de la canción en la web (por Emilio)
def getmediaurl(audio_url):
	xbmc.output("[goear.py] getdownloadurl")
	# Encontrar la ID del archivo

	inicio_id = audio_url.find("listen/") + 7
	fin_id = inicio_id + 7
	sst=audio_url[inicio_id]
	audio_id = audio_url[inicio_id:fin_id]

	# Abrir el archivo xml que contiene la información 
	# de la forma http://www.goear.com/hellocalsec.php?f=xxyyzzz

	url_xml = "http://www.goear.com/localtrackhost.php?f=" + audio_id
	data = None

	xmldoc = urllib2.urlopen(url_xml,data)
	xml_data = minidom.parse(xmldoc)
	xmldoc.close()
	data = xml_data.toxml()

	# Buscar la linea "song path=" que es la dirección del archivo
	inicio_path = data.find("path=")
	fin_path = data.find(".mp3")
	path = data[inicio_path + 6:fin_path + 4]
	xbmc.output("[goear.py] path="+path)

	#Buscar nombre del archivo (artista+nombre cancion)

	artista = data[data.find("artist=") + 8:data.find("bild=") - 2]
	xbmc.output("[goear.py] artista="+artista)
	cancion = data[data.find("title=") + 7:data.find("/>") - 1]
	xbmc.output("[goear.py] cancion="+cancion)
	titulo = artista + " - " + cancion
	
	return path

# Crea una playlist para pasársela al reproductor
def createplaylist(title,mediaurl):
	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Creando playlist...', title )
	dialogWait.update(0) #Jur. Para evitar los porcentajes aleatorios

	# Playlist vacia
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()

	# Crea la entrada y la añade al playlist
	listitem = xbmcgui.ListItem( title, iconImage="DefaultAudio.png", path=mediaurl)
	listitem.setInfo( "audio", { "Title": title } )
	playlist.add( mediaurl, listitem )

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	return playlist

# Lanza el reproductor
def launchplayer(playlist):
	# Reproduce

	player_type = xbmc.PLAYER_CORE_AUTO
	xbmcPlayer = xbmc.Player( player_type )
	xbmcPlayer.play(playlist)
