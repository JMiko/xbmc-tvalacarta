# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newdivx.net by Bandavi
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

CHANNELNAME = "newdivx"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[newdivx.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[newdivx.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos"       , category , "Ultimas Pel�culas A�adidas"    ,"http://www.newdivx.net/","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListaCat"         , category , "Listado por Categorias"    ,"http://www.newdivx.net/","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListvideosMirror" , category , "Estrenos","http://www.newdivx.net/peliculas-online/estrenos/","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListvideosMirror" , category , "Documentales","http://www.newdivx.net/peliculas-online/documentales/","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListvideosMirror" , category , "Peliculas V.O.S.","http://www.newdivx.net/peliculas-online/peliculas-vos/","","")
	xbmctools.addnewfolder( CHANNELNAME , "search" , category , "Buscar","http://www.newdivx.net/index.php","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[newdivx.py] search")

	keyboard = xbmc.Keyboard()
	#keyboard.setDefault('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.newdivx.net/index.php?do=search&subaction=search&story="+tecleado
			searchresults(params,searchUrl,category)

def searchresults(params,url,category):
	xbmc.output("[newdivx.py] SearchResult")
	
	#post = {"do": "search","subaction":"search","story":tecleado}
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#print data
	# Extrae las entradas (carpetas)
	patronvideos  = '<td class="copy" valign="top" colspan="2"><a href="([^"]+)" >'
	patronvideos += '<[^>]+><[^>]+><img src="([^"]+)" '
	patronvideos += "alt=.*?title='([^']+)' /></div>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedurl = match[0]
		
		scrapedtitle =match[2]
		scrapedtitle = scrapedtitle.replace("&#8211;","-")
		scrapedtitle = scrapedtitle.replace("&nbsp;"," ")
		scrapedthumbnail = match[1]
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
			

def ListaCat(params,url,category):
	xbmc.output("[newdivx.py] ListaCat")
	
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Acci�n","http://www.newdivx.net/peliculas-online/accion/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Adolescencia","http://www.newdivx.net/peliculas-online/adolescencia/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Animaci�n","http://www.newdivx.net/peliculas-online/animacion/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Aventuras","http://www.newdivx.net/peliculas-online/aventuras/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Belico","http://www.newdivx.net/peliculas-online/belico/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Ciencia-Ficci�n","http://www.newdivx.net/peliculas-online/ciencia-ficcion/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Comedia","http://www.newdivx.net/peliculas-online/comedia/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Drama","http://www.newdivx.net/peliculas-online/drama/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Fantastico","http://www.newdivx.net/peliculas-online/fantastico/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Intriga","http://www.newdivx.net/peliculas-online/intriga/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Infantil","http://www.newdivx.net/peliculas-online/infantil/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Musical","http://www.newdivx.net/peliculas-online/musical/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Romantico","http://www.newdivx.net/peliculas-online/romantico/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Terror","http://www.newdivx.net/peliculas-online/terror/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Thriller","http://www.newdivx.net/peliculas-online/thriller/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Western","http://www.newdivx.net/peliculas-online/western/","","")

	# Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        
def ListvideosMirror(params,url,category):
	xbmc.output("[newdivx.py] ListvideosMirror")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)


	# Patron de las entradas
	patronvideos  = '<td class="copy" align="left" valign="top" ><[^>]+><[^>]+><a href="([^"]+)"' # URL
	patronvideos += '></span><[^>]+><[^>]+><img src="([^"]+)" '                                   # TUMBNAIL
	patronvideos += "alt=.*?title='([^']+)' /></div>"                                             # TITULO 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# A�ade las entradas encontradas
	for match in matches:
		# Atributos
		scrapedtitle = match[2]
		scrapedurl = match[0]
		scrapedthumbnail = match[1]
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	#Extrae la marca de siguiente p�gina
	patronvideos  = '</span> <a href="(http://www.newdivx.net/peliculas-online/[^\/]+/page/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = matches[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "ListvideosMirror" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        

def listvideos(params,url,category):
	xbmc.output("[newdivx.py] listvideos")

	if url=="":
		url = "http://www.newdivx.com/"
                
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)


	# Extrae las entradas (carpetas)
	patronvideos  = '<title></title>.*?<div class="news"><[^>]+>[^<]+<a href="([^"]+)"'     # URL
	patronvideos += '></span><img src="([^"]+)" '                                           # TUMBNAIL
	patronvideos += 'style=.*?title="([^"]+)"><span'                                         # TITULO 
	#patronvideos += '</div>[^<]+<div class=[^>]+>.*?href="[^"]+"><img '                    
	#patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                  # IMAGEN , DESCRIPCION
	#patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                      # VIDEO FLV 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		
		scrapedtitle = match[2]
		# URL
		scrapedurl = match[0]
		# Thumbnail
		scrapedthumbnail = match[1]
		# Argumento
		scrapedplot = ""
		

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		
			# A�ade al listado de XBMC
			xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	#Extrae la marca de siguiente p�gina
	patronvideos  = '</span> <a href="(http://www.newdivx.net/videos/page/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = matches[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[newdivx.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	patronvideos = '<p class="Estilo2">([^<]+)</p>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		title = matches[0]   
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos en los servidores habilitados
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		if "stagevu.com/embed" not in video[1]:
			videotitle = video[0]
			url = video[1]
			server = video[2]
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------
        #--- Busca los videos Directos
    ## ------------------------------------------------------------------------------------##
    #               Busca  enlaces en el servidor  przeklej                                 #
    ## ------------------------------------------------------------------------------------## 
        patronvideos = '<param name="src" value="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        if len(matches)>0:
			if len(matches)==1:
				subtitle = "[Divx-Directo-Przeklej]"
				xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle, matches[0] , thumbnail , plot )
                 
			else:
				parte = 0
				subtitle = "[Divx-Directo-Przeklej]"
				for match in matches:
					xbmc.output(" matches = "+match)
					parte = parte + 1
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle+" "+str(parte), match , thumbnail , plot )
					
   ## --------------------------------------------------------------------------------------##
   #  				 Busca enlaces en el servidor Fishker                                    #
   ## --------------------------------------------------------------------------------------##
	patronvideos = '<a href="(http\:\/\/www.fishker.com\/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		data2 = scrapertools.cachePage(matches[0])
		#print data2
		#<param name="flashvars" value="comment=Q&amp;m=video&amp;file=http://fish14.st.fishker.com/videos/1249504.flv?c=3948597662&amp;st=/plstyle.txt?video=1"
		patron = 'file=([^"]+)"'
		matches2 = re.compile(patron,re.DOTALL).findall(data2)
		if len(matches2)>0:
			videourl = matches2[0].replace("&amp;","&")
			subtitle = "[FLV-Directo-Fishker]"
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
			
   ## --------------------------------------------------------------------------------------##
   #  				 Busca enlaces en el servidor Cinshare                                   #
   ## --------------------------------------------------------------------------------------##
	patronvideos = '<iframe src="(http://www.cinshare.com/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		'''
		data2 = scrapertools.cachePage(matches[0])
		#print data2
		
		patron = '<param name="src" value="([^"]+)"'
		matches2 = re.compile(patron,re.DOTALL).findall(data2)
		if len(matches2)>0:
		'''
		import cinshare
		videourl = cinshare.geturl(matches[0])
		subtitle = "[divx-Directo-Cinshare]"
		xbmctools.addnewvideo( CHANNELNAME , "play" , category ,"Directo", title + " - "+subtitle, videourl , thumbnail , plot )
			
	## --------------------------------------------------------------------------------------##
	#               Busca enlaces a videos .flv o (.mp4 dentro de un xml)                     #
	## --------------------------------------------------------------------------------------##
	patronvideos = 'file=(http\:\/\/[^\&]+)\&'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		subtitle = "[FLV-Directo]"
		if ("xml" in matches[0]):
			data2 = scrapertools.cachePage(matches[0])
			xbmc.output("data2="+data2)
			patronvideos  = '<track>.*?'
			patronvideos += '<title>([^<]+)</title>(?:[^<]+'
			patronvideos += '<annotation>([^<]+)</annotation>[^<]+|[^<]+)'
			patronvideos += '<location>([^<]+)</location>[^<]+'
			patronvideos += '</track>'
			matches = re.compile(patronvideos,re.DOTALL).findall(data2)
			scrapertools.printMatches(matches)

			for match in matches:
				if ".mp4" in match[2]:
					subtitle = "[MP4-Directo]"
				scrapedtitle = '%s (%s) - %s  %s' %(title,match[1].strip(),match[0],subtitle)
				scrapedurl = match[2].strip()
				scrapedthumbnail = thumbnail
				scrapedplot = plot
				if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

				# A�ade al listado de XBMC
				xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , scrapedtitle, scrapedurl , scrapedthumbnail, scrapedplot )
		else:
			
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle, matches[0] , thumbnail , plot )
			
	## --------------------------------------------------------------------------------------##
	#            Busca enlaces a video en el servidor Dailymotion                             #
	## --------------------------------------------------------------------------------------##
	patronvideos = '<param name="movie" value="http://www.dailymotion.com/swf/video/([^\_]+)\_[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	playWithSubt = "play"
	if len(matches)>0:
		daily = 'http://www.dailymotion.com/video/%s'%matches[0]
		data2 = scrapertools.cachePage(daily)
		
		# Busca los subtitulos en espa�ol 
		subtitulo = re.compile('%22es%22%3A%22(.+?)%22').findall(data2)
		subtit = urllib.unquote(subtitulo[0])
		subtit = subtit.replace("\/","/")
		#subt_ok = downloadstr(subtit,title)
		#print "subtitulo subt_ok = %s" % str(subt_ok)
				
		# Busca el enlace al video con formato FLV 	
		Lowres=re.compile('%22sdURL%22%3A%22(.+?)%22').findall(data2)
		if len(Lowres)>0:
			videourl = urllib.unquote(Lowres[0])
			videourl = videourl.replace("\/","/")
			if len(subtit)>0:
				videourl = videourl + "|" + subtit
				playWithSubt = "play2"
			subtitle = "[FLV-Directo-Dailymotion]"
			xbmctools.addnewvideo( CHANNELNAME , playWithSubt , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
		
		# Busca el enlace al video con formato HQ (H264)		
		Highres=re.compile('%22hqURL%22%3A%22(.+?)%22').findall(data2)
		if len(Highres)>0:
			videourl = urllib.unquote(Highres[0])
			videourl = videourl.replace("\/","/")
			if len(subtit)>0:
				videourl = videourl + "|" + subtit
				playWithSubt = "play2"			
			subtitle = "[h264-Directo-Dailymotion]"
			xbmctools.addnewvideo( CHANNELNAME , playWithSubt , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
	## --------------------------------------------------------------------------------------##
	#            Busca enlaces a video en el servidor Gigabyteupload.com                      #
	## --------------------------------------------------------------------------------------##

	patronvideos = '<a href="(http://www.gigabyteupload.com/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		print " encontro: %s" %matches[0]
		import gigabyteupload as giga
		videourl = giga.geturl(matches[0])
		if len(videourl)>0:
			subtitle = "[Divx-Directo-Gigabyteupload]"
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )



def play(params,url,category):
	xbmc.output("[newdivx.py] play")
	strmplay = False
	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
	if xbmcplugin.getSetting("subtitulo") == "true":
		xbmc.Player().setSubtitles(xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib', 'subtitulo.srt' ) ) )
		xbmcplugin.setSetting("subtitulo", "false")

def play2(params,url,category):
	xbmc.output("[newdivx.py] play")
	url1 = url
	if "|" in url:
		urlsplited = url.split("|")
		url1 = urlsplited[0]
		urlsubtit = urlsplited[1]
		subt_ok = "0"
		while subt_ok == "0":		
			subt_ok = downloadstr(urlsubtit)
			print "subtitulo subt_ok = %s" % str(subt_ok)
			if subt_ok is None: # si es None la descarga del subtitulo esta ok
				xbmcplugin.setSetting("subtitulo", "true")
				break
	play(params,url1,category)
		
def acentos(title):

        title = title.replace("Â�", "")
        title = title.replace("Ã©","�")
        title = title.replace("Ã¡","�")
        title = title.replace("Ã³","�")
        title = title.replace("Ãº","�")
        title = title.replace("Ã­","�")
        title = title.replace("Ã±","�")
        title = title.replace("â€", "")
        title = title.replace("â€œÂ�", "")
        title = title.replace("â€œ","")
        title = title.replace("é","�")
        title = title.replace("á","�")
        title = title.replace("ó","�")
        title = title.replace("ú","�")
        title = title.replace("í","�")
        title = title.replace("ñ","�")
        title = title.replace("Ã“","�")
        return(title)
        
        
def downloadstr(urlsub):
	
	import downloadtools
	
	fullpath = os.path.join( os.getcwd(), 'resources', 'lib', 'subtitulo.srt' )
	if os.path.exists(fullpath):
		try:
			subtitfile = open(fullpath,"w")
			subtitfile.close()
		except IOError:
			xbmc.output("Error al limpiar el archivo subtitulo.srt "+fullpath)
			raise		
	ok = downloadtools.downloadfile(urlsub,fullpath)
	#xbmc.setSubtitles(fullpath)
	return ok

def getpost(url,values): # Descarga la pagina con envio de un Form
	
	#url=url
	try:
		data = urllib.urlencode(values)          
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read() 
		return the_page 
	except Exception: 
		return "Err "
def geturl(url):
	
	try:
		response = urllib.urlopen(url)
		trulink = response.geturl()
		return truelink
	except:
		return ""