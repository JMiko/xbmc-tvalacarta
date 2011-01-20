# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import scrapertools
from core import config
from core import logger
try:
    from core import descargadoslist
    DOWNLOAD_ENABLED = True
except:
    DOWNLOAD_ENABLED = False

DEBUG = True
CHANNELNAME = "channelselector"

def mainlist(params,url,category):
    logger.info("[channelselector.py] mainlist")

    # Verifica actualizaciones solo en el primer nivel
    try:
        from core import updater
    except ImportError:
        logger.info("[channelselector.py] No disponible modulo actualizaciones")
    else:
        if config.get_setting("updatecheck2") == "true":
            logger.info("[channelselector.py] Verificar actualizaciones activado")
            updater.checkforupdates()
        else:
            logger.info("[channelselector.py] Verificar actualizaciones desactivado")

    addfolder(config.get_localized_string(30118),"channelselector","channeltypes")
    #addfolder(config.get_localized_string(30103),"buscador"       ,"mainlist")
    addfolder(config.get_localized_string(30102),"favoritos"      ,"mainlist")
    if (DOWNLOAD_ENABLED):
        addfolder(config.get_localized_string(30101),"descargados","mainlist")
    addfolder(config.get_localized_string(30100),"configuracion"  ,"mainlist")
    #addfolder(config.get_localized_string(30104),"ayuda"          ,"mainlist")

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def channeltypes(params,url,category):
    logger.info("[channelselector.py] channeltypes")

    addfolder(config.get_localized_string(30121),"channelselector","listchannels","*")  # Todos
    addfolder(config.get_localized_string(30129),"channelselector","listchannels","N")  # Nacionales
    addfolder(config.get_localized_string(30130),"channelselector","listchannels","A")  # Autonomicos
    addfolder(config.get_localized_string(30131),"channelselector","listchannels","L")  # Locales
    addfolder(config.get_localized_string(30132),"channelselector","listchannels","T")  # Temáticos
    addfolder(config.get_localized_string(30133),"channelselector","listchannels","I")  # Web

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def listchannels(params,url,category):
    logger.info("[channelselector.py] listchannels")

    idiomav=""

    channelslist = channels_list()

    for channel in channelslist:
        # Pasa si no ha elegido "todos" y no está en la categoría elegida
        if category<>"*" and category not in channel[4]:
            #logger.info(channel[0]+" no entra por tipo #"+channel[4]+"#, el usuario ha elegido #"+category+"#")
            continue
        # Pasa si no ha elegido "todos" y no está en el idioma elegido
        if channel[3]<>"" and idiomav<>"" and idiomav not in channel[3]:
            #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
            continue
        addfolder(channel[0] , channel[1] , "mainlist" , channel[2])

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def channels_list():
    channelslist = []
    channelslist.append([ "Antena3"                    , "antena3"              , "" , "ES" , "N" , "generic" ])
    channelslist.append([ "ADNStream"                  , "adnstream"            , "" , "ES" , "I" , "generic" ])
    channelslist.append([ "Barcelona TV"               , "barcelonatv"          , "" , "ES" , "L" , "generic" ])
    channelslist.append([ "Clan TVE"                   , "clantve"              , "" , "ES" , "T" , "generic" ])
    channelslist.append([ "El cine de las 3 mellizas"  , "tresmellizas"         , "" , "ES" , "I" , "generic"  ])
    #addfolder("Boing","boing","mainlist")
    #addfolder("Totlol","totlol","mainlist")
    channelslist.append([ "EITB (País vasco)"          , "eitb"                 , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "Extremadura TV"             , "extremaduratv"        , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "Hogarutil"                  , "hogarutil"            , "" , "ES" , "T" , "generic"  ])
    #addfolder("Plus TV","plus","mainlist")
    channelslist.append([ "RTVA (Andalucia)"           , "rtva"                 , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "TVE"                        , "rtve"                 , "" , "ES" , "N" , "generic"  ])
    channelslist.append([ "TVE Programas"              , "rtveprogramas"        , "" , "ES" , "N" , "generic"  ])
    channelslist.append([ "TVE Mediateca"              , "rtvemediateca"        , "" , "ES" , "N" , "generic"  ])
    #addfolder("TV Azteca","tva","mainlist")
    channelslist.append([ "Berria TB (Euskera)"        , "berriatb"             , "" , "ES" , "L" , "generic"  ])
    channelslist.append([ "Argia Multimedia (Euskera)" , "argia"                , "" , "ES" , "L" , "generic"  ])
    channelslist.append([ "Earth TV"                   , "earthtv"              , "" , "ES" , "T" , "xbmc"  ])
    channelslist.append([ "Euronews"                   , "euronews"             , "" , "ES" , "T" , "xbmc"  ])
    channelslist.append([ "RTVV (Comunidad Valenciana)", "rtvv"                 , "" , "ES" , "A" , "generic"  ])
    #addfolder("Terra TV","terratv","mainlist")
    channelslist.append([ "Turbonick"                  , "turbonick"            , "" , "ES" , "T" , "generic"  ])
    channelslist.append([ "TV3 (Cataluña)"             , "tv3"                  , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "TVG (Galicia)"              , "tvg"                  , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "Mallorca TV"                , "tvmallorca"           , "" , "ES" , "L" , "xbmc"  ])
    channelslist.append([ "Meristation"                , "meristation"          , "" , "ES" , "T" , "xbmc"  ])
    channelslist.append([ "7RM (Murcia)"               , "sieterm"              , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "Internautas TV"             , "internautastv"        , "" , "ES" , "I" , "xbmc"  ])
    channelslist.append([ "Publico.tv"                 , "publicotv"            , "" , "ES" , "I" , "xbmc"  ])
    #channelslist.append([ "La Sexta"                   , "lasexta"              , "" , "ES" , "N" , "generic"  ])
    channelslist.append([ "Solidaria TV"               , "solidariatv"          , "" , "ES" , "I" , "generic"  ])
    channelslist.append([ "Giralda TV (Sevilla)"       , "giraldatv"            , "" , "ES" , "L" , "generic"  ])
    channelslist.append([ "IB3 (Islas Baleares)"       , "ib3"                  , "" , "ES" , "A" , "generic"  ])

    return channelslist

def addfolder(nombre,channelname,accion,category=""):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    if config.get_setting("thumbnail_type")=="0":
        IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' ) )
    else:
        IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'banners' ) )
    
    if config.get_setting("thumbnail_type")=="0":
        WEB_PATH = "http://www.mimediacenter.info/xbmc/tvalacarta/posters/"
    else:
        WEB_PATH = "http://www.mimediacenter.info/xbmc/tvalacarta/banners/"

    # Preferencia: primero JPG
    thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, channelname+".jpg")
    # Preferencia: segundo PNG
    if not os.path.exists(thumbnail):
        thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, channelname+".png")
    # Preferencia: tercero WEB
    if not os.path.exists(thumbnail):
        thumbnail = thumbnailImage=WEB_PATH+channelname+".png"
    #Si no existe se usa el logo del plugin
    #if not os.path.exists(thumbnail):
    #    thumbnail = thumbnailImage=WEB_PATH+"ayuda.png" #Check: ruta del logo

    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
