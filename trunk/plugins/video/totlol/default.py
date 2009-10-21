# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# totlol - XBMC Plugin
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/totlol/
#------------------------------------------------------------

# Constantes
__plugin__  = "totlol"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/totlol/"
__date__    = "05 Octubre 2009"
__version__ = "1.1"

import os
import sys
import xbmc

xbmc.output("[default.py] totlol init...")

# Configura los directorios donde hay librerías
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'servers' ) )
sys.path.append (librerias)

# Ejecuta el programa principal
import totlol
totlol.run()
