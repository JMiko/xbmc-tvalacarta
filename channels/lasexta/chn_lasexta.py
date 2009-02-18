#===============================================================================
# Import the default modules
#===============================================================================
from types import *
import xbmc, xbmcgui
import re, sys, os
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import config
import controls
import contextmenu
import chn_class

logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

#===============================================================================
# register the channels
#===============================================================================
if (sys.modules.has_key('progwindow')):
    register = sys.modules['progwindow']
elif (sys.modules.has_key('plugin')):
    register = sys.modules['plugin']
#register.channelButtonRegister.append(108)

register.channelRegister.append('chn_lasexta.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="lasexta")')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """
    
    #===============================================================================
    def InitialiseVariables(self):
        """
        Used for the initialisation of user defined parameters. All should be 
        present, but can be adjusted
        """
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        #self.guid = "3ac3d6d0-5b2a-11dd-ae16-0800200c9a66"
        self.icon = "lasexta-icon.png"
        self.iconLarge = "lasexta-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "LaSexta"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "misexta.tv"
        self.moduleName = "chn_lasexta.py"
        self.mainListUri = "http://www.misexta.tv/feed_misextatv2"
        self.baseUrl = "http://www.antena3videos.com/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        
        #self.episodeItemRegex = '<li><a href="(/guide/season/[^"]+)">(\d+)</a></li>' # used for the ParseMainList
        #self.episodeItemRegex = '<a href="(/tvcarta/impe/web/contenido?id=[^"]+)" title="([^"])+">([^<]+)</a>'
        #self.episodeItemRegex = '<a href="(/tvcarta/impe/web/contenido\?id=[^"]+)" title="([^"]+)">'
        #
        #<div class="infoPrograma">
        #<h3 class="h3TituloProgramaCarta">
        #<a href="/tvcarta/impe/web/contenido?id=3643" title=" ARRAYAN">ARRAYAN</a>
        #</h3>
        #<p>Programa 21 Diciembre 2008</p><p>Serie de ficci&oacute;n</p>
        #</div>
        #<div class="enlacePrograma"><a href="/tvcarta/impe/web/contenido?id=3643" title=" "><img class="imgLista" src="http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8/ARRAYAN_21DIC.00.00.00.00.png" alt="" title=""></a></div><div class="pie_bloq"></div></div>
        self.episodeItemRegex = '<item id="(\d+)">\W+<title>([^<]+)</title>\W+<num_videos>([^<]+)</num_videos>\W+<guid[^<]*>([^<]+)</guid>' #\W+<picture>([^<]+)</picture>'
        #<embed width="393" height="344" align="middle" flashvars="&amp;video=http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8/CAMINOS HIERRO_20OCT.flv" src="/tvcarta/html/nav/com/css/cssimg/video2.swf" quality="high" bgcolor="#016a32" menu="false" name="video" allowscriptaccess="always" allowfullscreen="true" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/>
        #self.videoItemRegex = '<item id="(\d+)">\W+<title>([^<]+)</title>\W+<num_videos>([^<]+)</num_videos>\W+<description><!\[CDATA\[([^>]+)></description>\W+<guid[^<]*>([^<]+)</guid>\W+<show><!\[CDATA\[([^<]+)</show>\W+<section_id>([^<]+)</section_id>\W+<section><!\[CDATA\[([^<]+)</section>\W+<id>([^<]+)</id>\W+<picture>([^<]+)</picture>\W+<picture_small>([^<]+)</picture_small>\W+<links>\W+<link publi="true">[^<]+</link>\W+<link>([^<]+)</link>'
        self.videoItemRegex = '<item id="(\d+)">\W+<title>([^<]+)</title>\W+<num_videos>([^<]+)</num_videos>\W+<description><!\[CDATA\[([^>]+)></description>\W+<guid[^<]*>([^<]+)</guid>\W+<show><!\[CDATA\[([^<]+)</show>\W+<section_id>([^<]+)</section_id>\W+<section><!\[CDATA\[([^<]+)</section>\W+<id>([^<]+)</id>\W+<picture>([^<]+)</picture>\W+<picture_small>([^<]+)</picture_small>\W*(<links>\W+(?:<link(?: publi="true")?>[^<]+</link>\W*)*</links>)\W+(<linksHD>\W+(?:<linkHD(?: publi="true")?>[^<]+</linkHD>\W*)*</linksHD>)'
        self.folderItemRegex = '<item id="(\d+)">\W+<title>([^<]+)</title>\W+<num_videos>([^<]+)</num_videos>\W+<guid[^<]*>([^<]+)</guid>\W+<section_id>([^<]+)</section_id>\W+<id>([^<]+)</id>\W+(<picture>([^<]+)</picture>)?\W+(<picture_small>([^<]+)</picture_small>)?'
        #self.mediaUrlRegex = '<param name="src" value="([^"]+)" />'    # used for the UpdateVideoItem
        self.mediaUrlRegex = '<location>([^<]+)</location>'    # used for the UpdateVideoItem
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnUpdateItem(self, selectedIndex):
        logFile.debug('Updating item (Called from ContextMenu)')
        self.onUpDown(ignoreDisabled = True)
    
    def CtMnDownloadItem(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.listItems[selectedIndex] = self.DownloadEpisode(item)

    def CtMnPlayMplayer(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item, "mplayer")
    
    def CtMnPlayDVDPlayer(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item,"dvdplayer")    
    
    #============================================================================== 
    def DownloadEpisode(self, item):
        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            if item.mediaurl.endswith(".mp4"):
                destFilename = item.name + ".mp4"
            else:
                destFilename = item.name + ".flv"
            if item.mediaurl=="":
                logFile.error("Cannot determine mediaurl")
                return item
            logFile.info("Going to download %s", destFilename)
            downLoader = uriHandler.Download(item.mediaurl, destFilename)
            item.downloaded = True
            return item
        else:
            logFile.warning('Error determining folder/video type of selected item');

    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[1] + " (" + resultSet[2] + " videos)"
        titulo = unicode( titulo, "utf-8" ).encode("iso-8859-1")
        # <li><a href="(/guide/season/[^"]+)">(\d+)</a></li>
        #item = common.clistItem( resultSet[1] , urlparse.urljoin(self.baseUrl, resultSet[0]))
        
        # Lee rss de seccion de http://www.misexta.tv/feed_misextatv3/3_182361
        # Saca numero videos (33) y seccion (1121)
        # Lee lista de videos de /feed_misextatv5/3_182361/video/33/1121/0
        
        item = common.clistItem( titulo , "http://www.misexta.tv/feed_misextatv3/" + resultSet[3] )
        #item = common.clistItem( resultSet[1] , resultSet[1])
        item.icon = self.folderIcon
        item.complete = True
        return item
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        titulo = resultSet[1] + " (" + resultSet[2] + " videos)"
        titulo = unicode( titulo, "utf-8" ).encode("iso-8859-1")
        item = common.clistItem(titulo,"http://www.misexta.tv/feed_misextatv5/" + resultSet[3] + "/video/" + resultSet[2] + "/" + resultSet[4] + "/0")
        item.description = item.name
        item.icon = self.folderIcon
        item.type = 'folder'
        item.thumb = self.noImage
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)

        # Título del vídeo
        titulolistado = ""
        try:
            titulolistado = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulolistado = ""
        logFile.debug("titulo="+titulolistado)
        
        # Descripcion del video
        descripcionlistado = ""
        try:
            descripcionlistado = unicode( resultSet[3], "utf-8" ).encode("iso-8859-1")
        except:
            descripcionlistado = resultSet[3]
        logFile.debug("descripcion="+descripcionlistado)
        
        # XML con las partes
        xmlpartes = resultSet[11]
        logFile.debug("xmlpartes="+xmlpartes)

        # Lista de partes
        listapartes = common.DoRegexFindAll( "<link>([^<]*)</link>" , xmlpartes )
        logFile.debug("***")
        logFile.debug(listapartes)

        listaitems = []
        contador = 0;
        
        for parte in listapartes:
            logFile.debug("parte="+parte)
            contador = contador + 1
            if len(listapartes)>1:
                item = common.clistItem( titulolistado + " " + str(contador), resultSet[11] )
            else:
                item = common.clistItem( titulolistado , resultSet[11] )
            item.thumbUrl = resultSet[9]
            item.thumb = self.noImage
            item.date = "01/01/2009"
            item.icon = "newmovie.png"
            if len(listapartes)>1:
                item.description = descripcionlistado + "(Parte " + str(contador) + ")"
            else:
                item.description = descripcionlistado
            item.type = 'video'
            item.complete = False
            item.mediaurl = parte
            if item.mediaurl.startswith("rtmp"):
                item.mediaurl = item.mediaurl.replace("rtmp://","http://")
                item.mediaurl = item.mediaurl.replace("{","%7B")
                item.mediaurl = item.mediaurl.replace("}","%7D")
                item.mediaurl = item.mediaurl.replace("fl.interoute.com","dnl.interoute.com")
                item.mediaurl = item.mediaurl.replace("/streamrt/","/")
            logFile.debug("mediaurl="+item.mediaurl)
            
            listaitems.append(item)

        # XML con las partes HD
        xmlpartes = resultSet[12]
        logFile.debug("xmlpartes="+xmlpartes)

        # Lista de partes HD
        listapartes = common.DoRegexFindAll( "<linkHD>([^<]*)</linkHD>" , xmlpartes )
        logFile.debug("***")
        logFile.debug(listapartes)

        contador = 0;
        
        for parte in listapartes:
            logFile.debug("parte="+parte)
            contador = contador + 1
            item = common.clistItem( "HD " + titulolistado + " " + str(contador), resultSet[11] )
            item.thumbUrl = resultSet[9]
            item.thumb = self.noImage
            item.date = "01/01/2009"
            item.icon = "newmovie.png"
            item.description = "HD " + descripcionlistado + "(Parte " + str(contador) + ")"
            item.type = 'video'
            item.complete = False
            item.mediaurl = parte
            if item.mediaurl.startswith("rtmp"):
                item.mediaurl = item.mediaurl.replace("rtmp://","http://")
                item.mediaurl = item.mediaurl.replace("{","%7B")
                item.mediaurl = item.mediaurl.replace("}","%7D")
                item.mediaurl = item.mediaurl.replace("fl.interoute.com","dnl.interoute.com")
                item.mediaurl = item.mediaurl.replace("/streamrt/","/")
            logFile.debug("mediaurl="+item.mediaurl)
            
            listaitems.append(item)

        return listaitems
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl)
        item.complete = True
        return item