# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxonline
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
import servertools
import binascii
import xbmctools
import anotador
import config

CHANNELNAME = "divxonline"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[divxonline.py] init")

DEBUG = False
Generate = False # poner a true para generar listas de peliculas
Notas = False # indica si hay que añadir la nota a las películas
LoadThumbs = True # indica si deben cargarse los carteles de las películas; en MacOSX cuelga a veces el XBMC

def mainlist(params,url,category):
	xbmc.output("[divxonline.py] mainlist")

	xbmctools.addnewfolder( CHANNELNAME , "megavideo" , CHANNELNAME , "Películas en Megavideo" , "" , "", "" )
#	xbmctools.addnewfolder( CHANNELNAME , "veoh" , CHANNELNAME , "Películas en Veoh" , "" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "pelisconficha" , CHANNELNAME , "Estrenos" , "http://www.divxonline.info/peliculas-estreno/1.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "pelisporletra" , CHANNELNAME , "Películas de la A a la Z" , "" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "pelisporanio" , CHANNELNAME , "Películas por año de estreno" , "" , "", "" )

	if config.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def megavideo(params,url,category):
	xbmc.output("[divxonline.py] megavideo")

	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Acción" , "http://www.divxonline.info/peliculas/50/accion-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Animación" , "http://www.divxonline.info/peliculas/53/animacion-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Anime" , "http://www.divxonline.info/peliculas/51/anime-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Aventura" , "http://www.divxonline.info/peliculas/52/aventura-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Bélicas" , "http://www.divxonline.info/peliculas/95/belicas-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Ciencia Ficción" , "http://www.divxonline.info/peliculas/55/ciencia-ficcion-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Clásico" , "http://www.divxonline.info/peliculas/58/cine-clasico-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine español" , "http://www.divxonline.info/peliculas/57/cine-espa%C3%B1ol-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Clásicos Disney" , "http://www.divxonline.info/peliculas/59/clasicos-disney-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Comedias" , "http://www.divxonline.info/peliculas/60/comedias-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Documentales" , "http://www.divxonline.info/peliculas/54/documentales-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Drama" , "http://www.divxonline.info/peliculas/62/drama-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Infantil" , "http://www.divxonline.info/peliculas/63/infantil-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Musicales" , "http://www.divxonline.info/peliculas/64/musicales-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Suspense" , "http://www.divxonline.info/peliculas/65/suspense-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Terror" , "http://www.divxonline.info/peliculas/66/terror-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Western" , "http://www.divxonline.info/peliculas/67/western-megavideo/" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def veoh(params,url,category):
	xbmc.output("[divxonline.py] veoh")

	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Acción" , "http://www.divxonline.info/peliculas/30/accion-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Animación" , "http://www.divxonline.info/peliculas/33/animacion-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Anime" , "http://www.divxonline.info/peliculas/41/anime-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Aventura" , "http://www.divxonline.info/peliculas/32/aventura-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Bélicas" , "http://www.divxonline.info/peliculas/96/belicas-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Ciencia Ficción" , "http://www.divxonline.info/peliculas/35/ciencia-ficcion-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Clásico" , "http://www.divxonline.info/peliculas/38/cine-clasico-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Español" , "http://www.divxonline.info/peliculas/37/cine-español-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Clásicos Disney" , "http://www.divxonline.info/peliculas/39/clasicos-disney-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Comedias" , "http://www.divxonline.info/peliculas/40/comedias-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cortometrajes" , "http://www.divxonline.info/peliculas/41/cortometrajes-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Documentales" , "http://www.divxonline.info/peliculas/34/documentales-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Drama" , "http://www.divxonline.info/peliculas/42/dramas-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Infantiles" , "http://www.divxonline.info/peliculas/43/infantiles-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Musicales" , "http://www.divxonline.info/peliculas/44/musicales-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Suspense" , "http://www.divxonline.info/peliculas/45/suspense-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Terror" , "http://www.divxonline.info/peliculas/46/terror-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Western" , "http://www.divxonline.info/peliculas/49/western-veoh/" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def stepinto (url, data, pattern): # expand a page adding "next page" links given some pattern
	# Obtiene el trozo donde están los links a todas las páginas de la categoría
	match = re.search(pattern,data)
	trozo = match.group(1)
	#xbmc.output(trozo)

	# carga todas las paginas juntas para luego extraer las urls
	patronpaginas = '<a href="([^"]+)"'
	matches = re.compile(patronpaginas,re.DOTALL).findall(trozo)
	#scrapertools.printMatches(matches)
	res = ''
	for match in matches:
		urlpage = urlparse.urljoin(url,match)
		#xbmc.output(match)
		#xbmc.output(urlpage)
		res += scrapertools.cachePage(urlpage)
	return res


html_escape_table = {
	"&ntilde;": "ñ", "&iquest;": "¿", "&iexcl;": "¡"
}
def removeacutes (s):
	for exp in html_escape_table.iterkeys():
		s = s.replace(exp,html_escape_table[exp])
	return s
		

def pelisporletra(params,url,category):
	xbmc.output("[divxonline.py] pelisporletra")

	letras = "9ABCDEFGHIJKLMNÑOPQRSTUVWXYZ" # el 9 antes era 1, que curiosamente está mal en la web divxonline (no funciona en el navegador)
	for letra in letras:
		xbmctools.addnewfolder( CHANNELNAME , "pelisconfichaB" , CHANNELNAME , str(letra) , "http://www.divxonline.info/verpeliculas/"+str(letra)+"_pagina_1.html" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def pelisporanio(params,url,category):
	xbmc.output("[divxonline.py] pelisporanio")

	for anio in range(2009,1915,-1):
		xbmctools.addnewfolder( CHANNELNAME , "pelisconficha" , CHANNELNAME , str(anio) , "http://www.divxonline.info/peliculas-anho/"+str(anio)+"/1.html" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

	
def pelisconficha(params,url,category): # fichas en listados por año y en estrenos
	xbmc.output("[divxonline.py] pelisconficha")
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas
	patronvideos  = '<td class="contenido"><a href="(.*?)">' # link
	patronvideos += '<img src="(.*?)"' # cartel
	patronvideos += '.*?title="(.*?)"' # título
#	patronvideos += '.*?<b>Descripción:</b>(.*?)\.\.\.'
		
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = removeacutes(match[2])
		if (not Generate and Notas):
			score = anotador.getscore(match[2])
			if (score != ""):
				scrapedtitle += " " + score

		# URL
		scrapedurl = urlparse.urljoin(url,match[0]) # url de la ficha divxonline
		scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción

		# Thumbnail
		scrapedthumbnail = ""
		if LoadThumbs:
			scrapedthumbnail = match[1]

		# procesa el resto
		scrapeddescription = "" #match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )


	# añade siguiente página
	match = re.search('(.*?)(\d+?)(\.html)',url)
	xbmc.output("url="+url)
	pag = match.group(2)
	newpag = match.group(1) + str(int(pag)+1) + match.group(3)
	xbmc.output("newpag="+newpag)
	xbmctools.addnewfolder( CHANNELNAME , "pelisconficha" , CHANNELNAME , "Siguiente" , newpag , "", "" )
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
		

import time
def pelisconfichaB(params,url,category): # fichas con formato en entradas alfabéticas
	xbmc.output("[divxonline.py] pelisconfichaB")
	t0 = time.time()
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# carga N páginas
	N = 10
	match = re.search('(.*?)(\d+?)(\.html)',url)
	pag = int(match.group(2))
	#xbmc.output("pag="+match.group(2))
	
	for i in range(pag+1,pag+N):
		newurl = match.group(1) + str(i) + match.group(3)
		data += scrapertools.cachePage(newurl)

	nexturl = match.group(1) + str(pag+N) + match.group(3)

	# Extrae las entradas
	patronvideos  = '<td class="contenido"><img src="(.*?)"' # cartel
	patronvideos += '.*?alt="(.*?)"' # título
	patronvideos += '.*?<b>Sinopsis.*?<a href="(.*?)"' # url
		
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = removeacutes(match[1]) # 7.49 seg 
#		scrapedtitle = match[1] # 7.33 seg
		if (not Generate and Notas):
			score = anotador.getscore(match[1])
			if (score != ""):
				scrapedtitle += " " + score

		# URL
		scrapedurl = urlparse.urljoin(url,match[2]) # url de la ficha divxonline
		scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción

		# Thumbnail
		scrapedthumbnail = ""
		if LoadThumbs:
			scrapedthumbnail = match[0]

		# procesa el resto
		scrapeddescription = "" # match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )


	# añade siguiente página
	xbmctools.addnewfolder( CHANNELNAME , "pelisconfichaB" , CHANNELNAME , "Siguiente" , nexturl , "", "" )
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
	if DEBUG:
		xbmc.output("Tiempo de ejecución = "+str(time.time()-t0))

def movielist(params,url,category): # pelis sin ficha (en listados por género)
	xbmc.output("[divxonline.py] movielist")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	data = stepinto(url,data,'Ver página:(.*?)</p>')

	# Extrae las entradas (carpetas)
	patronvideos  = '<li><a href="([^"]+)">(.*?)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)

	if (Generate):
		f = open(os.getcwd()+'/films.tab', 'w') # fichero para obtener las notas

	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		if (not Generate and Notas):
			score = anotador.getscore(match[1])
			if (score != ""):
				scrapedtitle += " " + score

		# URL
		scrapedurl = urlparse.urljoin(url,match[0]) # url de la ficha divxonline
		scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción

		# Thumbnail
		#scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedthumbnail = ""

		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		if (Generate):
			sanio = re.search('(.*?)\((.*?)\)',scrapedtitle)
			if (sanio): # si hay anio
				fareg = sanio.group(1) + "\t" + sanio.group(2) + "\t" + scrapedtitle
			else:
				fareg = scrapedtitle + "\t\t" + scrapedtitle
			f.write(fareg+"\n")

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

	if (Generate):
		f.close()


def detail(params,url,category):
	xbmc.output("[divxonline.py] detail")

	title = params.get("title")
	thumbnail = params.get("thumbnail")
	xbmc.output("[divxonline.py] title="+title)
	xbmc.output("[divxonline.py] thumbnail="+thumbnail)

	data0 = scrapertools.cachePage(url) # descarga pagina de reproduccion
	
	# tipo 1: hay un iframe con una página con los videos
	# obtiene la url del frame con los videos	
	match = re.search('<iframe src="(.*?)"',data0,re.DOTALL | re.IGNORECASE)
	
	if match:
		xbmc.output("URLVideo: " + match.group(1)) # los cambios suelen afectar por aquí
		
		# Descarga el frame con los videos
		data = scrapertools.cachePage(urlparse.urljoin(url,match.group(1)))
		#xbmc.output(data)

		listavideos = servertools.findvideos(data)

	else:
		# tipo 2: los vídeos están en la página (no sé si sigue siendo vigente)
		listavideos = servertools.findvideos(data0)


	# ------------------------------------------------------------------------------------
	# Añade los enlaces a los videos
	# ------------------------------------------------------------------------------------
	for video in listavideos:
		xbmctools.addvideo( CHANNELNAME , "Megavideo - "+video[0] , video[1] , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[divxonline.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[divxonline.py] thumbnail="+thumbnail)
	xbmc.output("[divxonline.py] server="+server)

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")








