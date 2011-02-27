# -*- coding: utf-8 -*-

from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

import re,urlparse

from core.item import Item
cerealizer.register(Item)

#----------------------------------------------------------------------------------------------------------------
VIDEO_PREFIX = "/video/pelisalacarta"
NAME = L('Title')
ART           = 'art-default.jpg'
ICON          = 'icon-default.png'
#----------------------------------------------------------------------------------------------------------------

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, mainlist, L('VideoTitle'), ICON, ART)    
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("MediaPreview", viewMode="MediaPreview", mediaType="items")
    Plugin.AddViewGroup("Showcase", viewMode="Showcase", mediaType="items")
    #Plugin.AddViewGroup("CoverFlow", viewMode="CoverFlow", mediaType="items")
    Plugin.AddViewGroup("PanelStream", viewMode="PanelStream", mediaType="items")
    Plugin.AddViewGroup("WallStream", viewMode="WallStream", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def CreatePrefs():
    Prefs.Add(id="updatecheck2"      , type='bool', default = 'true' , label='Verificar actualizaciones')
    #Prefs.Add(id="updatechannels"    , type="boolean" label="30004" default="true"/>
    Prefs.Add(id="enableadultmode"   , type="bool", default = 'false' , label = 'Modo adulto')
    Prefs.Add(id="debug"             , type="bool", default = 'true' , label = 'Usar log completo')
    #Prefs.Add(id="default_action"    , type="enum" lvalues="30006|30007|30008|30009" label="30005" default="0"/>
    #Prefs.Add(id="thumbnail_type"    , type="enum" lvalues="30011|30012" label="30010" default="0"/>
    #Prefs.Add(id="languagefilter"    , type="enum" lvalues="30025|30026|30027|30028|30029" values="0|1|2|3|4" label="30019" default="0"/>
    
    Prefs.Add(id="megavideopremium"  , type="bool", default='', label='Usar Megavideo premium')
    Prefs.Add(id="megavideouser"     , type="text", default='', label="Usuario Megavideo")
    Prefs.Add(id="megavideopassword" , type="text", default='', label="Contraseña Megavideo")
    Prefs.Add(id="privateuser"     , type="text", default='', label="Usuario páginas privadas")
    Prefs.Add(id="privatepassword" , type="text", default='', label="Contraseña páginas privadas")

    #Prefs.Add(id="downloadpath"      , type="text" source="video" option="writeable" label="30017" default=""/>
    #Prefs.Add(id="downloadlistpath"  , type="text" source="video" option="writeable" label="30018" default=""/>
    #Prefs.Add(id="bookmarkpath"      , type="text" label="30030" default=""/>
    #Prefs.Add(id="quality_youtube"    , type="enum" values="Low|Medium (3gp)|240p (FLV)|360P (FLV)|360p (MP4)|480p (FLV)|720p (HD)|1080p (HD)|Menu", label="Calidad para YouTube" default="3")
    #Prefs.Add(id="subtitulo"         , type="boolean" label="30021" default="false"/>    
    #Prefs.Add(id="jdownloader"       , type="text" label="30022" default="http://127.0.0.1:10025"/>
    #Prefs.Add(id="limite_busquedas"  , type="enum" values="10|20|30|40" label="30024" default="0"/>

def mainlist():
    Log("[__init__.py] channelselector")

    from core import config
    
    dir = MediaContainer(viewGroup="InfoList")

    import channelselector
    canales = channelselector.getmainlist()

    Log(canales)

    for canal in canales:
        if canal.channel=="configuracion":
            dir.Append(PrefsItem(title="Configuración", thumb=R('images/posters/'+canal.channel+'.png')))
        else:
            dir.Append( Function( DirectoryItem( runchannel, title = canal.title, subtitle = "", thumb = R('images/posters/'+canal.channel+'.png'), art=R(ART) ) , channel=canal.channel , action = canal.action ))

    return dir

def runchannel(sender,channel,action="mainlist",category=""):
    Log("[__init__.py] runchannel")

    Log("channel="+channel)
    Log("action="+action)

    dir = MediaContainer(viewGroup="InfoList")
    
    # Importa el canal y obtiene los items
    try:
        exec "from pelisalacarta.channels import "+channel
    except:
        try:
            exec "from core import "+channel
        except:
            exec "import "+channel
        
    if channel!="channelselector":
        exec "itemlist = "+channel+"."+action+"(None)"
    elif action=="channeltypes":
        itemlist = channelselector.getchanneltypes()
    elif action=="listchannels":
        itemlist = channelselector.filterchannels(category)

    Log("itemlist %d items" % len(itemlist))

    for item in itemlist:    
        Log("item="+item.tostring()+" channel=["+item.channel+"]")

        if item.category=="F":
            category = "Películas"
        elif item.category=="S":
            category = "Series"
        elif item.category=="D":
            category = "Documentales"
        elif item.category=="A":
            category = "Anime"
        elif item.category=="M":
            category = "Música"
        elif item.category=="G":
            category = "Servidores"
        elif item.category=="NEW":
            category = "Los nuevos"
        else:
            category=""
        #Log("category=%s" % category)
        
        thumbnail = 'images/posters/'+item.channel+'.png'
        #Log("thumbnail=%s" % thumbnail)

        # Opciones de menú
        if item.channel=="channelselector":
            dir.Append( Function( DirectoryItem( runchannel, title = item.title, subtitle = "", thumb = R(thumbnail), art=R(ART) ) , channel=item.channel , action = item.action , category = item.category ))
        # Los canales
        else:
            if item.type=="generic":
                dir.Append( Function( DirectoryItem( actionexecute, title = item.title, subtitle = category, thumb = R(thumbnail) ) , item = item ) )

    return dir

def actionexecute(sender,item):
    from core import logger
    Log("[__init__.py] actionexecute")

    Log(item.tostring())
    dir = MediaContainer(viewGroup="InfoList")
    
    if item.action=="":
        item.action="mainlist"
    Log("[__init__.py] action="+item.action)
    
    exec "from pelisalacarta.channels import "+item.channel
    
    if item.action!="findvideos":
        exec "itemlist = "+item.channel+"."+item.action+"(item)"
    else:
        try:
            exec "itemlist = "+item.channel+"."+item.action+"(item)"
        except:
            itemlist = findvideos(item)
            
    for item in itemlist:
        item.title = encodingsafe(item.title)
        item.plot = encodingsafe(item.plot)
        logger.info("item="+item.tostring())

        if item.folder:
            dir.Append( Function( DirectoryItem( actionexecute, title = item.title, subtitle = "subtitle", thumb = item.thumbnail ) , item = item ))
        else:
            dir.Append( Function( DirectoryItem( playvideo , title=item.title, subtitle="", summary=item.plot, thumb = item.thumbnail), item = item ))
    
    return dir

def findvideos(item):
    Log("[__init__.py] findvideos")

    url = item.url
    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot

    # ------------------------------------------------------------------------------------
    # Descarga la pagina
    # ------------------------------------------------------------------------------------
    from core import scrapertools
    data = scrapertools.cachePage(url)
    
    from servers import servertools
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = video[0]
        scrapedurl = video[1]
        server = video[2]

        itemlist.append( Item(channel=item.channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist

def playvideo(sender,item):
    Log("[__init__.py] playvideo")

    dir = MediaContainer(viewGroup="InfoList")

    if item.action=="play":
        try:
            exec "from pelisalacarta.channels import "+item.channel
            exec "itemlist = "+item.channel+"."+item.action+"(item)"
            item = itemlist[0]
            item.title = encodingsafe(item.title)
            item.plot = encodingsafe(item.plot)
        except:
            pass
        

    from core import config

    if item.server.lower() == "megavideo":
        if config.get_setting("megavideopremium")=="true":
            dir.Append(Function( VideoItem(playvideohigh,   title="Ver en calidad alta (Megavideo)", subtitle="", summary=item.plot, thumb = item.thumbnail), item = item ))
        dir.Append(Function( VideoItem(playvideonormal, title="Ver en calidad baja (Megavideo)", subtitle="", summary=item.plot, thumb = item.thumbnail), item = item ))
    elif item.server.lower() == "megaupload":
        if config.get_setting("megavideopremium")=="true":
            dir.Append(Function( VideoItem(playvideohigh,   title="Ver en calidad alta (Megaupload)", subtitle="", summary=item.plot, thumb = item.thumbnail), item = item ))
        dir.Append(Function( VideoItem(playvideonormal, title="Ver en calidad baja (Megavideo)", subtitle="", summary=item.plot, thumb = item.thumbnail), item = item ))
    elif item.server.lower()=="youtube":
        from servers import servertools
        url = servertools.findurl(item.url,item.server)
        for item in url:
            Log("item="+item.tostring())
            dir.Append(Function( VideoItem(playvideonormal, title=item.title, url=item.url, server="directo"), item = item ))
    else:
        dir.Append(Function( VideoItem(playvideonormal, title="Ver el vídeo ("+item.server+")", subtitle="", summary=item.plot, thumb = item.thumbnail), item = item ))
    
    return dir

def playvideonormal(sender,item):
    Log("[__init__.py] playvideonormal")
    Log("url="+item.url)

    if item.server.lower() == "directo":
        url = item.url
    elif item.server.lower() == "megavideo":
        from servers import servertools
        url = servertools.getmegavideolow(item.url)
    elif item.server.lower() == "megaupload":
        from server import servertools
        url = servertools.getmegauploadlow(item.url)
    else:
        from servers import servertools
        url = servertools.findurl(item.url,item.server)

    Log("url="+url)
    return Redirect(url)

def playvideohigh(sender,item):
    Log("[__init__.py] playvideohigh")
    Log("url="+item.url)

    if item.server.lower() == "directo":
        url = item.url
    elif item.server.lower() == "megavideo":
        from servers import servertools
        url = servertools.getmegavideohigh(item.url)
    elif item.server.lower() == "megaupload":
        from server import servertools
        url = servertools.getmegauploadhigh(item.url)
    else:
        from servers import servertools
        url = servertools.findurl(item.url,item.server)

    Log("url="+url)
    return Redirect(url)

def encodingsafe(text):
    from core import logger
    try:
        # Si es utf-8 esto funciona, si no fallará
        text = unicode( text , "utf-8" )
    except:
        try:
            # Si no es utf-8 puede ser iso-8859-1
            text = unicode( text , "iso-8859-1" )
        except:
            # Si no, probablemente será ya unicode
            pass

    text = text.encode("utf-8")

    return text