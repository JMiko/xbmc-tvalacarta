# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# Constantes
__plugin__  = "pelisalacarta"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/"
__date__    = "31 Mayo 2009"
__version__ = "2.1"

import os
import sys
import xbmc

xbmc.output("[default.py] pelisalacarta init...")

# Configura los directorios donde hay librerías
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'channels' ) )
sys.path.append (librerias)
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'servers' ) )
sys.path.append (librerias)

# Ejecuta el programa principal
import pelisalacarta
pelisalacarta.run()
