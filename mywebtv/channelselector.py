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
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel, thumbnail = thumbnail, folder=channel.folder )


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
    itemlist.append( Item( title="Favoritos"       , channel="favoritos" , type="generic"  ))
    itemlist.append( Item( title="Configuración"   , channel="configuracion" , type="generic", folder=False ))
    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",thumbnail="",folder=True):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
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