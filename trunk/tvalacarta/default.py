# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta
# XBMC (pre-dharma) entry point
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

# Constants
__plugin__  = "tvalacarta"
__author__  = "tvalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/"
__date__    = "09 Octubre 2012"
__version__ = "3.3.2"

import os
import sys
from core import config
from core import logger

logger.info("[default.py] tvalacarta init...")

librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)

# Runs xbmc launcher
from platformcode.xbmc import launcher
launcher.run()