# -*- coding: cp1252 -*-

import os.path
import sys, traceback, platform
import xbmcgui

versionactual = "1.1a1"

sys.path.append(os.path.join(os.getcwd().replace(";",""),'resources','libs'))

import envcontroller
envController = envcontroller.EnvController()
env = envController.GetEnvironment()
#print env

sys.path.append(os.path.join(os.getcwd().replace(";",""),'resources','libs', env))
        
# import environment specific path: get the OS and do Win32 if fails. Then if XBox, do Win32 (TRUE = 1 and thus the win32 
# from the (,,,) will be used

        
#sys.path.insert(1, os.path.join(os.getcwd().replace(";",""),'libs'))


#===============================================================================
# Handles an AttributeError during intialization
#===============================================================================
def HandleInitAttributeError(loadedModules):
    if(globalLogFile != None):
        globalLogFile.critical("AtrributeError during intialization", exc_info=True)
        if ("config" in loadedModules):
            globalLogFile.debug("'config' was imported from %s", config.__file__)
        if ("logger" in loadedModules):
            globalLogFile.debug("'logger' was imported from %s", logger.__file__)
        if ("uriopener" in loadedModules):
            globalLogFile.debug("'uriopener' was imported from %s", uriopener.__file__)
        if ("common" in loadedModules):
            globalLogFile.debug("'common' was imported from %s", common.__file__)
        if ("update" in loadedModules):
            globalLogFile.debug("'update' was imported from %s", update.__file__)
    else:
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        if ("config" in loadedModules):
            print("'config' was imported from %s" % config.__file__)
        if ("logger" in loadedModules):
            print("'logger' was imported from %s" % logger.__file__)
        if ("uriopener" in loadedModules):
            print("'uriopener' was imported from %s" % uriopener.__file__)
        if ("common" in loadedModules):
            print("'common' was imported from %s" % common.__file__)
        if ("update" in loadedModules):
            print("'update' was imported from %s" % update.__file__)   
    return  

#===============================================================================
# Here the script starts
#===============================================================================
# Check for function: Plugin or Script
if hasattr(sys, "argv") and len(sys.argv) > 1:
    #===============================================================================
    # PLUGIN: Import XOT stuff
    #===============================================================================
    try:
        import config
        import logger
        globalLogFile = logger.Customlogger(os.path.join(config.rootDir, config.logFileNamePlugin), config.logLevel, config.logDual, append=True)
        import uriopener
        globalUriHandler = uriopener.UriHandler()
        import common
        config.skinFolder = common.GetSkinFolder()
        import plugin
        tmp = plugin.XotPlugin()    
    except AttributeError:
        HandleInitAttributeError(dir())
    except:
        #globalLogFile.critical("Error initializing %s plugin", config.appName, exc_info=True)
        try:
            orgEx = sys.exc_info()
            globalLogFile.critical("Error al inicializar el plugin %s", config.appName, exc_info=True)
        except:
            print "Exception during the initialisation of the script. No logging information was present because the logger was not loaded."
            traceback.print_exception(orgEx[0], orgEx[1], orgEx[2])       
else:
    #===============================================================================
    # SCRIPT: Setup the script
    #===============================================================================
    try:
        pb = xbmcgui.DialogProgress()
        import config
        pb.create("Inicializando %s" % (config.appName), "Importando configuración...")
        
        pb.update(10,"Inicializando log...")
        import logger
        globalLogFile = None
        globalLogFile = logger.Customlogger(os.path.join(config.rootDir, config.logFileName), config.logLevel, config.logDual)
        
        pb.update(25,"Inicializando urihandler...")
        import uriopener
        globalUriHandler = uriopener.UriHandler()
        
        pb.update(30,"Cargando librerías...")
        import common
        common.DirectoryPrinter(config.rootDir)
        
        pb.update(40,"Cargando skin...")
        config.skinFolder = common.GetSkinFolder()        
        
        globalLogFile.info("************** Starting %s version v%s **************", config.appName, config.version)
        globalLogFile.info("Skinfolder = %s", config.skinFolder)
        print("************** Starting %s version v%s **************" % (config.appName, config.version))
        
        # Comprueba actualizaciones...
        import urllib2,urllib,re
        if config.checkforupdates:
            pb.update(50,"Buscando actualizaciones...")
            try:
                req = urllib2.Request("http://xbmc-tvalacarta.googlecode.com/files/tvalacarta.ver")
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                patron = 'version=([0-9\.a-z]+)'
                matches = re.compile(patron,re.MULTILINE).findall(link)
                versionnueva = matches[0]
                dialog = xbmcgui.Dialog()
                if (versionnueva > versionactual):
                    dialog.ok("Nueva versión disponible","Hay una nueva versión disponible de este script\n"+versionnueva)
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("Error al buscar actualizaciones","Se ha producido un error al buscar las actualizaciones del script")

        """
        pb.update(50,"Checking for updates")
        import update
        try:
            #pass
            update.CheckVersion(config.version, config.updateUrl)
        except:
            globalLogFile.critical("Error checking for updates", exc_info=True)
        """
        pb.update(60,"Verificando cache...")
        #check for cache folder. If not present. Create it!
        if os.path.exists(config.cacheDir)!=True:
             os.mkdir(config.cacheDir)
        
        pb.update(80, "Limpiando cache...")
        #cleanup the cachefolder
        common.CacheCleanUp()
        
        pb.close()
        
        #===============================================================================
        # Now starting the real app
        #===============================================================================
        if not pb.iscanceled():
            import progwindow
            
            MyWindow = progwindow.GUI(config.appSkin ,config.rootDir, config.skinFolder)
            MyWindow.doModal()
            del MyWindow
    
    except AttributeError:
        HandleInitAttributeError(dir())        
    except:
        try:
            orgEx = sys.exc_info()
            globalLogFile.critical("Error initializing %s script", config.appName, exc_info=True)
        except:
            print "Exception during the initialisation of the script. No logging information was present because the logger was not loaded."
            traceback.print_exception(orgEx[0], orgEx[1], orgEx[2])            
        pb.close()
        
        
