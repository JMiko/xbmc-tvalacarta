# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Herramientas de integración en Librería
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Autor: jurrabi
#------------------------------------------------------------
#import urlparse,urllib2,urllib,re
import urllib
import os
import sys
import xbmc
import xbmcgui
#import xbmcplugin
#import scrapertools
#import megavideo
#import servertools
#import binascii
#import xbmctools
import downloadtools
import string

CHANNELNAME = "library"
allchars = string.maketrans('', '')
deletechars = '\\/:*"<>|?' #Caracteres no válidos en nombres de archivo

# Esto permite su ejecución en modo emulado (preguntar a jesus por esto)
# seguro que viene bien para debuguear
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[library.py] init")

DEBUG = True

#LIBRARY_PATH
LIBRARY_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'library' ) )
if not os.path.exists(LIBRARY_PATH):
	xbmc.output("[library.py] Library path doesn't exist:"+LIBRARY_PATH)
	os.mkdir(LIBRARY_PATH)

#MOVIES_PATH
MOVIES_PATH = xbmc.translatePath( os.path.join( LIBRARY_PATH, 'CINE' ) )
if not os.path.exists(MOVIES_PATH):
	xbmc.output("[library.py] Movies path doesn't exist:"+MOVIES_PATH)
	os.mkdir(MOVIES_PATH)

#SERIES_PATH
SERIES_PATH = xbmc.translatePath( os.path.join( LIBRARY_PATH, 'SERIES' ) )
if not os.path.exists(SERIES_PATH):
	xbmc.output("[library.py] Series path doesn't exist:"+SERIES_PATH)
	os.mkdir(SERIES_PATH)


def savelibrary(titulo,url,thumbnail,server,plot,canal="seriesyonkis",category="",Serie="",verbose=True,accion="strm"):
	# category puede ser "Series", "Cine", "Documental" u "Otros". Si es Otros se permite un tipo personalizado
	# Si category="Series" entonces Serie contiene el nombre de la serie
	# Si asktitulo  = True entonces se muestra pantalla de selección

	xbmc.output("[favoritos.py] saveLIBRARY")
	xbmc.output("[library.py] saveLIBRARY titulo="+titulo)
	xbmc.output("[library.py] saveLIBRARY url="+url)
	xbmc.output("[library.py] saveLIBRARY server="+server)
	xbmc.output("[library.py] saveLIBRARY canal="+canal)
	xbmc.output("[library.py] saveLIBRARY category="+category)
	xbmc.output("[library.py] saveLIBRARY serie="+Serie)
	xbmc.output("[library.py] saveLIBRARY accion="+accion)

	#Pedir título y 
	#Determinar Tipo: Cine, Serie, Documental, Otro
	#if asktitulo :
	#	keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(titulo))
	#	keyboard.doModal()
	#	if (keyboard.isConfirmed()):
	#		titulo = keyboard.getText()
	
	#Limpiamos el título para usarlo como fichero
	filename = string.translate(titulo,allchars,deletechars)+".strm"

	if category == "Cine":
		fullfilename = os.path.join(MOVIES_PATH,filename)
	elif category == "Series":
		if Serie == "": #Añadir comprobación de len>0 bien hecha
			xbmc.output('[library.py] ERROR: intentando añadir una serie y serie=""')
			pathserie = SERIES_PATH
		else:
			#Eliminamos caracteres indeseados para archivos en el nombre de la serie
			Serie = string.translate(Serie,allchars,deletechars)
			pathserie = xbmc.translatePath( os.path.join( SERIES_PATH, Serie ) )
		if not os.path.exists(pathserie):
			xbmc.output("[library.py] Creando directorio serie:"+pathserie)
			os.mkdir(pathserie)
		fullfilename = os.path.join(pathserie,filename)
	else:    #Resto de categorias de momento en la raiz de library
		fullfilename = os.path.join(LIBRARY_PATH,filename)
		
	xbmc.output("[favoritos.py] saveLIBRARY fullfilename="+fullfilename)
	if os.path.exists(fullfilename):
		xbmc.output("[favoritos.py] el fichero existe. Se sobreescribe")

	LIBRARYfile = open(fullfilename,"w")
#	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , "strm" , urllib.quote_plus( category ) , urllib.quote_plus( titulo ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
# Eliminación de plot i thumnai
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( titulo ) , urllib.quote_plus( url ) , "" , "" , server )
	xbmc.output("[library.py] itemurl=%s" % itemurl)

	LIBRARYfile.write(itemurl)
#	LIBRARYfile.write(urllib.quote_plus(url)+'\n')
#	LIBRARYfile.write(urllib.quote_plus(thumbnail)+'\n')
#	LIBRARYfile.write(urllib.quote_plus(server)+'\n')
#	LIBRARYfile.write(urllib.quote_plus(downloadtools.limpia_nombre_excepto_1(plot))+'\n')
	LIBRARYfile.flush();
	LIBRARYfile.close()

	if verbose:
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('pelisalacarta' , titulo , 'se ha añadido a Librería')

def update(total):
	if total == 1:
		texto = 'Se ha añadido 1 episodio a la Biblioteca'
	else:
		texto = 'Se han añadido '+str(total)+' episodios a la Biblioteca'
	
	advertencia = xbmcgui.Dialog()
	if advertencia.yesno('pelisalacarta' , texto ,'¿Deseas que actualice ahora la Biblioteca?'):
		xbmc.executebuiltin('UpdateLibrary(video)')