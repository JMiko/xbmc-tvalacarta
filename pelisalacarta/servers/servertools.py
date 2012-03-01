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

# Listas de servidores empleadas a la hora de reproducir para explicarle al usuario por qué no puede ver un vídeo

# Lista de los servidores que se pueden ver sin cuenta premium de ningún tipo
FREE_SERVERS = []
FREE_SERVERS.extend(['directo','adnstream','bliptv','divxstage','downupload','facebook','fourshared'])
FREE_SERVERS.extend(['googlevideo','gigabyteupload','hdplay','mediafire','modovideo','movshare','novamov','ovfile','putlocker'])
FREE_SERVERS.extend(['rapidtube','royalvids','rutube','sockshare','stagevu','stagero','tutv','userporn','veoh','veevr','videobam'])
FREE_SERVERS.extend(['vidbux','videoweed','vidxden','vimeo','vk','watchfreeinhd','youtube'])

# Lista de TODOS los servidores que funcionan con cuenta premium individual
PREMIUM_SERVERS = ['wupload','fileserve','uploadedto']

# Lista de TODOS los servidores soportados por Filenium
FILENIUM_SERVERS = ['linkto','uploadedto','gigasize','youtube','filepost','hotfile','rapidshare','turbobit','wupload','mediafire','bitshare','depositfiles','oron','downupload','allmyvideos','novamov','videoweed','movshare','fooget','letitbit','fileserve','shareonline']

# Lista de TODOS los servidores soportados por Real-Debrid
REALDEBRID_SERVERS = ['tenupload','onefichier','twoshared','fourfastfile','fourshared','abc','badongo','bayfiles','bitshare','bulletupload','cbscom','cramit','crocko','cwtv','dailymotion','dateito',
                    'dengee','depositfiles','diglo','easybytez','extabit','fileape','filebox','filedino','filefactory','fileflyer','filejungle','filekeen','filemade','fileover','filepost',
                   'filesend','fileserve','filesmonster','filevelocity','freakshare','free','furk','fyels','gigapeta','gigasize','gigaup','glumbouploads','goldfile','grupload','hitfile',
                   'hotfile','hulkshare','hulu','ifile','jakfile','jumbofiles','justintv','kickload','letitbit','loadto','mediafire','megashare','megashares','mixturevideo','netload',
                   'novamov','przeklej','purevid','putlocker','rapidgator','redtube','rapidshare','rutube','scribd','sendspace','shareonline','shareflare','shragle','slingfile','sockshare',
                   'soundcloud','speedyshare','turbobit','unibytes','uploadboost','uploadc','uploadedto','uploadhere','uploading','uploadking','uploadspace','uploadstation','uptobox',
                   'userporn','videoweed','vidxden','vimeo','vipfile','wattv','wupload','youporn','youtube','yunfile','zippyshare','zshare']

# Lista completa de todos los servidores soportados por pelisalacarta, usada para buscar patrones
ALL_SERVERS = list( set(FREE_SERVERS) | set(FILENIUM_SERVERS) | set(REALDEBRID_SERVERS) )
ALL_SERVERS.sort()

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
        try:
            exec "from servers import "+serverid
            exec "devuelve.extend("+serverid+".find_videos(data))"
        except ImportError:
            logger.info("No existe conector para "+serverid)
        except:
            logger.info("Error en el conector "+serverid)
            import traceback,sys
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

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
