# -*- coding: utf-8 -*-

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
import config
import logger

PLUGIN_NAME = "pelisalacarta"

if config.get_setting("thumbnail_type")=="0":
    IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'posters' ) )
else:
    IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'banners' ) )

ROOT_DIR = config.get_runtime_path()

REMOTE_VERSION_FILE = "http://blog.tvalacarta.info/descargas/"+PLUGIN_NAME+"-version.xml"
LOCAL_VERSION_FILE = xbmc.translatePath( os.path.join( ROOT_DIR , "version.xml" ) )
LOCAL_FILE = xbmc.translatePath( os.path.join( ROOT_DIR , PLUGIN_NAME+"-" ) )

try:
    if config.get_platform()=="xbmcdharma":
        REMOTE_FILE = "http://blog.tvalacarta.info/descargas/"+PLUGIN_NAME+"-xbmc-addon-"
        DESTINATION_FOLDER = xbmc.translatePath( "special://home/addons")
    else:
        REMOTE_FILE = "http://blog.tvalacarta.info/descargas/"+PLUGIN_NAME+"-xbmc-plugin-"
        DESTINATION_FOLDER = xbmc.translatePath( "special://home/plugins/video")
except:
    REMOTE_FILE = "http://blog.tvalacarta.info/descargas/"+PLUGIN_NAME+"-xbmc-plugin-"
    DESTINATION_FOLDER = xbmc.translatePath( os.path.join( ROOT_DIR , ".." ) )

def checkforupdates():
    xbmc.output("[updater.py] checkforupdates")

    # Descarga el fichero con la versión en la web
    xbmc.output("[updater.py] Verificando actualizaciones...")
    xbmc.output("[updater.py] Version remota: "+REMOTE_VERSION_FILE)
    data = scrapertools.cachePage( REMOTE_VERSION_FILE )
    #xbmc.output("xml descargado="+data)
    patronvideos  = '<tag>([^<]+)</tag>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    versiondescargada = matches[0]
    xbmc.output("[updater.py] version descargada="+versiondescargada)
    
    # Lee el fichero con la versión instalada
    localFileName = LOCAL_VERSION_FILE
    xbmc.output("[updater.py] Version local: "+localFileName)
    infile = open( localFileName )
    data = infile.read()
    infile.close();
    #xbmc.output("xml local="+data)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    versionlocal = matches[0]
    xbmc.output("[updater.py] version local="+versionlocal)

    arraydescargada = versiondescargada.split(".")
    arraylocal = versionlocal.split(".")
    
    # local 2.8.0 - descargada 2.8.0 -> no descargar
    # local 2.9.0 - descargada 2.8.0 -> no descargar
    # local 2.8.0 - descargada 2.9.0 -> descargar
    if len(arraylocal) == len(arraydescargada):
        #xbmc.output("caso 1")
        hayqueactualizar = False
        for i in range(0, len(arraylocal)):
            #print arraylocal[i], arraydescargada[i], int(arraydescargada[i]) > int(arraylocal[i])
            if int(arraydescargada[i]) > int(arraylocal[i]):
                hayqueactualizar = True
    # local 2.8.0 - descargada 2.8 -> no descargar
    # local 2.9.0 - descargada 2.8 -> no descargar
    # local 2.8.0 - descargada 2.9 -> descargar
    if len(arraylocal) > len(arraydescargada):
        #xbmc.output("caso 2")
        hayqueactualizar = False
        for i in range(0, len(arraydescargada)):
            #print arraylocal[i], arraydescargada[i], int(arraydescargada[i]) > int(arraylocal[i])
            if int(arraydescargada[i]) > int(arraylocal[i]):
                hayqueactualizar = True
    # local 2.8 - descargada 2.8.8 -> descargar
    # local 2.9 - descargada 2.8.8 -> no descargar
    # local 2.10 - descargada 2.9.9 -> no descargar
    # local 2.5 - descargada 3.0.0
    if len(arraylocal) < len(arraydescargada):
        #xbmc.output("caso 3")
        hayqueactualizar = True
        for i in range(0, len(arraylocal)):
            #print arraylocal[i], arraydescargada[i], int(arraylocal[i])>int(arraydescargada[i])
            if int(arraylocal[i]) > int(arraydescargada[i]):
                hayqueactualizar =  False
            elif int(arraylocal[i]) < int(arraydescargada[i]):
                hayqueactualizar =  True
                break

    if (hayqueactualizar):
        xbmc.output("[updater.py] actualizacion disponible")
        
        # Añade al listado de XBMC
        listitem = xbmcgui.ListItem( "Descargar version "+versiondescargada, iconImage=os.path.join(IMAGES_PATH, "poster" , "Crystal_Clear_action_info.png"), thumbnailImage=os.path.join(IMAGES_PATH, "Crystal_Clear_action_info.png") )
        itemurl = '%s?action=update&version=%s' % ( sys.argv[ 0 ] , versiondescargada )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
        
        # Avisa con un popup
        dialog = xbmcgui.Dialog()
        dialog.ok("Versión "+versiondescargada+" disponible","Ya puedes descargar la nueva versión del plugin\ndesde el listado principal")

    '''
    except:
        xbmc.output("No se han podido verificar actualizaciones...")
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
    '''
def update(params):
    # Descarga el ZIP
    xbmc.output("[updater.py] update")
    remotefilename = REMOTE_FILE+params.get("version")+".zip"
    localfilename = LOCAL_FILE+params.get("version")+".zip"
    xbmc.output("[updater.py] remotefilename=%s" % remotefilename)
    xbmc.output("[updater.py] localfilename=%s" % localfilename)
    xbmc.output("[updater.py] descarga fichero...")
    inicio = time.clock()
    
    #urllib.urlretrieve(remotefilename,localfilename)
    from core import downloadtools
    downloadtools.downloadfile(remotefilename, localfilename)
    
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

def get_channel_remote_url(channel_name):
    if channel_name<>"channelselector":
        remote_channel_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/"+PLUGIN_NAME+"/"+PLUGIN_NAME+"/channels/"+channel_name+".py"
        remote_version_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/"+PLUGIN_NAME+"/"+PLUGIN_NAME+"/channels/"+channel_name+".xml"
    else:
        remote_channel_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/"+PLUGIN_NAME+"/"+channel_name+".py"
        remote_version_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/"+PLUGIN_NAME+"/"+channel_name+".xml"

    logger.info("remote_channel_url="+remote_channel_url)
    logger.info("remote_version_url="+remote_version_url)
    
    return remote_channel_url , remote_version_url

def get_channel_local_path(channel_name):
    import xbmc
    # TODO: (3.2) El XML debería escribirse en el userdata, de forma que se leerán dos ficheros locales: el del userdata y el que está junto al py (vendrá con el plugin). El mayor de los 2 es la versión actual, y si no existe fichero se asume versión 0
    if channel_name<>"channelselector":
        local_channel_path = xbmc.translatePath( os.path.join( config.get_runtime_path(), PLUGIN_NAME , 'channels' , channel_name+".py" ) )
        local_version_path = xbmc.translatePath( os.path.join( config.get_runtime_path(), PLUGIN_NAME , 'channels' , channel_name+".xml" ) )
        local_compiled_path = xbmc.translatePath( os.path.join( config.get_runtime_path(), PLUGIN_NAME , 'channels' , channel_name+".pyo" ) )
    else:
        local_channel_path = xbmc.translatePath( os.path.join( config.get_runtime_path() , channel_name+".py" ) )
        local_version_path = xbmc.translatePath( os.path.join( config.get_runtime_path() , channel_name+".xml" ) )
        local_compiled_path = xbmc.translatePath( os.path.join( config.get_runtime_path() , channel_name+".pyo" ) )

    logger.info("local_channel_path="+local_channel_path)
    logger.info("local_version_path="+local_version_path)
    logger.info("local_compiled_path="+local_compiled_path)
    
    return local_channel_path , local_version_path , local_compiled_path

def updatechannel(channel_name):
    logger.info("[updater.py] updatechannel('"+channel_name+"')")
    
    # Canal remoto
    remote_channel_url , remote_version_url = get_channel_remote_url(channel_name)
    
    # Canal local
    local_channel_path , local_version_path , local_compiled_path = get_channel_local_path(channel_name)
    
    if not os.path.exists(local_channel_path):
        return False;

    # Version remota
    try:
        data = scrapertools.cachePage( remote_version_url )
        logger.info("remote_data="+data)
        patronvideos  = '<tag>([^<]+)</tag>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        remote_version = int(matches[0])
    except:
        remote_version = 0

    logger.info("remote_version=%d" % remote_version)

    # Version local
    if os.path.exists( local_version_path ):
        infile = open( local_version_path )
        data = infile.read()
        infile.close();
        logger.info("local_data="+data)
        patronvideos  = '<tag>([^<]+)</tag>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        local_version = int(matches[0])
    else:
        local_version = 0
    
    logger.info("local_version=%d" % local_version)
    
    # Comprueba si ha cambiado
    updated = remote_version > local_version

    if updated:
        logger.info("[updater.py] updated")
        download_channel(channel_name)

    return updated

def download_channel(channel_name):
    logger.info("[updater.py] download_channel('"+channel_name+"')")
    # Canal remoto
    remote_channel_url , remote_version_url = get_channel_remote_url(channel_name)
    
    # Canal local
    local_channel_path , local_version_path , local_compiled_path = get_channel_local_path(channel_name)

    # Descarga el canal
    updated_channel_data = scrapertools.cachePage( remote_channel_url )
    outfile = open(local_channel_path,"w")
    outfile.write(updated_channel_data)
    outfile.flush()
    outfile.close()
    logger.info("Grabado a " + local_channel_path)

    # Descarga la version (puede no estar)
    try:
        updated_version_data = scrapertools.cachePage( remote_version_url )
        outfile = open(local_version_path,"w")
        outfile.write(updated_version_data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + local_version_path)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

    if os.path.exists(local_compiled_path):
        os.remove(local_compiled_path)
    