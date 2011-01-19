# -*- coding: utf-8 -*-
import urllib
import os
import binascii
import md5

from core.item import Item
from core import logger

from lib import cerealizer
cerealizer.register(Item)

def getitems(requestpath):

    ruta = requestpath.split("?")[0]
    print "ruta="+ruta

    rutas = ruta.split("/")
    for linea in rutas:
        print linea

    # El primero es el canal
    channel = rutas[1]
    print "channel="+channel
    accion=rutas[2]
    print "accion="+accion
    url=rutas[3]
    if url!="none": url = urllib.unquote_plus(url)
    print "url="+url
    server=rutas[4]
    print "server="+server

    # Obtiene un nombre válido para la cache
    hashed_url = binascii.hexlify(md5.new(requestpath).digest())
    cached_file = os.path.join( os.getcwd() , "tmp" , "cache" , hashed_url )
    print cached_file
    
    if os.path.exists(cached_file):
        print "De cache"
        fichero = open( cached_file ,"rb")
        itemlist = cerealizer.load(fichero)
        fichero.close()

    else:
        print "Generado"
    
        # Parametros
        senderitem = Item( title="" , url=url , server=server )
    
        exec "from tvalacarta.channels import "+channel
        itemlist = []
    
        if accion=="play":
            itemlist = play(senderitem)
    
        elif accion=="findvideos":
            try:
                exec "itemlist = "+channel+"."+accion+"(senderitem)"
            except:
                itemlist = findvideos(senderitem,channel)
        else:
            if senderitem.url=="none":
                senderitem.url=""
            exec "itemlist = "+channel+"."+accion+"(senderitem)"
        
        # Lo almacena en cache
        fichero = open( cached_file ,"wb")
        cerealizer.dump(itemlist,fichero)
        fichero.close()

    return itemlist,channel

def play(item):
    itemlist = []
    logger.info("[wiitools.py] play")
    logger.info("url="+item.url)
    
    # Va a megavideo
    from servers import servertools
    if item.server.lower()=="megavideo":
        mediaurl = servertools.getmegavideolow(item.url)
        logger.info("mediaurl="+mediaurl)
        videoitem = Item( title="Ver en calidad baja (Megavideo)" , url = mediaurl , folder = False )
        itemlist.append( videoitem )
        
        import config
        if config.get_setting("megavideopremium")=="true":
            mediaurl = servertools.getmegavideohigh(item.url)
            logger.info("mediaurl="+mediaurl)
            videoitem = Item( title="Ver en calidad alta (Megavideo)" , url = mediaurl , folder = False )
            itemlist.append( videoitem )
    elif item.server.lower()=="megaupload":
        mediaurl = servertools.getmegauploadlow(item.url)
        logger.info("mediaurl="+mediaurl)
        videoitem = Item( title="Ver en calidad baja (Megavideo)" , url = mediaurl , folder = False )
        itemlist.append( videoitem )
        
        from core import config
        if config.get_setting("megavideopremium")=="true":
            mediaurl = servertools.getmegauploadhigh(item.url)
            logger.info("mediaurl="+mediaurl)
            videoitem = Item( title="Ver en calidad alta (Megaupload)" , url = mediaurl , folder = False )
            itemlist.append( videoitem )
    else:
        mediaurl = servertools.findurl(item.url,item.server)
        logger.info("mediaurl="+mediaurl)
        videoitem = Item( title="Ver el vídeo ("+item.server+")" , url = mediaurl , folder = False )
        itemlist.append( videoitem )

    return itemlist

def findvideos(item,channel):
    logger.info("[wiitools.py] findvideos")

    url = item.url
    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot

    # ------------------------------------------------------------------------------------
    # Descarga la pagina
    # ------------------------------------------------------------------------------------
    import scrapertools
    data = scrapertools.cachePage(url)
    
    import servertools
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = video[0]
        scrapedurl = video[1]
        server = video[2]

        itemlist.append( Item(channel=channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist