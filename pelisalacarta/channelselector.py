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

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("[channelselector.py] idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]
    
    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30118)+" ("+idiomav+")" , channel="channelselector" , action="channeltypes" ) )
    itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist") )
    itemlist.append( Item(title=config.get_localized_string(30128) , channel="trailertools" , action="mainlist") )
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
    if config.get_platform()!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist") )
    return itemlist

# TODO: (3.1) Pasar el código específico de XBMC al laucher
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
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail="peliculas"))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail="series"))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail="anime"))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail="documentales"))
    itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail="musica"))
    itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail="servidores"))
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
        try:
            idioma = config.get_setting("languagefilter")
            logger.info("[channelselector.py] idioma=%s" % idioma)
            langlistv = ["","ES","EN","IT","PT"]
            idiomav = langlistv[int(idioma)]
            logger.info("[channelselector.py] idiomav=%s" % idiomav)
        except:
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
    itemlist.append( Item( title="Series.ly (19/11/2011)"              ,channel="seriesly"              , language="ES" , category="S" , type="generic" )) # jesus/mrfloffy 19/11/2011
    itemlist.append( Item( title="Teledocumentales (19/10/2011)"       ,channel="teledocumentales"      , language="ES" , category="D" , type="generic" )) # mrfloffy 19/10/2011
    itemlist.append( Item( title="Descarrega Directa (CAT) (19/10/2011)",channel="descarregadirecta"    , language="CAT" , category="F,S,D,A" , type="generic" )) # mrfloffy 19/10/2011
    itemlist.append( Item( title="DL-More (FR) (14/10/2011)"           , channel="dlmore"               , language="FR" , category="S"   , type="generic" )) # jesus 14/10/2011
    itemlist.append( Item( title="Megaupload Premium (FR) (14/10/2011)", channel="megauploadpremiumfr"  , language="FR" , category="S"   , type="generic" )) # jesus 14/10/2011
    itemlist.append( Item( title="Peliculasaudiolatino (14/10/2011)"   , channel="peliculasaudiolatino" , language="ES" , category="F"   , type="generic" )) # Dalim 14/10/2011
    itemlist.append( Item( title="Animeflv (14/10/2011)"               , channel="animeflv"             , language="ES" , category="A"   , type="generic" )) # MarioXD 14/10/2011
    itemlist.append( Item( title="Moviezet (01/10/2011)"               , channel="moviezet"             , language="ES" , category="F.S" , type="generic" )) # mrfluffy 01/10/2011
    itemlist.append( Item( title="Asia-Team (20/05/2011)"              , channel="asiateam"             , language="ES" , category="F,S" , type="generic" )) # xextil 20/05/2011
    #itemlist.append( Item( title="Internapoli City (IT) (16/05/2011)"  , channel="internapoli"          , language="IT" , category="F"   , type="generic" )) # jesus 16/05/2011
    itemlist.append( Item( title="Robinfilm (IT) (16/05/2011)"         , channel="robinfilm"            , language="IT" , category="F"   , type="generic" )) # jesus 16/05/2011
    itemlist.append( Item( title="Liberateca (15/05/2011)"             , channel="liberateca"           , language="ES" , category="S"   , type="generic" )) # jesus 15/05/2011
    itemlist.append( Item( title="IslaPelículas (09/05/2011)"          , channel="islapeliculas"        , language="ES" , category="F"   , type="generic" )) # xextil 09/05/2011
    itemlist.append( Item( title="Buena Isla (09/05/2011)"             , channel="buenaisla"            , language="ES" , category="A"   , type="generic" )) # xextil 09/05/2011
    itemlist.append( Item( title="NewHD (05/05/2011)"                  , channel="newhd"                , language="ES" , category="F"   , type="generic" )) # xextil 05/05/2011
    return itemlist

def channels_list():
    itemlist = []

    itemlist.append( Item( title="Animeflv"              , channel="animeflv"             , language="ES"    , category="A"       , type="generic" ))
    #itemlist.append( Item( title="Anime Foros"           , channel="animeforos"           , language="ES"    , category="A"       , type="xbmc"     ))
    itemlist.append( Item( title="Animeid"               , channel="animeid"              , language="ES"    , category="A"       , type="generic"  ))
    itemlist.append( Item( title="Asia-Team"             , channel="asiateam"             , language="ES"    , category="F,S"     , type="generic"  ))
    itemlist.append( Item( title="Biblioteca XBMC"       , channel="libreria"             , language=""      , category="F,S,D,A" , type="wiimc"    ))
    itemlist.append( Item( title="Buena Isla"            , channel="buenaisla"            , language="ES"    , category="A"       , type="generic"  ))
    #temlist.append( Item( title="Capitan Cinema"        , channel="capitancinema"        , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="CastTV"                , channel="casttv"               , language="ES,EN" , category="S"       , type="xbmc"     ))
    itemlist.append( Item( title="Cine-Adicto"           , channel="cineadicto"           , language="ES"    , category="F,D"     , type="generic"  ))
    itemlist.append( Item( title="Cinegratis"            , channel="cinegratis"           , language="ES"    , category="F,S,A,D" , type="generic"  ))
    itemlist.append( Item( title="Cinetube"              , channel="cinetube"             , language="ES"    , category="F,S,A,D" , type="generic"  ))
    itemlist.append( Item( title="Cineblog01 (IT)"       , channel="cineblog01"           , language="IT"    , category="F,S,A"   , type="generic"  ))
    itemlist.append( Item( title="Cuevana"               , channel="cuevana"              , language="ES"    , category="F,S"     , type="generic"  ))
    itemlist.append( Item( title="DeLaTV"                , channel="delatv"               , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Descarga Cine Clásico" , channel="descargacineclasico"  , language="ES"    , category="F,S"     , type="generic"  ))
    itemlist.append( Item( title="Descargapelis"         , channel="descargapelis"        , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Descarrega Directa (CAT)",channel="descarregadirecta"   , language="CAT"   , category="F,S,D,A" , type="generic" ))
    itemlist.append( Item( title="dibujosanimadosgratis" , channel="dibujosanimadosgratis", language="ES"    , category="A"       , type="generic"  ))
    itemlist.append( Item( title="Discoverymx"           , channel="discoverymx"          , language="ES"    , category="D"       , type="generic"  ))
    itemlist.append( Item( title="Divx Online"           , channel="divxonline"           , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="DL-More (FR)"          , channel="dlmore"               , language="FR"    , category="S"       , type="generic"  ))
    itemlist.append( Item( title="DocumaniaTV"           , channel="documaniatv"          , language="ES"    , category="D"       , type="generic"  ))
    itemlist.append( Item( title="Documentalesyonkis"    , channel="documentalesyonkis"   , language="ES"    , category="D"       , type="generic"  ))
    itemlist.append( Item( title="DocumentariesTV"       , channel="documentariestv"      , language="EN"    , category="D"       , type="generic"  ))

    itemlist.append( Item( title="Filmixt"               , channel="filmixt"              , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="FilmesOnlineBr"        , channel="filmesonlinebr"       , language="PT"    , category="F"       , type="xbmc"     ))
    itemlist.append( Item( title="Gratisdocumentales"    , channel="gratisdocumentales"   , language="ES"    , category="D"       , type="generic"  ))
    #itemlist.append( Item( title="Internapoli City (IT)" , channel="internapoli"          , language="IT"    , category="F"       , type="generic"  )) 
    itemlist.append( Item( title="Italia film (IT)"      , channel="italiafilm"           , language="IT"    , category="F,S,A"   , type="xbmc"     ))
    itemlist.append( Item( title="IslaPelículas"         , channel="islapeliculas"        , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="La Guarida de bizzente", channel="documentalesatonline2", language="ES"    , category="D"       , type="generic"  ))
    itemlist.append( Item( title="LetMeWatchThis"        , channel="letmewatchthis"       , language="EN"    , category="F,S"     , type="generic"  ))
    itemlist.append( Item( title="Liberateca"            , channel="liberateca"           , language="ES"    , category="S"       , type="generic"  ))
    itemlist.append( Item( title="MCAnime"               , channel="mcanime"              , language="ES"    , category="A"       , type="xbmc"  ))
    itemlist.append( Item( title="Megavideo"             , channel="megavideosite"        , language=""      , category="G"       , type="generic"  ))
    itemlist.append( Item( title="Megaupload"            , channel="megauploadsite"       , language=""      , category="G"       , type="xbmc"  ))
    itemlist.append( Item( title="Megaupload Premium (FR)", channel="megauploadpremiumfr"  , language="FR"    , category="S"       , type="generic"  ))
    itemlist.append( Item( title="Megalive"              , channel="megalivewall"         , language=""      , category="G"       , type="xbmc"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="MocosoftX"             , channel="mocosoftx"            , language="ES" , category="F" , type="generic"  ))
    itemlist.append( Item( title="Moviezet"              , channel="moviezet"             , language="ES"    , category="F.S"     , type="generic" )) # mrfluffy 01/10/2011
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="myhentaitube"         , channel="myhentaitube"         , language="ES" , category="F" , type="generic"  ))
    itemlist.append( Item( title="NewDivx"               , channel="newdivx"              , language="ES"    , category="F,D"     , type="xbmc"  ))
    itemlist.append( Item( title="NewHD"                 , channel="newhd"                , language="ES"    , category="F"       , type="generic" )) # xextil 05/05/2011
    #itemlist.append( Item( title="NKI"                   , channel="nki"                  , language="ES"    , category="S"       , type="generic" ))
    #itemlist.append( Item( title="No Megavideo"          , channel="nomegavideo"          , language="ES"    , category="F"       , type="xbmc"  ))
    itemlist.append( Item( title="NoloMires"             , channel="nolomires"            , language="ES"    , category="F"       , type="xbmc"  ))
    itemlist.append( Item( title="Peliculas Online FLV"  , channel="peliculasonlineflv"   , language="ES"    , category="F,D"     , type="xbmc"  ))
    itemlist.append( Item( title="Peliculas21"           , channel="peliculas21"          , language="ES"    , category="F"       , type="xbmc"  ))
    itemlist.append( Item( title="Peliculasaudiolatino"  , channel="peliculasaudiolatino" , language="ES"    , category="F"       , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PeliculasEroticas"     , channel="peliculaseroticas"    , language="ES" , category="F" , type="xbmc"  ))
    itemlist.append( Item( title="PeliculasFLV"          , channel="peliculasflv"         , language="ES"    , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Peliculasid"           , channel="peliculasid"          , language="ES"    , category="F"       , type="xbmc"  ))
    itemlist.append( Item( title="Peliculasyonkis"       , channel="peliculasyonkis_generico" , language="ES"    , category="F"   , type="generic" ))
    itemlist.append( Item( title="Pelis Pekes"           , channel="pelispekes"           , language="ES" , category="F,A"        , type="xbmc"  ))
    itemlist.append( Item( title="Pelis24"               , channel="pelis24"              , language="ES" , category="F,S"        , type="xbmc"  ))
    itemlist.append( Item( title="PelisFlv"              , channel="pelisflv"             , language="ES" , category="F"          , type="xbmc"  ))
    itemlist.append( Item( title="Redes.tv"              , channel="redestv"              , language="ES" , category="D"          , type="xbmc"  ))
    itemlist.append( Item( title="Robinfilm (IT)"        , channel="robinfilm"            , language="IT" , category="F"          , type="generic"  )) # jesus 16/05/2011
    #itemlist.append( Item( title="Seriematic"            , channel="seriematic"           , language="ES" , category="S,D,A"      , type="generic"  ))
    itemlist.append( Item( title="Serieonline"           , channel="serieonline"          , language="ES" , category="F,S,D"      , type="generic"  ))
    itemlist.append( Item( title="Series.ly"             , channel="seriesly"             , language="ES" , category="S,A"        , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Series Hentai"         , channel="serieshentai"         , language="ES" , category="F" , type="generic"  )) # kira 10/04/2011
    itemlist.append( Item( title="Series21"              , channel="series21"             , language="ES" , category="S"          , type="xbmc"  ))
    itemlist.append( Item( title="Seriesdanko"           , channel="seriesdanko"          , language="ES" , category="S"          , type="generic" ))
    itemlist.append( Item( title="Seriespepito"          , channel="seriespepito"         , language="ES" , category="S"          , type="generic" ))
    itemlist.append( Item( title="Seriesyonkis"          , channel="seriesyonkis"         , language="ES" , category="S,A"        , type="generic" , extra="Series" ))
    itemlist.append( Item( title="Sofacine"              , channel="sofacine"             , language="ES" , category="F"          , type="generic"  ))
    itemlist.append( Item( title="Somosmovies"           , channel="somosmovies"          , language="ES" , category="F,S,D,A"    , type="generic"  ))
    itemlist.append( Item( title="Sonolatino"            , channel="sonolatino"           , language=""   , category="M"          , type="xbmc"  ))
    itemlist.append( Item( title="Stagevu"               , channel="stagevusite"          , language=""   , category="G"          , type="xbmc"  ))
    itemlist.append( Item( title="Teledocumentales"      , channel="teledocumentales"     , language="ES" , category="D"          , type="generic" )) # mrfloffy 19/10/2011
    itemlist.append( Item( title="Terror y Gore"         , channel="terrorygore"          , language="ES,EN" , category="F"       , type="xbmc"  ))
    itemlist.append( Item( title="Trailers ecartelera"   , channel="ecarteleratrailers"   , language="ES,EN" , category="F"       , type="xbmc"  ))
    itemlist.append( Item( title="tu.tv"                 , channel="tutvsite"             , language="ES" , category="G"          , type="generic" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="tubehentai"        , channel="tubehentai" , language="ES" , category="F" , type="xbmc"  ))
    itemlist.append( Item( title="tumejortv.com"         , channel="tumejortv"            , language="ES" , category="F,S"        , type="generic" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="tuporno.tv"        , channel="tupornotv" , language="ES" , category="F" , type="generic"  ))
    #itemlist.append( Item( title="TVShack"               , channel="tvshack"              , language="EN" , category="F,S,A,D,M"  , type="xbmc"  ))
    itemlist.append( Item( title="Vagos"                 , channel="vagos"                , language="ES" , category="F,S" , type="xbmc"  ))
    itemlist.append( Item( title="Veocine"               , channel="veocine"              , language="ES" , category="F,A,D" , type="xbmc"  ))
    itemlist.append( Item( title="Ver Telenovelas Online", channel="vertelenovelasonline" , language="ES" , category="S" , type="xbmc"  ))
    itemlist.append( Item( title="Ver-anime"             , channel="veranime"             , language="ES" , category="A" , type="generic"  ))
    itemlist.append( Item( title="Watchanimeon"          , channel="watchanimeon"         , language="EN" , category="A" , type="xbmc"  ))
    itemlist.append( Item( title="Yotix.tv"              , channel="yotix"                , language="ES" , category="A" , type="generic" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="xhamster"          , channel="xhamster"             , language="ES" , category="F" , type="generic"  ))

    #itemlist.append( Item( title="Dospuntocerovision"    , channel="dospuntocerovision"   , language="ES" , category="F,S" , type="xbmc"  ))
    #itemlist.append( Item( title="Pintadibujos"          , channel="pintadibujos"         , language="ES" , category="F,A" , type="xbmc"  ))
    #itemlist.append( Item( title="Film Streaming"        , "filmstreaming"        , language="IT" , "F,A" , type="xbmc"  ))
    #itemlist.append( Item( title="Pelis-Sevillista56"    , "sevillista"           , language="ES" , "F" , type="xbmc"))
    #itemlist.append( Item( title="SoloSeries"            , "soloseries"           , language="ES" , "S" , type="xbmc"  ))
    #itemlist.append( Item( title="seriesonline.us"       , "seriesonline"         , language="ES" , "S" , type="xbmc" ))
    #itemlist.append( Item( title="Animetakus"            , channel="animetakus"           , language="ES" , category="A" , type="generic" ))
    #itemlist.append( Item( title="Documentalesatonline"  , channel="documentalesatonline" , language="ES" , category="D" , type="xbmc"  ))
    #itemlist.append( Item( title="Programas TV Online"   , channel="programastv"          , language="ES" , category="D" , type="xbmc"  ))
    #itemlist.append( Item( title="Futbol Virtual"        , "futbolvirtual"        , language="ES" , "D" , type="xbmc"  ))
    #channelslist.append([ "Eduman Movies" , "edumanmovies" , "" , "ES" , "F" ])
    #channelslist.append([ "SesionVIP" , "sesionvip" , "" , "ES" , "F" ])
    #channelslist.append([ "Newcineonline" , "newcineonline" , "" , "ES" , "S" ])
    #channelslist.append([ "PeliculasHD" , "peliculashd" , "" , "ES" , "F" ])
    #channelslist.append([ "Wuapi" , "wuapisite" , "" , "ES" , "F" ])
    #channelslist.append([ "Frozen Layer" , "frozenlayer" , "" , "ES" , "A" ])
    #channelslist.append([ "Ovasid"                , "ovasid"               , "" , "ES" , "A" , "xbmc"  ])
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
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_data_path(), 'resources' , 'images' , 'posters' ) )
    else:
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_data_path(), 'resources' , 'images' , 'banners' ) )
    
    if config.get_setting("thumbnail_type")=="0":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/posters/"
    else:
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/banners/"

    if config.get_platform()=="boxee":
        IMAGES_PATH="http://pelisalacarta.mimediacenter.info/posters/"

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
