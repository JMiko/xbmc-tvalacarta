# -*- coding: iso-8859-1 -*-

#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta
# XBMC Plugin
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import time

PLUGIN_NAME = "pelisalacarta"
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )
ROOT_DIR = os.getcwd()

REMOTE_VERSION_FILE = "http://www.mimediacenter.info/xbmc/pelisalacarta/version.xml"
LOCAL_VERSION_FILE = xbmc.translatePath( os.path.join( ROOT_DIR , "version.xml" ) )
REMOTE_FILE = "http://xbmc-tvalacarta.googlecode.com/files/pelisalacarta-"
LOCAL_FILE = xbmc.translatePath( os.path.join( ROOT_DIR , "pelisalacarta-" ) )

try:
	DESTINATION_FOLDER = xbmc.translatePath( "special://home/plugins/video")
except:
	DESTINATION_FOLDER = xbmc.translatePath( os.path.join( ROOT_DIR , ".." ) )

def checkforupdates():
	xbmc.output("[updater.py] checkforupdates")
	try:
		# Descarga el fichero con la versión en la web
		xbmc.output("Verificando actualizaciones...")
		xbmc.output("Version remota: "+REMOTE_VERSION_FILE)
		data = scrapertools.cachePage( REMOTE_VERSION_FILE )
		xbmc.output("xml descargado="+data)
		patronvideos  = '<tag>([^<]+)</tag>'
		matches = re.compile(patronvideos,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		versiondescargada = matches[0]
		xbmc.output("version descargada="+versiondescargada)
		
		# Lee el fichero con la versión instalada
		localFileName = LOCAL_VERSION_FILE
		xbmc.output("Version local: "+localFileName)
		infile = open( localFileName )
		data = infile.read()
		infile.close();
		xbmc.output("xml local="+data)
		matches = re.compile(patronvideos,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		versionlocal = matches[0]
		xbmc.output("version local="+versionlocal)

		if (versiondescargada > versionlocal):
			xbmc.output("actualizacion disponible")
			
			# Añade al listado de XBMC
			listitem = xbmcgui.ListItem( "Descargar version "+versiondescargada, iconImage=os.path.join(IMAGES_PATH, "Crystal_Clear_action_info.png"), thumbnailImage=os.path.join(IMAGES_PATH, "Crystal_Clear_action_info.png") )
			itemurl = '%s?action=update&version=%s' % ( sys.argv[ 0 ] , versiondescargada )
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
			
			# Avisa con un popup
			dialog = xbmcgui.Dialog()
			dialog.ok("Versión "+versiondescargada+" disponible","Ya puedes descargar la nueva versión del plugin\ndesde el listado principal")

	except:
		xbmc.output("No se han podido verificar actualizaciones...")
		print "ERROR: %s (%d) - %s" % ( sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

def update(params):
	# Descarga el ZIP
	xbmc.output("[updater.py] update")
	xbmc.output("[updater.py] cwd="+os.getcwd())
	remotefilename = REMOTE_FILE+params.get("version")+".zip"
	localfilename = LOCAL_FILE+params.get("version")+".zip"
	xbmc.output("[updater.py] remotefilename=%s" % remotefilename)
	xbmc.output("[updater.py] localfilename=%s" % localfilename)
	xbmc.output("[updater.py] descarga fichero...")
	inicio = time.clock()
	urllib.urlretrieve(remotefilename,localfilename)
	fin = time.clock()
	xbmc.output("[updater.py] Descargado en %d segundos " % (fin-inicio+1))
	
	# Lo descomprime
	xbmc.output("[updater.py] descomprime fichero...")
	import ziptools
	unzipper = ziptools.ziptools()
	destpathname = DESTINATION_FOLDER
	xbmc.output("[updater.py] destpathname=%s" % destpathname)
	unzipper.extract(localfilename,destpathname)
	
	# Borra el zip descargado
	xbmc.output("[updater.py] borra fichero...")
	os.remove(localfilename)