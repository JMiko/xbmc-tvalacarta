# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# XBMC entry point
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

# Constantes
__plugin__  = "mywebtv"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/mywebtv/"
__date__    = "01 Enero 2013"
__version__ = "1.0.7"

import os
import sys
from core import config
from core import logger

logger.info("[default.py] mywebtv init...")

# Configura los directorios donde hay librerías
librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)

# Ejecuta el programa principal
import mywebtv
mywebtv.run()