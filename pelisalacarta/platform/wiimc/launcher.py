# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib
import os
import binascii
import md5

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from core import config
from core.item import Item

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("wiimc")

#from lib import cerealizer
#cerealizer.register(Item)

def controller(plugin_name,port,host,path,headers):

    respuesta = ""

    respuesta += "version=7\n"
    respuesta += "logo=http://www.mimediacenter.info/xbmc/tvalacarta/icon.jpg\n"
    respuesta += "title="+plugin_name+" 3.0.0 (WiiMC)\n"
    respuesta += "\n"

    if path == "/wiimc/" or path=="/wiimc":
        import channelselector
        channelslist = channelselector.getmainlist()

        # Actualización automática de canales, actualiza la lista
        if config.get_setting("updatechannels")=="true":
            logger.info("Verificando actualización del channelselector")
            try:
                from core import updater
                actualizado = updater.updatechannel("channelselector")

                if actualizado:
                    respuesta += "type=playlist\n"
                    respuesta += "name=¡Lista de canales actualizada!\n"
                    respuesta += "thumb=\n"
                    respuesta += "URL=http://"+host+"/wiimc/\n"
                    respuesta += "\n"
            except:
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line )

        for channel in channelslist:

            # Quita el canal de ayuda y el de configuración, no sirven en WiiMC
            if channel.channel!="configuracion" and channel.channel!="ayuda":
                
                if channel.channel!="buscador":
                    respuesta += "type=playlist\n"
                else:
                    respuesta += "type=search\n"
                respuesta += "name="+channel.title+"\n"
                respuesta += "thumb=http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.channel+".png\n"
                respuesta += "URL=http://"+host+"/wiimc/"+channel.channel+"/"+channel.action+"/none/none/none/none/none/none/playlist.plx\n"
                respuesta += "\n"
    
    elif path.startswith("/wiimc/channelselector/channeltypes"):
        
        import channelselector
        channelslist = channelselector.getchanneltypes()
        
        for channel in channelslist:
            respuesta += "type=playlist\n"
            respuesta += "name="+channel.title+"\n"
            respuesta += "thumb=http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.channel+".png\n"
            respuesta += "URL=http://"+host+"/wiimc/"+channel.channel+"/"+channel.action+"/"+channel.category+"/none/none/none/none/playlist.plx\n"
            respuesta += "\n"
    
    elif path.startswith("/wiimc/channelselector/listchannels"):
        
        category = path.split("/")[4]
        logger.info("##category="+category)

        import channelselector
        channelslist = channelselector.filterchannels(category)
        
        for channel in channelslist:
            if channel.type=="generic" or channel.type=="wiimc":
                respuesta += "type=playlist\n"
                respuesta += "name="+channel.title+"\n"
                respuesta += "thumb=http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.channel+".png\n"
                respuesta += "URL=http://"+host+"/wiimc/"+channel.channel+"/mainlist/none/none/none/none/none/playlist.plx\n"
                respuesta += "\n"

    else:
        itemlist,channel = getitems(path)
        
        # Las listas vacías son problemáticas, añade un elemento dummy
        if len(itemlist)==0:
            itemlist.append( Item(title="(No hay elementos)") )
        
        import urllib
        for item in itemlist:
            if item.action=="search":
                logger.info("  Buscador")
                if item.server=="": item.server="none"
                if item.url=="": item.url="none"
                url = "http://%s/%s/%s/%s/%s/%s/%s/%s/playlist.plx" % ( host+"/wiimc" , channel , item.action , urllib.quote_plus(item.url) , item.server, urllib.quote_plus(item.title),urllib.quote_plus(item.extra),urllib.quote_plus(item.category) )
                respuesta += "type=search\n"
                respuesta += "name=%s\n" % item.title
                if item.thumbnail != "":
                    respuesta += "thumb=%s\n" % item.thumbnail
                respuesta += "URL=%s\n" % url
                respuesta += "\n"
 
            elif item.folder or item.action=="play" or item.action=="downloadall":
                logger.info("  Nivel intermedio")
                if item.server=="": item.server="none"
                if item.url=="": item.url="none"
                if item.title=="": item.title="Ver el video-"

                url = "http://%s/%s/%s/%s/%s/%s/%s/%s/playlist.plx" % ( host+"/wiimc" , channel , item.action , urllib.quote_plus(item.url) , item.server ,urllib.quote_plus(item.title),urllib.quote_plus(item.extra),urllib.quote_plus(item.category) )
                respuesta += "type=playlist\n"
                respuesta += "name=%s\n" % item.title
                if item.thumbnail != "":
                    respuesta += "thumb=%s\n" % item.thumbnail
                respuesta += "URL=%s\n" % url
                respuesta += "\n"
            else:
                logger.info("  Video")
                respuesta += "type=video\n"
                respuesta += "name=%s\n" % item.title
                respuesta += "URL=%s\n" % item.url
                respuesta += "\n"

    return respuesta

def getitems(requestpath):
    logger.info("getitems")
    itemlist = []

    # La ruta empleada en la petición
    ruta = requestpath.split("?")[0]
    logger.info("ruta="+ruta)

    # Los parámetros son las partes de la ruta separadas por "/"
    rutas = ruta.split("/")
    cadena = " "
    
    # Las imprime en el log
    for linea in rutas:
        cadena = cadena + linea + " | "
    logger.info( cadena )

    # Extrae los parámetros
    channel = rutas[2]
    accion = rutas[3]
    url = rutas[4]
    if url!="none": url = urllib.unquote_plus(url)
    server = rutas[5].lower()
    title = urllib.unquote_plus(rutas[6])
    extra = urllib.unquote_plus(rutas[7])
    category = urllib.unquote_plus(rutas[8])
    logger.info( "channel="+channel+", accion="+accion+", url="+url+", server="+server+", title="+title+", extra="+extra+", category="+category)

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

    '''
    # Obtiene un nombre válido para la cache
    hashed_url = binascii.hexlify(md5.new(requestpath).digest())
    cached_file = os.path.join( config.get_data_path() , "tmp" , "cache" , hashed_url )
    logger.info( "Cache file must be "+cached_file )
    
    # Si el fichero está en cache
    if os.path.exists(cached_file):
        logger.info( "Reading from cache" )
        fichero = open( cached_file ,"rb")
        itemlist = cerealizer.load(fichero)
        fichero.close()
        
    # Si no está en cache
    else:
    '''
    logger.info( "Not cached" )

    # El item que invocó es importante para obtener el siguiente
    senderitem = Item( title=title , channel=channel, action=accion, url=url , server=server, extra=extra, category=category )
    if "|" in url:
        partes = urllib.unquote_plus(senderitem.url).split("|")
        refered_item = Item(title=partes[0],url=partes[2],thumbnail="",server=partes[1],plot="",extra=partes[3])
        logger.info( "refered_item title="+refered_item.title+", url="+refered_item.url+", server="+refered_item.server+", extra="+refered_item.extra)

    else:
        refered_item = Item()

    # Importa el canal y ejecuta la función
    try:
        exec "from pelisalacarta.channels import "+channel
    except:
        exec "from core import "+channel

    # play - es el menú de reproducción de un vídeo
    if accion=="play":
        logger.info("ACCION PLAY")
        try:
            exec "itemlist = "+channel+".play(senderitem)"
            senderitem = itemlist[0]
            senderitem.folder=False
        except:
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )

        itemlist = menu_video(senderitem)

    # play_video - genera una playlist con una sola entrada para que wiimc la reproduzca
    elif accion=="play_video":
        logger.info("ACCION PLAY_VIDEO")
        senderitem.folder=False
        itemlist.append( senderitem )

    # search - es el buscador
    elif accion=="search":
        logger.info("ACCION SEARCH")
        texto = requestpath.split("plx")[1]
        exec "itemlist = "+channel+"."+accion+"(senderitem,texto)"

    # findvideos - debe encontrar videos reproducibles
    elif accion=="findvideos":
        logger.info("ACCION FINDVIDEOS")
        try:
            exec "itemlist = "+channel+"."+accion+"(senderitem)"
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

    else:
        if senderitem.url=="none":
            senderitem.url=""
        exec "itemlist.extend( "+channel+"."+accion+"(senderitem) )"
    
    '''
    # Lo almacena en cache
    fichero = open( cached_file ,"wb")
    cerealizer.dump(itemlist,fichero)
    fichero.close()
    '''

    logger.info("Items devueltos")
    for item in itemlist:
        logger.info( " " + item.title + " | " + item.url + " | " + item.action)

    return itemlist,channel

def download_item(senderitem,refered_item):
    itemlist = []

    # Extrae todos los enlaces posibles
    exec "from servers import "+refered_item.server+" as server_connector"
    video_urls = server_connector.get_video_url( page_url=refered_item.url , premium=(config.get_setting("megavideopremium")=="true") , user=config.get_setting("megavideouser") , password=config.get_setting("megavideopassword") )

    if len(video_urls)>0:
        from core import downloadtools
        downloadtools.downloadtitle(video_urls[len(video_urls)-1][1],refered_item.title)
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
    favoritos.savebookmark(titulo=refered_item.title,url=refered_item.url,thumbnail="",server=refered_item.server,plot="")
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title ) )
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
    logger.info("menu_video url="+item.url+", server="+item.server)
    
    video_urls = []

    # Extrae todos los enlaces posibles
    exec "from servers import "+item.server+" as server_connector"
    video_urls = server_connector.get_video_url( page_url=item.url , premium=(config.get_setting("megavideopremium")=="true") , user=config.get_setting("megavideouser") , password=config.get_setting("megavideopassword") )

    if len(video_urls)==0:
        itemlist.append( Item(title="El vídeo no está disponible") )
        itemlist.append( Item(title="en %s." % item.server) )
        return itemlist
    
    for video_url in video_urls:
        itemlist.append( Item(channel=item.channel, title="Ver "+video_url[0], url=video_url[1], action="play_video") )
    
    refered_item_encoded = urllib.quote(item.title.replace("|","-"))+"|"+urllib.quote(item.server)+"|"+urllib.quote(item.url)+"|"+urllib.quote(item.extra)
    
    itemlist.append( Item(channel=item.channel, title="Descargar",action="descargar",url=refered_item_encoded ) )
    
    if item.channel!="favoritos":
        itemlist.append( Item(channel=item.channel, title="Añadir a favoritos",action="add_to_favorites",url=refered_item_encoded ) )
    else:
        itemlist.append( Item(channel=item.channel, title="Quitar de favoritos",action="remove_from_favorites",url=refered_item_encoded ) )
    
    if item.channel!="descargas":
        itemlist.append( Item(channel=item.channel, title="Añadir a la lista de descargas",action="add_to_downloads",url=refered_item_encoded ) )
    else:
        if item.category=="errores":
            itemlist.append( Item(channel=item.channel, title="Quitar definitivamente de la lista de descargas",action="remove_from_error_downloads",url=refered_item_encoded ) )
            itemlist.append( Item(channel=item.channel, title="Pasar de nuevo a la lista de descargas",action="add_again_to_downloads",url=refered_item_encoded ) )
        else:
            itemlist.append( Item(channel=item.channel, title="Quitar de la lista de descargas",action="remove_from_downloads",url=refered_item_encoded ) )

    itemlist.append( Item(channel=item.channel, title="Enviar a jdownloader",action="send_to_jdownloader",url=refered_item_encoded ) )
    itemlist.append( Item(channel=item.channel, title="Buscar trailer",action="search_trailer",url=refered_item_encoded ) )

    return itemlist

def findvideos(item,channel):
    logger.info("findvideos")

    url = item.url
    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot

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

        itemlist.append( Item(channel=channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist
