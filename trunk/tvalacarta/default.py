# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

# Constantes
__plugin__  = "tvalacarta"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/"
__date__    = "1 Septiembre 2010"
__version__ = "2.6"

import os
import sys
import xbmc

xbmc.output("[default.py] tvalacarta init...")

librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'lib' ) )
sys.path.append (librerias)

# Ejecuta el programa principal
from platform.xbmc import launcher
launcher.run()