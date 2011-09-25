# -*- coding: utf-8 -*-
import urllib
import os
import binascii
import md5

from core.item import Item
from core import config

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("wiimc")

from lib import cerealizer
cerealizer.register(Item)

def getitems(requestpath):

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
    logger.info( "channel="+channel+", accion="+accion+", url="+url+", server="+server+", title="+title )

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
        logger.info( "Not cached" )
    
        # El item que invocó es importante para obtener el siguiente
        senderitem = Item( title=title , channel=channel, action=accion, url=url , server=server )

        # Importa el canal y ejecuta la función
        try:
            exec "from pelisalacarta.channels import "+channel
        except:
            exec "from core import "+channel
        itemlist = []

        # play - es el menú de reproducción de un vídeo
        if accion=="play":
            try:
                exec "itemlist = "+channel+".play(senderitem)"
            except:
                pass

            itemlist = menu_video(senderitem)

        # play_video - genera una playlist con una sola entrada para que wiimc la reproduzca
        elif accion=="play_video":
            senderitem.folder=False
            itemlist.append( senderitem )
    
        # search - es el buscador
        elif accion=="search":
            extra = requestpath.split("plx")[1]
            senderitem.extra = extra
            exec "itemlist = "+channel+"."+accion+"(senderitem)"

        # findvideos - debe encontrar videos reproducibles
        elif accion=="findvideos":
            try:
                exec "itemlist = "+channel+"."+accion+"(senderitem)"
            except:
                itemlist = findvideos(senderitem,channel)
        elif accion=="add_to_favorites":
            
            partes = urllib.unquote_plus(url).split("|")

            from core import favoritos
            favoritos.savebookmark(titulo=partes[0],url=partes[1],thumbnail="",server=partes[2],plot="")

        else:
            if senderitem.url=="none":
                senderitem.url=""
            exec "itemlist = "+channel+"."+accion+"(senderitem)"
        
        # Lo almacena en cache
        fichero = open( cached_file ,"wb")
        cerealizer.dump(itemlist,fichero)
        fichero.close()

    logger.info("Items devueltos")
    for item in itemlist:
        logger.info( " " + item.title + " | " + item.url + " | " + item.action)

    return itemlist,channel

def menu_video(item):
    itemlist = []
    logger.info("play_video")
    logger.info("url="+item.url)
    
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
    
    itemlist.append( Item(channel=item.channel, title="Descargar",action="descargar" ) )
    
    if item.channel!="favoritos":
        itemlist.append( Item(channel=item.channel, title="Añadir a favoritos",action="add_to_favorites",url=urllib.quote(item.title)+"|"+urllib.quote(item.server)+"|"+urllib.quote(item.url) ) )
    else:
        itemlist.append( Item(channel=item.channel, title="Quitar de favoritos",action="remove_from_favorites" ) )
    
    if item.channel!="descargas":
        if item.action=="errores":
            itemlist.append( Item(channel=item.channel, title="Pasar de nuevo a la lista de descargas",action="add_again_to_downloads" ) )
        else:
            itemlist.append( Item(channel=item.channel, title="Añadir a la lista de descargas",action="add_to_downloads" ) )
    else:
        if item.action=="errores":
            itemlist.append( Item(channel=item.channel, title="Quitar definitivamente de la lista de descargas",action="remove_from_error_downloads" ) )
        else:
            itemlist.append( Item(channel=item.channel, title="Quitar de la lista de descargas",action="remove_from_downloads" ) )
    
    itemlist.append( Item(channel=item.channel, title="Enviar a jdownloader",action="send_to_jdownloader" ) )
    itemlist.append( Item(channel=item.channel, title="Buscar trailer",action="search_trailer" ) )

    return itemlist

def findvideos(item,channel):
    logger.info("findvideos")

    url = item.url
    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot

    # ------------------------------------------------------------------------------------
    # Descarga la pagina
    # ------------------------------------------------------------------------------------
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