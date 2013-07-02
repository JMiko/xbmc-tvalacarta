# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# XBMC entry point
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# Constants
__plugin__  = "mywebtv"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/mywebtv/"
__date__ = "27/06/2013"
__version__ = "2.0.1"

import os
import sys
from core import config
from core import logger

librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)

# Runs xbmc launcher
from platformcode.xbmc import launcher
launcher.run()