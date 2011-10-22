# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import sys

from core import config
from core import logger
from core.item import Item

CHANNELNAME = "buscador"

logger.info("[buscador.py] init")

DEBUG = True

def mainlist(params,url="",category=""):
    logger.info("[buscador.py] mainlist")

    global CHANNELNAME
    CHANNELNAME = params.url.split("/")[0]

 
    categoria = "30121"
    titulo = "..."
    return resultado(categoria, titulo)

def resultado(categoria, titulo):

    titulo_cat = config.get_localized_string(30402)+": "+config.get_localized_string(int(categoria))
    titulo_tit = config.get_localized_string(30140)+": "+titulo 
    buscar = config.get_localized_string(30169)
    salir = config.get_localized_string(30167)
    pulse_ok = config.get_localized_string(30165)
    url = categoria
    extra = titulo
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=titulo_cat , action="busca_cat" , url=url , extra=extra, fulltitle=pulse_ok ))
    itemlist.append( Item(channel=CHANNELNAME, title=titulo_tit , action="search" , url=url , extra=extra, fulltitle=pulse_ok  ))
    itemlist.append( Item(channel=CHANNELNAME, title=buscar , action="buscar" , url=url, extra=extra) )
    itemlist.append( Item(channel="", title=salir , action="EXIT") )
    return itemlist

# Cambia la categoria
def busca_cat(item):
    
    CHANNELNAME = item.channel
    item.url = urllib.unquote_plus(item.url)
    categoria = item.url
    titulo = item.extra
    
    if categoria=="30121": categoria="30122"   # Todos -> Películas
    elif categoria=="30122": categoria="30123" # Peliculas -> Series
    elif categoria=="30123": categoria="30125" # Series -> Documentales
    else: categoria="30121"
    return resultado(categoria, titulo)

# Cambia el titulo a buscar
def search(item,titulo):
    
    print item.tostring()
    CHANNELNAME = item.channel
    item.url = urllib.unquote_plus(item.url)
    categoria = item.url
    return resultado(categoria, titulo)

# Realiza la busqueda
def buscar(item):
    logger.info("[buscador.py] buscar")
    CHANNELNAME = item.channel
    categoria = item.url
    titulo = item.extra
    texto = titulo
    item.url = "" # Para que los canales sepan que es una busqueda generica
    if categoria=="30121": category="*"   # Todos
    elif categoria=="30122": category="F" # Peliculas
    elif categoria=="30123": category="S" # Series
    else: category="D"                    # Documentales

    matches = []
    itemlist = []
    try:
        from pelisalacarta.channels import seriesyonkis
        item.channel="seriesyonkis"
        item.fulltitle = "seriesyonkis"
        itemlist.extend( seriesyonkis.search(item,texto,category) )
    except:
        logger.info("[buscador.py] ERROR en seriesyonkis")

    try:
        from pelisalacarta.channels import peliculasyonkis_generico
        item.channel="peliculasyonkis_generico"
        item.fulltitle = "peliculasyonkis"
        itemlist.extend( peliculasyonkis_generico.search(item,texto,category) )
    except:
        logger.info("[buscador.py] ERROR en peliculasyonkis_generico")

    try:
        from pelisalacarta.channels import cuevana
        item.channel="cuevana"
        item.fulltitle = "cuevana"
        itemlist.extend( cuevana.search(item,texto,category) )
    except:
        logger.info("[buscador.py] ERROR en cuevana")

    try:
        from pelisalacarta.channels import cinetube
        item.channel="cinetube"
        item.fulltitle = "cinetube"
        itemlist.extend( cinetube.search(item,texto,category) )
    except:
        logger.info("[buscador.py] ERROR en cinetube")

    try:
        from pelisalacarta.channels import cinegratis
        item.channel="cinegratis"
        item.fulltitle = "cinegratis"
        itemlist.extend( cinegratis.search(item,texto,category) )
    except:
        logger.info("[buscador.py] ERROR en cinegratis")

    try:
        from pelisalacarta.channels import tumejortv
        item.channel="tumejortv"
        item.fulltitle = "tumejortv"
        itemlist.extend( tumejortv.search(item,texto,category) )
    except:
        logger.info("[buscador.py] ERROR en tumejortv")

    resultado = []

    # Dejo solo los que contenga <texto> dentro del título
    from core.downloadtools import limpia_nombre_excepto_1 as limpia_nombre
    for item in itemlist:
        buscado = limpia_nombre(texto).lower()
        titulo = limpia_nombre(item.title).lower()
        if buscado in titulo: 
            resultado.append(item)
    
    return resultado

'''

def searchresults(params,url,category):
    logger.info("[buscador.py] searchresults")
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
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


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
    logger.info("[buscador.py] teclado")
    tecleado = ""
    keyboard = xbmc.Keyboard(default)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)<=0:
            return
    
    return tecleado
    
def por_teclado(params,url,category):
    logger.info("[buscador.py] por_teclado")
    channel2 = params.get("channel2")
    tecleado = teclado(url)
    if len(tecleado)<=0:
        return
    #borrar_busqueda(params,tecleado,category)
    #salvar_busquedas(params,tecleado,category)
    #tecleado = tecleado.replace(" ", "+")
    url = tecleado
    if params.get("channel") == "buscador":
        exec "import pelisalacarta.buscador as plugin"
    elif channel2 == "":
        exec "import pelisalacarta.channels."+params.get("channel")+" as plugin"
    else:
        exec "import pelisalacarta.channels."+channel2+" as plugin"
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
        
    xbmcplugin.addDirectoryItem( handle = int( sys.argv[ 1 ] ), url = itemurl , listitem=listitem, isFolder=True)
'''    
