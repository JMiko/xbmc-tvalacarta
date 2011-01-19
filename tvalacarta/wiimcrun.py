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
from core import config
from core import logger

logger.info("[wiimcrun.py] tvalacarta init...")

# Ejecuta el programa principal
from platform.wiimc import launcher
launcher.run()