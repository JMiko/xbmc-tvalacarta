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
import megavideo, vreel, stagevu, tutv, wuapi

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

register.channelRegister.append('chn_newcineonline.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="newcineonline")')


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
        self.icon = "newcineonline-icon.png"
        self.iconLarge = "newcineonline-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "newcineonline"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "www.newcineonline.com"
        self.moduleName = "chn_newcineonline.py"
        self.mainListUri = 'http://www.newcineonline.com/'
        self.baseUrl = 'http://www.newcineonline.com/'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using PAPlayer", "CtMnPlayPaplayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        # Los episiodios (nivel 1) están puestos a mano (menú de la página)
        self.episodeItemRegex = 'xxxyyyzz'
        
        # Las carpetas son cada una de las películas
        patronvideos  = '<div id="post-info-mid">[^<]+<div class="post-title"><a href="([^"]+)">([^<]+)</a></div>'
        patronvideos += '.*?<td class="post-story"><div[^>]+><img src="([^"]+)"[^>]+>(.*?)<img src="[^"]+"[^>]+>.*?</div>'
        self.folderItemRegex = patronvideos

        # Los enlaces a megavideo son manuales
        self.videoItemRegex   = 'xxxxyyyyzzzz'

        # Aquí el vídeo sale directamente de la URL
        self.mediaUrlRegex = ''
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Novedades", "http://www.newcineonline.com/" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Estrenos", "http://www.newcineonline.com/index.php?do=cat&category=estrenos" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Peliculas", "http://www.newcineonline.com/index.php?do=cat&category=peliculas" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Documentales", "http://www.newcineonline.com/index.php?do=cat&category=documentales" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Peliculas VOS", "http://www.newcineonline.com/index.php?do=cat&category=peliculas-vos" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Dibujos", "http://www.newcineonline.com/index.php?do=cat&category=dibujos" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Series", "http://www.newcineonline.com/index.php?do=cat&category=series" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        self.mainListItems = items

        return items

    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        titulo = resultSet[1]
        url = urlparse.urljoin(self.baseUrl,resultSet[0])
        item = common.clistItem(titulo,url)
        
        descripcion = resultSet[3]
        descripcion = descripcion.replace("<br />","\n")
        descripcion = descripcion.replace("<b>","")
        descripcion = descripcion.replace("</b>","")
        descripcion = descripcion.replace("<i>","")
        descripcion = descripcion.replace("</i>","")
        descripcion = descripcion.replace("<!--colorstart:#589BB9-->","")
        descripcion = descripcion.replace("<!--colorend-->","")
        descripcion = descripcion.replace("<!--/colorend-->","")
        descripcion = descripcion.replace("<!--/colorstart-->","")
        descripcion = descripcion.replace('<span style="color:#589BB9">',"")
        descripcion = descripcion.replace("</span>","")
        descripcion = descripcion.strip()
        item.description = descripcion
        
        item.icon = self.folderIcon
        item.type = 'folder'
        item.thumbUrl = resultSet[2]
        item.complete = False
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)

        titulo = "Megavideo "+resultSet
        item = common.clistItem( titulo , resultSet )
        
        item.thumb = self.noImage
        item.description = ""
        item.date = "."
        item.icon = "newmovie.png"
        item.type = 'video'
        item.mediaurl = megavideo.Megavideo(resultSet)
        item.complete = True
        logFile.info('item.mediaurl=' + item.mediaurl)

        return item

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []

        logFile.info("Busca el enlace de página siguiente...")
        try:
            # La siguiente página
            patronvideos  = '<a href\="([^"]+)"><span class\="navigation"[^>]+>Sigu'
            matches = re.compile(patronvideos,re.DOTALL).findall(data)
            
            url = matches[0]
            paginaitem = common.clistItem("#Siguiente",url)
            paginaitem.description = paginaitem.name
            paginaitem.icon = self.folderIcon
            paginaitem.type = 'folder'
            paginaitem.thumb = self.noImage
            paginaitem.complete = True
            _items.append(paginaitem)
        except:
            logFile.info("No encuentro la pagina...")

        # Megavideo - Vídeos con título
        logFile.info("Busca el enlace a megavideo con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0] + " ("+match[1]+")"
            url = match[1]
            _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )

        # Megavideo - Vídeos sin título
        logFile.info("Busca el enlace a megavideo sin titulo...")
        patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
        
        # Vreel - Vídeos con título
        logFile.info("Busca el enlace a vreel con titulo...")
        patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0]
            url = match[1]
            _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
        
        # Vreel - Vídeos con título
        logFile.info("Busca el enlace a vreel con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0]
            url = match[1]
            _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
        
        # WUAPI
        logFile.info("Busca el enlace a wuapi...")
        patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[23:]
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
        
        # WUAPI
        logFile.info("Busca el enlace a wuapi...")
        patronvideos  = '(http://wuapi.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[23:]
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
        
        # STAGEVU
        logFile.info("Busca el enlace a stagevu...")
        patronvideos  = '"(http://stagevu.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
        
        # TUTV
        logFile.info("Busca el enlace a tutv...")
        patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
        
        # TUTV
        logFile.info("Busca el enlace a tutv...")
        #<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
        patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
        
        # Megavideo - Vídeos sin título
        logFile.info("Busca el enlace a megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo ("+match+")"
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )

        # Megavideo - Vídeos sin título
        logFile.info("Busca el enlace a megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo ("+match+")"
            url = match
            _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )

        # STAGEVU
        logFile.info("Busca el enlace a stagevu...")
        patronvideos  = '(http://stagevu.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            _items.append( self.nuevoVideoItem( match , match , "Stagevu" ) )
            
        # Vreel - Vídeos sin título
        logFile.info("Busca el enlace a vreel sin titulo...")
        patronvideos  = '(http://beta.vreel.net[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            _items.append( self.nuevoVideoItem( match , match , "Vreel" ) )
        
        return (data, _items)

    def nuevoVideoItem( self , titulo , url , tipo ):
        logFile.info("  Detectado vídeo "+tipo+" ("+titulo+") ("+url+")")
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

    def CtMnPlayPaplayer(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item, "paplayer")
    
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
