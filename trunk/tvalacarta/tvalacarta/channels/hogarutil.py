# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para hogarutil
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

try:
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

logger.info("[hogarutil.py] init")

DEBUG = True
CHANNELNAME = "hogarutil"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[hogarutil.py] channel")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Cocina"     , action="videococinalist"    , url="http://www.hogarutil.com/Cocina/Recetas+en+v%C3%ADdeo", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Bricolaje"  , action="videobricolajelist" , url="http://www.hogarutil.com/Bricomania/Tareas+en+v%C3%ADdeo", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Decoración" , action="videobricolajelist" , url="http://www.hogarutil.com/Decogarden/Trabajos+en+v%C3%ADdeo", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Jardineria" , action="videobricolajelist" , url="http://www.hogarutil.com/Jardineria/Trabajos+en+v%C3%ADdeo", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar"     , action="search"             , folder=True) )

    return itemlist

def search(item):
    logger.info("[hogarutil.py] search")

    itemlist = []

    import xbmc
    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            itemlist = searchresults(tecleado)
    
    return itemlist

def searchresults(term):
    logger.info("[hogarutil.py] searchresults")

    itemlist = []

    #convert to HTML
    tecleado = term.replace(" ", "+")
    url = "http://www.hogarutil.com/fwk_googleminitools/GoogleServlet?tipoBusqueda=cabecera&cadenaABuscar="+urllib.quote_plus("vídeo "+tecleado)+"&siteDondeBuscar=&urlBuscador=http%3A%2F%2Fwww.hogarutil.com%2Fportal%2Fsite%2FPortalUtil%2Fmenuitem.c4c49aecb2a32733c4a69810843000a0"
    logger.info("url="+url)

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<li><font size="-2"><b></b></font> <a href="http://www.hogarutil.com/Jardineria/Trabajos+en+v%C3%ADdeo/Palmera+de+Roebelen?q=palmera&start=0&urlBuscador=http://www.hogarutil.com/portal/site/PortalUtil/menuitem.c4c49aecb2a32733c4a69810843000a0&site=Delivery"><span>Palmera de Roebelen</span></a>
    patronvideos  = '<li[^>]+><font size="-2"><b></b></font> <a href="([^\?]+)\?[^"]+"><span>([^<]+)</span></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
        if scrapedurl.find("Trabajos+en+v%C3%ADdeo")!=-1 or scrapedurl.find("Recetas+en+v%C3%ADdeo")!=-1:
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, folder=True) )

    return itemlist


def videococinalist(item):
    logger.info("[hogarutil.py] videolist")
    
    itemlist = []

    if not item.extra == "":
        baseurl = item.extra
    else:
        baseurl = item.url
    logger.info("[hogarutil.py] baseurl="+baseurl)

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    patronvideos = '<li.*?><span[^>]+><img.*?src="/staticFiles/logo-hogarutil-video.gif"[^>]+>([^<]+)</span><a title="([^"]+)" href="([^"]+)">[^<]+</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[1]+" ("+match[0]+")"
        try:
            scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
        except:
            pass

        scrapedurl = urlparse.urljoin("http://www.hogarutil.com",urllib.quote(match[2]))
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , server="directo" , folder=False) )

    # Extrae el enlace a la página siguiente
    patronvideos = '<span.*?class="pagActual">[^<]+</span><a.*?href="([^"]+)".*?>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Ir a página "+match[1]
        scrapedurl = baseurl+match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videococinalist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra=baseurl) )

    return itemlist

def videobricolajelist(item):
    logger.info("[hogarutil.py] videolist")

    itemlist = []
    if not item.extra == "":
        baseurl = item.extra
    else:
        baseurl = item.url
    logger.info("[hogarutil.py] baseurl="+baseurl)

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae las entradas (carpetas)
    patronvideos = '<li.*?><span.*?><img src="/staticFiles/logo-hogarutil-video.gif"/></span><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        try:
            scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
        except:
            pass
        scrapedurl = urlparse.urljoin("http://www.hogarutil.com",urllib.quote(match[0]))
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , server="directo" , folder=False) )

    # Extrae el enlace a la página siguiente
    patronvideos = '<span.*?class="pagActual">[^<]+</span><a.*?href="([^"]+)".*?>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Ir a página "+match[1]
        scrapedurl = baseurl+match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videobricolajelist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra=baseurl) )

    return itemlist

def play(item):
    logger.info("[hogarutil.py] play")

    itemlist = []

    logger.info("url="+item.url)

    # Averigua la descripcion (plot)
    data = scrapertools.cachePage(item.url)
    patronvideos = '<meta name="BNT_RECETA_DESC" content="([^"]+)" />'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        infoplot = matches[0]
    except:
        infoplot = ""
    logger.info("[hogarutil.py] infoplot="+infoplot)

    # Averigua el thumbnail
    patronvideos = '<img class="fotoreceta" alt="[^"]*" src="([^"]+)"/>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        infothumbnail = scrapedurl = urlparse.urljoin("http://www.hogarutil.com",urllib.quote(matches[0]))
    except:
        infothumbnail = ""
    logger.info("[hogarutil.py] infothumbnail="+infothumbnail)

    # Averigua la URL del video
    patronvideos = '\&urlVideo=([^\&]+)\&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        mediaurl = matches[0]
    except:
        mediaurl = ""
    logger.info("[hogarutil.py] mediaurl="+mediaurl)

    '''
    listitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
    listitem.setInfo( "video", { "Title": infotitle, "Plot" : infoplot , "Studio" : CHANNELNAME , "Genre" : category } )
    playlist.add( mediaurl, listitem )
    '''
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=mediaurl, thumbnail=infothumbnail , plot=infoplot , server = "directo" , folder=False) )
    return itemlist

def directplay(item):

    # Playlist vacia
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()

    # Crea la entrada y la añade al playlist
    listitem = xbmcgui.ListItem( "Emision en directo", iconImage="DefaultVideo.png" )
    listitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
    listitem.setInfo( "video", { "Title": "Emision en directo", "Studio" : CHANNELNAME , "Genre" : category } )
    playlist.add( url, listitem )

    # Reproduce
    xbmcPlayer = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
    xbmcPlayer.play(playlist)   

def addfolder(nombre,url,accion):
    logger.info('[hogarutil.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
    itemurl = '%s?channel=hogarutil&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addpagina(nombre,url,baseurl,accion):
    logger.info('[hogarutil.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
    itemurl = '%s?channel=hogarutil&action=%s&category=%s&url=%s&baseurl=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url)  , urllib.quote_plus(baseurl) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category):
    logger.info('[hogarutil.py] addvideo( "'+nombre+'" , "' + url + '" , "'+category+'")"')
    listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
    listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
    itemurl = '%s?channel=hogarutil&action=play&category=%s&url=%s' % ( sys.argv[ 0 ] , category , urllib.quote_plus(url) )
    xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addvideodirecto(nombre,url,category):
    logger.info('[hogarutil.py] addvideodirecto( "'+nombre+'" , "' + url + '" , "'+category+'")"')
    listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
    listitem.setInfo( "video", { "Title" : nombre, "Plot" : "Emision en directo" } )
    itemurl = '%s?channel=hogarutil&action=directplay&category=%s&url=%s' % ( sys.argv[ 0 ] , category , urllib.quote_plus(url) )
    xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
    logger.info('[hogarutil.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
    listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
    itemurl = '%s?channel=hogarutil&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

#mainlist(None,"","mainlist")
#videolist(None,"http://www.hogarutil.com/Cocina/Recetas+en+vídeo","Cocina")
#play(None,"http://www.hogarutil.com/Cocina/Recetas+en+v%C3%ADdeo/Sepia+con+arroz+negro","")
