# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# ayuda - Videos de ayuda y tutoriales para pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribuci�n de jurrabi
#----------------------------------------------------------------------
import re
import sys
import xbmc
import xbmcplugin
import xbmcgui
import scrapertools
import xbmctools
import config
import logger

CHANNELNAME = "ayuda"

# Esto permite su ejecuci�n en modo emulado
try:
  pluginhandle = int( sys.argv[ 1 ] )
except:
  pluginhandle = ""

# Traza el inicio del canal
logger.info("[ayuda.py] init")

DEBUG = True

SOURCE_URL = 'http://www.mimediacenter.info/foro/viewtopic.php?f=6&t=402'

def fixSTRMLibrary(params,url,category):
    import library
    total,errores = library.fixStrmLibrary()
    dlg = xbmcgui.Dialog()
    dlg.ok('pelisalacarta - Fix STRM','Se convirti� la biblioteca.','%s actualizados, %s errores' % (total,errores))
    return
    
##############################################################################
def mainlist(params,url,category):
  """Obtiene los videos de ayuda del foro y los lista para su visionado

  """
  logger.info("[ayuda.py] mainlist")

  #Arreglador de biblioteca
  xbmctools.addnewfolder( CHANNELNAME , "fixSTRMLibrary" , "Other" , "Convertir Biblioteca strm" , "http://null" , thumbnail="" , plot="Convierte los archivos strm existentes en la biblioteca actual para que funcionen tras un upgrade a XBMC Dharma (v10.5). Tambien se puede ejecutar para adaptar archivos de un XBMC mas moderno a otro anterior. B�sicamente deja los ficheros strm de la forma correcta para que funcionen en la versi�n actualmente instalada." )

  
  data = scrapertools.cachePage(SOURCE_URL)
  if len(data) == 0:
    dlog ("[ayuda.py] No se pudo descargar la p�gina de ayuda :" + SOURCE_URL)
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal Ayuda','No se han podido recuperar los videos de ayuda')
    return

# Ej. VIDEO 1 - <a href="http://www.youtube.com/watch?v=W3m-EBxRsfs" class="postlink">Demo del uso de la biblioteca de series alimentada desde pelisalacarta</a><img src="http://lh5.ggpht.com/_0n3bg7O9o2M/S6VNz04c6tI/AAAAAAAAB6Y/MseMGa7FWVg/s800/Ayuda%201.%20Como%20configurar%20la%20biblioteca.jpg" alt="Imagen" />
  patronvideos = '''(?x)                                #      Activa opci�n VERBOSE.
    VIDEO\                                              #      Basura
    ([0-9]+)\ -\                                        # $0 = N� de Video de Ayuda
    <a\ href="                                          #      Basura
    ([^"]+)"\ class="postlink">                         # $1 = url del contenido (youtube)
    ([^<]+)</a><img\ src="                              # $2 = Nombre del video
    (?:([^"]+)"\ alt="Imagen"\ />)?                     # $3 = Foto de portada
    (?:<br\ />[^<]*<a\ href="                           #      Basura (opcional)
    ([^"]+)                                             # $4 = Link Megavideo (opcional)
    "\ class="postlink">Megavideo</a>)?                 #      Basura (opcional)
    ''' 
  matches = re.findall(patronvideos,data)
  totalmatches = len(matches)
  if totalmatches == 0:
    dlog ("[ayuda.py] La p�gina de ayuda no contiene v�deos accesibles :" + SOURCE_URL)
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal Ayuda','No se han podido recuperar los videos de ayuda')
    return

  for match in matches:
    title = '%s. %s' % (match[0],match[2])
    image = match[3]
    if match[4] == '':
      url = match[1]
      xbmctools.addnewvideo( "trailertools" , "youtubeplay" , "Ayuda" , "Directo" , title , url , image , plot="")
    else: #Megavideo Disponible
      url = match[4][-8:]
      xbmctools.addnewvideo( "cinetube" , "play" , "Ayuda", "megavideo" , title , url , image , plot="")

  FinalizaPlugin (pluginhandle,category)

def FinalizaPlugin (pluginhandle,category):
  """Tareas comunes al final del plugin. Sin ordenaci�n
  """
  # Indicar metadatos del plugin para skis (Categor�a y contenido)
  xbmcplugin.setPluginCategory (pluginhandle , category)
  xbmcplugin.setContent (pluginhandle , category) #Estamos usando category como content.

  # Deshabilitar ordenaci�n
  xbmcplugin.addSortMethod (handle=pluginhandle , sortMethod=xbmcplugin.SORT_METHOD_NONE)

  # Finalizar Directorio del Plugin
  xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
  
def dlog (text):
  if DEBUG:
    logger.info(text)
