#===============================================================================
# Import the default modules
#===============================================================================
import xbmc, xbmcgui
import re, sys, os
import urlparse, urllib, urllib2
#===============================================================================
# Make global object available
#===============================================================================
import common
import config
import controls
import contextmenu
import chn_class
import megavideo

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

register.channelRegister.append('chn_seriesonline.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="seriesonline")')


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
        self.icon = "seriesonline-icon.png"
        self.iconLarge = "seriesonline-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "seriesonline.us"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "seriesonline.us"
        self.moduleName = "chn_seriesonline.py"
        self.mainListUri = "http://www.seriesonline.us/"
        self.baseUrl = "http://www.seriesonline.us/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))

        self.requiresLogon = False

        self.episodeItemRegex = '> <a href="([^"]+)">([^<]+)</a><br />'
        self.folderItemRegex = '<li><a href="(/serie[^"]+)">([^<]+)</a></li>'
        self.videoItemRegex  = "xxxxxyyyyyzzzzz"
        self.mediaUrlRegex = 'xxxxxyyyyyzzzzz'
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[1].strip()
        logFile.debug("titulo="+titulo)
        url = urlparse.urljoin( self.baseUrl , resultSet[0] )
        logFile.debug("url="+url)

        item = common.clistItem( titulo, url )
        item.icon = self.folderIcon
        item.complete = True
        return item
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[1]

        url = urlparse.urljoin( self.baseUrl , resultSet[0].replace("/serie/","/serie-divx/") )
        item = common.clistItem(titulo,url)

        item.description = titulo
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
        return common.clistItem("vacio","")

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []
        
        encontrados = set()

        # Megavideo - Vídeos con título
        logFile.info("1) Megavideo con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0].strip()
            if titulo == "":
                titulo = "Sin título"
            titulo = titulo + " (id "+match[1]+")"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # Megavideo - Vídeos sin título
        logFile.info("2) Megavideo sin titulo...")
        patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin título (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Vreel - Vídeos con título
        logFile.info("3) Vreel con título...")
        patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0].strip()
            if titulo == "":
                titulo = "Sin título"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Vreel - Vídeos con título
        logFile.info("4) Vreel con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0].strip()
            if titulo == "":
                titulo = "Sin título"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # WUAPI
        logFile.info("5) wuapi sin título")
        patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match[23:]+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # WUAPI
        logFile.info("6) wuapi sin título...")
        patronvideos  = '(http://wuapi.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match[23:]+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # STAGEVU
        logFile.info("7) Stagevu sin título...")
        patronvideos  = '"(http://stagevu.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # TUTV
        logFile.info("8) Tu.tv sin título...")
        patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # TUTV
        logFile.info("9) Tu.tv sin título...")
        #<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
        patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Megavideo - Vídeos sin título
        logFile.info("10 ) Megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # Megavideo - Vídeos sin título
        logFile.info("11) Megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # STAGEVU
        logFile.info("12) Stagevu...")
        patronvideos  = '(http://stagevu.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
            
        # Vreel - Vídeos sin título
        logFile.info("13) Vreel sin titulo...")
        patronvideos  = '(http://beta.vreel.net[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        return (data, _items)

    def nuevoVideoItem( self , titulo , url , tipo ):
        logFile.info("  Detectado vídeo "+tipo+" (titulo=#"+titulo+"#) (url=#"+url+"#)")
        item = common.clistItem( titulo , url )
        item.thumb = self.noImage
        item.description = ""
        item.date = tipo
        item.icon = "newmovie.png"
        item.type = 'video'
        item.mediaurl = url
        item.complete = False
        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        logFile.info('Tipo de video='+item.date)

        if item.date == "Megavideo":
            item.mediaurl = megavideo.Megavideo(item.url)
            
        if item.date == "Wuapi":
            item.mediaurl = wuapi.Wuapi(item.url)
            
        if item.date == "Vreel":
            item.mediaurl = vreel.Vreel(item.url)

        if item.date == "Stagevu":
            item.mediaurl = stagevu.Stagevu(item.url)
        
        if item.date == "tu.tv":
            item.mediaurl = tutv.Tutv(item.url)

        logFile.info('item.mediaurl='+item.mediaurl)
        item.complete = True
        
        return item

    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnUpdateItem(self, selectedIndex):
        logFile.debug('Updating item (Called from ContextMenu)')
        self.onUpDown(ignoreDisabled = True)
    
    def CtMnDownloadItem(self, selectedIndex):
        item = self.listItems[selectedIndex]
        logFile.info(item)
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
