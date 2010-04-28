# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

# Constantes
__plugin__  = "mywebtv"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/mywebtv/"
__date__    = "25 Abril 2010"
__version__ = "0.5"

import os
import sys
import xbmc

xbmc.output("[default.py] mywebtv init...")

# Configura los directorios donde hay librerías
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'servers' ) )
sys.path.append (librerias)

# Ejecuta el programa principal
import mywebtv
mywebtv.run()