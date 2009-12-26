# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de descargas
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
import downloadtools
import shutil

CHANNELNAME = "descargadoslist"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[descargadoslist.py] init")

DEBUG = True

DOWNLOAD_PATH = os.path.join( downloadtools.getDownloadListPath() )
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )
ERROR_PATH = os.path.join( downloadtools.getDownloadListPath(), 'error' )

def mainlist(params,url,category):
	xbmc.output("[descargadoslist.py] mainlist")

	# Crea el directorio de la lista de descargas si no existe
	try:
		os.mkdir(DOWNLOAD_PATH)
	except:
		pass
	try:
		os.mkdir(ERROR_PATH)
	except:
		pass

	# Crea un listado con las entradas de favoritos
	ficheros = os.listdir(DOWNLOAD_PATH)
	for fichero in ficheros:

		try:
			# Lee el bookmark
			titulo,thumbnail,plot,server,url = readbookmark(fichero)

			# Crea la entrada
			# En la categoría va el nombre del fichero para poder borrarlo
			xbmctools.addnewvideo( CHANNELNAME , "play" , os.path.join( DOWNLOAD_PATH, fichero ) , server , titulo , url , thumbnail, plot )
		except:
			pass

	xbmctools.addnewvideo( CHANNELNAME , "downloadall" , "category" , "server" , "(Empezar la descarga de la lista)" , "" , os.path.join(IMAGES_PATH, "Crystal_Clear_action_db_update.png"), "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def errorlist(params,url,category):
	xbmc.output("[descargadoslist.py] errorlist")

	# Crea el directorio de la lista de descargas con error si no existe
	try:
		os.mkdir(DOWNLOAD_PATH)
	except:
		pass
	try:
		os.mkdir(ERROR_PATH)
	except:
		pass

	# Crea un listado con las entradas de favoritos
	ficheros = os.listdir(ERROR_PATH)
	for fichero in ficheros:

		try:
			# Lee el bookmark
			titulo,thumbnail,plot,server,url = readbookmark(fichero)

			# Crea la entrada
			# En la categoría va el nombre del fichero para poder borrarlo
			xbmctools.addnewvideo( CHANNELNAME , "play" , os.path.join( DOWNLOAD_PATH, fichero ) , server , titulo , url , thumbnail, plot )
		except:
			pass

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def downloadall(params,url,category):
	xbmc.output("[downloadall.py] mainlist")

	# Crea un listado con las entradas de favoritos
	while len(os.listdir(DOWNLOAD_PATH))>0:
		# El primer video de la lista
		fichero = os.listdir(DOWNLOAD_PATH)[0]
		if fichero!="error":
			xbmc.output("[downloadall.py] fichero="+fichero)

			# Descarga el vídeo
			try:
				# Lee el bookmark
				titulo,thumbnail,plot,server,url = readbookmark(fichero)
				xbmc.output("[downloadall.py] url="+url)

				# Averigua la URL del vídeo
				if (server=="Megavideo" or server=="Megaupload") and xbmcplugin.getSetting("megavideopremium")=="true":
					if server=="Megaupload":
						mediaurl = servertools.getmegauploadhigh(url)
					else:
						mediaurl = servertools.getmegavideohigh(url)
				else:
					mediaurl = servertools.findurl(url,server)
				xbmc.output("[downloadall.py] mediaurl="+mediaurl)
				
				# Genera el NFO
				nfofilepath = downloadtools.getfilefromtitle("sample.nfo",titulo)
				outfile = open(nfofilepath,"w")
				outfile.write("<movie>\n")
				outfile.write("<title>"+titulo+")</title>\n")
				outfile.write("<originaltitle></originaltitle>\n")
				outfile.write("<rating>0.000000</rating>\n")
				outfile.write("<year>2009</year>\n")
				outfile.write("<top250>0</top250>\n")
				outfile.write("<votes>0</votes>\n")
				outfile.write("<outline></outline>\n")
				outfile.write("<plot>"+plot+"</plot>\n")
				outfile.write("<tagline></tagline>\n")
				outfile.write("<runtime></runtime>\n")
				outfile.write("<thumb></thumb>\n")
				outfile.write("<mpaa>Not available</mpaa>\n")
				outfile.write("<playcount>0</playcount>\n")
				outfile.write("<watched>false</watched>\n")
				outfile.write("<id>tt0432337</id>\n")
				outfile.write("<filenameandpath></filenameandpath>\n")
				outfile.write("<trailer></trailer>\n")
				outfile.write("<genre></genre>\n")
				outfile.write("<credits></credits>\n")
				outfile.write("<director></director>\n")
				outfile.write("<actor>\n")
				outfile.write("<name></name>\n")
				outfile.write("<role></role>\n")
				outfile.write("</actor>\n")
				outfile.write("</movie>")
				outfile.flush()
				outfile.close()
				
				# Descarga el thumbnail
				xbmc.output("[downloadall.py] thumbnail="+thumbnail)
				thumbnailfile = downloadtools.getfilefromtitle(thumbnail,titulo)
				xbmc.output("[downloadall.py] thumbnailfile="+thumbnailfile)
				thumbnailfile = thumbnailfile[:-4] + ".tbn"
				xbmc.output("[downloadall.py] thumbnailfile="+thumbnailfile)
				try:
					downloadtools.downloadfile(thumbnail,thumbnailfile)
				except:
					xbmc.output("[downloadall.py] error al descargar thumbnail")
					for line in sys.exc_info():
						xbmc.output( "%s" % line , xbmc.LOGERROR )
				
				# Descarga el video
				dev = downloadtools.downloadtitle(mediaurl,titulo)
				if dev == -1:
					# El usuario ha cancelado la descarga
					xbmc.output("[downloadall.py] cancelando descarga")
					return
				elif dev == -2:
					# Error en la descarga, lo mueve a ERROR y continua con el siguiente
					xbmc.output("[downloadall.py] ERROR EN DESCARGA DE "+fichero)
					origen = os.path.join( DOWNLOAD_PATH , fichero )
					destino = os.path.join( ERROR_PATH , fichero )
					shutil.move( origen , destino )
				else:
					# Borra el bookmark e itera para obtener el siguiente video
					filepath = os.path.join( DOWNLOAD_PATH , fichero )
					os.remove(filepath)
			except:
				xbmc.output("[downloadall.py] ERROR EN DESCARGA DE "+fichero)
				origen = os.path.join( DOWNLOAD_PATH , fichero )
				destino = os.path.join( ERROR_PATH , fichero )
				shutil.move( origen , destino )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
def play(params,url,category):
	xbmc.output("[descargadoslist.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo3(CHANNELNAME,server,url,category,title,thumbnail,plot)

def readbookmark(filename):
	xbmc.output("[descargadoslist.py] readbookmark")

	filepath = os.path.join( DOWNLOAD_PATH , filename )

	# Lee el fichero de configuracion
	xbmc.output("[descargadoslist.py] filepath="+filepath)
	bookmarkfile = open(filepath)
	lines = bookmarkfile.readlines()

	try:
		titulo = urllib.unquote_plus(lines[0].strip())
	except:
		titulo = lines[0].strip()
	
	try:
		url = urllib.unquote_plus(lines[1].strip())
	except:
		url = lines[1].strip()
	
	try:
		thumbnail = urllib.unquote_plus(lines[2].strip())
	except:
		thumbnail = lines[2].strip()
	
	try:
		server = urllib.unquote_plus(lines[3].strip())
	except:
		server = lines[3].strip()
		
	try:
		plot = urllib.unquote_plus(lines[4].strip())
	except:
		plot = lines[4].strip()

	bookmarkfile.close();

	return titulo,thumbnail,plot,server,url

def savebookmark(titulo,url,thumbnail,server,plot):
	xbmc.output("[descargadoslist.py] savebookmark")

	try:
		os.mkdir(DOWNLOAD_PATH)
		os.mkdir(ERROR_PATH)
	except:
		pass

	# No va bien más que en Windows
	#bookmarkfiledescriptor,bookmarkfilepath = tempfile.mkstemp(suffix=".txt",prefix="",dir=DOWNLOAD_PATH)
	
	filenumber=0
	salir = False
	while not salir:
		filename = '%08d.txt' % filenumber
		xbmc.output("[descargadoslist.py] savebookmark filename="+filename)
		fullfilename = os.path.join(DOWNLOAD_PATH,filename)
		xbmc.output("[descargadoslist.py] savebookmark fullfilename="+fullfilename)
		if not os.path.exists(fullfilename):
			salir=True
		filenumber = filenumber + 1

	bookmarkfile = open(fullfilename,"w")
	bookmarkfile.write(urllib.quote_plus(downloadtools.limpia_nombre_excepto_1(titulo))+'\n')
	bookmarkfile.write(urllib.quote_plus(url)+'\n')
	bookmarkfile.write(urllib.quote_plus(thumbnail)+'\n')
	bookmarkfile.write(urllib.quote_plus(server)+'\n')
	bookmarkfile.write(urllib.quote_plus(downloadtools.limpia_nombre_excepto_1(plot))+'\n')
	bookmarkfile.flush();
	bookmarkfile.close()
