# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Herramientas de integraci�n en Librer�a
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
deletechars = '\\/:*"<>|?	' #Caracteres no v�lidos en nombres de archivo

# Esto permite su ejecuci�n en modo emulado (preguntar a jesus por esto)
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


def savelibrary(titulo,url,thumbnail,server,plot,canal="seriesyonkis",category="Cine",Serie="",verbose=True,accion="strm",pedirnombre=True):
	# category puede ser "Series", "Cine", "Documental" u "Otros". Si es Otros se permite un tipo personalizado
	# Si category="Series" entonces Serie contiene el nombre de la serie
	# Si pedirnombre  = True entonces se muestra pantalla de selecci�n

	xbmc.output("[favoritos.py] saveLIBRARY")
	xbmc.output("[library.py] saveLIBRARY titulo="+titulo)
	xbmc.output("[library.py] saveLIBRARY url="+url)
	xbmc.output("[library.py] saveLIBRARY server="+server)
	xbmc.output("[library.py] saveLIBRARY canal="+canal)
	xbmc.output("[library.py] saveLIBRARY category="+category)
	xbmc.output("[library.py] saveLIBRARY serie="+Serie)
	xbmc.output("[library.py] saveLIBRARY accion="+accion)
	
	#Limpiamos el t�tulo para usarlo como fichero
	try:
		filename = string.translate(titulo,allchars,deletechars)
	except:
		filename = titulo

	if pedirnombre:
		keyboard = xbmc.Keyboard(filename)
		keyboard.doModal()
		if not keyboard.isConfirmed():
			return
		filename = keyboard.getText()
	try:
		filename = string.translate(filename,allchars,deletechars)+".strm" #Volvemos a limpiar por si acaso
	except:
		filename = filename + ".strm"

	if category != "Series":  #JUR - DEBUGIN INTERNO PARA 2.14
		category = "Cine"
		
	if category == "Cine":
		fullfilename = os.path.join(MOVIES_PATH,filename)
	elif category == "Series":
		if Serie == "": #A�adir comprobaci�n de len>0 bien hecha
			xbmc.output('[library.py] ERROR: intentando a�adir una serie y serie=""')
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
	try:
		LIBRARYfile = open(fullfilename,"w")
	except IOError:
		xbmc.output("Error al grabar el archivo "+fullfilename)
		raise
#	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , "strm" , urllib.quote_plus( category ) , urllib.quote_plus( titulo ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
# Eliminaci�n de plot i thumnai
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
		resultado = advertencia.ok('pelisalacarta' , titulo , 'se ha a�adido a Librer�a')

def update(total,errores=0):
	"""Pide confirmaci�n para actualizar la biblioteca de xbmc despues de a�adir serie.

	total:  N�mero de episodios actualizados. Se muestra como resumen en la ventana 
	        de confirmaci�n.
	Erores: N�mero de episodios que no se pudo a�adir (generalmente por caracteres 
	        no v�lidos en el nombre del archivo o por problemas de permisos.
	"""
	
	if total == 1:
		texto = 'Se ha a�adido 1 episodio a la Biblioteca'
	else:
		texto = 'Se han a�adido '+str(total)+' episodios a la Biblioteca'
	advertencia = xbmcgui.Dialog()

	# Pedir confirmaci�n para actualizar la biblioteca
	if errores == 0:
		actualizar = advertencia.yesno('pelisalacarta' , texto ,'�Deseas que actualice ahora la Biblioteca?')
	else:  # Si hubo errores muestra una l�nea adicional en la pregunta de actualizar biblioteca
		if errores == 1:
			texto2 = '(No se pudo a�adir 1 episodio)'
		else:
			texto2 = '(No se pudieron a�adir '+str(errores)+' episodios)'
		actualizar = advertencia.yesno('pelisalacarta' , texto , texto2 , '�Deseas que actualice ahora la Biblioteca?')

	if actualizar:
		xbmc.executebuiltin('UpdateLibrary(video)')
