# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta
# XBMC Launcher (dharma / pre-dharma)
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urllib
import urllib2
import os
import sys

from core import logger
from core import config

def run():
    import sys
    logger.info("[tvalacarta.py] run")
    
    # Verifica si el path de usuario del plugin est� creado
    if not os.path.exists(config.get_data_path()):
        logger.debug("[tvalacarta.py] Path de usuario no existe, se crea: "+config.get_data_path())
        os.mkdir(config.get_data_path())

    # Imprime en el log los par�metros de entrada
    logger.info("[tvalacarta.py] sys.argv=%s" % str(sys.argv))
    
    # Crea el diccionario de parametros
    params = dict()
    if len(sys.argv)>=2 and len(sys.argv[2])>0:
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
    logger.info("[tvalacarta.py] params=%s" % str(params))
    
    # Extrae la url de la p�gina
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


    try:
        # Accion por defecto - elegir canal
        if ( action=="selectchannel" ):
            
            if config.get_setting("updatechannels")=="true":
                from core import updater
                actualizado = updater.updatechannel("channelselector")

                if actualizado:
                    import xbmcgui
                    advertencia = xbmcgui.Dialog()
                    advertencia.ok("tvalacarta",config.get_localized_string(30064))

            import channelselector as plugin
            plugin.mainlist(params, url, category)

        # Actualizar version
        elif ( action=="update" ):
            try:
                from core import updater
                updater.update(params)
            except ImportError:
                logger.info("[pelisalacarta.py] Actualizacion autom�tica desactivada")

            import channelselector as plugin
            plugin.listchannels(params, url, category)

        elif (action=="channeltypes"):
            import channelselector as plugin
            plugin.channeltypes(params,url,category)

        elif (action=="listchannels"):
            import channelselector as plugin
            plugin.listchannels(params,url,category)

        # El resto de acciones vienen en el par�metro "action", y el canal en el par�metro "channel"
        else:
            if action=="mainlist" and config.get_setting("updatechannels")=="true":
                from core import updater
                actualizado = updater.updatechannel(params.get("channel"))

                if actualizado:
                    import xbmcgui
                    advertencia = xbmcgui.Dialog()
                    advertencia.ok("plugin",params.get("channel"),config.get_localized_string(30063))

            # Primero intenta cargarlo como canal normal
            try:
                logger.info("[channelselector.py] canal normal")
                exec "import tvalacarta.channels."+params.get("channel")+" as channel"
            except ImportError:
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line )
                
                # Luego intenta cargarlo como canal del core
                try:
                    logger.info("[channelselector.py] canal core")
                    exec "from core import "+params.get("channel")+" as channel"
                except:
                    # Como �ltimo recurso, intenta descargar el canal para ver si es nuevo
                    from core import updater
                    updater.download_channel(params.get("channel"))
                    exec "import tvalacarta.channels."+params.get("channel")+" as channel"
            generico = False
            try:
                generico = channel.isGeneric()
            except:
                generico = False

            print "generico=" , generico 
            
            if not generico:
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
            
                from core.item import Item
                item = Item(channel=params.get("channel"), title=title , url=url, thumbnail=thumbnail , plot=plot , server=server, category=category, extra=extra)

                from core import xbmctools
                if action=="play":
                    # Si el canal tiene una acci�n "play" tiene prioridad
                    try:
                        itemlist = channel.play(item)
                        if len(itemlist)>0:
                            item = itemlist[0]
                        
                        xbmctools.playvideo(params.get("channel"),item.server,item.url,item.category,item.title,item.thumbnail,item.plot)
                    except:
                        import sys
                        for line in sys.exc_info():
                            logger.error( "%s" % line )
                        xbmctools.playvideo(params.get("channel"),server,url,category,title,thumbnail,plot)
                elif action=="search":
                    logger.info("[launcher.py] search")
                    import xbmc
                    keyboard = xbmc.Keyboard("")
                    keyboard.doModal()
                    if (keyboard.isConfirmed()):
                        tecleado = keyboard.getText()
                        tecleado = tecleado.replace(" ", "+")
                        itemlist = channel.search(item,tecleado)
                    else:
                        itemlist = []
                    xbmctools.renderItems(itemlist, params, url, category)
                else:
                    if action!="findvideos":
                        exec "itemlist = channel."+action+"(item)"
                    else:
                        # Intenta ejecutar una posible funcion "findvideos" del canal
                        try:
                            exec "itemlist = channel."+action+"(item)"
                        # Si no funciona, lanza el m�todo gen�rico para detectar v�deos
                        except:
                            itemlist = findvideos(item)

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
            ok = ventana_error.ok ("tvalacarta", texto)
        # Agarra los errores con codigo de respuesta del servidor externo solicitado     
        elif hasattr(e,'code'):
            logger.info("codigo de error HTTP : %d" %e.code)
            texto = (config.get_localized_string(30051) % e.code) # "El sitio web no funciona correctamente (error http %d)"
            ok = ventana_error.ok ("tvalacarta", texto)    

# Funci�n gen�rica para encontrar v�deos en una p�gina
def findvideos(item):
    logger.info("[pelisalacarta.py] findvideos")

    # Descarga la p�gina
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
