# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist():
    logger.info("[channelselector.py] getmainlist")
    itemlist = []

    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes" ) )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist") )
    if config.get_platform() in ("wiimc","rss") :itemlist.append( Item(title="Wiideoteca (Beta)" , channel="wiideoteca" , action="mainlist") )
    if config.get_platform()=="rss":itemlist.append( Item(title="pyLOAD (Beta)" , channel="pyload" , action="mainlist") )

    try:
        from core import descargas
        itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist") )
    except:
        logger.error("[channelselector.py] no encuentra core/descargas.py, se deshabilitan las descargas")
    itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist") )
    
    #if config.get_library_support():
    #if config.get_platform()!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist") )
    return itemlist

def mainlist(params,url,category):
    logger.info("[channelselector.py] mainlist")

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
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

    itemlist = getmainlist()
    for elemento in itemlist:
        logger.info("[channelselector.py] item="+elemento.title)
        addfolder(elemento.title,elemento.channel,elemento.action)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def getchanneltypes():
    logger.info("[channelselector.py] getchanneltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail="channelselector"))
    itemlist.append( Item( title=config.get_localized_string(30129) , channel="channelselector" , action="listchannels" , category="N"   , thumbnail="nacionales"))
    itemlist.append( Item( title=config.get_localized_string(30130) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail="autonomicos"))
    itemlist.append( Item( title=config.get_localized_string(30131) , channel="channelselector" , action="listchannels" , category="L"   , thumbnail="locales"))
    itemlist.append( Item( title=config.get_localized_string(30132) , channel="channelselector" , action="listchannels" , category="T"   , thumbnail="tematicos"))
    itemlist.append( Item( title=config.get_localized_string(30133) , channel="channelselector" , action="listchannels" , category="I"   , thumbnail="internet"))
    itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW"   , thumbnail="novedades"))
    return itemlist
    
def channeltypes(params,url,category):
    logger.info("[channelselector.py] channeltypes")

    lista = getchanneltypes()
    for item in lista:
        addfolder(item.title,item.channel,item.action,item.category,item.thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def listchannels(params,url,category):
    logger.info("[channelselector.py] listchannels")

    lista = filterchannels(category)
    for channel in lista:
        if channel.type=="xbmc" or channel.type=="generic":
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def filterchannels(category):
    returnlist = []

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            returnlist.append(channel)
    else:
		idiomav=""
        channelslist = channels_list()
    
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en la categoría elegida
            if category<>"*" and category not in channel.category:
                #logger.info(channel[0]+" no entra por tipo #"+channel[4]+"#, el usuario ha elegido #"+category+"#")
                continue
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel.language<>"" and idiomav<>"" and idiomav not in channel.language:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            returnlist.append(channel)

    return returnlist

def channels_history_list():
    itemlist = []
    itemlist.append( Item( title="Aragón TV (25/01/2012)"               , channel="aragontv"    , language="ES" , category="A" , type="generic"  )) # jesus 25/01/2012
    itemlist.append( Item( title="Telefe (22/01/2012)"                  , channel="telefe"      , language=""   , category="N" , type="generic"  )) # jesus 22/01/2012
    return itemlist

def channels_list():
    itemlist = []

    itemlist.append( Item( title="7RM (Murcia)"               , channel="sieterm"             , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="ADNStream"                  , channel="adnstream"           , language="ES"    , category="I" , type="generic" ))
    itemlist.append( Item( title="Antena3"                    , channel="antena3"             , language=""      , category="N" , type="generic" ))
    itemlist.append( Item( title="Buena Isla"                 , channel="buenaisla"           , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="Aragón TV"                  , channel="aragontv"            , language="ES"    , category="A" , type="generic" )) # jesus 25/01/2012
    itemlist.append( Item( title="Argia Multimedia (Euskera)" , channel="argia"               , language="ES"    , category="L" , type="generic" ))
    itemlist.append( Item( title="Barcelona TV"               , channel="barcelonatv"         , language="ES"    , category="L" , type="generic" ))
    itemlist.append( Item( title="Boing"                      , channel="boing"               , language="ES"    , category="T" , type="generic" ))
    itemlist.append( Item( title="Clan TVE"                   , channel="clantve"             , language="ES"    , category="T" , type="generic" ))
    itemlist.append( Item( title="EITB (País vasco)"          , channel="eitb"                , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="Earth TV"                   , channel="earthtv"             , language="ES"    , category="T" , type="xbmc" ))
    itemlist.append( Item( title="El cine de las 3 mellizas"  , channel="tresmellizas"        , language="ES"    , category="I" , type="generic" ))
    itemlist.append( Item( title="Euronews"                   , channel="euronews"            , language="ES"    , category="T" , type="xbmc" ))
    itemlist.append( Item( title="Extremadura TV"             , channel="extremaduratv"       , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="Giralda TV (Sevilla)"       , channel="giraldatv"           , language="ES"    , category="L" , type="generic" ))
    itemlist.append( Item( title="Hogarutil"                  , channel="hogarutil"           , language="ES"    , category="T" , type="generic" ))
    itemlist.append( Item( title="IB3 (Islas Baleares)"       , channel="ib3"                 , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="Internautas TV"             , channel="internautastv"       , language="ES"    , category="I" , type="xbmc" ))
    itemlist.append( Item( title="Mallorca TV"                , channel="tvmallorca"          , language="ES"    , category="L" , type="xbmc" ))
    itemlist.append( Item( title="Meristation"                , channel="meristation"         , language="ES"    , category="L" , type="xbmc" ))
    itemlist.append( Item( title="Publico.tv"                 , channel="publicotv"           , language="ES"    , category="I" , type="xbmc" ))
    itemlist.append( Item( title="RTVA (Andalucia)"           , channel="rtva"                , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="RTVV (Comunidad Valenciana)", channel="rtvv"                , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="La Sexta"                   , channel="lasexta"             , language="ES"    , category="N" , type="generic" ))
    itemlist.append( Item( title="Skai folders"               , channel="skai_folders"        , language="GR"    , category="N" , type="generic" ))
    itemlist.append( Item( title="Telecinco"                  , channel="telecinco"           , language="ES"    , category="N" , type="generic" ))
    itemlist.append( Item( title="Telefe"                     , channel="telefe"              , language="ES"    , category="N" , type="generic" ))
    itemlist.append( Item( title="TVE"                        , channel="rtve"                , language="ES"    , category="N" , type="generic" ))
    itemlist.append( Item( title="Turbonick"                  , channel="turbonick"           , language="ES"    , category="T" , type="generic" ))
    itemlist.append( Item( title="TV3 (Cataluña)"             , channel="tv3"                 , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="TVG (Galicia)"              , channel="tvg"                 , language="ES"    , category="A" , type="generic" ))
    itemlist.append( Item( title="UPV TV"                     , channel="upvtv"               , language="ES"    , category="T" , type="xbmc" ))
    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname=""):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    
    #print "thumbnail_type="+config.get_setting("thumbnail_type")
    if config.get_setting("thumbnail_type")=="0":
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'posters' ) )
    elif config.get_setting("thumbnail_type")=="1":
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'banners' ) )
    elif config.get_setting("thumbnail_type")=="2":
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'squares' ) )
    
    if config.get_setting("thumbnail_type")=="0":
        WEB_PATH = "http://tvalacarta.mimediacenter.info/posters/"
    else:
        WEB_PATH = "http://tvalacarta.mimediacenter.info/banners/"

    if config.get_platform()=="boxee":
        IMAGES_PATH="http://tvalacarta.mimediacenter.info/posters/"

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
