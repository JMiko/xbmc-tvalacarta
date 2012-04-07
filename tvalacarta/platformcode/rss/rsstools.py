# -*- coding: utf-8 -*-
import urllib, os, binascii, md5, string, re

from core.item import Item
from core import scrapertools,config,wiideoteca

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("rss")

from lib import cerealizer
cerealizer.register(Item)

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
    fulltitle = urllib.unquote_plus(rutas[9])
    logger.info( "channel="+channel+", accion="+accion+", url="+url+", server="+server+", title="+title+", extra="+extra+", category="+category+" fulltitle="+fulltitle)
    print "channel="+channel+", accion="+accion+", url="+url+", server="+server+", title="+title+", extra="+extra+", category="+category

    if accion=="mainlist" and config.get_setting("updatechannels")=="true":
        logger.info("Verificando actualización del canal")
        from core import updater
        actualizado = updater.updatechannel(channel)

        if actualizado:
            itemlist.append( Item(title="¡Canal descargado y actualizado!") )

    # Obtiene un nombre válido para la cache
    hashed_url = binascii.hexlify(md5.new(requestpath).digest())
    cached_file = os.path.join( config.get_data_path() , "tmp" , "cache" , hashed_url )
    logger.info("cached_file="+cached_file)
    
    # Si el fichero está en cache
    if channel not in ("trailertools","buscador","configuracion","pyload","wiidoteca") and os.path.exists(cached_file): # <--
        logger.info( "Reading from cache" )
        fichero = open( cached_file ,"rb")
        itemlist = cerealizer.load(fichero)
        fichero.close()

    else:
        logger.info( "Not cached" )

### ESTUDIAR 
        #if accion not in ("play","findvideos","detail"): titulo = ""
### 
        # El item que invocó es importante para obtener el siguiente
        senderitem = Item( title=title , channel=channel, action=accion, url=url , server=server, extra=extra, category=category, fulltitle=fulltitle )
        if "|" in url:
            ## <-- unquote despues de split para no interferir cuando | aparece en algun campo
            partes = senderitem.url.split("|")
            decpartes = []
            for parte in partes:
               decpartes.append(urllib.unquote_plus(parte))
            partes = decpartes
            ## <--
            refered_item = Item(title=partes[0],url=partes[2],thumbnail=partes[5],server=partes[1],plot=partes[6],extra=partes[3], fulltitle=partes[4])
            logger.info( "refered_item title="+refered_item.title+", url="+refered_item.url+", server="+refered_item.server+", extra="+refered_item.extra)
    
        else:
            refered_item = Item()
    
        # Importa el canal y ejecuta la función
        if channel in ("configuracion", "trailertools", "buscador") :
           exec "import "+channel
        else:
            try:
               exec "from tvalacarta.channels import "+channel
            except:
               exec "from core import "+channel
    
        # play - es el menú de reproducción de un vídeo
        if accion=="play":
            logger.info("ACCION PLAY")
            print "ACCION PLAY"
            try:
                exec "itemlist = "+channel+".play(senderitem)"
                print "itemlist = "+channel+".play(senderitem)"
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
        elif accion == "search":
            logger.info("ACCION SEARCH")
            texto = requestpath.split(".rss")[1]
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
        elif accion=="downloadall":                                ## <--
            itemlist = downloadall(senderitem,refered_item)        ## <--
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
        elif accion=="send_to_pyload":
            itemlist = send_to_pyload(senderitem,refered_item)
        elif accion=="search_trailer":
            itemlist = search_trailer(senderitem,refered_item)
        elif accion=="add_serie_to_wiideoteca":
            itemlist = wiideoteca.AgregarSerie(senderitem)
        elif accion=="UltimoVisto":
            itemlist = wiideoteca.UltimoVisto(senderitem)
    
        else:
            if senderitem.url=="none":
                senderitem.url=""
            exec "itemlist.extend( "+channel+"."+accion+"(senderitem) )"
    
        # Lo almacena en cache
        fichero = open( cached_file ,"wb")
        cerealizer.dump(itemlist,fichero)
        fichero.close()
    
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
        downloadtools.downloadtitle(video_urls[len(video_urls)-1][1],refered_item.fulltitle) ## <--
        itemlist.append( Item( title="Descarga finalizada", action = "mainlist" ) )
    else:
        itemlist.append( Item( title="El video ya no está disponible", action = "mainlist" ) )
    
    return itemlist

def send_to_jdownloader(senderitem,refered_item):
    itemlist = []
    return itemlist
    
def send_to_pyload(senderitem,refered_item):
    from core import pyload
    refered_item.action = "play"
    return pyload.descargar(refered_item)

def search_trailer(senderitem,refered_item):
    import trailertools
    itemlist = []
    print refered_item.tostring()
    itemlist = trailertools.search(refered_item, senderitem.extra)
    return itemlist

def add_to_favorites(senderitem,refered_item):
    from core import favoritos
    favoritos.savebookmark(canal=senderitem.channel,titulo=refered_item.title,url=refered_item.url,thumbnail=senderitem.thumbnail,server=refered_item.server,plot="",fulltitle=senderitem.fulltitle )
    itemlist = []
    itemlist.append( Item( title="El video %s" % senderitem.extra, channel=senderitem.channel,action="play",url=refered_item.url,server=refered_item.server, fulltitle=senderitem.fulltitle, folder=True ) )
    itemlist.append( Item( title="ha sido añadido a favoritos", channel=senderitem.channel,action="play",url=refered_item.url,server=refered_item.server, fulltitle=senderitem.fulltitle, folder=True  ) )

    return itemlist

def remove_from_favorites(senderitem,refered_item):
    from core import favoritos
    favoritos.deletebookmark(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % senderitem.fulltitle, channel="favoritos", action="mainlist" ) )
    itemlist.append( Item( title="ha sido eliminado de favoritos", channel="favoritos", action="mainlist" ) )
    
    return itemlist

def downloadall(senderitem,refered_item):
    from core import descargas
    itemlist = []
    descargas.downloadall(senderitem)
    itemlist.append( Item( title="Fin de todas las descargas pendientes", action="mainlist" ) )
    
    return itemlist

def add_to_downloads(senderitem,refered_item):
    from core import descargas
    descargas.savebookmark(canal=senderitem.channel,titulo=refered_item.title,url=refered_item.url,thumbnail=senderitem.thumbnail,server=refered_item.server,plot="",fulltitle=senderitem.fulltitle)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % senderitem.fulltitle, channel=senderitem.channel,action="play",url=refered_item.url,server=refered_item.server, fulltitle=senderitem.fulltitle, folder=True ) )
    itemlist.append( Item( title="ha sido añadido a la lista de descargas", channel=senderitem.channel,action="play",url=refered_item.url,server=refered_item.server, fulltitle=senderitem.fulltitle, folder=True ) )
    
    return itemlist

def remove_from_downloads(senderitem,refered_item):
    from core import descargas
    descargas.deletebookmark(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % senderitem.fulltitle, action = "mainlist" ) )
    itemlist.append( Item( title="ha sido eliminado de la lista de descargas", action = "mainlist" ) )
    
    return itemlist

def remove_from_error_downloads(senderitem,refered_item):
    from core import descargas
    descargas.delete_error_bookmark(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title, action = "mainlist" ) )
    itemlist.append( Item( title="ha sido eliminado definitivamente", action = "mainlist" ) )
    
    return itemlist

def add_again_to_downloads(senderitem,refered_item):
    from core import descargas
    descargas.mover_descarga_error_a_pendiente(refered_item.extra)
    
    itemlist = []
    itemlist.append( Item( title="El video %s" % refered_item.title, action = "mainlist" ) )
    itemlist.append( Item( title="ha sido movido a la lista", action = "mainlist" ) )
    itemlist.append( Item( title="de descargas de nuevo", action = "mainlist" ) )
    
    return itemlist

def menu_video(item):
    itemlist = []
    logger.info("menu_video url="+item.url+", server="+item.server)
    
    if item.server=="local":
       itemlist.append( Item(title=item.title, fulltitle=item.fulltitle, url=item.url, action="play_video", thumbnail=item.thumbnail, plot=item.plot, folder=False))
       return itemlist
       
    video_urls = []

    # Extrae todos los enlaces posibles
    exec "from servers import "+item.server+" as server_connector"
    video_urls = server_connector.get_video_url( page_url=item.url , premium=(config.get_setting("megavideopremium")=="true") , user=config.get_setting("megavideouser") , password=config.get_setting("megavideopassword") )

    if config.get_setting("fileniumpremium")=="true" and item.server not in ["vk","fourshared","directo","adnstream","facebook","megalive","tutv","stagevu"]:
        exec "from servers import filenium as gen_conector"
        
        # Parche para solucionar el problema habitual de que un vídeo http://www.megavideo.com/?d=XXX no está, pero http://www.megaupload.com/?d=XXX si
        url = url.replace("http://www.megavideo.com/?d","http://www.megaupload.com/?d")

        video_gen = gen_conector.get_video_url( page_url=item.url , premium=(config.get_setting("fileniumpremium")=="true") , user=config.get_setting("fileniumuser") , password=config.get_setting("fileniumpassword") )
        logger.info("[rsstools.py] filenium url="+video_gen)
        video_urls.append( [ "[filenium]", video_gen ] )

    if len(video_urls)==0:
        itemlist.append( Item(title="El vídeo no está disponible",channel=item.channel, action=item.action, url=item.url, server=item.server, extra=item.extra, fulltitle=item.fulltitle) )
        itemlist.append( Item(title="en %s." % item.server,channel=item.channel, action=item.action, url=item.url, server=item.server, extra=item.extra, fulltitle=item.fulltitle) )
        return itemlist
    
    for video_url in video_urls:
        itemlist.append( Item(channel=item.channel, title="Ver "+video_url[0], url=video_url[1], action="play_video", extra=item.extra, fulltitle=item.fulltitle) )
    
    refered_item_encoded = urllib.quote(item.title)+"|"+urllib.quote(item.server)+"|"+urllib.quote(item.url)+"|"+urllib.quote(item.extra)+"|"+urllib.quote(item.fulltitle)+"|"+urllib.quote(item.thumbnail)+"|"+urllib.quote(item.plot)
    
    itemlist.append( Item(channel=item.channel, title="Descargar",action="descargar",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
    
    if item.channel!="favoritos":
        itemlist.append( Item(channel=item.channel, title="Añadir a favoritos",action="add_to_favorites",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
    else:
        itemlist.append( Item(channel=item.channel, title="Quitar de favoritos",action="remove_from_favorites",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
    
    if item.channel!="descargas":
        itemlist.append( Item(channel=item.channel, title="Añadir a la lista de descargas",action="add_to_downloads",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
    else:
        if item.category=="errores":
            itemlist.append( Item(channel=item.channel, title="Quitar definitivamente de la lista de descargas",action="remove_from_error_downloads",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
            itemlist.append( Item(channel=item.channel, title="Pasar de nuevo a la lista de descargas",action="add_again_to_downloads",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
        else:
            itemlist.append( Item(channel=item.channel, title="Quitar de la lista de descargas",action="remove_from_downloads",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )

    itemlist.append( Item(channel=item.channel, title="Enviar a pyLoad",action="send_to_pyload",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
#    itemlist.append( Item(channel=item.channel, title="Enviar a jdownloader",action="send_to_jdownloader",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
    if item.channel != "trailertools" or item.action != "play":
        itemlist.append( Item(channel=item.channel, title="Buscar trailer",action="search_trailer",url=refered_item_encoded, extra=item.extra, fulltitle=item.fulltitle ) )
    if item.category=="wiideoteca":
        itemlist.append( Item(channel=item.channel, title="Marcar como Ultimo Episodio Visto",action="UltimoVisto",url=item.extra,fulltitle=item.fulltitle ) )

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

        itemlist.append( Item(channel=channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, fulltitle=item.fulltitle, folder=True))

    return itemlist


def LimpiarTitulo(title):
        title = string.lower(title)
        #title = re.sub('\([^\)]+\)','',title)
        title = re.sub(' $','',title)
        title = title.replace("ÃÂ", "")
        title = title.replace("ÃÂ©","e")
        title = title.replace("ÃÂ¡","a")
        title = title.replace("ÃÂ³","o")
        title = title.replace("ÃÂº","u")
        title = title.replace("ÃÂ­","i")
        title = title.replace("ÃÂ±","ñ")
        title = title.replace("Ã¢â¬Â", "")
        title = title.replace("Ã¢â¬ÅÃÂ", "")
        title = title.replace("Ã¢â¬Å","")
        title = title.replace("Ã©","e")
        title = title.replace("Ã¡","a")
        title = title.replace("Ã³","o")
        title = title.replace("Ãº","u")
        title = title.replace("Ã­","i")
        title = title.replace("Ã±","ñ")

        title = title.replace("Ãâ","O")
        title = title.replace("@","")
        title = title.replace("é","e")
        title = title.replace("á","a")
        title = title.replace("ó","o")
        title = title.replace("ú","u")
        title = title.replace("í","i")
        title = title.replace('ñ','n')
        title = title.replace('Á','a')
        title = title.replace('É','e')
        title = title.replace('Í','i')
        title = title.replace('Ó','o')
        title = title.replace('Ú','u')
        title = title.replace('Ñ','n')
        title = title.replace(":"," ")
        title = title.replace("&","")
        title = title.replace('#','')
        title = title.replace('-','')
        title = title.replace('?','')
        title = title.replace('¿','')
        title = title.replace(",","")
        title = title.replace("*","")
        title = title.replace("\\","")
        title = title.replace("/","")
        title = title.replace("'","")
        title = title.replace('"','')
        title = title.replace("<","")
        title = title.replace(">","")
        title = title.replace(".","")
        title = title.replace("_"," ")
        title = title.replace("\("," ")
        title = title.replace("\)"," ")
        title = title.replace('|','')
        title = title.replace('!','')
        title = title.replace('¡','')
        title = title.replace("  "," ")
        title = title.replace("\Z  ","")
        return(title)

def DepuraTitulo(titulo,quita_parte="true", quita_especiales="true"):
    titulo = re.sub('\([^\)]+\)','',titulo)
    titulo = title = re.sub('\[[^\]]+\]','',titulo)

    sopa_palabras_invalidas = ("dvdrip" ,  "dvdscreener2" ,"tsscreener" , "latino" ,     # Esto es para peliculasyonkis o parecidos
                               "dvdrip1",  "dvdscreener"  ,"tsscreener1", "latino1",
                               "latino2",  "dvdscreener1" ,"screener"    ,
                               "mirror" ,  "megavideo"    ,"vose"        , "subtitulada"
                              )
                                   
    if quita_especiales=="true": titulo = LimpiarTitulo(titulo)
    trozeado = titulo.split()
    for trozo in trozeado:
        if trozo in sopa_palabras_invalidas:
            titulo = titulo.replace(trozo ,"")
    titulo = re.sub(' $','',titulo)
    titulo = titulo.replace("ver pelicula online vos","").strip()
    titulo = titulo.replace("ver pelicula online","").strip()
    titulo = titulo.replace("mirror 1","").strip()
    if quita_parte=="true": titulo = titulo.replace("parte 1","").strip()
    if quita_parte=="true": titulo = titulo.replace("part 1","").strip()
    titulo = titulo.replace("pt 1","").strip()        
    titulo = titulo.replace("peliculas online","").strip()
    return titulo

