# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para UPV TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import binascii
import xbmctools

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""
	
# Traza el inicio del canal
xbmc.output("[upvtv.py] init")

DEBUG = True

CHANNELNAME = "UPV TV"
CHANNELCODE = "upvtv"

def mainlist(params,url,category):
	xbmc.output("[upvtv.py] mainlist")

	if url=="":
		url="http://www.upv.es/pls/oreg/rtv_web.ListaProg?p_idioma=c"

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data) # hace un print de la captura del html en el log del XBMC

	# Extrae las entradas (carpetas de programas UPV TV)
	'''
	<div id="ventana">
	</div><!-- ventana -->
	<ul>
	<li><a href="javascript:getAjaxFile('1366');">Acto Institucional UPV</a></li>
	<li><a href="javascript:getAjaxFile('1510');">�gora Valencia</a></li>
	'''
	
	#patron  = '<div id="ventana">[^<]+'
	#patron += '</div><!-- ventana -->[^<]+'
	#patron += '<ul>[^<]+'
	patron = '<li><a href="javascript:getAjaxFile([^"]+)' # [0] ID de la pagina del programa (se carga en un frame en javascript pero
							      # monto la URL m�s abajo usando este ID)
	patron += ';">([^"]+)</a></li>' # [1] T�tulo del programa
	#patron += '<img width=160 height=121 src="([^"]+)" alt="Img. del programa" /></a>[^<]+' # [1] Imagen del programa
	#patron += '<p>([^"]+)</p>[^<]+' # [3] Argumento del programa
	matches = re.compile(patron,re.DOTALL).findall(data)
	
	for match in matches:
		# Atributos del vÃ­deo
		scrapedtitle = match[1] 
		scrapedurl = "http://www.upv.es/pls/oreg/rtv_web.ProgFicha?p_id="+match[0][2:-2]+"&p_idioma=c" #urlparse.urljoin(url,)
		scrapedthumbnail = urlparse.urljoin(url,"http://mediaserver01.upv.es/UPRTV/TV/MC/img/"+match[0][2:-2]+".jpg") #urlparse.urljoin(url,match[1])
		scrapedplot = "Pulsa sobre el nombre de un programa para ver los detalles y escoger el cap�tulo que deseas ver en el hist�rico de sus emisiones." # match[3]
		if (DEBUG): xbmc.output("\n"+"title="+" "+scrapedtitle+"\n"+"url="+" "+scrapedurl+"\n"+"thumbnail="+" "+scrapedthumbnail+"\n"+"url="+" "+scrapedplot)


		# AÃ±ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def videolist(params,url,category):
	xbmc.output("[upvtv.py] videolist")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data) # hace un print de la captura del html en el log del XBMC
	#logger.info(data)

	# Extrae los capitulos
	'''
	<dt>20-01-2011</dt>
	<dd>
		<span class="archivo"><a href="javascript:getAjaxFile2('1366','35547');" onClick="scroll(0,0)" >
		Toma de posesi�n Nemesio Fern�ndez [Dtor ETS Ingenier�a Agron�mica y Medio Natural]
	</a></span>
		<a target="_blank" href="http://mediaserver01.upv.es/UPRTV/TV/ActoInstitucionalUPV/2011-01-20 Acto_Insti Toma de posesi�n Nemesio Fern�ndez [Dtor ETS Ingenier�a Agron�mica y Medio Natural].wmv"title="Descargar Programa" class="verPrograma">Ver programa</a>
	</dd>
	'''
	
	patron  = '<dt>([0-9][^\ ]+)+</dt>[^<]+' # [0] Fecha de emisi�n
	patron += '<dd>.*?'
	#patron += '<span class="archivo"><a href="[^"]+" onClick="([^"]+)" >' #[0] captura en blanco
	patron += '>([^<]+)'# [1] T�tulo del cap�tulo
	patron += '</a></span>[^<]+'
	patron += '<a target="_blank" href="([^<]+)" title="Descargar Programa.*?' #[2] URL del v�deo
	matches = re.compile(patron,re.DOTALL).findall(data)

	for match in matches:
		# Atributos del v�deo
		scrapedtitle = "["+match[0].strip()+"] "+match[1][1:-1] #match[2]#.strip()
		#scrapedurl = urlparse.urljoin(url,match[2])
                
		URLqueMola = urllib.quote(match[2]) #urllib.quote("http://mediaserver01.upv.es/UPRTV/TV/ActoInstitucionalUPV/2010-04-08 Acto_Insti Toma de posesi�n decano ADE.wmv")[5:]
                URLconHTTPok = URLqueMola.replace("http%3A","http:")
                scrapedurl = (URLconHTTPok)
        	scrapedthumbnail = ""
		scrapedplot = "HAZ CLICK SOBRE EL NOMBRE PARA REPRODUCIR EL CAP�TULO"
		if (DEBUG): xbmc.output("\n"+"title="+" "+scrapedtitle+"\n"+"url="+" "+scrapedurl+"\n"+"thumbnail="+" "+scrapedthumbnail+"\n"+"Descripci�n="+" "+scrapedplot)

		# A�ade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , category , "Directo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
	
	#Mirar posible soluci�n reemplazar caracteres extra�os aqu�:
	#http://gomputor.wordpress.com/2008/09/27/search-replace-multiple-words-or-characters-with-python/
	#http://www.python.org/dev/peps/pep-0263/


	# Extrae los capitulos de la p�gina siguiente y/o anterior
	'''
	<div class="paginador"><ul>
	<li><a href="javascript:getAjaxFile3(1327,151)" class="anterior">Siguiente</a></li>
	<li class="numero">1/7</li>
	<li><a href="javascript:getAjaxFile3(1327,26)" class="siguiente">Anterior</a></li>
	</ul></div><!-- paginador (1) --><br class="clearFloat"/>
	'''

	
	#patron  = '<div class="paginador"><ul>'
	patron  = '<li><a href="javascript:getAjaxFile3\(([^"]+)\,([^"]+)\)" class="anterior".*?'#[0] y [1] id programa + id n� primer cap�tulo de la p�gina anterior
	patron += '<li><a href="javascript:getAjaxFile3\(([^"]+)\,([^"]+)\)" class="siguiente".*?' #[2] y [3] id programa + id n� primer cap�tulo de la p�gina anterior
	#patron  += '<li class="numero">([^"]+)</li>' #[2] y [3] n�mero de p�gina actual y n�mero total de p�ginas
	#patron += '([^"]+),([^"]+).*?'
	#patron += ')" class="anterior".*?'# 
	#patron += '<li><a href="javascript:getAjaxFile3(([^"]+),([^"]+))" class="siguiente".*?'# [2] y [3] id programa + id n� primer programa de la p�gina siguiente
	matches = re.compile(patron,re.DOTALL).findall(data)

	for match in matches:
		# Atributos del "Paginador"
		scrapedtitle = "<<P�gina anterior<<"# ["+match[2]+"]" 
		#Meto prueba de la TV en directo pero no se la come
		scrapedurl = "http://www.upv.es/pls/oreg/rtv_web.ProgFichaAnteriores?p_id="+match[0]+"&p_reg="+match[1]+"&p_idioma=c&rndval=" #urlparse.urljoin(url,match) #match 
		scrapedthumbnail = ""
		scrapedplot = "Emisiones Anteriores"
		if (DEBUG): xbmc.output("\n"+"title="+" "+scrapedtitle+"\n"+"url="+" "+scrapedurl+"\n"+"thumbnail="+" "+scrapedthumbnail+"\n"+"Descripci�n="+" "+scrapedplot)
		
		# A�ade nueva carpeta (Bot�n) al listado de XBMC
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	for match in matches:
		# Atributos del "Paginador"
		scrapedtitle = ">>P�gina siguiente>>"# ["+match[2]+"]" 
		#Meto prueba de la TV en directo pero no se la come
		scrapedurl = "http://www.upv.es/pls/oreg/rtv_web.ProgFichaAnteriores?p_id="+match[2]+"&p_reg="+match[3]+"&p_idioma=c&rndval=" #urlparse.urljoin(url,match) #match 
		scrapedthumbnail = ""
		scrapedplot = "Emisiones Anteriores"
		if (DEBUG): xbmc.output("\n"+"title="+" "+scrapedtitle+"\n"+"url="+" "+scrapedurl+"\n"+"thumbnail="+" "+scrapedthumbnail+"\n"+"Descripci�n="+" "+scrapedplot)
		
		# A�ade nueva carpeta (Bot�n) al listado de XBMC
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	#patron = '<a class="list-siguientes" href="([^"]+)" title="Ver siguientes archivos">'
	#matches = re.compile(patron,re.DOTALL).findall(data)
	#for match in matches:
	#	# Atributos del v�deo
	#	scrapedtitle = "P�gina siguiente"
	#	scrapedurl = urlparse.urljoin(url,match)
	#	scrapedthumbnail = ""
	#	scrapedplot = ""
	#	if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
	#
	#	# A�ade al listado de XBMC
	#	xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[upvtv.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	xbmctools.playvideo(CHANNELCODE,server,url,category,title,thumbnail,plot)
