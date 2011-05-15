# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import scrapertools
from core import config
from core import logger

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist():
    # TODO: (3.1) PMS no acepta arrays, hay que usar itemlists para que los coja el cerealizer
    channelslist = []
    channelslist.append( [ config.get_localized_string(30118) , "channelselector" , "channeltypes" ])
    #channelslist.append( [ config.get_localized_string(30103) , "buscador"       , "mainlist" ])
    channelslist.append( [ config.get_localized_string(30102) , "favoritos"        , "mainlist" ])
    if config.get_setting("download.enabled")=="true":
        channelslist.append( [ config.get_localized_string(30101) , "descargados" , "mainlist" ])
    channelslist.append( [ config.get_localized_string(30100) , "configuracion"   , "mainlist" ])
    #channelslist.append( [ config.get_localized_string(30104) , "ayuda" , "mainlist" ])
    return channelslist

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

    lista = getmainlist()
    for elemento in lista:
        addfolder(elemento[0],elemento[1],elemento[2])

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def getchanneltypes():
    channelslist = []
    channelslist.append( [ config.get_localized_string(30121) , "channelselector" , "listchannels" , "*"   , "channelselector"])
    channelslist.append( [ config.get_localized_string(30129) , "channelselector" , "listchannels" , "N"   , "nacionales"])
    channelslist.append( [ config.get_localized_string(30130) , "channelselector" , "listchannels" , "A"   , "autonomicos"])
    channelslist.append( [ config.get_localized_string(30131) , "channelselector" , "listchannels" , "L"   , "locales"])
    channelslist.append( [ config.get_localized_string(30132) , "channelselector" , "listchannels" , "T"   , "tematicos"])
    channelslist.append( [ config.get_localized_string(30133) , "channelselector" , "listchannels" , "I"   , "internet"])
    channelslist.append( [ config.get_localized_string(30134) , "channelselector" , "listchannels" , "NEW" , "novedades"])
    return channelslist
    
def channeltypes(params,url,category):
    logger.info("[channelselector.py] channeltypes")

    lista = getchanneltypes()
    for elemento in lista:
        addfolder(elemento[0],elemento[1],elemento[2],elemento[3],elemento[4])

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def listchannels(params,url,category):
    logger.info("[channelselector.py] listchannels")

    lista = filterchannels(category)
    for channel in lista:
        addfolder(channel[0] , channel[1] , "mainlist" , channel[2])

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def filterchannels(category):
    returnlist = []

    idiomav=""

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel[3]<>"" and idiomav<>"" and idiomav not in channel[3]:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            returnlist.append(channel)
    else:
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
            returnlist.append(channel)

    return returnlist

def channels_history_list():
    channelslist = []
    channelslist.append([ "Telecinco (15/05/2011)"                  , "telecinco"            , "" , "ES" , "N" , "xbmc"  ])  # beesop 29/03/2011
    channelslist.append([ "UPV TV (29/03/2011)"                     , "upvtv"                , "" , "ES" , "T" , "xbmc"  ])  # beesop 29/03/2011
    channelslist.append([ "La Sexta (07/02/2011)"                   , "lasexta"              , "" , "ES" , "N" , "generic"  ])  # juanfran 07/02/2011
    channelslist.append([ "Boing (07/02/2011)"                      , "boing"                , "" , "ES" , "T" , "generic"  ])  # juanfran 07/02/2011
    channelslist.append([ "IB3 (Islas Baleares) (20/01/2011)"       , "ib3"                  , "" , "ES" , "A" , "generic"  ])  # jesus 20/01/2010
    channelslist.append([ "Giralda TV (Sevilla) (20/01/2011)"       , "giraldatv"            , "" , "ES" , "L" , "generic"  ])  # jesus 20/01/2010
    channelslist.append([ "Solidaria TV (20/01/2011)"               , "solidariatv"          , "" , "ES" , "I" , "generic"  ])  # jesus 20/01/2010
    return channelslist

def channels_list():
    channelslist = []
    channelslist.append([ "7RM (Murcia)"               , "sieterm"              , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "ADNStream"                  , "adnstream"            , "" , "ES" , "I" , "generic" ])
    channelslist.append([ "Antena3"                    , "antena3"              , "" , "ES" , "N" , "generic" ])
    channelslist.append([ "Argia Multimedia (Euskera)" , "argia"                , "" , "ES" , "L" , "generic"  ])
    channelslist.append([ "Barcelona TV"               , "barcelonatv"          , "" , "ES" , "L" , "generic" ])
    channelslist.append([ "Berria TB (Euskera)"        , "berriatb"             , "" , "ES" , "L" , "generic"  ])
    channelslist.append([ "Boing"                      , "boing"                , "" , "ES" , "T" , "generic"  ])   # juanfran 07/02/2011
    channelslist.append([ "Clan TVE"                   , "clantve"              , "" , "ES" , "T" , "generic" ])
    channelslist.append([ "EITB (País vasco)"          , "eitb"                 , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "Earth TV"                   , "earthtv"              , "" , "ES" , "T" , "xbmc"  ])
    channelslist.append([ "El cine de las 3 mellizas"  , "tresmellizas"         , "" , "ES" , "I" , "generic"  ])
    channelslist.append([ "Euronews"                   , "euronews"             , "" , "ES" , "T" , "xbmc"  ])
    channelslist.append([ "Extremadura TV"             , "extremaduratv"        , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "Giralda TV (Sevilla)"       , "giraldatv"            , "" , "ES" , "L" , "generic"  ])  # jesus 20/01/2010
    channelslist.append([ "Hogarutil"                  , "hogarutil"            , "" , "ES" , "T" , "generic"  ])
    channelslist.append([ "IB3 (Islas Baleares)"       , "ib3"                  , "" , "ES" , "A" , "generic"  ])  # jesus 20/01/2010
    channelslist.append([ "Internautas TV"             , "internautastv"        , "" , "ES" , "I" , "xbmc"  ])
    channelslist.append([ "Mallorca TV"                , "tvmallorca"           , "" , "ES" , "L" , "xbmc"  ])
    channelslist.append([ "Meristation"                , "meristation"          , "" , "ES" , "T" , "xbmc"  ])
    #addfolder("Plus TV","plus","mainlist")
    channelslist.append([ "Publico.tv"                 , "publicotv"            , "" , "ES" , "I" , "xbmc"  ])
    channelslist.append([ "RTVA (Andalucia)"           , "rtva"                 , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "RTVV (Comunidad Valenciana)", "rtvv"                 , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "La Sexta"                   , "lasexta"              , "" , "ES" , "N" , "generic"  ])  # juanfran 07/02/2011
    channelslist.append([ "Solidaria TV"               , "solidariatv"          , "" , "ES" , "I" , "generic"  ])  # jesus 20/01/2010
    channelslist.append([ "Telecinco"                  , "telecinco"            , "" , "ES" , "N" , "generic"  ])  # jesus 15/05/2011
    channelslist.append([ "TVE"                        , "rtve"                 , "" , "ES" , "N" , "generic"  ])
    #addfolder("TV Azteca","tva","mainlist")
    #addfolder("Terra TV","terratv","mainlist")
    channelslist.append([ "Turbonick"                  , "turbonick"            , "" , "ES" , "T" , "generic"  ])
    channelslist.append([ "TV3 (Cataluña)"             , "tv3"                  , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "TVG (Galicia)"              , "tvg"                  , "" , "ES" , "A" , "generic"  ])
    channelslist.append([ "UPV TV (29/03/2011)"        , "upvtv"                , "" , "ES" , "T" , "xbmc"  ])  # beesop 29/03/2011

    return channelslist

def addfolder(nombre,channelname,accion,category="",thumbnailname=""):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    
    #print "thumbnail_type="+config.get_setting("thumbnail_type")
    if config.get_setting("thumbnail_type")=="0":
        IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' ) )
    else:
        IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'banners' ) )
    
    if config.get_setting("thumbnail_type")=="0":
        WEB_PATH = "http://www.mimediacenter.info/xbmc/tvalacarta/posters/"
    else:
        WEB_PATH = "http://www.mimediacenter.info/xbmc/tvalacarta/banners/"

    if config.get_platform()=="boxee":
        IMAGES_PATH="http://www.mimediacenter.info/xbmc/tvalacarta/posters/"

    if thumbnailname=="":
        thumbnailname = channelname

    # Preferencia: primero JPG
    thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, thumbnailname+".jpg")
    # Preferencia: segundo PNG
    if not os.path.exists(thumbnail):
        thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, thumbnailname+".png")
    # Preferencia: tercero WEB
    if not os.path.exists(thumbnail):
        thumbnail = thumbnailImage=WEB_PATH+thumbnailname+".png"
    #Si no existe se usa el logo del plugin
    #if not os.path.exists(thumbnail):
    #    thumbnail = thumbnailImage=WEB_PATH+"ayuda.png" #Check: ruta del logo

    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
