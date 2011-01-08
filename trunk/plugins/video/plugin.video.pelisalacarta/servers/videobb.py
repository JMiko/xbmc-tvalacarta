# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import logger

# Obtiene la URL que hay detrás de un enlace a linkbucks
def geturl(url):

    logger.info("[videobb.py] url="+url)
    # El formato de la URL de la página es
    # http://videobb.com/video/zFFw8n8w1r1s
    # El formato de la URL del vídeo es
    # http://s.videobb.com/s2?v=zFFw8n8w1r1s&r=1&t=1294503726&u=&c=ad60cbaec0af97d5d911d5a236841b42&start=0
    
    devuelve = url.replace("http://videobb.com/video/","http://s.videobb.com/s2?v=")
    import random
    devuelve = "%s&r=1&t=%d&u=&c=12&start=0" % (devuelve,random.randint(1000000000,9999999999))

    logger.info("[videobb.py] url="+devuelve)
    
    return devuelve
