# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item
from os import listdir
from os.path import isfile, join

DEBUG = config.get_setting("debug")
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
        returnlist = channels_history_list()
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
    itemlist = getChannels()
    itemlist = sorted(itemlist, key=lambda item: item.extra, reverse=True)
    return itemlist[0:14]

def channels_list():
    itemlist = getChannels()
    
    return sorted(itemlist, key=lambda item: item.title)

def getChannels():

    TITLE = re.compile(r'__title__.*=.*["\'](.*?)["\']')
    CHANNEL = re.compile(r'__channel__.*=.*["\'](.*?)["\']')
    LANGUAGE = re.compile(r'__language__.*=.*["\'](.*?)["\']')
    CATEGORY = re.compile(r'__category__.*=.*["\'](.*?)["\']')
    TYPE = re.compile(r'__type__.*=.*["\'](.*?)["\']')
    WORKING = re.compile(r'__working__.*=.*["\'](.*?)["\']')
    ADULT = re.compile(r'__adult__.*=.*["\'](.*?)["\']')
    CREATIONDATE = re.compile(r'__creationdate__.*=.*["\'](.*?)["\']')
    
    pfolder = join("pelisalacarta", "channels")
    logger.info("[channelselector.py] pfolder" + pfolder)

    itemlist = []
    for f in listdir(pfolder):
        if (isfile(join(pfolder, f)) and f.endswith(".py")) and not f.startswith("_"):
            logger.debug("[channelselector.py] parseando " + f)
            data = open(join(pfolder, f))
            content = data.read()
            data.close()
            title = TITLE.findall(content)
            channel = CHANNEL.findall(content)
            language = LANGUAGE.findall(content)
            category = CATEGORY.findall(content)
            type = TYPE.findall(content)
            working = WORKING.findall(content)
            adult = ADULT.findall(content)
            creationdate = CREATIONDATE.findall(content)
            
            if adult:
                adult=(adult[0].upper()=="TRUE")
            else:
                adult= False
             
            if working:
                working =(working[0].upper()=="TRUE")
            else:
                working = True
             
            if creationdate:
                creationdate=int(creationdate[0])
            else:
                creationdate= 0
                
            if channel and (working or DEBUG) and (not adult or config.get_setting("enableadultmode")):
                logger.debug("append")
                logger.debug("title" + title[0])
                logger.debug("channel " + channel[0])
                logger.debug("language " + language[0])
                logger.debug("category " + category[0])
                logger.debug("type " + type[0])
                logger.debug("creationdate " + str(creationdate))
                
                itemlist.append( Item( title=title[0], channel=channel[0], language=language[0], category=category[0], type=type[0], extra=str(creationdate)))

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
    else:
        IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'banners' ) )
    
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
