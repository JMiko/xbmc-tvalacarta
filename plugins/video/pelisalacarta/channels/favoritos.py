# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos favoritos
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
import tempfile

CHANNELNAME = "favoritos"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[favoritos.py] init")

DEBUG = True

BOOKMARK_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'bookmarks' ) )

def mainlist(params,url,category):
	xbmc.output("[favoritos.py] mainlist")

	# Crea un listado con las entradas de favoritos
	ficheros = os.listdir(BOOKMARK_PATH)
	for fichero in ficheros:

		# Lee el bookmark
		titulo,thumbnail,plot,server,url = readbookmark(fichero)

		# Crea la entrada
		# En la categoría va el nombre del fichero para poder borrarlo
		xbmctools.addnewvideo( CHANNELNAME , "play" , os.path.join( BOOKMARK_PATH, fichero ) , server , titulo , url , thumbnail, plot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[favoritos.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo2(CHANNELNAME,server,url,category,title,thumbnail,plot)

def readbookmark(filename):
	xbmc.output("[favoritos.py] readbookmark")

	filepath = os.path.join( BOOKMARK_PATH , filename )

	# Lee el fichero de configuracion
	xbmc.output("[favoritos.py] filepath="+filepath)
	bookmarkfile = open(filepath)
	lines = bookmarkfile.readlines()

	titulo = lines[0].strip()
	url = lines[1].strip()
	thumbnail = lines[2].strip()
	server = lines[3].strip()
	plot = lines[4].strip()

	bookmarkfile.close();

	return titulo,thumbnail,plot,server,url

def savebookmark(titulo,url,thumbnail,server,plot):
	xbmc.output("[favoritos.py] savebookmark")

	bookmarkfiledescriptor,bookmarkfilepath = tempfile.mkstemp(suffix=".txt",prefix="",dir=BOOKMARK_PATH)
	
	xbmc.output("[favoritos.py] savebookmark bookmarkfilepath="+bookmarkfilepath)
	bookmarkfile = os.fdopen(bookmarkfiledescriptor)
	#open(bookmarkfilepath,"w")
	bookmarkfile.write(titulo+'\n')
	bookmarkfile.write(url+'\n')
	bookmarkfile.write(thumbnail+'\n')
	bookmarkfile.write(server+'\n')
	bookmarkfile.write(plot+'\n')
	bookmarkfile.flush();
	bookmarkfile.close()
