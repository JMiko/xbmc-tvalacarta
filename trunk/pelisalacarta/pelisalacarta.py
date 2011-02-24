# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os
import sys
from core import config
config.force_platform("wiimc")

from core import logger

logger.info("[wiimcrun.py] pelisalacarta init...")

# Ejecuta el programa principal
from platform.wiimc import launcher
launcher.run()
