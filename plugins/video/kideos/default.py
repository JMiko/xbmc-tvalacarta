# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# kideos - XBMC Plugin
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/kideos/
#------------------------------------------------------------

# Constantes
__plugin__  = "Kideos"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/kideos/"
__date__    = "15 Octubre 2009"
__version__ = "1.1"

import os
import sys
import xbmc

xbmc.output("[default.py] kideos init...")

# Configura los directorios donde hay librerías
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'servers' ) )
sys.path.append (librerias)

# Ejecuta el programa principal
import kideos
kideos.run()
