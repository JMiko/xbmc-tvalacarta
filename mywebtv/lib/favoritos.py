# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de v�deos favoritos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
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
import downloadtools

from core import config
from core import logger

CHANNELNAME = "favoritos"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[favoritos.py] init")

DEBUG = True

BOOKMARK_PATH = xbmc.translatePath( os.path.join( config.get_data_path(), 'bookmarks' ) )
if not os.path.exists(BOOKMARK_PATH):
    os.makedirs(BOOKMARK_PATH)

def mainlist(params,url,category):
	logger.info("[favoritos.py] mainlist")

	# Crea un listado con las entradas de favoritos
	ficheros = os.listdir(BOOKMARK_PATH)
	for fichero in ficheros:

		try:
			# Lee el bookmark
			titulo,thumbnail,plot,server,url = readbookmark(fichero)

			# Crea la entrada
			# En la categor�a va el nombre del fichero para poder borrarlo
			xbmctools.addnewvideo( CHANNELNAME , "play" , os.path.join( BOOKMARK_PATH, fichero ) , server , titulo , url , thumbnail, plot )
		except:
			pass

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	logger.info("[favoritos.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo2(CHANNELNAME,server,url,category,title,thumbnail,plot)

def readbookmark(filename):
	logger.info("[favoritos.py] readbookmark")

	filepath = os.path.join( BOOKMARK_PATH , filename )

	# Lee el fichero de configuracion
	logger.info("[favoritos.py] filepath="+filepath)
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
	logger.info("[favoritos.py] savebookmark")

	# No va bien m�s que en Windows
	#bookmarkfiledescriptor,bookmarkfilepath = tempfile.mkstemp(suffix=".txt",prefix="",dir=BOOKMARK_PATH)
	
	filenumber=0
	salir = False
	while not salir:
		filename = '%08d.txt' % filenumber
		logger.info("[favoritos.py] savebookmark filename="+filename)
		fullfilename = os.path.join(BOOKMARK_PATH,filename)
		logger.info("[favoritos.py] savebookmark fullfilename="+fullfilename)
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
