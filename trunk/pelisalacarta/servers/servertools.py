# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re,sys

from core import scrapertools
from core import config
from core import logger

# Listas de servidores empleadas a la hora de reproducir para explicarle al usuario por qué no puede ver un vídeo

# Lista de los servidores que se pueden ver sin cuenta premium de ningún tipo
FREE_SERVERS = []
FREE_SERVERS.extend(['directo','allmyvideos','adnstream','bliptv','divxstage','downupload','facebook','fourshared', 'hulkshare', 'twitvid'])
FREE_SERVERS.extend(['googlevideo','gigabyteupload','hdplay','filebox','mediafire','modovideo','moevideos','movshare','novamov','ovfile','putlocker'])
FREE_SERVERS.extend(['rapidtube','royalvids','rutube','sockshare','stagevu','stagero','tutv','userporn','veoh','videobam'])
FREE_SERVERS.extend(['vidbux','videoweed','vidxden','vimeo','vk','watchfreeinhd','youtube'])
FREE_SERVERS.extend(['jumbofiles','nowvideo','allbox4'])
#bayfiles

# Lista de TODOS los servidores que funcionan con cuenta premium individual
PREMIUM_SERVERS = [''] #wupload','fileserve']#,'uploadedto']

# Lista de TODOS los servidores soportados por Filenium
FILENIUM_SERVERS = []
FILENIUM_SERVERS.extend(['linkto','uploadedto','gigasize','youtube','filepost','hotfile','rapidshare','turbobit','mediafire','bitshare','depositfiles'])
FILENIUM_SERVERS.extend(['oron','downupload','allmyvideos','novamov','videoweed','movshare','fooget','letitbit','shareonline','rapidgator'])
FILENIUM_SERVERS.extend(['filebox','filefactory','netload','filevelocity','freakshare','userporn','divxstage','putlocker','extabit','vidxden'])
FILENIUM_SERVERS.extend(['vimeo','dailymotion','jumbofiles'])
#wupload,fileserve

# Lista de TODOS los servidores soportados por Real-Debrid
REALDEBRID_SERVERS = ['one80upload','tenupload','onefichier','onehostclick','twoshared','fourfastfile','fourshared','abc','asfile','badongo','bayfiles','bitshare','cbscom','cramit','crocko','cwtv','dailymotion','dateito',
                    'dengee','diglo','extabit','fiberupload','filebox','filedino','filefactory','fileflyer','filekeen','filemade','filemates','fileover','filepost',
                   'filereactor','filesend','filesmonster','filevelocity','freakshare','free','furk','fyels','gigasize','gigaup','glumbouploads','goldfile','hitfile','hipfile','hostingbulk',
                   'hotfile','hulkshare','hulu','ifile','jakfile','jumbofiles','justintv','letitbit','loadto','mediafire','megashare','megashares','mixturevideo','muchshare','netload',
                   'novafile','nowdownload','purevid','putbit','putlocker','redtube','rapidshare','rutube','ryushare','scribd','sendspace','sharebees','shareflare','shragle','slingfile','sockshare',
                   'soundcloud','speedyshare','turbobit','unibytes','uploadc','uploadedto','uploading','uploadspace','uptobox',
                   'userporn','veevr','vidbux','vidhog','vidxden','vimeo','vipfile','wattv','xfileshare','youporn','youtube','yunfile','zippyshare']
#wupload,fileserve

# Lista completa de todos los servidores soportados por pelisalacarta, usada para buscar patrones
ALL_SERVERS = list( set(FREE_SERVERS) | set(FILENIUM_SERVERS) | set(REALDEBRID_SERVERS) )
ALL_SERVERS.sort()

# Función genérica para encontrar vídeos en una página
def find_video_items(item=None, data=None, channel=""):
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

def resolve_video_urls_for_playing(server,url,video_password="",muestra_dialogo=False):
    logger.info("[servertools.py] resolve_video_urls_for_playing, server="+server+", url="+url)
    video_urls = []

    # Si el vídeo es "directo", no hay que buscar más
    if server=="directo" or server=="local":
        logger.info("[servertools.py] server=directo, la url es la buena")
        
        try:
            import urlparse
            parsed_url = urlparse.urlparse(url)
            logger.info("parsed_url="+str(parsed_url))
            extension = parsed_url.path[-4:]
        except:
            extension = url[-4:]

        video_urls = [[ "%s [%s]" % (extension,server) , url ]]
        return video_urls,True,""

    # Averigua las URL de los vídeos
    else:

        # Carga el conector
        try:
            # Muestra un diálogo de progreso
            if muestra_dialogo:
                import xbmcgui
                progreso = xbmcgui.DialogProgress()
                progreso.create( "pelisalacarta" , "Conectando con "+server)

            exec "from servers import "+server+" as server_connector"
            logger.info("[servertools.py] servidor de "+server+" importado")
            if muestra_dialogo:
                progreso.update( 25 , "Conectando con "+server)

            # Si tiene una función para ver si el vídeo existe, lo comprueba ahora
            if hasattr(server_connector, 'test_video_exists'):
                logger.info("[servertools.py] invocando a "+server+".test_video_exists")
                puedes,motivo = server_connector.test_video_exists( page_url=url )

                # Si la funcion dice que no existe, fin
                if not puedes:
                    logger.info("[servertools.py] test_video_exists dice que el video no existe")
                    if muestra_dialogo: progreso.close()
                    return video_urls,puedes,motivo
                else:
                    logger.info("[servertools.py] test_video_exists dice que el video SI existe")

            # Obtiene enlaces free
            if server in FREE_SERVERS:
                logger.info("[servertools.py] invocando a "+server+".get_video_url")
                video_urls = server_connector.get_video_url( page_url=url , video_password=video_password )
                
                # Si no se encuentran vídeos en modo free, es porque el vídeo no existe
                if len(video_urls)==0:
                    if muestra_dialogo: progreso.close()
                    return video_urls,False,"No se puede encontrar el vídeo en "+server

            # Obtiene enlaces premium si tienes cuenta en el server
            if server in PREMIUM_SERVERS and config.get_setting(server+"premium")=="true":
                video_urls = server_connector.get_video_url( page_url=url , premium=(config.get_setting(server+"premium")=="true") , user=config.get_setting(server+"user") , password=config.get_setting(server+"password"), video_password=video_password )
                
                # Si no se encuentran vídeos en modo premium directo, es porque el vídeo no existe
                if len(video_urls)==0:
                    if muestra_dialogo: progreso.close()
                    return video_urls,False,"No se puede encontrar el vídeo en "+server
    
            # Obtiene enlaces filenium si tienes cuenta
            if server in FILENIUM_SERVERS and config.get_setting("fileniumpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 50 , "Conectando con Filenium")
    
                exec "from servers import filenium as gen_conector"
                
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("fileniumpremium")=="true") , user=config.get_setting("fileniumuser") , password=config.get_setting("fileniumpassword"), video_password=video_password )
                logger.info("[xbmctools.py] filenium url="+video_gen)
                video_urls.append( [ "[filenium]", video_gen ] )

            # Obtiene enlaces realdebrid si tienes cuenta
            if server in REALDEBRID_SERVERS and config.get_setting("realdebridpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 75 , "Conectando con Real-Debrid")

                exec "from servers import realdebrid as gen_conector"
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("realdebridpremium")=="true") , user=config.get_setting("realdebriduser") , password=config.get_setting("realdebridpassword"), video_password=video_password )
                logger.info("[xbmctools.py] realdebrid url="+video_gen)
                if not "REAL-DEBRID" in video_gen:
                    video_urls.append( [ "."+video_gen.rsplit('.',1)[1]+" [realdebrid]", video_gen ] )
                else:
                    if muestra_dialogo: progreso.close()
                    # Si RealDebrid da error pero tienes un enlace válido, no te dice nada
                    if len(video_urls)==0:
                        return video_urls,False,video_gen

                if muestra_dialogo:
                    progreso.update( 100 , "Proceso finalizado")

                # Cierra el diálogo de progreso
                if muestra_dialogo: progreso.close()

            # Llegas hasta aquí y no tienes ningún enlace para ver, así que no vas a poder ver el vídeo
            if len(video_urls)==0:
                # ¿Cual es el motivo?
                
                # 1) No existe -> Ya está controlado
                # 2) No tienes alguna de las cuentas premium compatibles

                # Lista de las cuentas que soportan este servidor
                listapremium = ""
                if server in FILENIUM_SERVERS: listapremium+="Filenium o "
                if server in REALDEBRID_SERVERS: listapremium+="Real-Debrid o "
                if server in PREMIUM_SERVERS: listapremium+=server+" o "
                listapremium = listapremium[:-3]
    
                return video_urls,False,"Para ver un vídeo en "+server+" necesitas<br/>una cuenta en "+listapremium

        except:
            if muestra_dialogo: progreso.close()
            import traceback
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

            return video_urls,False,"Se ha producido un error en<br/>el conector con "+server

    return video_urls,True,""
