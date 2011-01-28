# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import os
import sys
from core import config
config.force_platform("wiimc")

from core import logger

logger.info("[wiimcrun.py] tvalacarta init...")

# Ejecuta el programa principal
from platform.wiimc import launcher
launcher.run()
