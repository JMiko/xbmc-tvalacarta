# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib
import base64
import os
import binascii

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from core import config
from core import wiideoteca
from core.item import Item
from core import platform_name
from core import scrapertools

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("wiimc")

#TODO: Pasar esto a ¿config?
VERSIONTAG = "3.2.65"

#from lib import cerealizer
#cerealizer.register(Item)

def get_content_type():
    return "text/html"

def controller(plugin_name,port,host,path,headers):

    # Lee la plantilla
    file_plantilla = open( os.path.join( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , "page.html") )
    plantilla_pagina = file_plantilla.read()
    file_plantilla.close()
    
    file_plantilla = open( os.path.join( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , "item.html") )
    plantilla_item = file_plantilla.read()
    file_plantilla.close()
    
    itemlist_respuesta = []
    respuesta = ""

    try:
    
        # Menú principal 
        if path == "/"+platform_name.PLATFORM_NAME+"/" or path=="/"+platform_name.PLATFORM_NAME:
            respuesta = plantilla_pagina.replace("{$page-title}","pelisalacarta")
    
            import channelselector
            channelslist = channelselector.getmainlist()
    
            # Actualización automática de canales, actualiza la lista
            if config.get_setting("updatechannels")=="true":
                
                logger.info("Verificando actualización del channelselector")
                from core import updater
                actualizado = updater.updatechannel("channelselector")

                if actualizado:
                    itemlist_respuesta.append( Item( url="http://"+host+"/"+platform_name.PLATFORM_NAME , title="¡Lista de canales actualizada¡" , thumbnail="http://pelisalacarta.mimediacenter.info/squares/Crystal_Clear_action_info.png", plot=channel.plot ) )
    
            for channel in channelslist:
    
                # Quita el canal de ayuda y el de configuración, no sirven en WiiMC
                if channel.channel!="configuracion" and channel.channel!="ayuda":
                    itemlist_respuesta.append( Item(title=channel.title, url="http://"+host+"/"+platform_name.PLATFORM_NAME+"/"+base64.b64encode(channel.serialize()).replace("/","%2F"),thumbnail=channel.thumbnail, plot=channel.plot) )
        else:
            
            item = extract_item_from_url(path)
            respuesta = plantilla_pagina.replace("{$page-title}",item.title)
    
            if item.channel=="channelselector" and item.action=="channeltypes":
                
                import channelselector
                channelslist = channelselector.getchanneltypes()
                
                for channel in channelslist:
                    itemlist_respuesta.append( Item( url = "http://"+host+"/"+platform_name.PLATFORM_NAME+"/"+base64.b64encode(channel.serialize()).replace("/","%2F"), title = channel.title, thumbnail = channel.thumbnail, plot=channel.plot) )
            
            elif item.channel=="channelselector" and item.action=="listchannels":
                
                import channelselector
                channelslist = channelselector.filterchannels(item.category)
                
                for channel in channelslist:
                    if channel.type=="generic" or channel.type=="wiimc":
                        channel.action="mainlist"
                        itemlist_respuesta.append( Item( url = "http://"+host+"/"+platform_name.PLATFORM_NAME+"/"+base64.b64encode(channel.serialize()).replace("/","%2F"), title = channel.title, thumbnail = channel.thumbnail, plot=channel.plot) )
        
            else:
                itemlist,channel = getitems(item)
                
                # Las listas vacías son problemáticas, añade un elemento dummy
                if len(itemlist)==0:
                    itemlist.append( Item(title="(No hay elementos)") )
                
                for item in itemlist:
                    if item.action=="search":
                        if item.server=="": item.server="none"
                        if item.url=="": item.url="none"
                        url = "http://%s/%s" % ( host+"/"+platform_name.PLATFORM_NAME , base64.b64encode( item.serialize() ).replace("/","%2F") )
                        if item.thumbnail=="":
                            item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/search.png"
                        
                        itemlist_respuesta.append( Item(url=url, title = item.title, thumbnail=item.thumbnail, plot=item.plot) )

                    elif item.folder or item.action=="play" or item.action=="downloadall":
                        if item.server=="": item.server="none"
                        if item.url=="": item.url="none"
                        if item.title=="": item.title="Ver el video-"

                        if item.thumbnail=="":
                            #if item.server!="" and item.server.lower()!="directo":
                            #    item.thumbnail = "http://pelisalacarta.mimediacenter.info/servers/"+item.server+".png"
                            #else:
                            if item.folder:
                                item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/folder.png"
                            else:
                                item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/file.png"


                        url = "http://%s/%s" % ( host+"/"+platform_name.PLATFORM_NAME , base64.b64encode( item.serialize() ).replace("/","%2F") )
                        itemlist_respuesta.append( Item(url=url, title = item.title, thumbnail=item.thumbnail, plot=item.plot) )
                        logger.info("  Nivel intermedio "+url)
                    else:
                        if item.thumbnail=="":
                            #if item.server!="" and item.server.lower()!="directo":
                            #    item.thumbnail = "http://pelisalacarta.mimediacenter.info/servers/"+item.server+".png"
                            #else:
                            if item.folder:
                                item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/folder.png"
                            else:
                                item.thumbnail = "http://pelisalacarta.mimediacenter.info/squares/file.png"

                        itemlist_respuesta.append( Item(url=item.url, title = item.title, thumbnail=item.thumbnail, plot=item.plot) )
                        logger.info("  Video "+item.url)

        itemlist_string =""
        for item in itemlist_respuesta:
            item_string = plantilla_item
            item_string = item_string.replace("{$title}",item.title)
            item_string = item_string.replace("{$url}",item.url)
            item_string = item_string.replace("{$thumbnail}",item.thumbnail)
            item_string = item_string.replace("{$plot}",scrapertools.htmlclean(item.plot))
            itemlist_string = itemlist_string+item_string+"\n"
    
        respuesta = respuesta.replace("{$itemlist}",itemlist_string)

    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

    return respuesta

def extract_item_from_url(requestpath):
    logger.info("extract_item_from_url()")
    # La ruta empleada en la petición
    ruta = requestpath.split("?")[0]
    logger.info("ruta="+ruta)

    # El item serializado está codificado en base64
    itemserializado = ruta.split("/")[2]
    itemserializado = itemserializado.replace("%2F","/")
    itemserializado = itemserializado.replace("%2f","/")
    logger.info("item base64="+itemserializado)
    import base64
    item = Item()
    item.deserialize(base64.b64decode(itemserializado))
    logger.info("item: channel="+item.channel+", action="+item.action+", title="+item.title+", url="+item.url+", server="+item.server+", category="+item.category)

    return item

def getitems(item):
    logger.info("getitems")
    itemlist = []
    
    # Extrae los parámetros
    channel = item.channel
    accion = item.action
    url = item.url
    if url!="none":
        if not "filenium" in url:
            url = urllib.unquote_plus(url)
    server = item.server
    title = item.title
    extra = item.extra
    category = item.category
    fulltitle = item.fulltitle

    try:
        if accion=="mainlist" and config.get_setting("updatechannels")=="true":
            try:
                logger.info("Verificando actualización del canal")
                from core import updater
                actualizado = updater.updatechannel(channel)
        
                if actualizado:
                    itemlist.append( Item(title="¡Canal descargado y actualizado!") )
            except:
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line )
    
        # El item que invocó es importante para obtener el siguiente
        senderitem = Item( title=title , channel=channel, action=accion, url=url , server=server, extra=extra, category=category, fulltitle=fulltitle )
        if "|" in url:
            partes = urllib.unquote_plus(senderitem.url).split("|")
            refered_item = Item(title=partes[0],url=partes[2],thumbnail="",server=partes[1],plot="",extra=partes[3])
            logger.info( "refered_item title="+refered_item.title+", url="+refered_item.url+", server="+refered_item.server+", extra="+refered_item.extra)
    
        else:
            refered_item = Item()
    
        # Importa el canal y ejecuta la función
        try:
            exec "from pelisalacarta.channels import "+channel+" as channelmodule"
        except:
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
            try:
                exec "from pelisalacarta import "+channel+" as channelmodule"
            except:
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line )
                try:
                    exec "from core import "+channel+" as channelmodule"
                except:
                    pass
    
        # play - es el menú de reproducción de un vídeo
        if accion=="play":
            logger.info("ACCION PLAY")
            if hasattr(channelmodule, 'play'):
                logger.info("[launcher.py] executing channel 'play' method")
                logger.info(channelmodule.__file__)
                itemlist = channelmodule.play(senderitem)
                senderitem = itemlist[0]
                senderitem.folder=False
            else:
                logger.info("[launcher.py] no channel 'play' method, executing core method")
            itemlist = menu_video(senderitem)
    
        # play_video - genera una playlist con una sola entrada para que wiimc la reproduzca
        elif accion=="play_video":
            logger.info("ACCION PLAY_VIDEO")
            logger.info("url="+senderitem.url)
            senderitem.folder=False
            itemlist.append( senderitem )
    
        # search - es el buscador
        elif channel=="buscador" and accion=="mainlist":
            logger.info("ACCION SEARCH (buscador)")
            texto = requestpath.split("plx")[1]
            exec "itemlist = buscador.do_search_results(texto)"
            
        elif accion=="search":
            logger.info("ACCION SEARCH")
            texto = requestpath.split("plx")[1]
            exec "itemlist = channelmodule."+accion+"(senderitem,texto)"
    
        # findvideos - debe encontrar videos reproducibles
        elif accion=="findvideos":
            logger.info("ACCION FINDVIDEOS")
            try:
                exec "itemlist = channelmodule."+accion+"(senderitem)"
            except:
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line )
                itemlist = findvideos(senderitem,channel)
        
        elif accion=="descargar":
            itemlist = download_item(senderitem,refered_item)
        elif accion=="download_all":
            itemlist = download_all(senderitem,refered_item)
        elif accion=="add_to_favorites":
            itemlist = add_to_favorites(senderitem,refered_item)
        elif accion=="remove_from_favorites":
            itemlist = remove_from_favorites(senderitem,refered_item)
        elif accion=="add_to_downloads":
            itemlist = add_to_downloads(senderitem,refered_item)
        elif accion=="remove_from_downloads":
            itemlist = remove_from_downloads(senderitem,refered_item)
    
        elif accion=="remove_from_error_downloads":
            itemlist = remove_from_error_downloads(senderitem,refered_item)
        elif accion=="add_again_to_downloads":
            itemlist = add_again_to_downloads(senderitem,refered_item)
        elif accion=="send_to_jdownloader":
            itemlist = send_to_jdownloader(senderitem,refered_item)
        elif accion=="search_trailer":
            itemlist = search_trailer(senderitem,refered_item)
        elif accion=="add_serie_to_wiideoteca":
            itemlist = wiideoteca.AgregarSerie(senderitem)
        elif accion=="UltimoVisto":
            itemlist = wiideoteca.UltimoVisto(senderitem)
    
        else:
            if senderitem.url=="none":
                senderitem.url=""
            exec "itemlist.extend( channelmodule."+accion+"(senderitem) )"
        
        '''
        # Lo almacena en cache
        fichero = open( cached_file ,"wb")
        cerealizer.dump(itemlist,fichero)
        fichero.close()
        '''
    
        logger.info("Items devueltos")
        for item in itemlist:
            logger.info( " " + item.title + " | " + item.url + " | " + item.action)
    except:
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                logger.error(line_split)

    return itemlist,channel

def download_item(senderitem,refered_item):
    itemlist = []

    # Extrae todos los enlaces posibles
    exec "from servers import "+refered_item.server+" as server_connector"
    video_urls = server_connector.get_video_url( page_url=refered_item.url , premium=(config.get_setting("megavideopremium")=="true") , user=config.get_setting("megavideouser") , password=config.get_setting("megavideopassword") )

    if len(video_urls)>0:
        from core import downloadtools
        titulo = senderitem.fulltitle
        if titulo=="": titulo=refered_item.title
        downloadtools.downloadtitle(video_urls[len(video_urls)-1][1],titulo)
        itemlist.append( Item( title="Descarga finalizada" ) )
    else:
        itemlist.append( Item( title="El video ya no está disponible" ) )
    
    return itemlist

def send_to_jdownloader(senderitem,refered_item):
    itemlist = []
    itemlist.append( Item( title="Opcion no disponible" ) )

def search_trailer(senderitem,refered_item):
    itemlist = []
    itemlist.append( Item( title="Opcion no disponible" ) )

def add_to_favorites(senderitem,refered_item):
    from core import favoritos
    favoritos.savebookmark(titulo=refered_item.title,url=refered_item.url,thumbnail="",server=refered_item.server,fulltitle=senderitem.fulltitle,plot="")

    itemlist = []
    itemlist.append( Item( title="El video %s" % senderitem.fulltitle ) )
    itemlist.append( Item( title="ha sido añadido a favoritos" ) )
    
    return itemlist

def remove_from_favorites(senderitem,refered_item):
    from core import favoritos
    favoritos.deletebookmark(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title ) )
    itemlist.append( Item( title="ha sido eliminado de favoritos" ) )
    
    return itemlist

def download_all(senderitem,refered_item):
    from core import descargas
    descargas.downloadall(senderitem)
    
    itemlist = []
    itemlist.append( Item( title="Fin de todas las descargas pendientes" ) )
    
    return itemlist

def add_to_downloads(senderitem,refered_item):
    from core import descargas
    descargas.savebookmark(titulo=refered_item.title,url=refered_item.url,thumbnail="",server=refered_item.server,plot="")
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title ) )
    itemlist.append( Item( title="ha sido añadido a la lista" ) )
    itemlist.append( Item( title="de descargas" ) )
    
    return itemlist

def remove_from_downloads(senderitem,refered_item):
    from core import descargas
    descargas.deletebookmark(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title ) )
    itemlist.append( Item( title="ha sido eliminado de la lista" ) )
    itemlist.append( Item( title="de descargas" ) )
    
    return itemlist

def remove_from_error_downloads(senderitem,refered_item):
    from core import descargas
    descargas.delete_error_bookmark(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title ) )
    itemlist.append( Item( title="ha sido eliminado definitivamente" ) )
    
    return itemlist

def add_again_to_downloads(senderitem,refered_item):
    from core import descargas
    descargas.mover_descarga_error_a_pendiente(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title ) )
    itemlist.append( Item( title="ha sido movido a la lista" ) )
    itemlist.append( Item( title="de descargas de nuevo" ) )
    
    return itemlist

def menu_video(item):
    itemlist = []
    logger.info("menu_video url="+item.url+", server="+item.server+", fulltitle="+item.fulltitle)

    from servers import servertools
    video_urls,puede,motivo = servertools.resolve_video_urls_for_playing( item.server , item.url , video_password="" , muestra_dialogo=False)

    if puede:
        for video_url in video_urls:
            itemlist.append( Item(channel=item.channel, title="Ver "+video_url[0], url=video_url[1], action="play_video") )
        
        refered_item_encoded = urllib.quote(item.title.replace("|","-"))+"|"+urllib.quote(item.server)+"|"+urllib.quote(item.url)+"|"+urllib.quote(item.extra)
        
        itemlist.append( Item(channel=item.channel, title="Descargar",action="descargar",url=refered_item_encoded,fulltitle=urllib.quote(item.fulltitle) ) )
        
        if item.channel!="favoritos":
            itemlist.append( Item(channel=item.channel, title="Añadir a favoritos",action="add_to_favorites",url=refered_item_encoded,fulltitle=urllib.quote(item.fulltitle) ) )
        else:
            itemlist.append( Item(channel=item.channel, title="Quitar de favoritos",action="remove_from_favorites",url=refered_item_encoded,fulltitle=urllib.quote(item.fulltitle) ) )
        
        if item.channel!="descargas":
            itemlist.append( Item(channel=item.channel, title="Añadir a la lista de descargas",action="add_to_downloads",url=refered_item_encoded,fulltitle=urllib.quote(item.fulltitle) ) )
        else:
            if item.category=="errores":
                itemlist.append( Item(channel=item.channel, title="Quitar definitivamente de la lista de descargas",action="remove_from_error_downloads",url=refered_item_encoded ) )
                itemlist.append( Item(channel=item.channel, title="Pasar de nuevo a la lista de descargas",action="add_again_to_downloads",url=refered_item_encoded ) )
            else:
                itemlist.append( Item(channel=item.channel, title="Quitar de la lista de descargas",action="remove_from_downloads",url=refered_item_encoded ) )
    
        itemlist.append( Item(channel=item.channel, title="Enviar a jdownloader",action="send_to_jdownloader",url=refered_item_encoded ) )
        itemlist.append( Item(channel=item.channel, title="Buscar trailer",action="search_trailer",url=refered_item_encoded ) )
        if item.category=="wiideoteca":
            itemlist.append( Item(channel=item.channel, title="Marcar como Ultimo Episodio Visto",action="UltimoVisto",url=item.extra,fulltitle=item.fulltitle ) )

    # Si no puedes ver el vídeo te informa
    else:
        itemlist.append( Item(title="No puedes ver ese vídeo porque...") )
        if item.server!="":
            if "<br/>" in motivo:
                itemlist.append( Item(title=motivo.split("<br/>")[0]) )
                itemlist.append( Item(title=motivo.split("<br/>")[1]) )
                itemlist.append( Item(title=item.url) )
            else:
                itemlist.append( Item(title=motivo) )
                itemlist.append( Item(title=item.url) )
        else:
            itemlist.append( Item(title="El servidor donde está alojado no está") )
            itemlist.append( Item(title="soportado en pelisalacarta todavía") )
            itemlist.append( Item(title=item.url) )

    return itemlist

def findvideos(item,channel):
    logger.info("findvideos")

    url = item.url
    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot
    fulltitle = item.fulltitle
    # Descarga la pagina
    from core import scrapertools
    data = scrapertools.cachePage(url)
    
    from servers import servertools
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = video[0]
        scrapedurl = video[1]
        server = video[2]

        itemlist.append( Item(channel=channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, fulltitle=fulltitle, folder=False))

    return itemlist
