# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Meristation
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

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[meristation.py] init")

DEBUG = True
CHANNELNAME = "Meristation"
CHANNELCODE = "meristation"

def mainlist(params,url,category):
	xbmc.output("[meristation.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELCODE , "listaporconsola" , CHANNELNAME , "Listado por consola", "http://www.meristation.com/v3/GEN_videos.php" , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "listaalfabetica" , CHANNELNAME , "Listado alfabético" , "" , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "listaporgenero"  , CHANNELNAME , "Listado por género" , "http://www.meristation.com/v3/GEN_videos.php" , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "ultimosvideos"   , CHANNELNAME , "Últimos vídeos"     , "http://www.meristation.com/v3/GEN_videos.php" , "" , "" )
	xbmctools.addnewfolder( CHANNELCODE , "search"          , CHANNELNAME , "Buscar"             , "" , "" , "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def search(params,url,category):
	xbmc.output("[meristation.py] search")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.meristation.com/v3/resultado_busqueda.php?busca="+tecleado+"&tipo=10&palabras=1&pic=GEN"
			searchresults(params,searchUrl,category)

def searchresults(params,url,category):
	xbmc.output("[meristation.py] searchresults")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	'''
	   onMouseOut="this.style.background='#ffffff'"> 
		           <td class="tabla_borde_down" valign="top" width="250">

		             <font face="Arial, Helvetica, sans-serif" size="2">
		                              <a href="des_videos.php?pic=WII&idj=cw45ba12c3a8156&COD=cw4b002ff355067" class="mslink9">
		                              
		             <b>MeriStation TV Noticias 3x11</b></a></font>
		             <font face="Arial, Helvetica, sans-serif" size="2"> 
		             <a href="WII_portada.php" class="mslink8">
		             <font color="#3366CC"><b>WII</b></font></a><span class="mstrucos"></span> 
		             <br>
		             <a href="empresa.php?pic=GEN&id=cw428d365050c81" class="mslink9">
		             Nintendo</a></font>

		             <font face="Arial, Helvetica, sans-serif" size="2"></font>
		             <font face="Arial, Helvetica, sans-serif" size="2"> 
		             </font>
		           </td>
		           <td class="tabla_borde_down" valign="top" width="100">
		             <font face="Arial, Helvetica, sans-serif" size="2">
		             <a href="GEN_.php" class="mslink9">
		             Simulador</a></font>
		             <font face="Arial, Helvetica, sans-serif" size="2"></font><br>

		             <span class=fecha>
											16/11/09					                 </span>
		           </td>
		           <td class="tabla_borde_down" valign="top" width="200">
		             <a href="shopping.php?idj=cw45ba12c3a8156" target="_blank">
		             <img src="imgs/icono_busqueda_carrito1.gif" width="22" height="20" alt="Comprar" border="0"></a>

		                              <a href="listado_imagenes.php?pic=WII&idj=cw45ba12c3a8156">
		             <img src="imgs/icono_busqueda_imagenes.gif" width="22" height="20" alt="Galería de Imágenes" border="0"></a>

		                                       
		                              <a href="des_avances.php?pic=WII&pes=1&idj=cw45ba12c3a8156" >
		             <img src="imgs/icono_busqueda_avances.gif" width="22" height="20" alt="Avance" border="0"></a>
		                                       
		             
		                              <a href="des_videos.php?pic=WII&pes=1&idj=cw45ba12c3a8156" >
		             <img src="imgs/icono_busqueda_videos.gif" width="22" height="20" alt="Vídeos" border="0"></a>
		                                       
		                                       
		                                        
		             
		                             </td>
		            <td class="tabla_borde_down" width="50" valign="top" align="center"> 
		              <font face="Arial, Helvetica, sans-serif" size="2">
		                     
		                                <b>--</b></a></font>
		                              </td>
	'''
	
	patron  = '<tr onMouseOver="this.style.background =\'\'  "; this.style.cursor = \'hand\'"(.*?)</tr>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:

		patron2  = '<td class="tabla_borde_down" valign="top" width="250">[^<]+'
		patron2 += '<font face="Arial, Helvetica, sans-serif" size="2">[^<]+'
		patron2 += '<a href="([^"]+)" class="mslink9">[^<]+'
		patron2 += '<b>([^<]+)</b></a></font>[^<]+'
		patron2 += '<font face="Arial, Helvetica, sans-serif" size="2">[^<]+'
		patron2 += '<a href="[^"]+" class="mslink8">[^<]+'
		patron2 += '<font color="[^"]+"><b>([^<]+)</b></font></a><span class="mstrucos"></span>[^<]+'
		patron2 += '<br>[^<]+'
		patron2 += '<a href="empresa.php[^"]+" class="mslink9">([^<]+)</a></font>[^<]+'
		matches2 = re.compile(patron2,re.DOTALL).findall(match)

		for match2 in matches2:

			# Atributos del vídeo
			scrapedtitle = match2[1].strip()+" "+match2[2].strip()+" "+match2[3].strip()
			scrapedurl = match2[0]
			scrapedthumbnail = ""
			scrapedplot = ""
			if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

			# Añade al listado de XBMC
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Directo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
	# URL de detalle
	# http://www.meristation.com/v3/des_videos.php?pic=WII&idj=cw49944ba621067&COD=cw4a8d04e8e355d
	# URL con el vídeo
	# http://www.meristation.com/v3/des_videos.php?id=cw4a8d04e8e355d&c=1&pic=WII&idj=cw49944ba621067
	# URL descargar vídeo
	# http://www.meristation.com/v3/des_videos.php?id=cw4a8d04e8e355d&c=1&pic=WII&idj=cw49944ba621067

def listaalfabetica(params,url,category):
	xbmc.output("[meristation.py] listaalfabetica")

def listaporgenero(params,url,category):
	xbmc.output("[meristation.py] listaporgenero")

def listaporconsola(params,url,category):
	xbmc.output("[meristation.py] listaporconsola")

	url = 'http://www.meristation.com/v3/GEN_videos.php'

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae las categorias (carpetas)
	# --------------------------------------------------------
	patron = '<a href="([^"]+)" class="mslink8">[^<]+<font color="[^"]+"><b>([^<]+)</b></font></a><span class="mstrucos">'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		try:
			scrapedtitle = unicode( match[2], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2]
		scrapedtitle = scrapedtitle + " ("+match[4].replace("&iacute;","i")+")"
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		
		#scrapedurl = "http://www.rtve.es/infantil/components/"+match[0]+"/videos/videos-1.inc"
		scrapedurl = "http://www.rtve.es/infantil/components/"+match[0]+"/videos.xml.inc"
		scrapedthumbnail = urlparse.urljoin(url,match[3])
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[meristation.py] videolist")

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage2(url,[["Referer","http://www.rtve.es/infantil/videos-juegos/#/videos/edebits/todos/"],["User-Agent","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; InfoPath.2)"]])
	xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los capítulos
	# --------------------------------------------------------
	patron = '<video id="[^"]+" thumbnail="([^"]+)" url="([^"]+)" publication_date="([^T]+)T[^>]+>[^<]+<title>([^<]+)</title>[^<]+<sinopsis([^<]+)<'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		try:
			scrapedtitle = unicode( match[3], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[3]
		scrapedtitle = scrapedtitle + " ("+match[2]+")"
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedurl = urlparse.urljoin(url,match[1])
		scrapedthumbnail = urlparse.urljoin(url,match[0])
		scrapedplot = match[4]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[meristation.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
