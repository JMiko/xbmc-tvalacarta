# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# XBMC Launcher (xbmc / xbmc-dharma / boxee)
# http://blog.tvalacarta.info/plugin-xbmc/
#------------------------------------------------------------

import urllib, urllib2
import os,sys

from core import logger
from core import config

PLUGIN_NAME = "pelisalacarta"

def run():
    logger.info("[launcher.py] run")
    
    # Test if all the required directories are created
    verify_directories_created()
    
    # Extract parameters from sys.argv
    params, url, action, server, category = extract_parameters()

    try:
        # Accion por defecto - elegir canal
        if ( action=="selectchannel" ):
            
            if config.get_setting("updatechannels")=="true":
                try:
                    from core import updater
                    actualizado = updater.updatechannel("channelselector")

                    if actualizado:
                        import xbmcgui
                        advertencia = xbmcgui.Dialog()
                        advertencia.ok("tvalacarta",config.get_localized_string(30064))
                except:
                    pass

            import channelselector as plugin
            plugin.mainlist(params, url, category)

        # Actualizar version
        elif ( action=="update" ):
            try:
                from core import updater
                updater.update(params)
            except ImportError:
                logger.info("[launcher.py] Actualizacion automática desactivada")

            import channelselector as plugin
            plugin.listchannels(params, url, category)

        elif (action=="channeltypes"):
            import channelselector as plugin
            plugin.channeltypes(params,url,category)

        elif (action=="listchannels"):
            import channelselector as plugin
            plugin.listchannels(params,url,category)

        # El resto de acciones vienen en el parámetro "action", y el canal en el parámetro "channel"
        else:
            if action=="mainlist" and config.get_setting("updatechannels")=="true":
                try:
                    from core import updater
                    actualizado = updater.updatechannel(params.get("channel"))

                    if actualizado:
                        import xbmcgui
                        advertencia = xbmcgui.Dialog()
                        advertencia.ok("plugin",params.get("channel"),config.get_localized_string(30063))
                except:
                    pass

            # La acción puede estar en el core, o ser un canal regular. El buscador es un canal especial que está en pelisalacarta
            regular_channel_path = os.path.join( config.get_runtime_path(), PLUGIN_NAME , 'channels' , params.get("channel")+".py" )
            core_channel_path = os.path.join( config.get_runtime_path(), 'core' , params.get("channel")+".py" )

            if params.get("channel")=="buscador":
                import pelisalacarta.buscador as channel
            elif os.path.exists( regular_channel_path ):
                exec "import pelisalacarta.channels."+params.get("channel")+" as channel"
            elif os.path.exists( core_channel_path ):
                exec "from core import "+params.get("channel")+" as channel"

            generico = False
            # Esto lo he puesto asi porque el buscador puede ser generico o normal, esto estará asi hasta que todos los canales sean genericos 
            if category == "Buscador_Generico":
                generico = True
            else:
                try:
                    generico = channel.isGeneric()
                except:
                    generico = False

            print "generico=" , generico 
            
            if not generico:
                if (action=="strm"):
                    from core import xbmctools
                    xbmctools.playstrm(params, url, category)
                else:
                    exec "channel."+action+"(params, url, category)"
            else:
                if params.has_key("title"):
                    title = urllib.unquote_plus( params.get("title") )
                else:
                    title = ""
                if params.has_key("thumbnail"):
                    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
                else:
                    thumbnail = ""
                if params.has_key("plot"):
                    plot = urllib.unquote_plus( params.get("plot") )
                else:
                    plot = ""
                if params.has_key("server"):
                    server = urllib.unquote_plus( params.get("server") )
                else:
                    server = "directo"
                if params.has_key("extradata"):
                    extra = urllib.unquote_plus( params.get("extradata") )
                else:
                    extra = ""
                if params.has_key("subtitle"):
                    subtitle = urllib.unquote_plus( params.get("subtitle") )
                else:
                    subtitle = ""
            
                from core.item import Item
                item = Item(channel=params.get("channel"), title=title , url=url, thumbnail=thumbnail , plot=plot , server=server, category=category, extra=extra, subtitle=subtitle)

                if item.subtitle!="":
                    logger.info("Descargando subtítulos de "+item.subtitle)
                    from core import downloadtools
                    
                    ficherosubtitulo = os.path.join( config.get_data_path() , "subtitulo.srt" )
                    if os.path.exists(ficherosubtitulo):
                        os.remove(ficherosubtitulo)

                    downloadtools.downloadfile(item.subtitle, ficherosubtitulo )
                    config.set_setting("subtitulo","true")
                else:
                    logger.info("Sin subtitulos")

                from core import xbmctools
                if action=="play":
                    # Si el canal tiene una acción "play" tiene prioridad
                    try:
                        itemlist = channel.play(item)
                        if len(itemlist)>0:
                            item = itemlist[0]
                    except:
                        import sys
                        for line in sys.exc_info():
                            logger.error( "%s" % line )
                   
                    xbmctools.playvideo(params.get("channel"),item.server,item.url,item.category,item.title,item.thumbnail,item.plot,subtitle=item.subtitle)
                else:
                    if action!="findvideos":
                        exec "itemlist = channel."+action+"(item)"
                    else:
                        # Intenta ejecutar una posible funcion "findvideos" del canal
                        try:
                            exec "itemlist = channel."+action+"(item)"
                        # Si no funciona, lanza el método genérico para detectar vídeos
                        except:
                            itemlist = find_videos(item)

                    xbmctools.renderItems(itemlist, params, url, category)

    except urllib2.URLError,e:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        import xbmcgui
        ventana_error = xbmcgui.Dialog()
        # Agarra los errores surgidos localmente enviados por las librerias internas
        if hasattr(e, 'reason'):
            logger.info("Razon del error, codigo: %d , Razon: %s" %(e.reason[0],e.reason[1]))
            texto = config.get_localized_string(30050) # "No se puede conectar con el sitio web"
            ok = ventana_error.ok ("plugin", texto)
        # Agarra los errores con codigo de respuesta del servidor externo solicitado     
        elif hasattr(e,'code'):
            logger.info("codigo de error HTTP : %d" %e.code)
            texto = (config.get_localized_string(30051) % e.code) # "El sitio web no funciona correctamente (error http %d)"
            ok = ventana_error.ok ("plugin", texto)    

# Test if all the required directories are created
def verify_directories_created():

    # Force download path if empty
    download_path = config.get_setting("downloadpath")
    if download_path=="":
        download_path = os.path.join( config.get_data_path() , "downloads")
        config.set_setting("downloadpath" , download_path)

    # Force download list path if empty
    download_list_path = config.get_setting("downloadlistpath")
    if download_list_path=="":
        download_list_path = os.path.join( config.get_data_path() , "downloads" , "list")
        config.set_setting("downloadlistpath" , download_list_path)

    # Force bookmark path if empty
    bookmark_path = config.get_setting("bookmarkpath")
    if bookmark_path=="":
        bookmark_path = os.path.join( config.get_data_path() , "bookmarks")
        config.set_setting("bookmarkpath" , bookmark_path)

    # Create data_path if not exists
    if not os.path.exists(config.get_data_path()):
        logger.debug("[launcher.py] Creating data_path "+config.get_data_path())
        os.mkdir(config.get_data_path())

    # Create download_path if not exists
    if not download_path.lower().startswith("smb") and not os.path.exists(download_path):
        logger.debug("[launcher.py] Creating download_path "+download_path)
        os.mkdir(download_path)

    # Create download_list_path if not exists
    if not download_list_path.lower().startswith("smb") and not os.path.exists(download_list_path):
        logger.debug("[launcher.py] Creating download_list_path "+download_list_path)
        os.mkdir(download_list_path)

    # Create bookmark_path if not exists
    if not bookmark_path.lower().startswith("smb") and not os.path.exists(bookmark_path):
        logger.debug("[launcher.py] Creating bookmark_path "+bookmark_path)
        os.mkdir(bookmark_path)

    # Create library_path if not exists
    if not config.get_library_path().lower().startswith("smb") and not os.path.exists(config.get_library_path()):
        logger.debug("[launcher.py] Creating library_path "+config.get_library_path())
        os.mkdir(config.get_library_path())

# Extract parameters from sys.argv
def extract_parameters():

    #Imprime en el log los parámetros de entrada
    logger.info("[launcher.py] sys.argv=%s" % str(sys.argv))
    
    # Crea el diccionario de parametros
    params = dict()
    if len(sys.argv)>=2 and len(sys.argv[2])>0:
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
    logger.info("[launcher.py] params=%s" % str(params))
    
    # Extrae la url de la página
    if (params.has_key("url")):
        url = urllib.unquote_plus( params.get("url") )
    else:
        url=''

    # Extrae la accion
    if (params.has_key("action")):
        action = params.get("action")
    else:
        action = "selectchannel"

    # Extrae el server
    if (params.has_key("server")):
        server = params.get("server")
    else:
        server = ""

    # Extrae la categoria
    if (params.has_key("category")):
        category = urllib.unquote_plus( params.get("category") )
    else:
        if params.has_key("channel"):
            category = params.get("channel")
        else:
            category = ""
            
    return params, url, action, server, category

# Función genérica para encontrar vídeos en una página
def find_videos(item):
    logger.info("[launcher.py] findvideos")

    # Descarga la página
    from core import scrapertools
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Busca los enlaces a los videos
    from core.item import Item
    from servers import servertools
    listavideos = servertools.findvideos(data)

    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title.strip() + " - " + video[0]
        scrapedurl = video[1]
        server = video[2]
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

    return itemlist
