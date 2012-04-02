# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# ayuda - Videos de ayuda y tutoriales para pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribuci�n de jurrabi
#----------------------------------------------------------------------
import re
from core import scrapertools
from core import config
from core import logger
from core.item import Item

CHANNELNAME = "ayuda"

# Traza el inicio del canal
logger.info("[ayuda.py] init")

DEBUG = config.get_setting("debug")
SOURCE_URL = 'http://www.mimediacenter.info/foro/viewtopic.php?f=6&t=402'

def isGeneric():
    return True

def fixSTRMLibrary(params,url,category):
    from platformcode.xbmc import library
    total,errores = library.fixStrmLibrary()
    import xbmcgui
    dlg = xbmcgui.Dialog()
    dlg.ok('pelisalacarta - Fix STRM','Se convirti� la biblioteca.','%s actualizados, %s errores' % (total,errores))
    return
    
##############################################################################
def mainlist(item):
    """Obtiene los videos de ayuda del foro y los lista para su visionado
    
    """
    logger.info("[ayuda.py] mainlist")
    itemlist = []
    from core import platform_name
    if platform_name.PLATFORM_NAME=="xbmceden":
        itemlist.append( Item(channel=CHANNELNAME, action="force_creation_advancedsettings" , title="Crear fichero advancedsettings.xml optimizado"))
        
    if platform_name.PLATFORM_NAME!="xbmceden":
        itemlist.append( Item(channel=CHANNELNAME, action="updatebiblio" , title="Buscar nuevos episodios y actualizar biblioteca"))
        
    # Arreglador de biblioteca
    if config.get_platform()=="xbmc":
        itemlist.append( Item(channel=CHANNELNAME, action="fixSTRMLibrary" , title="Convertir Biblioteca strm",plot="Convierte los archivos strm existentes en la biblioteca actual para que funcionen tras un upgrade a XBMC Dharma (v10.5). Tambien se puede ejecutar para adaptar archivos de un XBMC mas moderno a otro anterior. B�sicamente deja los ficheros strm de la forma correcta para que funcionen en la versi�n actualmente instalada."))
        
    data = scrapertools.cachePage(SOURCE_URL)
    if len(data) == 0:
        logger.info("[ayuda.py] No se pudo descargar la p�gina de ayuda :" + SOURCE_URL)
        return itemlist

    # Ej. VIDEO 1 - <a href="http://www.youtube.com/watch?v=W3m-EBxRsfs" class="postlink">Demo del uso de la biblioteca de series alimentada desde pelisalacarta</a><img src="http://lh5.ggpht.com/_0n3bg7O9o2M/S6VNz04c6tI/AAAAAAAAB6Y/MseMGa7FWVg/s800/Ayuda%201.%20Como%20configurar%20la%20biblioteca.jpg" alt="Imagen" />
    patronvideos = '''(?x)                                  #      Activa opci�n VERBOSE.
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
        logger.info("[ayuda.py] La p�gina de ayuda no contiene v�deos accesibles :" + SOURCE_URL)
        return itemlist

    for match in matches:
        title = '%s. %s' % (match[0],match[2])
        image = match[3]
        if match[4] == '':
            url = match[1]
            itemlist.append( Item(channel=CHANNELNAME, action="play", server="youtube", title=title + " [youtube]", url=url, thumbnail=image , folder=False ) )
        else: #Megavideo Disponible
            url = match[4][-8:]
            itemlist.append( Item(channel=CHANNELNAME, action="play", server="megavideo", title=title + " [megavideo]", url=url, thumbnail=image , folder=False ) )

    return itemlist

def force_creation_advancedsettings(item):

    # Ruta del advancedsettings
    import xbmc,xbmcgui,os
    advancedsettings = xbmc.translatePath("special://userdata/advancedsettings.xml")

    # Copia el advancedsettings.xml desde el directorio resources al userdata
    fichero = open( os.path.join(config.get_runtime_path(),"resources","advancedsettings.xml") )
    texto = fichero.read()
    fichero.close()
    
    fichero = open(advancedsettings,"w")
    fichero.write(texto)
    fichero.close()
                
    dialog2 = xbmcgui.Dialog()
    dialog2.ok("plugin", "Se ha creado un fichero advancedsettings.xml","con la configuraci�n �ptima para el streaming.")

    return []

def updatebiblio(item):
    import library_service
    
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="" , title="Actualizaci�n en curso..."))        
    
    return itemlist