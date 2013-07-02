# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def mainlist():
    logger.info("[channelselector.py] getmainlist")
    itemlist = []

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
        try:
            from core import updater
        except ImportError:
            logger.info("[channelselector.py] No disponible modulo actualizaciones")
        else:
            if config.get_setting("updatecheck2") == "true":
                logger.info("[channelselector.py] Verificar actualizaciones activado")
                try:
                    updater.checkforupdates()
                except:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    dialog.ok("No se puede conectar","No ha sido posible comprobar","si hay actualizaciones")
                    logger.info("[channelselector.py] Fallo al verificar la actualización")
                    pass
            else:
                logger.info("[channelselector.py] Verificar actualizaciones desactivado")

    lista = channels_list()
    for channel in lista:
        if channel.type=="xbmc" or channel.type=="generic":
            thumbnail=urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel, thumbnail = thumbnail, url = channel.url , folder=channel.folder )


    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def channels_list():
    itemlist = []

    itemlist.append( Item( title="Verificados"     , channel="verificados" , type="generic"  ))
    itemlist.append( Item( title="Community Links" , channel="community_links" , type="generic"  ))
    itemlist.append( Item( title="Delicast"        , channel="delicast" , type="generic"  ))
    itemlist.append( Item( title="Justin.tv"       , channel="justintv" , type="generic"  ))
    itemlist.append( Item( title="SimpleTV"        , channel="simpletv" , type="generic"  ))
    itemlist.append( Item( title="Tivion"          , channel="tivion" , type="generic"  ))
    itemlist.append( Item( title="TVenLinux"       , channel="tvenlinux" , type="generic"  ))
    itemlist.append( Item( title="TVOnlineApp.com" , channel="tvonlineapp" , type="generic"  ))
    itemlist.append( Item( title="Android One"     , channel="android1" , type="generic"  ))
    if config.get_setting("xmlchannel1")=="true":
        itemlist.append( Item( title=config.get_setting("xmltitle1"), channel="xmlchannel", url=config.get_setting("xmllocation1"), thumbnail=config.get_setting("xmllogo1"), type="generic"))
    if config.get_setting("xmlchannel2")=="true":
        itemlist.append( Item( title=config.get_setting("xmltitle2"), channel="xmlchannel", url=config.get_setting("xmllocation2"), thumbnail=config.get_setting("xmllogo2"), type="generic"))
    if config.get_setting("xmlchannel3")=="true":
        itemlist.append( Item( title=config.get_setting("xmltitle3"), channel="xmlchannel", url=config.get_setting("xmllocation3"), thumbnail=config.get_setting("xmllogo3"), type="generic"))
    if config.get_setting("m3uchannel1")=="true":
        itemlist.append( Item( title=config.get_setting("m3utitle1"), channel="m3uchannel", url=config.get_setting("m3ulocation1"), thumbnail=config.get_setting("m3ulogo1"), type="generic"))
    if config.get_setting("m3uchannel2")=="true":
        itemlist.append( Item( title=config.get_setting("m3utitle2"), channel="m3uchannel", url=config.get_setting("m3ulocation2"), thumbnail=config.get_setting("m3ulogo2"), type="generic"))
    if config.get_setting("m3uchannel3")=="true":
        itemlist.append( Item( title=config.get_setting("m3utitle3"), channel="m3uchannel", url=config.get_setting("m3ulocation3"), thumbnail=config.get_setting("m3ulogo3"), type="generic"))

    itemlist.append( Item( title="Favoritos"       , channel="favoritos" , type="generic"  ))
    itemlist.append( Item( title="Configuración"   , channel="configuracion" , type="generic", folder=False ))
    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",thumbnail="",url="",folder=True):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&url=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , urllib.quote_plus( url ), category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=folder)

def get_thumbnail_path():

    WEB_PATH = ""
    
    thumbnail_type = config.get_setting("thumbnail_type")
    if thumbnail_type=="":
        thumbnail_type="2"
    
    if thumbnail_type=="0":
        WEB_PATH = "http://mywebtv.mimediacenter.info/posters/"
    elif thumbnail_type=="1":
        WEB_PATH = "http://mywebtv.mimediacenter.info/banners/"
    elif thumbnail_type=="2":
        WEB_PATH = "http://mywebtv.mimediacenter.info/squares/"

    return WEB_PATH