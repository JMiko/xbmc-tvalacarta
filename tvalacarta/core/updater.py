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

ROOT_DIR = os.getcwd()

REMOTE_VERSION_FILE = "http://blog.tvalacarta.info/descargas/tvalacarta-version.xml"
LOCAL_VERSION_FILE = xbmc.translatePath( os.path.join( ROOT_DIR , "version.xml" ) )
LOCAL_FILE = xbmc.translatePath( os.path.join( ROOT_DIR , "tvalacarta-" ) )

try:
    if config.get_platform()=="xbmcdharma":
        REMOTE_FILE = "http://blog.tvalacarta.info/descargas/tvalacarta-xbmc-addon-"
        DESTINATION_FOLDER = xbmc.translatePath( "special://home/addons")
    else:
        REMOTE_FILE = "http://blog.tvalacarta.info/descargas/tvalacarta-xbmc-plugin-"
        DESTINATION_FOLDER = xbmc.translatePath( "special://home/plugins/video")
except:
    REMOTE_FILE = "http://blog.tvalacarta.info/descargas/tvalacarta-xbmc-plugin-"
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
    if len(arraylocal) < len(arraydescargada):
        #xbmc.output("caso 3")
        hayqueactualizar = True
        for i in range(0, len(arraylocal)):
            #print arraylocal[i], arraydescargada[i], int(arraylocal[i])>int(arraydescargada[i])
            if int(arraylocal[i]) > int(arraydescargada[i]):
                hayqueactualizar = False

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
    xbmc.output("[updater.py] cwd="+os.getcwd())
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

def updatechannel(channel_name):
    logger.info("Buscando actualizacion del canal " + channel_name)
    
    # Canal remoto
    if channel_name<>"channelselector":
        remote_channel_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/tvalacarta/channels/"+channel_name+".py"
        remote_version_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/tvalacarta/channels/"+channel_name+".xml"
    else:
        remote_channel_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/tvalacarta/"+channel_name+".py"
        remote_version_url = "http://xbmc-tvalacarta.googlecode.com/svn/trunk/tvalacarta/"+channel_name+".xml"
    
    logger.info("remote_channel_url="+remote_channel_url)
    logger.info("remote_version_url="+remote_version_url)

    # Canal local
    import xbmc
    if channel_name<>"channelselector":
        local_channel_path = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' , channel_name+".py" ) )
        local_version_path = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' , channel_name+".xml" ) )
        local_compiled_path = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' , channel_name+".pyo" ) )
    else:
        local_channel_path = xbmc.translatePath( os.path.join( os.getcwd() , channel_name+".py" ) )
        local_version_path = xbmc.translatePath( os.path.join( os.getcwd() , channel_name+".xml" ) )
        local_compiled_path = xbmc.translatePath( os.path.join( os.getcwd() , channel_name+".pyo" ) )
    
    logger.info("local_channel_path="+local_channel_path)
    logger.info("local_version_path="+local_version_path)
    logger.info("local_compiled_path="+local_compiled_path)
    
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
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        local_version = int(matches[0])
    else:
        local_version = 0
    
    logger.info("local_version=%d" % local_version)
    
    # Comprueba si ha cambiado
    updated = remote_version > local_version

    if updated:
        # Descarga el canal
        updated_channel_data = scrapertools.cachePage( remote_channel_url )
        outfile = open(local_channel_path,"w")
        outfile.write(updated_channel_data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + local_channel_path)

        # Descarga la version
        updated_version_data = scrapertools.cachePage( remote_version_url )
        outfile = open(local_version_path,"w")
        outfile.write(updated_version_data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + local_version_path)

        if os.path.exists(local_compiled_path):
            os.remove(local_compiled_path)

    return updated
