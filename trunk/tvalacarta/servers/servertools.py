# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re

from core import scrapertools
from core import config
from core import logger

# Todos los servidores
ALL_SERVERS = []
ALL_SERVERS.extend(['directo','adnstream','bitshare','allmyvideos','bliptv','depositfiles','divxstage','downupload','facebook','fileserve','fourshared'])
ALL_SERVERS.extend(['googlevideo','gigabyteupload','hotfile','hdplay','letitbit','mediafire','modovideo','movshare','novamov','ovfile','putlocker','rapidshare'])
ALL_SERVERS.extend(['rapidtube','royalvids','rutube','sockshare','stagevu','stagero','turbobit','tutv','userporn','uploadedto','veoh','veevr','videobam'])
ALL_SERVERS.extend(['vidbux','videoweed','vidxden','vimeo','vk','wupload'])

# Todos los servidores soportados por Filenium
FILENIUM_SERVERS = ['linkto','uploadedto','gigasize','youtube','filepost','hotfile','rapidshare','turbobit','wupload','mediafire','bitshare','depositfiles','oron','downupload','allmyvideos','novamov','videoweed','movshare','fooget','letitbit','fileserve','shareonline']

# Los servidores que SÓLO funcionan con Filenium
FILENIUM_ONLY_SERVERS = ['linkto','uploadedto','gigasize','filepost','hotfile','rapidshare','turbobit','bitshare','depositfiles','oron','allmyvideos','fooget','letitbit','shareonline']

# Todos los servidores que funcionan con cuenta premium
PREMIUM_SERVERS = ['wupload','fileserve']

# Todos los servidores que SÓLo funcionan con cuenta premium
PREMIUM_ONLY_SERVERS = ['wupload','fileserve']

# Función genérica para encontrar vídeos en una página
def find_video_items(item=None, data=None):
    logger.info("[launcher.py] findvideos")

    # Descarga la página
    if data is None:
        from core import scrapertools
        data = scrapertools.cache_page(item.url)
        #logger.info(data)
    
    # Busca los enlaces a los videos
    from core.item import Item
    from servers import servertools
    listavideos = servertools.findvideos(data)

    if item is None:
        item = Item()

    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title.strip() + " - " + video[0]
        scrapedurl = video[1]
        server = video[2]
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

    return itemlist

def findvideos(data):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []

    # Ejecuta el findvideos en cada servidor
    for serverid in ALL_SERVERS:
        exec "import "+serverid
        exec "devuelve = devuelve.extend("+serverid+".find_videos(data))"

    return devuelve
    
def findurl(code,server):
    mediaurl = "ERROR"
    server = server.lower() #Para hacer el procedimiento case insensitive

    if server == "megavideo":
        import megavideo
        mediaurl = megavideo.Megavideo(code)

    elif server == "megaupload":
        import megaupload
        mediaurl = megaupload.gethighurl(code)
        
    elif server == "directo":
        mediaurl = code

    elif server == "4shared":
        import fourshared
        mediaurl = fourshared.geturl(code)
        
    elif server == "xml":
        import xmltoplaylist
        mediaurl = xmltoplaylist.geturl(code)

    else:
        try:
            exec "import "+server+" as serverconnector"
            mediaurl = serverconnector.geturl(code)
        except:
            mediaurl = "ERROR"
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
        
    return mediaurl

def getmegavideolow(code, password=None):
    import megavideo
    if password is not None:
        return megavideo.getlowurl(code,password)
    else:
        return megavideo.getlowurl(code,password)

def getmegavideohigh(code):
    import megavideo
    return megavideo.gethighurl(code)

def getmegauploadhigh(page_url, video_password=""):
    logger.info("getmegauploadhigh "+page_url)
    import megaupload
    if config.get_setting("megavideopremium")=="true":
        logger.info("modo premium")
        return megaupload.get_video_url( page_url , True , config.get_setting("megavideouser") , config.get_setting("megavideopassword") , video_password )
    else:
        logger.info("modo no premium")
        return megaupload.get_video_url( page_url , False , "" , "" , video_password )

def getmegauploadlow(code, password=None):
    import megaupload
    if password is not None:
        return megaupload.getlowurl(code,password)
    else:
        return megaupload.getlowurl(code)
