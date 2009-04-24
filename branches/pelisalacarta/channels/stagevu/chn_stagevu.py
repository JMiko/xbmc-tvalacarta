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
import stagevu

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

register.channelRegister.append('chn_stagevu.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="stagevu")')


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
        self.icon = "stagevu-icon.png"
        self.iconLarge = "stagevu-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "StageVU"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "stagevu.com"
        self.moduleName = "chn_stagevu.py"
        self.mainListUri = "http://stagevu.com/"
        self.baseUrl = "http://stagevu.com/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        self.episodeItemRegex = 'xxxyyyzz'

        self.videoSort = False

        # Los vídeos del resultado
        self.videoItemRegex  = '<div class="result[^>]+>[^<]+<div class="resultcont">[^<]+<h2><a href="([^"]+)">([^<]+)</a>.*?<img src="([^"]+)".*?</a>(.*?)</div>'

        # Pagina siguiente
        self.folderItemRegex = 'xxxyyyzzz'

        self.mediaUrlRegex = 'xxxyyyzzz'
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Buscar", "searchSite" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        self.mainListItems = items

        return items

    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        titulo = 'Siguiente'
        url = urlparse.urljoin(self.baseUrl,resultSet)
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
        logFile.debug('CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)

        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        url = resultSet[0]
        item = common.clistItem( titulo , url )
        
        item.thumbUrl = resultSet[2]
        
        try:
            descripcion = unicode( resultSet[3], "utf-8" ).encode("iso-8859-1")
        except:
            descripcion = resultSet[3]
        descripcion = descripcion.replace("\\t","")
        descripcion = descripcion.replace("<p>"," ")
        descripcion = descripcion.replace("</p>"," ")
        descripcion = descripcion.strip()
        item.description = descripcion
        
        item.date = ''
        item.icon = "newmovie.png"
        item.type = 'video'
        item.complete = False

        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        logFile.info('item.url='+item.url)
        item.mediaurl = stagevu.Stagevu(item.url)
        logFile.info('item.mediaurl=' + item.mediaurl)
        item.complete = True
        return item

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
                searchUrl = 'http://stagevu.com/search?for='+tecleado+'&in=Videos&x=0&y=0&perpage=25&page=2'
                return self.ProcessFolderList(searchUrl,"GET")
                
        return items
    
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
