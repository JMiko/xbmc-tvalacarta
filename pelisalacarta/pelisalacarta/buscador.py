# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import sys
import xbmc
import xbmcgui
import xbmcplugin

from core import config
from core import logger
from core import xbmctools

CHANNELNAME = "buscador"

logger.info("[buscador.py] init")

DEBUG = True

def mainlist(params,url,category):
    logger.info("[buscador.py] mainlist")

    listar_busquedas(params,url,category)

def searchresults(params,url,category):
    salvar_busquedas(params,url,category)
    tecleado = url
    tecleado = tecleado.replace(" ", "+")
    
    # Lanza las búsquedas
    
    # Cinegratis
    matches = []
    itemlist = []
    try:
        from pelisalacarta.channels import cinetube
        itemlist.extend( cinetube.getsearchresults(params,tecleado,category) )
    except:
        pass
    try:
        from pelisalacarta.channels import cinegratis
        matches.extend( cinegratis.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import peliculasyonkis
        matches.extend( peliculasyonkis.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import tumejortv
        matches.extend( tumejortv.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import cine15
        matches.extend( cine15.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import peliculas21
        matches.extend( peliculas21.performsearch(tecleado) )
    except:
        pass
    #matches.extend( sesionvip.performsearch(tecleado) )
    try:
        from pelisalacarta.channels import seriesyonkis
        matches.extend( seriesyonkis.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import documaniatv
        matches.extend( documaniatv.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import discoverymx
        matches.extend( discoverymx.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import yotix
        matches.extend( yotix.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import stagevusite
        matches.extend( stagevusite.performsearch(tecleado) )
    except:
        pass
    try:
        from pelisalacarta.channels import tutvsite
        matches.extend( tutvsite.performsearch(tecleado) )
    except:
        pass
    
    for item in itemlist:
        targetchannel = item.channel
        action = item.action
        category = category
        scrapedtitle = item.title+" ["+item.channel+"]"
        scrapedurl = item.url
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        
        xbmctools.addnewfolder( targetchannel , action , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
    
    # Construye los resultados
    for match in matches:
        targetchannel = match[0]
        action = match[1]
        category = match[2]
        scrapedtitle = match[3]+" ["+targetchannel+"]"
        scrapedurl = match[4]
        scrapedthumbnail = match[5]
        scrapedplot = match[6]
        
        xbmctools.addnewfolder( targetchannel , action , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_TITLE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def salvar_busquedas(params,url,category):
    channel = params.get("channel")
    limite_busquedas = ( 10, 20, 30, 40, )[ int( config.get_setting( "limite_busquedas" ) ) ]
    matches = []
    try:
        presets = config.get_setting("presets_buscados")
        if "|" in presets:
            presets = matches = presets.split("|")            
            for count, preset in enumerate( presets ):
                if url in preset:
                    del presets[ count ]
                    break
        
        if len( presets ) >= limite_busquedas:
            presets = presets[ : limite_busquedas - 1 ]
    except:
        presets = ""
    presets2 = ""
    if len(matches)>0:
        for preset in presets:
            presets2 = presets2 + "|" + preset 
        presets = url + presets2
    elif presets != "":
        presets = url + "|" + presets
    else:
        presets = url
    config.set_setting("presets_buscados",presets)
    # refresh container so items is changed
    #xbmc.executebuiltin( "Container.Refresh" )
        
def listar_busquedas(params,url,category):
    print "listar_busquedas()"
    channel2 = ""
    # Despliega las busquedas anteriormente guardadas
    try:
        presets = config.get_setting("presets_buscados")
        channel_preset  = params.get("channel")
        if channel_preset != CHANNELNAME:
            channel2 = channel_preset
        print "channel_preset :%s" %channel_preset
        accion = params.get("action")
        matches = ""
        if "|" in presets:
            matches = presets.split("|")
            addfolder( "buscador"   , config.get_localized_string(30103)+"..." , matches[0] , "por_teclado", channel2 ) # Buscar
        else:
            addfolder( "buscador"   , config.get_localized_string(30103)+"..." , "" , "por_teclado", channel2 )
        if len(matches)>0:    
            for match in matches:
                
                title=scrapedurl = match
        
                addfolder( channel_preset , title , scrapedurl , "searchresults" )
        elif presets != "":
        
            title = scrapedurl = presets
            addfolder( channel_preset , title , scrapedurl , "searchresults" )
    except:
        addfolder( "buscador"   , config.get_localized_string(30103)+"..." , "" , "por_teclado" , channel2 )
        
    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def borrar_busqueda(params,url,category):
    channel = params.get("channel")
    matches = []
    try:
        presets = config.get_setting("presets_buscados")
        if "|" in presets:
            presets = matches = presets.split("|")
            for count, preset in enumerate( presets ):
                if url in preset:
                    del presets[ count ]
                    break
        elif presets == url:
            presets = ""
            
    except:
        presets = ""
    if len(matches)>1:
        presets2 = ""
        c = 0
        barra = ""
        for preset in presets:
            if c>0:
                barra = "|"
            presets2 =  presets2 + barra + preset 
            c +=1
        presets = presets2
    elif len(matches) == 1:
        presets = presets[0]
    config.set_setting("presets_buscados",presets)
    # refresh container so item is removed
    xbmc.executebuiltin( "Container.Refresh" )

def teclado(default="", heading="", hidden=False):
    tecleado = ""
    keyboard = xbmc.Keyboard(default)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)<=0:
            return
    
    return tecleado
    
def por_teclado(params,url,category):
    channel2 = params.get("channel2")
    tecleado = teclado(url)
    if len(tecleado)<=0:
        return
    #borrar_busqueda(params,tecleado,category)
    #salvar_busquedas(params,tecleado,category)
    #tecleado = tecleado.replace(" ", "+")
    url = tecleado
    if channel2 == "":
        exec "import "+params.get("channel")+" as plugin"
    else:
        exec "import "+channel2+" as plugin"
    exec "plugin.searchresults(params, url, category)"

def addfolder( canal , nombre , url , accion , channel2 = "" ):
    logger.info('[buscador.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
    itemurl = '%s?channel=%s&action=%s&category=%s&url=%s&channel2=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url),channel2 )
    
    
    if accion != "por_teclado":
        contextCommands = []
        DeleteCommand = "XBMC.RunPlugin(%s?channel=buscador&action=borrar_busqueda&title=%s&url=%s)" % ( sys.argv[ 0 ]  ,  urllib.quote_plus( nombre ) , urllib.quote_plus( url ) )
        contextCommands.append((config.get_localized_string( 30300 ),DeleteCommand))
        listitem.addContextMenuItems ( contextCommands, replaceItems=False)
        
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)
    
    
