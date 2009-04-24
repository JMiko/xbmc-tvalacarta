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

register.channelRegister.append('chn_peliculashd.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="peliculashd")')


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
        self.icon = "peliculashd-icon.png"
        self.iconLarge = "peliculashd-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "PeliculasHD"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "peliculashd.net"
        self.moduleName = "chn_peliculashd.py"
        self.mainListUri = "http://www.peliculashd.net/"
        self.baseUrl = "http://www.peliculashd.net/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        self.episodeItemRegex = 'xxxyyyzz'

        self.videoSort = False

        self.episodeItemRegex = 'xxxxxyyyyyzzzz'
        self.folderItemRegex = '<p class="news"><span class="title"><a href="([^"]+)"></span><img src="([^"]+)".*?alt="([^"]+)"[^>]+>'
        self.videoItemRegex  = "xxxxxyyyyyzzzzz"
        self.mediaUrlRegex = 'xxxxxyyyyyzzzzz'
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Novedades", self.mainListUri )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        #nuevoitem = common.clistItem("Buscar", "searchSite" )
        #nuevoitem.icon = self.folderIcon
        #items.append(nuevoitem)

        self.mainListItems = items

        return items

    #==============================================================================
    def SearchSite(self):
        items = []
        
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            if len(tecleado)>0:
                #convert to HTML
                tecleado = tecleado.replace(" ", "+")
                searchUrl = '/search?for='+tecleado+'&in=Videos&x=0&y=0&perpage=25&page=2'
                return self.ProcessFolderList(searchUrl,"GET")
                
        return items
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[2]

        url = resultSet[0]
        item = common.clistItem(titulo,url)

        item.description = titulo
        item.icon = self.folderIcon
        item.type = 'folder'
        item.thumbUrl = resultSet[1]
        item.complete = False
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
        
        patronvideos = '<span>\d+</span> <a href="(http://peliculashd.net/videos/page/[^"]+)">([^<]+)</a>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        for match in matches:
            logFile.info("Encontrada pagina "+match[1])
            item = common.clistItem("Pagina "+match[1],match[0])
            item.description = ""
            item.icon = self.folderIcon
            item.type = 'folder'
            item.thumb = self.noImage
            item.complete = True
            _items.append( item )

        encontrados = set()

        # Megavideo - Vídeos con título
        logFile.info("1) wuapi...")
        patronvideos = 'flashvars="file=([^\&]+)\&'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin titulo"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
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
