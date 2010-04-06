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
import xml.parsers.expat


CHANNELNAME = "library"
allchars = string.maketrans('', '')
deletechars = '\\/:*"<>|?	' #Caracteres no válidos en nombres de archivo

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

#MONITOR_FILE
MONITOR_FILE = xbmc.translatePath( os.path.join( LIBRARY_PATH, 'monitor.xml' ) )
if not os.path.exists(MONITOR_FILE):
	xbmc.output("[library.py] No existe fichero de monitorización de series:"+MONITOR_FILE)
#	os.mkdir(SERIES_PATH) SUSTITUIR POR FUNCION ADECUADA PARA CREACIÓN DE FICHEROS XML CON LA SIGUIENTE ESTRUCTURA:
# <monitor>
#   <series serie=name>url</serie>
# </monitor>

def savelibrary(titulo,url,thumbnail,server,plot,canal="",category="Cine",Serie="",verbose=True,accion="strm",pedirnombre=True):
	'''Añade el elemento indicado a la biblioteca de xbmc (a través de un fichero strm)
	
	 category puede ser "Series", "Cine", "Documental" u "Otros". Si es Otros se permite un tipo personalizado
	 Si category="Series" entonces Serie contiene el nombre de la serie
	 Si pedirnombre  = True entonces se muestra pantalla de selección
	'''

	xbmc.output("[favoritos.py] saveLIBRARY")
	xbmc.output("[library.py] saveLIBRARY titulo="+titulo)
	xbmc.output("[library.py] saveLIBRARY url="+url)
	xbmc.output("[library.py] saveLIBRARY server="+server)
	xbmc.output("[library.py] saveLIBRARY canal="+canal)
	xbmc.output("[library.py] saveLIBRARY category="+category)
	xbmc.output("[library.py] saveLIBRARY serie="+Serie)
	xbmc.output("[library.py] saveLIBRARY accion="+accion)
	
	#Limpiamos el título para usarlo como fichero
	try:
		filename = string.translate(titulo,allchars,deletechars)
	except:
		filename = titulo

	if pedirnombre:
		keyboard = xbmc.Keyboard(filename)
		keyboard.doModal()
		if not keyboard.isConfirmed():
			return False
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
		nuevo = 0
	else:
		nuevo = 1
	try:
		LIBRARYfile = open(fullfilename,"w")
	except IOError:
		xbmc.output("Error al grabar el archivo "+fullfilename)
		nuevo = 0
		raise
#	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , "strm" , urllib.quote_plus( category ) , urllib.quote_plus( titulo ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
# Eliminación de plot i thumnai
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( titulo ) , urllib.quote_plus( url ) , "" , "" , server , Serie)
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

	return nuevo
	
def update(total,errores=0, nuevos=0, serie="No indicada"):
	"""Pide Resumen de actualización. Además pregunta y actualiza la Biblioteca
	
	nuevos: Número de episodios actualizados. Se muestra como resumen en la ventana 
	        de confirmación.
	total:  Número de episodios Totales en la Biblioteca. Se muestra como resumen 
	        en la ventana de confirmación.
	Erores: Número de episodios que no se pudo añadir (generalmente por caracteres 
	        no válidos en el nombre del archivo o por problemas de permisos.
	"""
	
	if nuevos == 1:
		texto = 'Se ha añadido 1 episodio a la Biblioteca (%d en total)' % (total,)
	else:
		texto = 'Se han añadido %d episodios a la Biblioteca (%d en total)' % (nuevos,total)
	advertencia = xbmcgui.Dialog()

	# Pedir confirmación para actualizar la biblioteca
	if nuevos > 0:
		if errores == 0:
			actualizar = advertencia.yesno('pelisalacarta' , texto ,'¿Deseas que actualice ahora la Biblioteca?')
		else:  # Si hubo errores muestra una línea adicional en la pregunta de actualizar biblioteca
			if errores == 1:
				texto2 = '(No se pudo añadir 1 episodio)'
			else:
				texto2 = '(No se pudieron añadir '+str(errores)+' episodios)'
			actualizar = advertencia.yesno('pelisalacarta' , texto , texto2 , '¿Deseas que actualice ahora la Biblioteca?')
	else: #No hay episodios nuevos -> no actualizar
		if errores == 0:
			texto2 = ""
		elif errores == 1:
			texto2 = '(No se pudo añadir 1 episodio)'
		else:
			texto2 = '(No se pudieron añadir '+str(errores)+' episodios)'
		advertencia.ok('pelisalacarta',texto,texto2)
		actualizar = False
	
	if actualizar:
		xbmc.executebuiltin('UpdateLibrary(video)')

	xbmc.output ('[Library update] Serie: "%s". Total: %d, Erroneos: %d, Nuevos: %d' %(serie, total, errores, nuevos))

def MonitorSerie ( canal, accion, server, url, serie): 
	''' Añade una serie a la lista de series a monitorizar.
	
	Si se configura para que lo haga pelisalacarta arrancará un proceso al inicio de XBMC
	para monitorizar las series que se desee mediante una llamada a esta función.
	Los episodios nuevos que vayan apareciendo en la web del canal para la serie indicada
	se irán añadiendo a la biblioteca.
	Para dejar de monitorizar una serie llamar a StopMonitorSerie
	'''
	parser = xml.parsers.expat.ParserCreate()
	
	
def dlog (text):
	if DEBUG:
		xbmc.output(text)
