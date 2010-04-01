# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinetube
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

CHANNELNAME = "cinetube"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[cinetube.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[cinetube.py] mainlist")

	# Añade al listado de XBMC
	addfolder("Películas - Novedades","http://www.cinetube.es/subindices/inovedades.html","list")
	addfolder("Películas - Todas","http://www.cinetube.es/subindices/ipelitodas.html","listtodas")
	addfolder("Películas - Alfabético","","listalfabetico")
	addfolder("Series - Novedades","http://www.cinetube.es/subindices/iserienovedades.html","list")
	addfolder("Series - Todas","http://www.cinetube.es/subindices/iserietodas.html","listtodasseries")
	addfolder("Series - Alfabético","","listalfabeticoseries")
	addfolder("Documentales - Novedades","http://www.cinetube.es/subindices/idocumentalesnovedades.html","list")
	addfolder("Documentales - Todos","http://www.cinetube.es/subindices/idocumentalestodos.html","listtodasseries")
	addfolder("Documentales - Alfabético","","listalfabeticodocumentales")
	addfolder("Anime - Series","http://www.cinetube.es/subindices/ianimeseries.html","list")
	addfolder("Anime - Peliculas","http://www.cinetube.es/subindices/ianimepeliculas.html","list")

	if xbmctools.getPluginSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetico(params, url, category):
	addfolder("0-9","http://www.cinetube.es/subindices/ipelinumero.html","list")
	addfolder("A","http://www.cinetube.es/subindices/ipelia.html","list")
	addfolder("B","http://www.cinetube.es/subindices/ipelib.html","list")
	addfolder("C","http://www.cinetube.es/subindices/ipelic.html","list")
	addfolder("D","http://www.cinetube.es/subindices/ipelid.html","list")
	addfolder("E","http://www.cinetube.es/subindices/ipelie.html","list")
	addfolder("F","http://www.cinetube.es/subindices/ipelif.html","list")
	addfolder("G","http://www.cinetube.es/subindices/ipelig.html","list")
	addfolder("H","http://www.cinetube.es/subindices/ipelih.html","list")
	addfolder("I","http://www.cinetube.es/subindices/ipelii.html","list")
	addfolder("J","http://www.cinetube.es/subindices/ipelij.html","list")
	addfolder("K","http://www.cinetube.es/subindices/ipelik.html","list")
	addfolder("L","http://www.cinetube.es/subindices/ipelil.html","list")
	addfolder("M","http://www.cinetube.es/subindices/ipelim.html","list")
	addfolder("N","http://www.cinetube.es/subindices/ipelin.html","list")
	addfolder("O","http://www.cinetube.es/subindices/ipelio.html","list")
	addfolder("P","http://www.cinetube.es/subindices/ipelip.html","list")
	addfolder("Q","http://www.cinetube.es/subindices/ipeliq.html","list")
	addfolder("R","http://www.cinetube.es/subindices/ipelir.html","list")
	addfolder("S","http://www.cinetube.es/subindices/ipelis.html","list")
	addfolder("T","http://www.cinetube.es/subindices/ipelit.html","list")
	addfolder("U","http://www.cinetube.es/subindices/ipeliu.html","list")
	addfolder("V","http://www.cinetube.es/subindices/ipeliv.html","list")
	addfolder("W","http://www.cinetube.es/subindices/ipeliw.html","list")
	addfolder("X","http://www.cinetube.es/subindices/ipelix.html","list")
	addfolder("Y","http://www.cinetube.es/subindices/ipeliy.html","list")
	addfolder("Z","http://www.cinetube.es/subindices/ipeliz.html","list")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabeticoseries(params, url, category):
	addfolder("0-9","http://www.cinetube.es/subindices/iserienumero.html","list")
	addfolder("A","http://www.cinetube.es/subindices/iseriea.html","list")
	addfolder("B","http://www.cinetube.es/subindices/iserieb.html","list")
	addfolder("C","http://www.cinetube.es/subindices/iseriec.html","list")
	addfolder("D","http://www.cinetube.es/subindices/iseried.html","list")
	addfolder("E","http://www.cinetube.es/subindices/iseriee.html","list")
	addfolder("F","http://www.cinetube.es/subindices/iserief.html","list")
	addfolder("G","http://www.cinetube.es/subindices/iserieg.html","list")
	addfolder("H","http://www.cinetube.es/subindices/iserieh.html","list")
	addfolder("I","http://www.cinetube.es/subindices/iseriei.html","list")
	addfolder("J","http://www.cinetube.es/subindices/iseriej.html","list")
	addfolder("K","http://www.cinetube.es/subindices/iseriek.html","list")
	addfolder("L","http://www.cinetube.es/subindices/iseriel.html","list")
	addfolder("M","http://www.cinetube.es/subindices/iseriem.html","list")
	addfolder("N","http://www.cinetube.es/subindices/iserien.html","list")
	addfolder("O","http://www.cinetube.es/subindices/iserieo.html","list")
	addfolder("P","http://www.cinetube.es/subindices/iseriep.html","list")
	addfolder("Q","http://www.cinetube.es/subindices/iserieq.html","list")
	addfolder("R","http://www.cinetube.es/subindices/iserier.html","list")
	addfolder("S","http://www.cinetube.es/subindices/iseries.html","list")
	addfolder("T","http://www.cinetube.es/subindices/iseriet.html","list")
	addfolder("U","http://www.cinetube.es/subindices/iserieu.html","list")
	addfolder("V","http://www.cinetube.es/subindices/iseriev.html","list")
	addfolder("W","http://www.cinetube.es/subindices/iseriew.html","list")
	addfolder("X","http://www.cinetube.es/subindices/iseriex.html","list")
	addfolder("Y","http://www.cinetube.es/subindices/iseriey.html","list")
	addfolder("Z","http://www.cinetube.es/subindices/iseriez.html","list")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabeticodocumentales(params, url, category):
	addfolder("0-9","http://www.cinetube.es/subindices/idocumentalesnumero.html","list")
	addfolder("A","http://www.cinetube.es/subindices/idocumentalesa.html","list")
	addfolder("B","http://www.cinetube.es/subindices/idocumentalesb.html","list")
	addfolder("C","http://www.cinetube.es/subindices/idocumentalesc.html","list")
	addfolder("D","http://www.cinetube.es/subindices/idocumentalesd.html","list")
	addfolder("E","http://www.cinetube.es/subindices/idocumentalese.html","list")
	addfolder("F","http://www.cinetube.es/subindices/idocumentalesf.html","list")
	addfolder("G","http://www.cinetube.es/subindices/idocumentalesg.html","list")
	addfolder("H","http://www.cinetube.es/subindices/idocumentalesh.html","list")
	addfolder("I","http://www.cinetube.es/subindices/idocumentalesi.html","list")
	addfolder("J","http://www.cinetube.es/subindices/idocumentalesj.html","list")
	addfolder("K","http://www.cinetube.es/subindices/idocumentalesk.html","list")
	addfolder("L","http://www.cinetube.es/subindices/idocumentalesl.html","list")
	addfolder("M","http://www.cinetube.es/subindices/idocumentalesm.html","list")
	addfolder("N","http://www.cinetube.es/subindices/idocumentalesn.html","list")
	addfolder("O","http://www.cinetube.es/subindices/idocumentaleso.html","list")
	addfolder("P","http://www.cinetube.es/subindices/idocumentalesp.html","list")
	addfolder("Q","http://www.cinetube.es/subindices/idocumentalesq.html","list")
	addfolder("R","http://www.cinetube.es/subindices/idocumentalesr.html","list")
	addfolder("S","http://www.cinetube.es/subindices/idocumentaless.html","list")
	addfolder("T","http://www.cinetube.es/subindices/idocumentalest.html","list")
	addfolder("U","http://www.cinetube.es/subindices/idocumentalesu.html","list")
	addfolder("V","http://www.cinetube.es/subindices/idocumentalesv.html","list")
	addfolder("W","http://www.cinetube.es/subindices/idocumentalesw.html","list")
	addfolder("X","http://www.cinetube.es/subindices/idocumentalesx.html","list")
	addfolder("Y","http://www.cinetube.es/subindices/idocumentalesy.html","list")
	addfolder("Z","http://www.cinetube.es/subindices/idocumentalesz.html","list")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def list(params,url,category):
	xbmc.output("[cinetube.py] list")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	patronvideos  = '<tr>[^<]*<td.*?>'
	patronvideos += '<img src="([^"]+)".*?'
	patronvideos += '<a href="([^"]+)".*?>(.*?)</a>(.*?)</tr>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[2], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2]

		# procesa el resto
		scrapedplot = ""
		argumento = re.compile("SINOPSIS:(.*?)</div>",re.DOTALL).findall(match[3])
		if len(argumento)>0:
			xbmc.output('argumento[0]=' + argumento[0])
			try:
				scrapedplot = unicode( argumento[0].strip(), "utf-8" ).encode("iso-8859-1")
			except:
				scrapedplot = argumento[0].strip()

		matchesconectores = re.compile('<img.*?alt="([^"]+)"',re.DOTALL).findall(match[3])
		conectores = ""
		for matchconector in matchesconectores:
			xbmc.output("matchconector="+matchconector)
			conectores = conectores + matchconector + "/"
		if len(matchesconectores)>0:
			scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"

		# URL
		scrapedurl = urlparse.urljoin("http://www.cinetube.es/subindices/",match[1])
		
		# Thumbnail
		scrapedthumbnail = match[0]
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listtodas(params,url,category):
	xbmc.output("[cinetube.py] list")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	patronvideos  = '<a.*?href="([^"]+)"[^>]+>Siguiente &gt;&gt;</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		# Añade al listado de XBMC
		addfolder( "!Página siguiente" , urlparse.urljoin(url,matches[0]) , "listtodas" )

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	patronvideos  = '<tr[^>]*>[^<]*<td height="35" align="center">'
	patronvideos += '<a href="([^"]+)".*?>(.*?)</a>(.*?)</tr>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)

		# procesa el resto
		scrapedplot = ""
		argumento = re.compile("SINOPSIS:(.*?)</div>",re.DOTALL).findall(match[2])
		if len(argumento)>0:
			xbmc.output('argumento[0]=' + argumento[0])
			try:
				scrapedplot = unicode( argumento[0], "utf-8" ).encode("iso-8859-1")
			except:
				scrapedplot = argumento[0]

		matchesconectores = re.compile('<img.*?alt="([^"]+)"',re.DOTALL).findall(match[2])
		conectores = ""
		for matchconector in matchesconectores:
			xbmc.output("matchconector="+matchconector)
			conectores = conectores + matchconector + "/"
		if len(matchesconectores)>0:
			scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"

		# URL
		scrapedurl = urlparse.urljoin("http://www.cinetube.es/subindices/",match[0])
		
		# Thumbnail
		scrapedthumbnail = ""
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listtodasseries(params,url,category):
	xbmc.output("[cinetube.py] list")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	patronvideos  = '<a.*?href="([^"]+)"[^>]+>Siguiente &gt;&gt;</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		# Añade al listado de XBMC
		addfolder( "!Página siguiente" , urlparse.urljoin(url,matches[0]) , "listtodasseries" )

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	patronvideos  = '<tr>[^<]+<td><img src="([^"]+)"[^>]+></td>[^<]+<td[^>]+><a href="([^"]+)"[^>]+>([^<]+)</a>(.*?)</td>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[2], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2]
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)

		# procesa el resto
		scrapedplot = ""

		matchesconectores = re.compile('<img.*?alt="([^"]+)"',re.DOTALL).findall(match[3])
		conectores = ""
		for matchconector in matchesconectores:
			xbmc.output("matchconector="+matchconector)
			conectores = conectores + matchconector + "/"
		if len(matchesconectores)>0:
			scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"

		# URL
		scrapedurl = urlparse.urljoin("http://www.cinetube.es/subindices/",match[1])
		
		# Thumbnail
		scrapedthumbnail = match[0]
		
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listmirrors(params,url,category):
	xbmc.output("[cinetube.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	#plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	plot = urllib.unquote_plus( params.get("plot") )

	# ------------------------------------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, o a los capítulos de las series...
	# ------------------------------------------------------------------------------------
	patronvideos  = '<iframe src="(.*?/subindices/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	for match in matches:
		xbmc.output("Encontrado iframe mirrors "+matches[0])
		# Lee el iframe
		url = urlparse.urljoin("http://www.cinetube.es/subindices/",matches[0].replace(" ","%20"))
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		data=response.read()
		response.close()
		
		# saca los enlaces
		patronvideos  = '<a href="(../[^"]+)"[^>]+>([^<]+)</a>'
		matches2 = re.compile(patronvideos,re.DOTALL).findall(data)
		
		# Los añade como folders
		for match2 in matches2:
			xbmc.output("Encontrado mirror "+match2[0])
			xbmc.output("titulo="+match2[1])
			try:
				titulo = unicode( match2[1], "utf-8" ).encode("iso-8859-1")
			except:
				titulo = match2[1]
				
			# Elimina los espacios multiples
			titulo = re.sub("\s+"," ",titulo)
			scrapedurl = urlparse.urljoin("http://www.cinetube.es/subindices/",match2[0]).replace(" ","%20")
			xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , title.strip().replace("(Megavideo)","").replace("  "," ") + " " + titulo , scrapedurl , thumbnail, plot )

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)
	
	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		if server=="Megavideo":
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip().replace("(Megavideo)","").replace("  "," ") + " - " + videotitle , url , thumbnail , plot )
		else:
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip().replace(server,"").replace("  "," ") + " - " + videotitle , url , thumbnail , plot )

	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[cinetube.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def addfolder(nombre,url,accion):
	xbmc.output('[cinetube.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=cinetube&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , url )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category,server):
	xbmc.output('[cinetube.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=cinetube&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , url , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[cinetube.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	itemurl = '%s?channel=cinetube&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
