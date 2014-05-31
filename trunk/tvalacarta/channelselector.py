﻿# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import scrapertools
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist():
    logger.info("channelselector.getmainlist")
    itemlist = []

    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes", thumbnail="channels.png") )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist", thumbnail="favorites.png") )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail="downloads.png") )

    if "xbmceden" in config.get_platform():
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail="settings.png", folder=False) )
    else:
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail="settings.png") )

    return itemlist

def mainlist(params,url,category):
    logger.info("channelselector.mainlist")

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
        try:
            from core import updater
        except ImportError:
            logger.info("channelselector.mainlist No disponible modulo actualizaciones")
        else:
            if config.get_setting("updatecheck2") == "true":
                logger.info("channelselector.mainlist Verificar actualizaciones activado")
                updater.checkforupdates()
            else:
                logger.info("channelselector.mainlist Verificar actualizaciones desactivado")

    itemlist = getmainlist()
    for elemento in itemlist:
        logger.info("channelselector item="+elemento.title)
        addfolder(elemento.title , elemento.channel , elemento.action , thumbnailname=elemento.thumbnail, folder=elemento.folder)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def getchanneltypes():
    logger.info("channelselector.getchanneltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail="channels.png"))
    itemlist.append( Item( title=config.get_localized_string(30129) , channel="channelselector" , action="listchannels" , category="N"   , thumbnail="channels-national.png"))
    itemlist.append( Item( title=config.get_localized_string(30130) , channel="channelselector" , action="listchannels" , category="R"   , thumbnail="channels-regional.png"))
    itemlist.append( Item( title=config.get_localized_string(30132) , channel="channelselector" , action="listchannels" , category="T"   , thumbnail="channels-thematic.png"))
    itemlist.append( Item( title=config.get_localized_string(30133) , channel="channelselector" , action="listchannels" , category="I"   , thumbnail="channels-children.png"))
    #itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail="novedades"))
    return itemlist

def channeltypes(params,url,category):
    logger.info("channelselector.channeltypes")

    lista = getchanneltypes()
    for item in lista:
        addfolder(item.title,item.channel,item.action,category=item.category,thumbnailname=item.thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def listchannels(params,url,category):
    logger.info("channelselector.listchannels")

    lista = filterchannels(category)
    for channel in lista:
        if "xbmc" in config.get_platform() and (channel.type=="xbmc" or channel.type=="generic"):
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel)

        elif config.get_platform()=="boxee" and channel.extra!="rtmp":
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def filterchannels(category):
    returnlist = []

    idiomav=""

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel.language<>"" and idiomav<>"" and idiomav not in channel.language:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            returnlist.append(channel)
    else:
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

def channels_list():
    itemlist = []
    itemlist.append( Item( title="7RM (Murcia)"               , channel="sieterm"              , language="ES" , category="R"   , type="generic" ))
    itemlist.append( Item( title="ACB TV"                     , channel="acbtv"                , language="ES" , category="T"   , type="generic" )) # jesus 17/12/2012
    itemlist.append( Item( title="ADNStream"                  , channel="adnstream"            , language="ES" , category="I,T" , type="generic" ))
    itemlist.append( Item( title="AtresPlayer"                , channel="a3media"              , language="ES" , category="N"   , type="generic" ))
    #itemlist.append( Item( title="Antena3"                    , channel="antena3"              , language="ES" , category="I,N" , type="generic", extra="rtmp" ))
    itemlist.append( Item( title="Aragón TV"                  , channel="aragontv"             , language="ES" , category="R"   , type="generic", extra="rtmp" ))  # jesus 25/01/2012
    itemlist.append( Item( title="Boing"                      , channel="boing"                , language="ES" , category="I"   , type="generic" )) # juanfran 07/02/2011
    itemlist.append( Item( title="Cadena Tres (México)"       , channel="cadenatres"           , language="ES" , category="N"   , type="generic" )) # rsantaella 22/03/2013
    #itemlist.append( Item( title="Cartoonito"                 , channel="cartoonito"           , language="ES" , category="I"   , type="generic" )) # jesus 05/04/2012
    itemlist.append( Item( title="CCTV Español (China)"       , channel="cctvspan"             , language="ES" , category="N"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="Clan TVE"                   , channel="clantve"              , language="ES" , category="I"   , type="generic" ))
    itemlist.append( Item( title="Conectate (Argentina)"      , channel="conectate"            , language="ES" , category="N"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="Contenidos Digitales Abiertos (Argentina)", channel="cda"    , language="ES" , category="N"   , type="generic" )) # Juan Pablo 01/02/2013
    itemlist.append( Item( title="Crackle"                    , channel="crackle"              , language="ES" , category="T,I" , type="generic" )) # rsantaella 05/04/2013
    itemlist.append( Item( title="CYLTV (Castilla y León)"    , channel="cyltv"                , language="ES" , category="R"   , type="generic" )) # jesus 01/01/2013
    itemlist.append( Item( title="Dibujos.tv"                 , channel="dibujostv"            , language="ES" , category="I"   , type="generic" )) # jesus 04/08/2013
    itemlist.append( Item( title="Disney Channel Replay"      , channel="disneychannel"        , language="ES" , category="I"   , type="generic" )) # jesus 05/04/2012
    itemlist.append( Item( title="Disney Junior"              , channel="disneyjunior"         , language="ES" , category="I"   , type="generic" )) # jesus 15/01/2013
    itemlist.append( Item( title="Disney Latino"              , channel="disneylatino"         , language="ES" , category="I"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="DW Español (Alemania)"      , channel="dwspan"               , language="ES" , category="N"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="EITB (País Vasco)"          , channel="eitb"                 , language="ES" , category="R"   , type="generic", extra="rtmp" )) # jesus 17/12/2012
    itemlist.append( Item( title="El Trece TV (Argentina)"    , channel="eltrece"              , language="ES" , category="N"   , type="generic" )) # jesus 05/04/2012
    itemlist.append( Item( title="elgourmet.com"              , channel="elgourmet"            , language="ES" , category="R"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="Euronews"                   , channel="euronews"             , language="ES" , category="T"   , type="generic" ))
    itemlist.append( Item( title="Extremadura TV"             , channel="extremaduratv"        , language="ES" , category="R"   , type="generic", extra="rtmp" ))
    itemlist.append( Item( title="Fútbol para todos (Argentina)", channel="fpt"                , language="ES" , category="N"   , type="generic" ))
    itemlist.append( Item( title="Giralda TV (Sevilla)"       , channel="giraldatv"            , language="ES" , category="R"   , type="generic" )) # jesus 20/01/2010
    itemlist.append( Item( title="HispanTV (Iran)"            , channel="hispantv"             , language="ES" , category="N"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="Hogarutil"                  , channel="hogarutil"            , language="ES" , category="T"   , type="generic", extra="background" ))
    itemlist.append( Item( title="IB3 (Islas Baleares)"       , channel="ib3"                  , language="ES" , category="R"   , type="generic" )) # jesus 20/01/2010
    itemlist.append( Item( title="Internautas TV"             , channel="internautastv"        , language="ES" , category="T"   , type="generic" ))
    itemlist.append( Item( title="Kideos"                     , channel="kideos"               , language="ES" , category="I"   , type="generic" )) # jesus 05/04/2012
    itemlist.append( Item( title="Mitele"                     , channel="mitele"               , language="ES" , category="N"   , type="generic" )) # jesus, truenon, boludiko 05/04/2012
    itemlist.append( Item( title="MTV"                        , channel="mtv"                  , language="ES" , category="T"   , type="generic" )) # jesus 04/08/2013
    itemlist.append( Item( title="MuchMusic Latinoamérica"    , channel="muchla"               , language="ES" , category="T"   , type="generic" )) # Juan Pablo 11/02/2013
    itemlist.append( Item( title="Mundo Nick"                 , channel="mundonick"            , language="ES" , category="I"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="Once TV (Mexico)"           , channel="oncetvmex"            , language="ES" , category="N"   , type="generic" )) # rsantaella 22/03/2013
    itemlist.append( Item( title="RT Español (Rusia)"         , channel="rtspan"               , language="ES" , category="N"   , type="generic" )) # richard 29/01/2013
    itemlist.append( Item( title="RTVCM (Castilla La Mancha)" , channel="rtvcm"                , language="ES" , category="R"   , type="generic" ))  # jesus 01/01/2013
    itemlist.append( Item( title="RTPA (Asturias)"            , channel="rtpa"                 , language="ES" , category="R"   , type="generic" )) # jesus 16/10/2011
    itemlist.append( Item( title="RTVA (Andalucia)"           , channel="rtva"                 , language="ES" , category="R"   , type="generic" ))
    #itemlist.append( Item( title="RTVV (Comunidad Valenciana)", channel="rtvv"                 , language="ES" , category="R"   , type="generic" ))
    #itemlist.append( Item( title="La Sexta"                   , channel="lasexta"              , language="ES" , category="N"   , type="generic" )) # juanfran 07/02/2011, jesus 05/04/2012
    #itemlist.append( Item( title="Skai folders"               , channel="skai_folders"         , language="GR" , category="N"   , type="xbmc"   , extra="rtmp" ))  # dusan 04/12/2011
    itemlist.append( Item( title="TAL (Televisión de América Latina)", channel="tal"           , language="ES" , category="N"   , type="generic" )) # rsantaella 22/03/2013
    itemlist.append( Item( title="TEC TV (Argentina)"         , channel="tectv"                , language="ES" , category="N"   , type="generic" )) # rsantaella 07/06/2013
    itemlist.append( Item( title="Telefe (Argentina)"         , channel="telefe"               , language="ES" , category="N"   , type="generic" )) # jesus 22/01/2012
    itemlist.append( Item( title="Telemadrid"                 , channel="telemadrid"           , language="ES" , category="R"   , type="generic", extra="rtmp" ))  # jesus 17/12/2012
    itemlist.append( Item( title="Telemundo"                  , channel="telemundo"            , language="ES" , category="N"   , type="generic" )) # rsantaella 30/03/2013
    itemlist.append( Item( title="TNU (Uruguay)"              , channel="tnu"                  , language="ES" , category="N"   , type="generic" )) # jesus 04/08/2013
    itemlist.append( Item( title="Tuteve (Perú)"              , channel="tuteve"               , language="ES" , category="N"   , type="generic" )) # jesus 04/08/2013
    itemlist.append( Item( title="TV Pública (Argentina)"     , channel="tvpublica"            , language="ES" , category="N"   , type="generic" )) # rsantaella 07/06/2013
    itemlist.append( Item( title="TVE"                        , channel="rtve"                 , language="ES" , category="N"   , type="generic" ))
    itemlist.append( Item( title="Tvolucion.com"              , channel="tvolucion"            , language="ES" , category="N"   , type="generic" )) # pedro 20/06/2012 
    itemlist.append( Item( title="TV3 (Cataluña)"             , channel="tv3"                  , language="ES" , category="I,A" , type="generic" ))
    itemlist.append( Item( title="TVC (Canarias)"             , channel="rtvc"                 , language="ES" , category="R"   , type="generic" ))
    itemlist.append( Item( title="TVG (Galicia)"              , channel="tvg"                  , language="ES" , category="R"   , type="generic" ))
    itemlist.append( Item( title="TVNPlayer (Chile)"                , channel="tvn"                  , language="ES" , category="N"   , type="generic" )) # jesus 04/08/2013
    itemlist.append( Item( title="UPV TV"                     , channel="upvtv"                , language="ES" , category="T"   , type="generic" )) # beesop 29/03/2011
    itemlist.append( Item( title="xip/tv"                     , channel="xiptv"                , language="ES" , category="R"   , type="generic" )) # jesus 30/07/2011

    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",folder=True):
    #print "addfolder"
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc

    if config.get_setting("thumbnail_type")=="0":
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'posters' ) )
    elif config.get_setting("thumbnail_type")=="1":
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'banners' ) )
    elif config.get_setting("thumbnail_type")=="2":
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'squares' ) )
    
    if config.get_setting("thumbnail_type")=="0":
        WEB_PATH = "http://tvalacarta.mimediacenter.info/posters/"
    elif config.get_setting("thumbnail_type")=="1":
        WEB_PATH = "http://tvalacarta.mimediacenter.info/banners/"
    elif config.get_setting("thumbnail_type")=="2":
        WEB_PATH = "http://tvalacarta.mimediacenter.info/squares/"

    if config.get_platform()=="boxee":
        IMAGES_PATH="http://tvalacarta.mimediacenter.info/posters/"

    if thumbnailname=="":
        thumbnailname = channelname

    thumbnail = os.path.join(IMAGES_PATH, "menu", thumbnailname)
    #logger.info("thumbnail="+thumbnail)
    if not os.path.exists(thumbnail):
        # Preferencia: primero JPG
        thumbnail = os.path.join(IMAGES_PATH, thumbnailname+".jpg")
    # Preferencia: segundo PNG
    if not os.path.exists(thumbnail):
        thumbnail = os.path.join(IMAGES_PATH, thumbnailname+".png")
    # Preferencia: tercero WEB
    if not os.path.exists(thumbnail):
        thumbnail = WEB_PATH+thumbnailname+".png"

    import xbmcgui
    import xbmcplugin
    #logger.info("thumbnail="+thumbnail)
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=folder)
