# -*- coding: utf-8 -*-
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
    logger.info("[channelselector.py] getmainlist")
    itemlist = []

    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes") )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist") )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist") )
    itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist") )

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
    itemlist.append( Item( title=config.get_localized_string(30133) , channel="channelselector" , action="listchannels" , category="I"   , thumbnail="infantil"))
    itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail="novedades"))
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
        if "xbmc" in config.get_platform() and (channel.type=="xbmc" or channel.type=="generic"):
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel)

        elif config.get_platform()=="boxee" and channel.extra!="rtmp":
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel)

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

def channels_history_list():
    itemlist = []
    itemlist.append( Item( title="ACB TV (17/12/2012)"                     , channel="acbtv"          , language="ES" , category="T" , type="generic"  ))  # jesus 17/12/2012
    itemlist.append( Item( title="Telemadrid (17/12/2012)"                 , channel="telemadrid"     , language="ES" , category="A" , type="generic", extra="rtmp" ))  # jesus 17/12/2012
    itemlist.append( Item( title="EITB (País Vasco) (17/12/2012)"          , channel="eitb"           , language="ES" , category="A" , type="generic", extra="rtmp" )) # jesus 17/12/2012
    itemlist.append( Item( title="RTPA (Asturias) (16/10/2012)"            , channel="rtpa"           , language="ES" , category="A" , type="generic"  ))  # jesus 16/10/2011
    itemlist.append( Item( title="xip/tv (30/07/2012)"                     , channel="xiptv"          , language="ES" , category="L" , type="generic"  ))  # jesus 30/07/2011
    itemlist.append( Item( title="Tvolucion.com (20/06/2012)"              , channel="tvolucion"      , language="ES" , category="N" , type="generic"  ))  # pedro 20/06/2012
    itemlist.append( Item( title="La Sexta (05/04/2012)"                   , channel="lasexta"        , language="ES" , category="N" , type="generic"  ))  # jesus 05/04/2012
    itemlist.append( Item( title="El Trece TV (05/04/2012)"                , channel="eltrece"        , language="ES" , category="N" , type="generic"  ))  # jesus 05/04/2012
    itemlist.append( Item( title="Mitele (05/04/2012)"                     , channel="mitele"         , language="ES" , category="I" , type="generic"  ))  # jesus, truenon, boludiko 05/04/2012
    itemlist.append( Item( title="Cartoonito (05/04/2012)"                 , channel="cartoonito"     , language="ES" , category="I" , type="generic"  ))  # jesus 05/04/2012
    itemlist.append( Item( title="Kideos (05/04/2012)"                     , channel="kideos"         , language="ES" , category="I" , type="generic"  ))  # jesus 05/04/2012
    itemlist.append( Item( title="Cromokids (05/04/2012)"                  , channel="cromokids"      , language="ES" , category="I" , type="generic"  ))  # jesus 05/04/2012
    itemlist.append( Item( title="Disney Channel Replay (05/04/2012)"      , channel="disneychannel"  , language="ES" , category="I" , type="generic"  ))  # jesus 05/04/2012
    itemlist.append( Item( title="Skai Folders (05/04/2012)"               , channel="skai_folders"   , language="ES" , category="I" , type="generic"  ))  # dusan 04/12/2011
    itemlist.append( Item( title="Aragón TV (25/01/2012)"                  , channel="aragontv"       , language="ES" , category="A" , type="generic"  ))  # jesus 25/01/2012
    itemlist.append( Item( title="Telefe (22/01/2012)"                     , channel="telefe"         , language="ES" , category="N" , type="generic"  ))  # jesus 22/01/2012
    itemlist.append( Item( title="UPV TV (29/03/2011)"                     , channel="upvtv"          , language="ES" , category="T" , type="generic"  ))  # beesop 29/03/2011
    itemlist.append( Item( title="Boing (07/02/2011)"                      , channel="boing"          , language="ES" , category="I" , type="generic"  ))  # juanfran 07/02/2011
    itemlist.append( Item( title="IB3 (Islas Baleares) (20/01/2011)"       , channel="ib3"            , language="ES" , category="A" , type="generic"  ))  # jesus 20/01/2010
    itemlist.append( Item( title="Giralda TV (Sevilla) (20/01/2011)"       , channel="giraldatv"      , language="ES" , category="L" , type="generic"  ))  # jesus 20/01/2010
    return itemlist

def channels_list():
    itemlist = []
    itemlist.append( Item( title="7RM (Murcia)"               , channel="sieterm"              , language="ES" , category="A"   , type="generic" ))
    itemlist.append( Item( title="ACB TV"                     , channel="acbtv"                , language="ES" , category="T" , type="generic"  ))  # jesus 17/12/2012
    itemlist.append( Item( title="ADNStream"                  , channel="adnstream"            , language="ES" , category="I,T" , type="generic" ))
    itemlist.append( Item( title="Antena3"                    , channel="antena3"              , language="ES" , category="I,N" , type="generic", extra="rtmp" ))
    itemlist.append( Item( title="Aragón TV"                  , channel="aragontv"             , language="ES" , category="A"   , type="generic", extra="rtmp" ))  # jesus 25/01/2012
    itemlist.append( Item( title="Boing"                      , channel="boing"                , language="ES" , category="I"   , type="generic" ))   # juanfran 07/02/2011
    itemlist.append( Item( title="Cartoonito"                 , channel="cartoonito"           , language="ES" , category="I"   , type="generic" ))
    itemlist.append( Item( title="Clan TVE"                   , channel="clantve"              , language="ES" , category="I"   , type="generic" ))
    itemlist.append( Item( title="Cromokids"                  , channel="cromokids"            , language="ES" , category="I"   , type="generic" ))  # jesus 05/04/2012
    itemlist.append( Item( title="Disney Channel Replay"      , channel="disneychannel"        , language="ES" , category="I"   , type="generic" ))#  jesus 05/04/2012
    itemlist.append( Item( title="EITB (País Vasco)"          , channel="eitb"                 , language="ES" , category="A"   , type="generic", extra="rtmp" ))
    itemlist.append( Item( title="El cine de las 3 mellizas"  , channel="tresmellizas"         , language="ES" , category="I"   , type="generic" ))
    itemlist.append( Item( title="El Trece TV (Argentina)"    , channel="eltrece"              , language="ES" , category="N"   , type="generic" ))
    itemlist.append( Item( title="Euronews"                   , channel="euronews"             , language="ES" , category="T"   , type="generic" ))
    itemlist.append( Item( title="Extremadura TV"             , channel="extremaduratv"        , language="ES" , category="A"   , type="generic", extra="rtmp" ))
    itemlist.append( Item( title="Giralda TV (Sevilla)"       , channel="giraldatv"            , language="ES" , category="L"   , type="generic" ))  # jesus 20/01/2010
    itemlist.append( Item( title="Hogarutil"                  , channel="hogarutil"            , language="ES" , category="T"   , type="generic", extra="background" ))
    itemlist.append( Item( title="IB3 (Islas Baleares)"       , channel="ib3"                  , language="ES" , category="A"   , type="generic" ))  # jesus 20/01/2010
    itemlist.append( Item( title="Internautas TV"             , channel="internautastv"        , language="ES" , category="T"   , type="generic" ))
    itemlist.append( Item( title="Kideos"                     , channel="kideos"               , language="ES" , category="I"   , type="generic" ))
    itemlist.append( Item( title="Mitele"                     , channel="mitele"               , language="ES" , category="I,N" , type="generic" ))
    itemlist.append( Item( title="Publico.tv"                 , channel="publicotv"            , language="ES" , category="T"   , type="generic" ))
    itemlist.append( Item( title="RTPA (Asturias)"            , channel="rtpa"                 , language="ES" , category="A"   , type="generic" ))
    itemlist.append( Item( title="RTVA (Andalucia)"           , channel="rtva"                 , language="ES" , category="A"   , type="generic" ))
    itemlist.append( Item( title="RTVV (Comunidad Valenciana)", channel="rtvv"                 , language="ES" , category="A"   , type="generic" ))
    itemlist.append( Item( title="La Sexta"                   , channel="lasexta"              , language="ES" , category="N"   , type="generic" ))  # juanfran 07/02/2011
    itemlist.append( Item( title="Skai folders"               , channel="skai_folders"         , language="GR" , category="N"   , type="xbmc"   , extra="rtmp" ))  # dusan 04/12/2011
    itemlist.append( Item( title="Telefe (Argentina)"         , channel="telefe"               , language="ES" , category="N"   , type="generic", extra="rtmp" ))  # jesus 28/10/2011
    itemlist.append( Item( title="Telemadrid"                 , channel="telemadrid"           , language="ES" , category="A"   , type="generic", extra="rtmp" ))  # jesus 17/12/2012
    itemlist.append( Item( title="TVE"                        , channel="rtve"                 , language="ES" , category="N"   , type="generic" ))
    itemlist.append( Item( title="Tvolucion.com"              , channel="tvolucion"            , language="ES" , category="N"   , type="generic" ))    
    itemlist.append( Item( title="Turbonick"                  , channel="turbonick"            , language="ES" , category="I"   , type="generic", extra="rtmp" ))
    itemlist.append( Item( title="TV3 (Cataluña)"             , channel="tv3"                  , language="ES" , category="I,A" , type="generic" ))
    itemlist.append( Item( title="TVC (Canarias)"             , channel="rtvc"                 , language="ES" , category="A"   , type="generic" ))
    itemlist.append( Item( title="TVG (Galicia)"              , channel="tvg"                  , language="ES" , category="A"   , type="generic" ))
    itemlist.append( Item( title="UPV TV"                     , channel="upvtv"                , language="ES" , category="T"   , type="generic" ))  # beesop 29/03/2011
    itemlist.append( Item( title="xip/tv"                     , channel="xiptv"                , language="ES" , category="L"   , type="generic" ))  # jesus 30/07/2011

    #itemlist.append( Item( title="Argia Multimedia (Euskera)" , "argia"                , language="ES" , "L" , "generic"  ])
    #itemlist.append( Item( title="Barcelona TV"               , "barcelonatv"          , language="ES" , "L" , "generic" ])
    #itemlist.append( Item( title="Berria TB (Euskera)"        , "berriatb"             , language="ES" , "L" , "generic"  ])
    #itemlist.append( Item( title="Cuatro"                     , "cuatro"               , language="ES" , "N" , "generic" ]) # jesus 02/09/2011
    #itemlist.append( Item( title="EITB (País vasco)"          , "eitb"                 , language="ES" , "A" , "generic"  ])
    #itemlist.append( Item( title="Earth TV"                   , "earthtv"              , language="ES" , "T" , "xbmc"  ])
    #itemlist.append( Item( title="Mallorca TV"                , "tvmallorca"           , language="ES" , "L" , "xbmc"  ])
    #itemlist.append( Item( title="Meristation"                , "meristation"          , language="ES" , "T" , "xbmc"  ])
    #addfolder("Plus TV","plus","mainlist")
    #itemlist.append( Item( title="Solidaria TV"               , "solidariatv"          , language="ES" , "I" , "generic"  ])  # jesus 20/01/2010
    #itemlist.append( Item( title="Telecinco"                  , "telecinco"            , language="ES" , "N" , "generic"  ])  # jesus 15/05/2011
    #addfolder("TV Azteca","tva","mainlist")
    #addfolder("Terra TV","terratv","mainlist")

    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname=""):
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
    #logger.info("thumbnail="+thumbnail)
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
