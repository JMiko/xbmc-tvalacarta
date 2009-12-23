# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para sevillista
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

CHANNELNAME = "sevillista"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[sevillista.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[sevillista.py] mainlist")
	
	if url=="":
		url="http://pelis-sevillista56.blogspot.com/"
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas
	'''
<div class='post hentry'>
<a name='8448768243226588323'></a>
<h3 class='post-title entry-title'>
<a href='http://pelis-sevillista56.blogspot.com/2009/12/ver-online-avatar-2009.html'>Ver Online Avatar (2009)</a>
</h3>
<div class='post-header-line-1'></div>
<span class='post-author vcard'>
Publicado por
<span class='fn'>Sevillista56</span>
</span>
<br><span class='post-comment-link'>
<a class='comment-link' href='http://pelis-sevillista56.blogspot.com/2009/12/ver-online-avatar-2009.html#comments' onclick=''>
44 comentarios, agrega el tuyo!</a>

</span></br>
<div class='post-body entry-content' oncontextmenu='return false' ondragstart='return false' onmousedown='return false' onselectstart='return false'>
<style>.fullpost{display:none;}</style>
<p><span style="font-weight: bold; color: rgb(255, 0, 0);">Ya Disponible Original</span><br /><a onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}" href="http://pelis-sevillista56.blogspot.com/2009/12/ver-online-avatar-2009.html" title=" Avatar (2009) http://pelis-sevillista56.blogspot.com/"><img style="margin: 0pt 10px 10px 0pt; float: left; cursor: pointer; width: 226px; height: 320px;" src="http://www.aullidos.com/imagenes/caratulas/avatar-2.jpg" alt="" id="BLOGGER_PHOTO_ID_5382862501907193618" border="0" /></a><span style="color: rgb(255, 0, 0);">Título:</span> Avatar<br /><span style="color: rgb(255, 0, 0);">Título original:</span> Avatar<br /><span style="color: rgb(255, 0, 0);">País: </span>USA<br /><span style="color: rgb(255, 0, 0);">Estreno en USA:</span> 18/12/2009<br /><span style="color: rgb(255, 0, 0);">Estreno en España:</span>18/12/2009<br /><span style="color: rgb(255, 0, 0);">Productora:</span> Twentieth Century, Fox Film Corporation<br /><span style="color: rgb(255, 0, 0);">Director: </span> James Cameron<br /><span style="color: rgb(255, 0, 0);">Guión:</span>  James Cameron<br /><span style="color: rgb(255, 0, 0);">Reparto:</span> Sam Worthington, Zoe Saldana, Sigourney Weaver, Michelle Rodriguez, Giovanni Ribisi, Joel David Moore, CCH Pounder, Peter Mensah, Laz Alonso, Wes Studi, Stephen Lang, Matt Gerald<br /><span class="fullpost"><br /><br /><span style="display: block; text-align: center; font-weight: bold;"><a href="http://octtopus.com/01grupos/01mochileros/00%20minis/00proximamente.jpg" target="blank"><span style="color: rgb(255, 0, 0);"></span> </a><br /><br /><span style="display: block; text-align: center; font-weight: bold;"><a href="http://octtopus.com/01grupos/01mochileros/00%20minis/00proximamente.jpg" target="blank"><span style="color: rgb(255, 0, 0);"></span> </a><br /><br /><span style="display: block; text-align: center; font-weight: bold;"><a href="http://octtopus.com/01grupos/01mochileros/00%20minis/00proximamente.jpg" target="blank"><span style="color: rgb(255, 0, 0);"></span> </a><br /><br /><span style="display: block; text-align: center; font-weight: bold;"><a href="http://octtopus.com/01grupos/01mochileros/00%20minis/00proximamente.jpg" target="blank"><span style="color: rgb(255, 0, 0);"><br />La Pelicula Avatar (2009) Estara Disponible En Español En Unas Horas </span> </a><br /><br /><br /><span style="display: block; text-align: center; font-weight: bold; color: rgb(255, 0, 0);">Versión Completa (Audio Original)</span><br /><object data="http://www.imagenesid.com/pid/mediaplayer.swf" type="application/x-shockwave-flash" width="500" height="340"><br /><br /><param name="bgcolor" value="#C0C0C0"><br /><param name="flashvars" value="file=http://www.imagenesid.com/pid/xmls/avatar.xml&amp;playlist=right&amp;autostart=false&amp;playlistsize=&amp;fullscreen=true&amp;backcolor=111111&amp;frontcolor=eeeeee&amp;controlbar=over"><br /><param name="src" value="http://www.imagenesid.com/pid/mediaplayer.swf"><br /><param name="allowfullscreen" value="true"><br /></object><br /><center><img src="http://peliculasok.com/sgtparte.jpg" alt="ver siguiente parte" border="0" /><br /><b><i>A ver si entendemos ahora!, El click se da en el player no en la imagen de EJEMPLO!!!!</i><br /><br /><br /><br /><br /><br /><span style="display: block; text-align: center; font-weight: bold;">Software Esencial Para Ver Peliculas Online Flv</span><br /><span style="display: block; text-align: center; font-weight: bold;"><img src="http://i34.tinypic.com/20iuanr_th.png" width="25" border="0" height="25" /> </span><a href="http://get.adobe.com/es/flashplayer/">Descargar Flash Player</a><br /><br /><br /><br /><span style="display: block; text-align: center; color: rgb(255, 0, 0);"> </span><span style="display: block; text-align: center;"><span style="display: block; text-align: center;"><span style="display: block; text-align: center;"><span style="display: block; text-align: center;"><span style="display: block; text-align: center; color: rgb(255, 0, 0);">Sinopsis:</span></span></span></span></span><span style="display: block; text-align: center; font-weight: bold;"><span style="display: block; text-align: center; font-weight: bold;"><span style="display: block; text-align: center; font-weight: bold;"><span style="display: block; text-align: center; font-weight: bold;"><span style="display: block; text-align: center; color: rgb(255, 0, 0);"> </span><br /><br />Avatar nos lleva a un espectacular nuevo mundo más allá de nuestra imaginación donde un héroe inesperado se embarca en una aventura, luchando por salvar un nuevo mundo alienígena al que ha aprendido a llamar hogar.<br /><br />Entramos en el nuevo mundo a través de los ojos de Jake Sully, un ex-Marine confinado en una silla de ruedas. A pesar de su cuerpo tullido, todavía es un guerrero de corazón. Jake ha sido reclutado para viajar a Pandora, donde las corporaciones están extrayendo un mineral extraño que es la clave para resolver los problemas de la crisis energética de la Tierra. Al ser tóxica la atmósfera de Pandora, ellos han creado el programa Avatar, en el cual los humanos &#8220;conductores&#8221; tienen sus conciencias unidas a un avatar, un cuerpo biológico controlado de forma remota que puede sobrevivir en el aire letal. Estos avatars están creados genéticamente de DNA humano mezclado con DNA de los nativos de Pandora&#8230;los Na&#180;vi.<br /><br />Ya en su forma avatar, Jake puede caminar otra vez. Ha recibido la misión de infiltrarse entre los Na&#180;vi, los cuales se han convertido en el mayor obstáculo para la extracción del mineral. Pero una bella Na&#180;vi, Naytiri, salva la vida de Jake, y todo cambia. Jake es admitido en su clan y aprende a ser uno de ellos, lo cual le hace someterse a muchas pruebas y aventuras. Según la relación de Jake con su profesora Neytiry se va intensificando, él aprende a respetar la vida de los Na&#180;vi y decide encontrar su lugar entre ellos. Pronto se enfrentará a la mayor de las pruebas cuando tenga que dirigir una batalla épica que decidirá nada menos que el destino de su nuevo mundo.</span><br /><br /><br /><br /><span style="display: block; text-align: center; font-weight: bold; color: rgb(255, 102, 0);"><a href="http://sevillista-56.blogspot.com/" target="blank"><span>[Enlace Roto] Comunicar Que Una Pelicula O Serie No Puede Ser Visualizado (Reportar enlace) </span> </a><br /><br /><br /><br /><a style="color: rgb(255, 255, 255);" href="http://pelis-sevillista56.blogspot.com/"><span style="font-weight: bold;">http://pelis-sevillista56.blogspot.com/</span></a><br /><br /><span style="display: block; text-align: center; font-weight: bold;"><span style="font-weight: bold;">&#191;Que te ha parecido la pelicula?Comentalo.</span></span><br /><br /><br /><br /><br /></span></span></span><br /></span></b></center></span></span></span></span></span></p>

<a href='http://pelis-sevillista56.blogspot.com/2009/12/ver-online-avatar-2009.html'>Ver Pelicula Online &#187;</a>
<div style='clear: both;'></div>
</div>
<div class='post-footer'>
<div class='post-footer-line post-footer-line-1'>
<span class='post-icons'>
<span class='item-control blog-admin pid-785248143'>
<a href='http://www.blogger.com/post-edit.g?blogID=3684018687757979783&postID=8448768243226588323' title='Editar entrada'>
<img alt='' class='icon-action' height='18' src='http://www.blogger.com/img/icon18_edit_allbkg.gif' width='18'/>
</a>
</span>
</span>
</div>
<div class='post-footer-line post-footer-line-2'>
</div>
<br><span class='post-comment-link'>

<a class='comment-link' href='http://pelis-sevillista56.blogspot.com/2009/12/ver-online-avatar-2009.html#comments'>44
Comentarios</a>
</span></br>
<div class='post-footer-line post-footer-line-3'></div>
</div>
</div>

	patron  = "<div class='post hentry'>[^<]+"
	patron += "<a[^>+]></a>[^<]+"
	patron += "<h3[^>]+>[^<]+"
	patron += "<a href='([^']+)'>([^<]+)</a>.*?"
	patron += '<img.*?src="([^"]+)"'
	'''
	patron = '<a onblur="[^"]+" href="([^"]+)" title="([^"]+)"><img style="[^"]+" src="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		# Thumbnail
		scrapedthumbnail = urlparse.urljoin(url,match[2])
		# Argumento
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	patron  = "<div id='blog-pager'>.*?a href='([^']+)' id='[^']+' title='Entradas antiguas'>"
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches)>0:
		# Titulo
		scrapedtitle = "!Página siguiente"
		# URL
		scrapedurl = urlparse.urljoin(url,matches[0])
		# Thumbnail
		scrapedthumbnail = ""
		# Argumento
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "mainlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[sevillista.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	patron = '<span class="title">([^<]+)</span>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		title = matches[0]

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		if server!="Megaupload":
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[sevillista.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
