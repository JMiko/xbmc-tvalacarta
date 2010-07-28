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
import logger

CHANNELNAME = "divxonline"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[divxonline.py] init")

DEBUG = True
Generate = False # poner a true para generar listas de peliculas
Notas = False # indica si hay que a�adir la nota a las pel�culas
LoadThumbs = True # indica si deben cargarse los carteles de las pel�culas; en MacOSX cuelga a veces el XBMC

def mainlist(params,url,category):
	logger.info("[divxonline.py] mainlist")

	xbmctools.addnewfolder( CHANNELNAME , "novedades" , CHANNELNAME , "Novedades" , "http://www.divxonline.info/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "megavideo" , CHANNELNAME , "Pel�culas en Megavideo" , "" , "", "" )
#	xbmctools.addnewfolder( CHANNELNAME , "veoh" , CHANNELNAME , "Pel�culas en Veoh" , "" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "pelisconficha" , CHANNELNAME , "Estrenos" , "http://www.divxonline.info/peliculas-estreno/1.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "pelisporletra" , CHANNELNAME , "Pel�culas de la A a la Z" , "" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "pelisporanio" , CHANNELNAME , "Pel�culas por a�o de estreno" , "" , "", "" )

	if config.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def novedades(params,url,category):
	logger.info("[divxonline.py] novedades")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Extrae las entradas
	'''
	<td class="contenido"><a href="/pelicula/8853/Conexion-Tequila-1998/"><img src="http://webs.ono.com/jeux/divxonline.info_conexiontequila.jpg" style="padding: 5px;"  border="0" width="150" height="200" align="left" alt="Conexi�n Tequila (1998)" title="Conexi�n Tequila (1998)" />
	<font color="#000000"><b>G�nero:</b></font> <a href="/peliculas/50/Accion-Megavideo/"><font color="#0066FF">Accion (Megavideo)</font></a><br />
	<b>T�tulo:</b> <a href="/pelicula/8853/Conexion-Tequila-1998/"><font color="#0066FF"><b>Conexi�n Tequila (1998) - </b></font></a>
	<b>Director(es):</b> <a href="/director/2917/Robert-Towne/"><font color="#0066FF">Robert Towne </font></a>
	<b> - A�o de estreno:</b><a href="/peliculas-anho/1998/1.html"><font color="#0066FF"> 1998</a></font> -
	<b>Autorizada:</b> <a href="/peliculas/Todos-los-publicos/1/"><font color="#0066FF"> Todos los publicos - </a></font>
	<b>Vista:</b><font color="#0066FF"> 1103 veces - </font><b>Colaborador(es):</b><font color="#0066FF"> jacinto</font><br /><BR><b>Sinopsis:</b> Nick y McKussic son amigos desde ni�os, pero ahora Nick es teniente de polic�a y McKussic el mejor traficante de drogas de la ciudad. Se prepara una operaci�n de mil doscientos kilos de coca�na y la Brigada Antinarc�ticos cree que McKussic va a coordinar la entrega.
	<a href="/pelicula/8853/Conexion-Tequila-1998/"> <font color="#0066FF">(leer m�s)</font></a><br><br>
	<a href="/pelicula/8853/Conexion-Tequila-1998/" style="font-weight: bold; font-size: 11pt">
	<img src="http://webs.ono.com/divx/imagenes/flecha.png" border="0"> <font size="3" color="#0066FF">Conexi�n Tequila (1998)</font></a></td>
	<td>
	'''
	patronvideos  = '<td class="contenido"><a href="([^"]+)"><img src="([^"]+)".*?title="([^"]+)"[^>]+>.*?'
	patronvideos += '<b>Sinopsis:</b>([^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[2]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = "" # = match[1]
		scrapedplot = match[3]
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<a href="peliculas-online-divx-1.html" style="border: 1px solid rgb(0, 51, 102); margin: 2px; padding: 2px; text-decoration: none; color: white; background-color: rgb(0, 51, 102);" onmouseover="javascript:style.backgroundColor='#963100';" onmouseout="javascript:style.backgroundColor='#003366';">1-15</a>
	#<a href="peliculas-online-divx-2.html" style="border: 1px solid rgb(0, 51, 102); margin: 2px; padding: 2px; text-decoration: none; color: black; background-color: rgb(202, 217, 234);" onmouseover="javascript:style.backgroundColor='#ececd9';" onmouseout="javascript:style.backgroundColor='#cad9ea';">16-30</a>
	patronvideos  = '<a href="[^"]+" style="border: 1px solid rgb(0, 51, 102); margin: 2px; padding: 2px; text-decoration: none; color: white[^>]+>[^<]+</a><a href="([^"]+)" style="border: 1px solid rgb(0, 51, 102); margin: 2px; padding: 2px; text-decoration: none; color: black[^>]+>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		xbmctools.addnewfolder( CHANNELNAME , "novedades" , category , "!P�gina siguiente (matches[0][1]" , urlparse.urljoin(url,matches[0][0]) , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def megavideo(params,url,category):
	logger.info("[divxonline.py] megavideo")

	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Acci�n" , "http://www.divxonline.info/peliculas/50/accion-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Animaci�n" , "http://www.divxonline.info/peliculas/53/animacion-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Anime" , "http://www.divxonline.info/peliculas/51/anime-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Aventura" , "http://www.divxonline.info/peliculas/52/aventura-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "B�licas" , "http://www.divxonline.info/peliculas/95/belicas-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Ciencia Ficci�n" , "http://www.divxonline.info/peliculas/55/ciencia-ficcion-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Cl�sico" , "http://www.divxonline.info/peliculas/58/cine-clasico-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine espa�ol" , "http://www.divxonline.info/peliculas/57/cine-espa%C3%B1ol-megavideo/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cl�sicos Disney" , "http://www.divxonline.info/peliculas/59/clasicos-disney-megavideo/" , "", "" )
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
	logger.info("[divxonline.py] veoh")

	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Acci�n" , "http://www.divxonline.info/peliculas/30/accion-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Animaci�n" , "http://www.divxonline.info/peliculas/33/animacion-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Anime" , "http://www.divxonline.info/peliculas/41/anime-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Aventura" , "http://www.divxonline.info/peliculas/32/aventura-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "B�licas" , "http://www.divxonline.info/peliculas/96/belicas-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Ciencia Ficci�n" , "http://www.divxonline.info/peliculas/35/ciencia-ficcion-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Cl�sico" , "http://www.divxonline.info/peliculas/38/cine-clasico-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Espa�ol" , "http://www.divxonline.info/peliculas/37/cine-espa�ol-veoh/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cl�sicos Disney" , "http://www.divxonline.info/peliculas/39/clasicos-disney-veoh/" , "", "" )
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
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def stepinto (url, data, pattern): # expand a page adding "next page" links given some pattern
	# Obtiene el trozo donde est�n los links a todas las p�ginas de la categor�a
	match = re.search(pattern,data)
	trozo = match.group(1)
	#logger.info(trozo)

	# carga todas las paginas juntas para luego extraer las urls
	patronpaginas = '<a href="([^"]+)"'
	matches = re.compile(patronpaginas,re.DOTALL).findall(trozo)
	#scrapertools.printMatches(matches)
	res = ''
	for match in matches:
		urlpage = urlparse.urljoin(url,match)
		#logger.info(match)
		#logger.info(urlpage)
		res += scrapertools.cachePage(urlpage)
	return res


html_escape_table = {
	"&ntilde;": "�", "&iquest;": "�", "&iexcl;": "�"
}
def removeacutes (s):
	for exp in html_escape_table.iterkeys():
		s = s.replace(exp,html_escape_table[exp])
	return s
		

def pelisporletra(params,url,category):
	logger.info("[divxonline.py] pelisporletra")

	letras = "9ABCDEFGHIJKLMN�OPQRSTUVWXYZ" # el 9 antes era 1, que curiosamente est� mal en la web divxonline (no funciona en el navegador)
	for letra in letras:
		xbmctools.addnewfolder( CHANNELNAME , "pelisconfichaB" , CHANNELNAME , str(letra) , "http://www.divxonline.info/verpeliculas/"+str(letra)+"_pagina_1.html" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def pelisporanio(params,url,category):
	logger.info("[divxonline.py] pelisporanio")

	for anio in range(2009,1915,-1):
		xbmctools.addnewfolder( CHANNELNAME , "pelisconficha" , CHANNELNAME , str(anio) , "http://www.divxonline.info/peliculas-anho/"+str(anio)+"/1.html" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

	
def pelisconficha(params,url,category): # fichas en listados por a�o y en estrenos
	logger.info("[divxonline.py] pelisconficha")
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Extrae las entradas
	patronvideos  = '<td class="contenido"><a href="(.*?)">' # link
	patronvideos += '<img src="(.*?)"' # cartel
	patronvideos += '.*?title="(.*?)"' # t�tulo
#	patronvideos += '.*?<b>Descripci�n:</b>(.*?)\.\.\.'
		
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
		scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la p�gina de reproducci�n

		# Thumbnail
		scrapedthumbnail = ""
		if LoadThumbs:
			scrapedthumbnail = match[1]

		# procesa el resto
		scrapeddescription = "" #match[3]

		# Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listmirrors" )


	# a�ade siguiente p�gina
	match = re.search('(.*?)(\d+?)(\.html)',url)
	logger.info("url="+url)
	pag = match.group(2)
	newpag = match.group(1) + str(int(pag)+1) + match.group(3)
	logger.info("newpag="+newpag)
	xbmctools.addnewfolder( CHANNELNAME , "pelisconficha" , CHANNELNAME , "Siguiente" , newpag , "", "" )
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
		

import time
def pelisconfichaB(params,url,category): # fichas con formato en entradas alfab�ticas
	logger.info("[divxonline.py] pelisconfichaB")
	t0 = time.time()
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# carga N p�ginas
	N = 10
	match = re.search('(.*?)(\d+?)(\.html)',url)
	pag = int(match.group(2))
	#logger.info("pag="+match.group(2))
	
	for i in range(pag+1,pag+N):
		newurl = match.group(1) + str(i) + match.group(3)
		data += scrapertools.cachePage(newurl)

	nexturl = match.group(1) + str(pag+N) + match.group(3)

	# Extrae las entradas
	patronvideos  = '<td class="contenido"><img src="(.*?)"' # cartel
	patronvideos += '.*?alt="(.*?)"' # t�tulo
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
		scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la p�gina de reproducci�n

		# Thumbnail
		scrapedthumbnail = ""
		if LoadThumbs:
			scrapedthumbnail = match[0]

		# procesa el resto
		scrapeddescription = "" # match[3]

		# Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listmirrors" )


	# a�ade siguiente p�gina
	xbmctools.addnewfolder( CHANNELNAME , "pelisconfichaB" , CHANNELNAME , "Siguiente" , nexturl , "", "" )
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
	if DEBUG:
		logger.info("Tiempo de ejecuci�n = "+str(time.time()-t0))

def movielist(params,url,category): # pelis sin ficha (en listados por g�nero)
	logger.info("[divxonline.py] movielist")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	data = stepinto(url,data,'Ver p�gina:(.*?)</p>')

	# Extrae las entradas (carpetas)
	patronvideos  = '<li><a href="([^"]+)">(.*?)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)

	if (Generate):
		f = open(config.DATA_PATH+'/films.tab', 'w') # fichero para obtener las notas

	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		if (not Generate and Notas):
			score = anotador.getscore(match[1])
			if (score != ""):
				scrapedtitle += " " + score

		# URL
		scrapedurl = urlparse.urljoin(url,match[0]) # url de la ficha divxonline
		scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la p�gina de reproducci�n

		# Thumbnail
		#scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedthumbnail = ""

		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		if (Generate):
			sanio = re.search('(.*?)\((.*?)\)',scrapedtitle)
			if (sanio): # si hay anio
				fareg = sanio.group(1) + "\t" + sanio.group(2) + "\t" + scrapedtitle
			else:
				fareg = scrapedtitle + "\t\t" + scrapedtitle
			f.write(fareg+"\n")

		# A�ade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listmirrors" )
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

	if (Generate):
		f.close()


def listmirrors(params,url,category):
	logger.info("[divxonline.py] listmirrors")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	data = scrapertools.cachePage(url) # descarga pagina de reproduccion
	'''
	<a style="color: #f2ac03; font-weight: bold; font-size: 12pt" href="/pelicula-divx/8853/Conexion-Tequila-1998/" target="_self" style="font-weight: bold; font-size: 11pt">
	<h2><align="center"><font size="4"><img src="http://webs.ono.com/mis-videos/imagenes/filmes.png" border="0">&nbsp;Ver Pel�cula Online: Conexi�n Tequila (1998)</font></h2></a>
	'''
	patronvideos  = '<a style="[^"]+" href="([^"]+)"[^<]+'
	patronvideos += '<h2><align[^>]+><font[^>]+><img[^>]+>.nbsp.Ver Pel'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		scrapedurl = urlparse.urljoin(url,match)
		if (DEBUG): logger.info("url=["+scrapedurl+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , title + " [online]" , scrapedurl , thumbnail, plot )

	'''
	<a href="/descarga-directa/8853/Conexion-Tequila-1998/" style="color: #f2ac03; font-weight: bold; font-size: 12pt;">Descarga Directa de: Conexi�n Tequila (1998)</a>
	'''
	patronvideos  = '<a href="([^"]+)"[^>]+>Descarga Directa'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		scrapedurl = urlparse.urljoin(url,match)
		if (DEBUG): logger.info("url=["+scrapedurl+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , title + " [descarga]" , scrapedurl , thumbnail, plot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	logger.info("[divxonline.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	logger.info("[divxonline.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	logger.info("[divxonline.py] thumbnail="+thumbnail)
	logger.info("[divxonline.py] server="+server)

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")








