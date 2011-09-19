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
    params, channel_name, title, url, thumbnail, plot, action, server, extra, subtitle, category, show, password = extract_parameters()
    logger.info("[launcher.py] channel_name=%s, title=%s, url=%s, thumbnail=%s, plot=%s, action=%s, server=%s, extra=%s, subtitle=%s, category=%s, show=%s, password=%s" % (channel_name, title, url, thumbnail, plot, action, server, extra, subtitle, category, show, password))

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
                    actualizado = updater.updatechannel(channel_name)

                    if actualizado:
                        import xbmcgui
                        advertencia = xbmcgui.Dialog()
                        advertencia.ok("plugin",channel_name,config.get_localized_string(30063))
                except:
                    pass

            # La acción puede estar en el core, o ser un canal regular. El buscador es un canal especial que está en pelisalacarta
            regular_channel_path = os.path.join( config.get_runtime_path(), PLUGIN_NAME , 'channels' , channel_name+".py" )
            core_channel_path = os.path.join( config.get_runtime_path(), 'core' , channel_name+".py" )
            logger.info("[launcher.py] regular_channel_path=%s" % regular_channel_path)
            logger.info("[launcher.py] core_channel_path=%s" % core_channel_path)

            if channel_name=="buscador":
                import pelisalacarta.buscador as channel
            elif os.path.exists( regular_channel_path ):
                exec "import pelisalacarta.channels."+channel_name+" as channel"
            elif os.path.exists( core_channel_path ):
                exec "from core import "+channel_name+" as channel"

            logger.info("[launcher.py] running channel %s %s" % (channel.__name__ , channel.__file__))

            generico = False
            # Esto lo he puesto asi porque el buscador puede ser generico o normal, esto estará asi hasta que todos los canales sean genericos 
            if category == "Buscador_Generico":
                generico = True
            else:
                try:
                    generico = channel.isGeneric()
                except:
                    generico = False

            if not generico:
                logger.info("[launcher.py] xbmc native channel")
                if (action=="strm"):
                    from platform.xbmc import xbmctools
                    xbmctools.playstrm(params, url, category)
                else:
                    exec "channel."+action+"(params, url, category)"
            else:            
                logger.info("[launcher.py] multiplatform channel")
                from core.item import Item
                item = Item(channel=channel_name, title=title , url=url, thumbnail=thumbnail , plot=plot , server=server, category=category, extra=extra, subtitle=subtitle, show=show, password=password)

                if item.subtitle!="":
                    logger.info("[launcher.py] Downloading subtitle file "+item.subtitle)
                    from core import downloadtools
                    
                    ficherosubtitulo = os.path.join( config.get_data_path() , "subtitulo.srt" )
                    if os.path.exists(ficherosubtitulo):
                        os.remove(ficherosubtitulo)

                    downloadtools.downloadfile(item.subtitle, ficherosubtitulo )
                    config.set_setting("subtitulo","true")
                else:
                    logger.info("[launcher.py] No subtitle")

                from platform.xbmc import xbmctools

                if action=="play":
                    # Si el canal tiene una acción "play" tiene prioridad
                    try:
                        logger.info("[launcher.py] executing channel 'play' method")
                        itemlist = channel.play(item)
                        if len(itemlist)>0:
                            item = itemlist[0]
                    except:
                        logger.info("[launcher.py] no channel 'play' method, executing core method")
                        #import sys
                        #for line in sys.exc_info():
                        #    logger.error( "%s" % line )

                    xbmctools.play_video(channel=channel_name, server=item.server, url=item.url, category=item.category, title=item.title, thumbnail=item.thumbnail, plot=item.plot, extra=item.extra, subtitle=item.subtitle, video_password = item.password)

                else:
                    logger.info("[launcher.py] executing channel '"+action+"' method")
                    if action!="findvideos":
                        exec "itemlist = channel."+action+"(item)"
                    else:
                        # Intenta ejecutar una posible funcion "findvideos" del canal
                        try:
                            exec "itemlist = channel."+action+"(item)"
                        # Si no funciona, lanza el método genérico para detectar vídeos
                        except:
                            logger.info("[launcher.py] no channel 'findvideos' method, executing core method")
                            from servers import servertools
                            itemlist = servertools.find_video_items(item)

                    # Activa el modo biblioteca para todos los canales genéricos, para que se vea el argumento
                    import xbmcplugin
                    import sys
                    handle = sys.argv[1]
                    xbmcplugin.setContent(int( handle ),"movies")
                    
                    # Añade los items a la lista de XBMC
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
    logger.info("[launcher.py] verify_directories_created")

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
        try:
            os.mkdir(config.get_data_path())
        except:
            pass

    # Create download_path if not exists
    if not download_path.lower().startswith("smb") and not os.path.exists(download_path):
        logger.debug("[launcher.py] Creating download_path "+download_path)
        try:
            os.mkdir(download_path)
        except:
            pass

    # Create download_list_path if not exists
    if not download_list_path.lower().startswith("smb") and not os.path.exists(download_list_path):
        logger.debug("[launcher.py] Creating download_list_path "+download_list_path)
        try:
            os.mkdir(download_list_path)
        except:
            pass

    # Create bookmark_path if not exists
    if not bookmark_path.lower().startswith("smb") and not os.path.exists(bookmark_path):
        logger.debug("[launcher.py] Creating bookmark_path "+bookmark_path)
        try:
            os.mkdir(bookmark_path)
        except:
            pass

    # Create library_path if not exists
    if not config.get_library_path().lower().startswith("smb") and not os.path.exists(config.get_library_path()):
        logger.debug("[launcher.py] Creating library_path "+config.get_library_path())
        try:
            os.mkdir(config.get_library_path())
        except:
            pass

# Extract parameters from sys.argv
def extract_parameters():
    logger.info("[launcher.py] extract_parameters")
    #Imprime en el log los parámetros de entrada
    logger.info("[launcher.py] sys.argv=%s" % str(sys.argv))
    
    # Crea el diccionario de parametros
    params = dict()
    if len(sys.argv)>=2 and len(sys.argv[2])>0:
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
    logger.info("[launcher.py] params=%s" % str(params))

    if (params.has_key("channel")):
        channel = urllib.unquote_plus( params.get("channel") )
    else:
        channel=''
    
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
            
    # Extrae el título de la serie
    if (params.has_key("show")):
        show = params.get("show")
    else:
        show = ""

    # Extrae el título del video
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

    if params.has_key("extradata"):
        extra = urllib.unquote_plus( params.get("extradata") )
    else:
        extra = ""

    if params.has_key("subtitle"):
        subtitle = urllib.unquote_plus( params.get("subtitle") )
    else:
        subtitle = ""

    if params.has_key("password"):
        password = urllib.unquote_plus( params.get("password") )
    else:
        password = ""

    if params.has_key("show"):
        show = urllib.unquote_plus( params.get("show") )
    else:
        show = ""

    return params, channel, title, url, thumbnail, plot, action, server, extra, subtitle, category, show, password
